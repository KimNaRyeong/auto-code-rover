"""
Modified ACR execution script that resumes from k=7 and runs k=8 only.
This script:
1. Loads existing FL results from k=1~7
2. Resumes SearchManager state
3. Runs only round 8 (k=8)
"""

import json
import os
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, os.path.abspath('..'))

from app import config
from app.search.search_manage import SearchManager
from app.data_structures import MessageThread
from app.agents import agent_search, agent_proxy
from loguru import logger


def load_existing_state(existing_output_dir):
    """
    Load existing search state from k=1~7.

    Returns:
        - tool_call_layers: list of tool call layers from round 0-6
        - message_thread: MessageThread from round 6
        - round_num: the last completed round number (should be 6 for k=7)
    """
    search_dir = os.path.join(existing_output_dir, "output_0", "search")

    # Load tool call layers
    tool_call_layers_file = os.path.join(search_dir, "tool_call_layers.json")
    with open(tool_call_layers_file, 'r') as f:
        tool_call_layers = json.load(f)

    # Find the last search round
    search_rounds = sorted([
        f for f in os.listdir(search_dir)
        if f.startswith("search_round_") and f.endswith(".json")
    ])

    if not search_rounds:
        raise ValueError("No search rounds found")

    # Get the last round number
    last_round_file = search_rounds[-1]
    last_round_num = int(last_round_file.replace("search_round_", "").replace(".json", ""))

    # Load the message thread from the last round
    last_round_path = os.path.join(search_dir, last_round_file)
    message_thread = MessageThread.load_from_file(last_round_path)

    logger.info(f"Loaded existing state: {len(tool_call_layers)} tool call layers, last round: {last_round_num}")

    return tool_call_layers, message_thread, last_round_num


def resume_search_from_round(
    search_manager: SearchManager,
    task,
    sbfl_result: str,
    reproducer_result: str,
    reproduced_test_content: str | None,
    existing_tool_call_layers: list,
    existing_message_thread: MessageThread,
    start_round: int,
    max_rounds: int = 8
):
    """
    Resume search from a specific round.

    Args:
        search_manager: SearchManager instance
        task: Task object
        sbfl_result: SBFL result string
        reproducer_result: Reproducer result string
        reproduced_test_content: Reproduced test content
        existing_tool_call_layers: Tool call layers from previous rounds
        existing_message_thread: Message thread from previous rounds
        start_round: Round to start from (e.g., 7 for k=8)
        max_rounds: Maximum number of rounds (e.g., 8 for k=8)

    Returns:
        - bug_locs: Bug locations found
        - search_msg_thread: Final message thread
    """
    # Restore the tool call layers
    search_manager.tool_call_layers = existing_tool_call_layers.copy()

    # Create the search API generator
    search_api_generator = agent_search.generator(
        task.get_issue_statement(), sbfl_result, reproducer_result
    )

    # Resume the generator with the existing message thread
    # We need to send None first to initialize, then send the existing thread
    search_api_generator.send(None)  # Initialize

    # Now resume from the start_round
    for round_no in range(start_round, max_rounds):
        search_manager.start_new_tool_call_layer()

        logger.info(f"CONTEXT RETRIEVAL ROUND {round_no} (resumed)")

        # For the first resumed round, we need to continue from existing thread
        if round_no == start_round:
            # Use existing message thread to continue
            generator_input = None  # Let the generator continue naturally
        else:
            generator_input = None

        # Invoke agent search
        try:
            agent_search_response, search_msg_thread = search_api_generator.send(generator_input)
        except StopIteration:
            logger.info("Search completed early")
            break

        # Save current state
        conversation_file = Path(search_manager.output_dir, f"search_round_{round_no}.json")
        search_msg_thread.save_to_file(conversation_file)

        # Extract JSON API calls
        selected_apis, proxy_threads = agent_proxy.run_with_retries(agent_search_response)

        proxy_msg_log = Path(search_manager.output_dir, f"agent_proxy_{round_no}.json")
        proxy_messages = [thread.to_msg() for thread in proxy_threads]
        proxy_msg_log.write_text(json.dumps(proxy_messages, indent=4))

        if selected_apis is None:
            logger.debug("Could not extract API calls, asking search agent to re-generate")
            search_result_msg = "The search API calls seem not valid. Please check the arguments you give carefully and try again."
            generator_input = (search_result_msg, True)
            continue

        # Parse selected APIs
        selected_apis_json = json.loads(selected_apis)
        json_api_calls = selected_apis_json.get("API_calls", [])
        buggy_locations = selected_apis_json.get("bug_locations", [])

        # Check if bug locations found
        if buggy_locations and (not json_api_calls):
            # Save bug locations
            bug_loc_file = Path(search_manager.output_dir, "bug_locations_before_process.json")
            bug_loc_file.write_text(json.dumps(buggy_locations, indent=4))

            # Process bug locations
            from app.data_structures import BugLocation
            new_bug_locations = []
            for loc in buggy_locations:
                new_bug_locations.extend(search_manager.backend.get_bug_loc_snippets_new(loc))

            # Remove duplicates
            unique_bug_locations = []
            for loc in new_bug_locations:
                if loc not in unique_bug_locations:
                    unique_bug_locations.append(loc)

            if unique_bug_locations:
                bug_loc_file_processed = Path(search_manager.output_dir, "bug_locations_after_process.json")
                json_obj = [loc.to_dict() for loc in unique_bug_locations]
                bug_loc_file_processed.write_text(json.dumps(json_obj, indent=4))

                logger.info(f"Bug locations extracted: {len(unique_bug_locations)}")
                return unique_bug_locations, search_msg_thread

        # Execute API calls and continue
        if json_api_calls:
            # Record the API calls in this layer
            search_manager.record_tool_calls(json_api_calls)

            # Execute the API calls
            search_result_msg = search_manager.execute_api_calls(json_api_calls)
            generator_input = (search_result_msg, False)
        else:
            generator_input = None

    # No bug locations found
    logger.warning("No bug locations found after all rounds")
    return [], search_msg_thread


def main():
    """
    Main function to test resuming ACR from k=7 to k=8.
    This is a proof-of-concept implementation.
    """
    # Example usage
    existing_output_dir = "/home/kimnal0/auto-code-rover/fl_outputs/only_fl_output_mixtral_1/no_patch/astropy__astropy-12825_2025-12-05_14-26-01"

    # Load existing state
    tool_call_layers, message_thread, last_round = load_existing_state(existing_output_dir)

    print(f"Loaded state from rounds 0-{last_round}")
    print(f"Tool call layers: {len(tool_call_layers)}")
    print(f"Starting from round {last_round + 1}")

    # NOTE: This is a simplified example
    # In practice, you would need to:
    # 1. Load the task object
    # 2. Create SearchManager
    # 3. Resume the search

    print("\nThis is a proof-of-concept. Full implementation requires:")
    print("1. Task object loading")
    print("2. SearchManager initialization")
    print("3. Proper generator state management")
    print("4. Integration with main ACR workflow")


if __name__ == "__main__":
    main()
