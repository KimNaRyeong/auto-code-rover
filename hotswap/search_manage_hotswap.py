"""
HOTSWAP VERSION of search_manage.py
This version supports resuming from a previous search output directory.
Modified to enable k=8 execution after loading k=1-7 results.
"""

import inspect
import json
import os
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
    def __init__(self, project_path: str, output_dir: str, resume_from_dir: str | None = None):
        # output dir for writing search-related things
        self.output_dir = pjoin(output_dir, "search")
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        # record the search APIs being used, in each layer
        self.tool_call_layers: list[list[Mapping]] = []

        # HOTSWAP: Resume configuration
        self.resume_from_dir = resume_from_dir
        self.resume_round = 0  # Round to resume from
        self.resumed_message_thread = None  # Loaded message thread

        self.backend: SearchBackend = SearchBackend(project_path)

        # HOTSWAP: Load existing state if resuming
        if self.resume_from_dir is not None:
            self._load_existing_state()

    def _load_existing_state(self):
        """
        HOTSWAP: Load existing search state from a previous run.
        This loads:
        1. tool_call_layers.json - all tool calls from previous rounds
        2. search_round_*.json files - to find the last completed round
        3. The last message thread - to resume from
        """
        if self.resume_from_dir is None:
            return

        resume_search_dir = pjoin(self.resume_from_dir, "output_0", "search")

        if not os.path.exists(resume_search_dir):
            logger.warning(f"Resume directory does not exist: {resume_search_dir}")
            return

        # Load tool call layers
        tool_call_layers_file = pjoin(resume_search_dir, "tool_call_layers.json")
        if os.path.exists(tool_call_layers_file):
            with open(tool_call_layers_file, 'r') as f:
                self.tool_call_layers = json.load(f)
            logger.info(f"HOTSWAP: Loaded {len(self.tool_call_layers)} tool call layers")
        else:
            logger.warning(f"Tool call layers file not found: {tool_call_layers_file}")

        # Find the last search round
        search_round_files = sorted([
            f for f in os.listdir(resume_search_dir)
            if f.startswith("search_round_") and f.endswith(".json")
        ])

        if search_round_files:
            last_round_file = search_round_files[-1]
            last_round_num = int(last_round_file.replace("search_round_", "").replace(".json", ""))
            self.resume_round = last_round_num + 1  # Resume from next round

            # Load the last message thread
            last_round_path = pjoin(resume_search_dir, last_round_file)
            self.resumed_message_thread = MessageThread.load_from_file(last_round_path)

            logger.info(f"HOTSWAP: Last completed round: {last_round_num}, will resume from round {self.resume_round}")

            # Copy previous round files to new output dir
            for round_file in search_round_files:
                src = pjoin(resume_search_dir, round_file)
                dst = pjoin(self.output_dir, round_file)
                with open(src, 'r') as f_src:
                    content = f_src.read()
                with open(dst, 'w') as f_dst:
                    f_dst.write(content)

            # Also copy agent_proxy files
            proxy_files = [f for f in os.listdir(resume_search_dir) if f.startswith("agent_proxy_")]
            for proxy_file in proxy_files:
                src = pjoin(resume_search_dir, proxy_file)
                dst = pjoin(self.output_dir, proxy_file)
                with open(src, 'r') as f_src:
                    content = f_src.read()
                with open(dst, 'w') as f_dst:
                    f_dst.write(content)

            logger.info(f"HOTSWAP: Copied {len(search_round_files)} search rounds and {len(proxy_files)} proxy files")
        else:
            logger.warning("No search round files found in resume directory")

    def search_iterative(
        self,
        task: Task,
        sbfl_result: str,
        reproducer_result: str,
        reproduced_test_content: str | None,
    ) -> tuple[list[BugLocation], MessageThread]:
        """
        Main entry point of the search manager.
        HOTSWAP: Modified to support resuming from a previous round.
        """
        search_api_generator = agent_search.generator(
            task.get_issue_statement(), sbfl_result, reproducer_result
        )

        generator_input = None
        search_msg_thread: MessageThread | None = None

        # HOTSWAP: If resuming, we need to "replay" previous rounds to the generator
        # This is necessary to maintain the generator's internal state
        if self.resume_from_dir is not None and self.resume_round > 0:
            logger.info(f"HOTSWAP: Replaying rounds 0-{self.resume_round-1} to generator")

            resume_search_dir = pjoin(self.resume_from_dir, "output_0", "search")

            # Replay each round to the generator without executing API calls
            for replay_round in range(self.resume_round):
                # Load the search round
                round_file = pjoin(resume_search_dir, f"search_round_{replay_round}.json")
                if not os.path.exists(round_file):
                    logger.warning(f"HOTSWAP: Round file not found: {round_file}")
                    break

                # Load agent proxy to get the selected APIs
                proxy_file = pjoin(resume_search_dir, f"agent_proxy_{replay_round}.json")
                if not os.path.exists(proxy_file):
                    logger.warning(f"HOTSWAP: Proxy file not found: {proxy_file}")
                    break

                with open(proxy_file, 'r') as f:
                    proxy_data = json.load(f)

                # Extract the JSON response (last message in proxy conversation)
                if proxy_data and len(proxy_data) > 0:
                    # Find the assistant's response with the JSON
                    selected_apis_json: dict | None = None
                    for msg_thread in proxy_data:
                        if 'messages' in msg_thread:
                            for msg in msg_thread['messages']:
                                if msg.get('role') == 'assistant' and msg.get('content'):
                                    try:
                                        # Try to parse as JSON
                                        test_json = json.loads(msg['content'])
                                        if 'API_calls' in test_json or 'bug_locations' in test_json:
                                            selected_apis_json = test_json
                                            break
                                    except:
                                        pass

                    if selected_apis_json:
                        json_api_calls = selected_apis_json.get("API_calls", [])
                        buggy_locations = selected_apis_json.get("bug_locations", [])

                        # Reconstruct the search result message
                        if json_api_calls:
                            collated_search_res_str = ""
                            for api_call in json_api_calls:
                                collated_search_res_str += f"[REPLAYED from round {replay_round}] Result of {api_call}\n\n"
                            generator_input = (collated_search_res_str, False)
                        elif buggy_locations:
                            # Bug locations found - this would have ended the search
                            logger.info(f"HOTSWAP: Bug locations found in round {replay_round} during replay")
                            break

                # Send to generator (replay)
                try:
                    agent_search_response, search_msg_thread = search_api_generator.send(generator_input)
                    logger.debug(f"HOTSWAP: Replayed round {replay_round}")
                except StopIteration:
                    logger.warning(f"HOTSWAP: Generator stopped during replay at round {replay_round}")
                    break

            logger.info(f"HOTSWAP: Replay complete. Starting actual execution from round {self.resume_round}")

        # HOTSWAP: Now run from resume_round to conv_round_limit
        start_round = self.resume_round if self.resume_from_dir else 0

        for round_no in range(start_round, config.conv_round_limit):
            self.start_new_tool_call_layer()

            print_banner(f"CONTEXT RETRIEVAL ROUND {round_no}")

            # invoke agent search to choose search APIs
            agent_search_response, search_msg_thread = search_api_generator.send(
                generator_input
            )

            conversation_file = Path(self.output_dir, f"search_round_{round_no}.json")
            # save current state before starting a new round
            search_msg_thread.save_to_file(conversation_file)

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
