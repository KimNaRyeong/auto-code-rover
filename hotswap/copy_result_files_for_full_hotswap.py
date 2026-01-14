import shutil
import os
import json
from glob import glob

def get_source_dir(base_dir, task):
    pattern = os.path.join(base_dir, f'{task}*')
    matching_dirs = glob(pattern)

    if len(matching_dirs) == 1:
        return matching_dirs[0]
    else:
        raise ValueError

task_list_file = '../atropos/sampled_tasks_1_and_2.txt'
with open(task_list_file, 'r') as f:
    task_list = f.read().splitlines()

hotswap_list_file = './predictions/k8_tasks_to_hotswap_for_r.json'
with open(hotswap_list_file, 'r') as f:
    hotswap_list = json.load(f)

for i in range(1, 6):
    no_hotswap_copy_list = []
    hotswap_copy_list = []
    for task in task_list:
        if task not in hotswap_list[str(i)]:
            no_hotswap_copy_list.append(task)
        else:
            hotswap_copy_list.append(task)

    dest_base_dir = f'../fl_outputs/only_fl_hotswap_full_{i}/no_patch'
    os.makedirs(dest_base_dir, exist_ok=True)

    source_base_dir = f'../fl_outputs/only_fl_output_mixtral_{i}/no_patch'
    for task in no_hotswap_copy_list:
        source_path = get_source_dir(source_base_dir, task)
        task_dir = source_path.split('/')[-1]
        dest_path = os.path.join(dest_base_dir, task_dir)
        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
    
    source_base_dir = f'../fl_outputs/only_fl_hotswap_{i}/no_patch'
    for task in hotswap_copy_list:
        source_path = get_source_dir(source_base_dir, task)
        task_dir = source_path.split('/')[-1]
        dest_path = os.path.join(dest_base_dir, task_dir)
        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)



