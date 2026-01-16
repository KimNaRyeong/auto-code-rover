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


embedding_size = 300
label_criteria = 1
test_tasks_file = f'/home/kimnal0/auto-code-rover/atropos/results/parallel/embedding/fasttext/nhot_normal/sentence_vector/{embedding_size}d/not_add/label_criteria_{label_criteria}/test_bug_names2.json'

with open(test_tasks_file, 'r') as f:
    test_tasks = json.load(f)

test_list = []
for i, tt in test_tasks.items():
    test_list.extend(tt)

hotswap_list_file = './predictions/k8_tasks_to_hotswap_for_r.json'
with open(hotswap_list_file, 'r') as f:
    hotswap_list = json.load(f)

for i in range(1, 6):
    # no_hotswap_copy_list = []
    # hotswap_copy_list = []
    # for task in test_list:
    #     if task not in hotswap_list[str(i)]:
    #         no_hotswap_copy_list.append(task)
    #     else:
    #         hotswap_copy_list.append(task)

    # hotswap_dest_base_dir = f'./results/hotswap/only_fl_{i}/no_patch'
    # os.makedirs(hotswap_dest_base_dir, exist_ok=True)

    # source_base_dir = f'../fl_outputs/only_fl_output_mixtral_{i}/no_patch'
    # for task in no_hotswap_copy_list:
    #     source_path = get_source_dir(source_base_dir, task)
    #     task_dir = source_path.split('/')[-1]
    #     dest_path = os.path.join(hotswap_dest_base_dir, task_dir)
    #     shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
    
    # source_base_dir = f'../fl_outputs/only_fl_hotswap_{i}/no_patch'
    # for task in hotswap_copy_list:
    #     source_path = get_source_dir(source_base_dir, task)
    #     task_dir = source_path.split('/')[-1]
    #     dest_path = os.path.join(hotswap_dest_base_dir, task_dir)
    #     shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
    
    
    # mixtral_dest_base_dir = f'./results/mixtral/only_fl_{i}/no_patch'
    # os.makedirs(mixtral_dest_base_dir, exist_ok=True)

    # source_base_dir = f'../fl_outputs/only_fl_output_mixtral_{i}/no_patch'
    # for task in test_list:
    #     source_path = get_source_dir(source_base_dir, task)
    #     task_dir = source_path.split('/')[-1]
    #     dest_path = os.path.join(mixtral_dest_base_dir, task_dir)
    #     shutil.copytree(source_path, dest_path, dirs_exist_ok=True)


    gpt4_dest_base_dir = f'./results/gpt-4/only_fl_{i}/no_patch'
    os.makedirs(gpt4_dest_base_dir, exist_ok=True)

    source_base_dir = f'../fl_outputs/only_fl_output{i}/no_patch'
    for task in test_list:
        source_path = get_source_dir(source_base_dir, task)
        task_dir = source_path.split('/')[-1]
        dest_path = os.path.join(gpt4_dest_base_dir, task_dir)
        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)



