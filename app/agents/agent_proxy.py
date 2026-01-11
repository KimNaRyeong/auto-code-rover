"""
A proxy agent. Process raw response into json format.
"""

import os
import inspect
import json
from typing import Any
from glob import glob

from loguru import logger

from app import config
from app.data_structures import MessageThread
from app.model import common
from app.post_process import ExtractStatus, is_valid_json
from app.search.search_backend import SearchBackend
from app.utils import parse_function_invocation

PROXY_PROMPT = """
You are a helpful assistant that retreive API calls and bug locations from a text into json format.
The text will consist of two parts:
1. do we need more context?
2. where are bug locations?
Extract API calls from question 1 (leave empty if not exist) and bug locations from question 2 (leave empty if not exist).

The API calls include:
search_method_in_class(method_name: str, class_name: str)
search_method_in_file(method_name: str, file_path: str)
search_method(method_name: str)
search_class_in_file(self, class_name, file_name: str)
search_class(class_name: str)
search_code_in_file(code_str: str, file_path: str)
search_code(code_str: str)
get_code_around_line(file_path: str, line_number: int, window_size: int)

Provide your answer in JSON structure like this, you should ignore the argument placeholders in api calls.
For example, search_code(code_str="str") should be search_code("str")
search_method_in_file("method_name", "path.to.file") should be search_method_in_file("method_name", "path/to/file")
Make sure each API call is written as a valid python expression.

{
    "API_calls": ["api_call_1(args)", "api_call_2(args)", ...],
    "bug_locations":[{"file": "path/to/file", "class": "class_name", "method": "method_name", "intended_behavior", "This code should ..."}, {"file": "path/to/file", "class": "class_name", "method": "method_name", "intended_behavior": "..."} ... ]
}
"""

def run_with_retries(text: str, retries=5, search_round: int = -1, task_id: str = "") -> tuple[str | None, list[MessageThread]]:
    msg_threads = []
    for idx in range(1, retries + 1):
        logger.debug(
            "Trying to convert API calls/bug locations into json. Try {} of {}.",
            idx,
            retries,
        )

        res_text, new_thread = run(text, search_round, task_id)
        msg_threads.append(new_thread)

        extract_status, data = is_valid_json(res_text)

        if extract_status != ExtractStatus.IS_VALID_JSON:
            logger.debug("Invalid json. Will retry.")
            continue

        valid, diagnosis = is_valid_response(data)
        if not valid:
            logger.debug(f"{diagnosis}. Will retry.")
            continue

        logger.debug("Extracted a valid json.")
        return res_text, msg_threads
    return None, msg_threads

def get_prev_output_dir(task_id, dir_idx):
    prev_output_dir = os.path.join('.', 'fl_outputs', f'only_fl_output_mixtral_{dir_idx}', 'no_patch')
    pattern = os.path.join(prev_output_dir, f"{task_id}*")
    matching_dirs = glob(pattern)

    if len(matching_dirs) == 1:
        return matching_dirs[0]
    else:
        raise Exception("There is no matching prev directory")

def run(text: str, search_round: int = -1, task_id: str = "") -> tuple[str, MessageThread]:
    """
    Run the agent to extract issue to json format.
    """

    resume_from = config.resume_from
    output_dir = config.output_dir
    dir_idx = output_dir.split('_')[-1]

    prev_output_dir = get_prev_output_dir(task_id, dir_idx)

    prev_search_dir = os.path.join(prev_output_dir, 'output_0', 'search')


    msg_thread = MessageThread()
    msg_thread.add_system(PROXY_PROMPT)
    msg_thread.add_user(text)
    with open('./search_debug', 'a+') as f:

        f.write(f"==========proxy prompt for task {task_id} (will be saved to agent_proxy_{search_round}.json)===========\n")
        f.write(str(msg_thread.to_msg())+'\n')
    
    if resume_from and search_round < resume_from - 1:
        prev_proxy_file = os.path.join(prev_search_dir, f'agent_proxy_{search_round}.json')
        with open(prev_proxy_file, 'r') as f:
            proxy_content = json.load(f)
            res_text = proxy_content[-1][-1]["content"]
    else:
        res_text, *_ = common.SELECTED_MODEL.call(
            msg_thread.to_msg(), response_format="json_object"
        )
    with open('./search_debug', 'a+') as f:
        f.write(f"==========proxy assistance for task {task_id} (will be saved to agent_proxy_{search_round}.json)===========\n")
        f.write(res_text+'\n')

    msg_thread.add_model(res_text, [])  # no tools

    return res_text, msg_thread


def is_valid_response(data: Any) -> tuple[bool, str]:
    if not isinstance(data, dict):
        return False, "Json is not a dict"

    if not data.get("API_calls"):
        bug_locations = data.get("bug_locations")
        if not isinstance(bug_locations, list) or not bug_locations:
            return False, "Both API_calls and bug_locations are empty"

        for loc in bug_locations:
            if loc.get("class") or loc.get("method") or loc.get("file"):
                continue
            return (
                False,
                "Bug location not detailed enough. Each location must contain at least a class or a method or a file.",
            )
    else:
        for api_call in data["API_calls"]:
            if not isinstance(api_call, str):
                return False, "Every API call must be a string"

            try:
                func_name, func_args = parse_function_invocation(api_call)
            except Exception:
                return False, "Every API call must be of form api_call(arg1, ..., argn)"

            function = getattr(SearchBackend, func_name, None)
            if function is None:
                return False, f"the API call '{api_call}' calls a non-existent function"

            # getfullargspec returns a wrapped function when the function defined
            # has a decorator. We unwrap it here.
            while "__wrapped__" in function.__dict__:
                function = function.__wrapped__

            arg_spec = inspect.getfullargspec(function)
            arg_names = arg_spec.args[1:]  # first parameter is self

            if len(func_args) != len(arg_names):
                return False, f"the API call '{api_call}' has wrong number of arguments"

    return True, "OK"
