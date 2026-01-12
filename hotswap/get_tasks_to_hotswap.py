# find tasks having more than 7 (resume_from - 1) api_call interactions

import os, json, ast
from glob import glob

def get_prev_output_dir(task_id, base_dir):

    pattern = os.path.join(base_dir, f"{task_id}*")
    matching_dirs = glob(pattern)

    if len(matching_dirs) == 1:
        return matching_dirs[0]
    else:
        raise Exception("There is no matching prev directory")
    
if __name__ == '__main__':
    resume_from = 8

    predicted_incorrect_tasks_file = f'./predictions/k{resume_from}_tasks_to_rerun.json'
    with open(predicted_incorrect_tasks_file, 'r') as f:
        predicted_incorrect_tasks = json.load(f)
        predicted_incorrect_tasks_list = []

        for fold_idx, tasks in predicted_incorrect_tasks.items():
            predicted_incorrect_tasks_list.extend(tasks)

    k8_tasks_to_hotswap = {}
    for i in range(1, 6):
        k8_tasks_to_hotswap[i]= []

        prev_output_base_dir = f'/home/kimnal0/auto-code-rover/fl_outputs/only_fl_output_mixtral_{i}/no_patch'

        for task in predicted_incorrect_tasks_list:
            prev_output_dir = get_prev_output_dir(task, prev_output_base_dir)

            tool_call_layer_file = os.path.join(prev_output_base_dir, prev_output_dir, 'output_0/search/tool_call_layers.json')

            if os.path.exists(tool_call_layer_file):
                with open(tool_call_layer_file, 'r') as f:
                    tool_call_layers = json.load(f)
                    if len(tool_call_layers) < resume_from - 1:
                        continue
            else:
                continue

            eighth_search_file = os.path.join(prev_output_base_dir, prev_output_dir, f'output_0/search/search_round_{resume_from - 1}.json')

            if os.path.exists(eighth_search_file):
                k8_tasks_to_hotswap[i].append(task)
    
    output_file = './predictions/k8_tasks_to_hotswap_for_r.json'
    with open(output_file, 'w') as f:
        json.dump(k8_tasks_to_hotswap, f, indent=2)