import inspect
import json
from collections.abc import Mapping
from os.path import join as pjoin
from pathlib import Path

from loguru import logger

from app import config
from app.agents import agent_proxy, agent_search
from app.data_structures import BugLocation, MessageThread
from app.log import print_acr, print_banner
from app.search.search_backend import SearchBackend
from app.task import Task
from app.utils import parse_function_invocation


class SearchManager:
    def __init__(self, project_path: str, output_dir: str):
        # output dir for writing search-related things
        self.output_dir = pjoin(output_dir, "search")
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        # record the search APIs being used, in each layer
        self.tool_call_layers: list[list[Mapping]] = []

        self.backend: SearchBackend = SearchBackend(project_path)

    def search_iterative(
        self,
        task: Task,
        sbfl_result: str,
        reproducer_result: str,
        reproduced_test_content: str | None,
        prev_output_dir: str | None = None,
    ) -> tuple[list[BugLocation], MessageThread]:
        """
        Main entry point of the search manager.
        Returns:
            - Bug location info, which is a list of (code, intended behavior)
            - Class context code as string, or None if there is no context
            - The message thread that contains the search conversation.
        """
        # Load previous state if resuming
        start_round = 0
        resume_messages = None

        if prev_output_dir and config.resume_from is not None:
            # Load previous state
            start_round, resume_messages = self._load_previous_state(prev_output_dir)
            if start_round >= config.resume_from - 1:
                logger.info(
                    f"Successfully loaded {start_round} previous interactions. "
                    f"Starting from interaction {config.resume_from}"
                )
            else:
                logger.warning(
                    f"Could only load {start_round} interactions, "
                    f"but resume_from was set to {config.resume_from}. "
                    f"Continuing from interaction {start_round + 1}"
                )

        # Create generator with or without resume messages
        search_api_generator = agent_search.generator(
            task.get_issue_statement(), sbfl_result, reproducer_result, resume_messages
        )
        generator_input = None

        round_no = 0
        prev_round_data = None  # (round_no, msg_thread) for delayed saving

        search_msg_thread: MessageThread | None = None  # for typing

        # TODO: change the global number to be local, since it's only for search
        for round_no in range(start_round, config.conv_round_limit):
            self.start_new_tool_call_layer()

            print_banner(f"CONTEXT RETRIEVAL ROUND {round_no}")

            # Save previous round's data now that it's complete
            # (Skip this on the first iteration of resume mode)
            if prev_round_data is not None:
                prev_round_no, prev_msg_thread = prev_round_data
                conversation_file = Path(self.output_dir, f"search_round_{prev_round_no}.json")
                prev_msg_thread.save_to_file(conversation_file)
                prev_round_data = None

            # invoke agent search to choose search APIs
            agent_search_response, search_msg_thread = search_api_generator.send(
                generator_input
            )
            # print_retrieval(agent_search_response, f"round {round_no}")

            # extract json API calls from the raw response.
            selected_apis, proxy_threads = agent_proxy.run_with_retries(
                agent_search_response
            )

            logger.debug("Agent proxy return the following json: {}", selected_apis)

            proxy_msg_log = Path(self.output_dir, f"agent_proxy_{round_no}.json")
            proxy_messages = [thread.to_msg() for thread in proxy_threads]
            proxy_msg_log.write_text(json.dumps(proxy_messages, indent=4))

            if selected_apis is None:
                # agent search response could not be propagated to backend;
                # ask it to retry
                logger.debug(
                    "Could not extract API calls from agent search response, asking search agent to re-generate response."
                )
                search_result_msg = "The search API calls seem not valid. Please check the arguments you give carefully and try again."
                generator_input = (search_result_msg, True)
                continue

            # there are valid search APIs - parse them
            selected_apis_json: dict = json.loads(selected_apis)

            json_api_calls = selected_apis_json.get("API_calls", [])
            buggy_locations = selected_apis_json.get("bug_locations", [])

            formatted = []
            if json_api_calls:
                formatted.append("API calls:")
                for call in json_api_calls:
                    formatted.extend([f"\n- `{call}`"])

            if buggy_locations:
                formatted.append("\n\nBug locations")
                for location in buggy_locations:
                    s = ", ".join(f"{k}: `{v}`" for k, v in location.items())
                    formatted.extend([f"\n- {s}"])

            print_acr("\n".join(formatted), "Agent-selected API calls")

            # locations are confirmed by the agent - let's see whether the bug
            # locations are valid/precise
            if buggy_locations and (not json_api_calls):
                # dump the locations for debugging
                bug_loc_file = Path(
                    self.output_dir, "bug_locations_before_process.json"
                )
                bug_loc_file.write_text(json.dumps(buggy_locations, indent=4))

                new_bug_locations: list[BugLocation] = list()

                for loc in buggy_locations:
                    # this is the transformed bug location
                    new_bug_locations.extend(self.backend.get_bug_loc_snippets_new(loc))

                # remove duplicates in the bug locations
                unique_bug_locations: list[BugLocation] = []
                for loc in new_bug_locations:
                    if loc not in unique_bug_locations:
                        unique_bug_locations.append(loc)

                if new_bug_locations:

                    # some locations can be extracted, good to proceed to patch gen
                    bug_loc_file_processed = Path(
                        self.output_dir, "bug_locations_after_process.json"
                    )

                    json_obj = [loc.to_dict() for loc in new_bug_locations]
                    bug_loc_file_processed.write_text(json.dumps(json_obj, indent=4))

                    logger.debug(
                        f"Bug location extracted successfully: {new_bug_locations}"
                    )

                    return new_bug_locations, search_msg_thread

                # bug location is not precise enough to go into patch gen
                # let's prepare some message to be send to agent search
                # and go into next round
                logger.debug(
                    "Failed to retrieve code from all bug locations. Asking search agent to re-generate response."
                )
                search_result_msg = "Failed to retrieve code from all bug locations. You may need to check whether the arguments are correct or issue more search API calls."
                generator_input = (search_result_msg, True)
                continue

            # location not confirmed by the search agent - send backend result and go to next round
            collated_search_res_str = ""

            for api_call in json_api_calls:
                func_name, func_args = parse_function_invocation(api_call)
                # TODO: there are currently duplicated code here and in agent_proxy.
                func_unwrapped = getattr(self.backend, func_name)
                while "__wrapped__" in func_unwrapped.__dict__:
                    func_unwrapped = func_unwrapped.__wrapped__
                arg_spec = inspect.getfullargspec(func_unwrapped)
                arg_names = arg_spec.args[1:]  # first parameter is self

                assert len(func_args) == len(
                    arg_names
                ), f"Number of argument is wrong in API call: {api_call}"

                kwargs = dict(zip(arg_names, func_args))

                function = getattr(self.backend, func_name)
                result_str, _, call_ok = function(**kwargs)
                collated_search_res_str += f"Result of {api_call}:\n\n"
                collated_search_res_str += result_str + "\n\n"

                # record the api calls made and the call status
                self.add_tool_call_to_curr_layer(func_name, kwargs, call_ok)

            print_acr(collated_search_res_str, f"context retrieval round {round_no}")
            # send the results back to the search agent
            logger.debug(
                "Obtained search results from API invocation. Going into next retrieval round."
            )
            search_result_msg = collated_search_res_str
            generator_input = (search_result_msg, False)

            # Store current round data for delayed saving (after next send completes it)
            prev_round_data = (round_no, search_msg_thread)

        # Save the final round's data
        if prev_round_data is not None:
            prev_round_no, prev_msg_thread = prev_round_data
            conversation_file = Path(self.output_dir, f"search_round_{prev_round_no}.json")
            prev_msg_thread.save_to_file(conversation_file)

        # used up all the rounds, but could not return the buggy locations
        logger.info("Too many rounds. Try writing patch anyway.")
        assert search_msg_thread is not None
        return [], search_msg_thread

    def start_new_tool_call_layer(self):
        self.tool_call_layers.append([])

    def add_tool_call_to_curr_layer(
        self, func_name: str, args: dict[str, str], result: bool
    ):
        self.tool_call_layers[-1].append(
            {
                "func_name": func_name,
                "arguments": args,
                "call_ok": result,
            }
        )

    def dump_tool_call_layers_to_file(self):
        """Dump the layers of tool calls to a file."""
        tool_call_file = Path(self.output_dir, "tool_call_layers.json")
        tool_call_file.write_text(json.dumps(self.tool_call_layers, indent=4))

    def _load_previous_state(
        self,
        prev_output_dir: str,
    ) -> tuple[int, list[dict] | None]:
        """
        Load previous search state from a previous output directory.

        Args:
            prev_output_dir: Path to the previous output directory

        Returns:
            Tuple of (number of rounds loaded, messages to resume from)
        """
        import shutil

        prev_search_dir = Path(prev_output_dir, "output_0", "search")

        if not prev_search_dir.exists():
            logger.warning(f"Previous search directory does not exist: {prev_search_dir}")
            return 0, None

        # Load tool_call_layers.json to determine how many interactions to load
        tool_call_layers_file = prev_search_dir / "tool_call_layers.json"
        if not tool_call_layers_file.exists():
            logger.warning(f"tool_call_layers.json not found in {prev_search_dir}")
            return 0, None

        with open(tool_call_layers_file) as f:
            prev_tool_call_layers = json.load(f)

        # Determine how many rounds to load (resume_from - 1, since it's 1-indexed)
        rounds_to_load = min(config.resume_from - 1, len(prev_tool_call_layers))

        if rounds_to_load <= 0:
            logger.warning(f"resume_from is {config.resume_from}, no previous rounds to load")
            return 0, None

        logger.info(f"Loading {rounds_to_load} previous interaction(s)")

        # Load the tool call layers
        self.tool_call_layers = prev_tool_call_layers[:rounds_to_load]

        # Copy previous interaction files to current output directory
        for round_idx in range(rounds_to_load):
            # Copy search_round_{round_idx}.json
            search_round_file = prev_search_dir / f"search_round_{round_idx}.json"
            if search_round_file.exists():
                dest_file = Path(self.output_dir) / f"search_round_{round_idx}.json"
                shutil.copy2(search_round_file, dest_file)
                logger.debug(f"Copied {search_round_file} to {dest_file}")

            # Copy agent_proxy_{round_idx}.json
            agent_proxy_file = prev_search_dir / f"agent_proxy_{round_idx}.json"
            if agent_proxy_file.exists():
                dest_file = Path(self.output_dir) / f"agent_proxy_{round_idx}.json"
                shutil.copy2(agent_proxy_file, dest_file)
                logger.debug(f"Copied {agent_proxy_file} to {dest_file}")

        # Load the final search_round file to get the complete message thread
        final_round_idx = rounds_to_load - 1
        final_search_round_file = prev_search_dir / f"search_round_{final_round_idx}.json"

        if not final_search_round_file.exists():
            logger.warning(f"search_round_{final_round_idx}.json not found")
            return 0, None

        # Load the message thread from the final round
        with open(final_search_round_file) as f:
            messages = json.load(f)

        logger.info(f"Successfully loaded {rounds_to_load} round(s) with {len(messages)} messages")
        return rounds_to_load, messages


# if __name__ == "__main__":
#     manager = SearchManager("/tmp", "/tmp/one")
#     func_name = "search_code"
#     func_args = {"code_str": "_separable"}

#     # func_name = "search_class"
#     # func_args = {"class_name": "ABC"}

#     function = getattr(manager.backend, func_name)

#     while "__wrapped__" in function.__dict__:
#         function = function.__wrapped__
#     arg_spec = inspect.getfullargspec(function)

#     print(arg_spec)
#     arg_names = arg_spec.args[1:]  # first parameter is self
#     kwargs = func_args

#     orig_func = getattr(manager.backend, func_name)
#     search_result, _, call_ok = orig_func(**kwargs)
