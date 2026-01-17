import os 
import argparse
import json
import shutil
from glob import glob

def get_source_dir(base_dir, task):
    pattern = os.path.join(base_dir, f'{task}*')
    matching_dirs = glob(pattern)

    if len(matching_dirs) == 1:
        return matching_dirs[0]
    else:
        raise ValueError


def copy_results_to_hotswap_dir(k):
    test_tasks_file = f'/home/kimnal0/auto-code-rover/atropos/results/parallel/embedding/fasttext/nhot_normal/sentence_vector/300d/not_add/label_criteria_1/test_bug_names2.json'

    with open(test_tasks_file, 'r') as f:
        test_tasks = json.load(f)

    test_list = []
    for i, tt in test_tasks.items():
        test_list.extend(tt)
    
    hotswap_tasks_file = f'/home/kimnal0/auto-code-rover/hotswap/predictions/k8_tasks_to_rerun.json'

    with open(hotswap_tasks_file, 'r') as f:
        hotswap_tasks_dict = json.load(f)
    hotswap_tasks = []
    for ht in hotswap_tasks_dict.values():
        hotswap_tasks.extend(ht)

    print(len(test_list))

    for task_name in test_list:
        for i in range(1, k+1):
            source_dir = f'/home/kimnal0/auto-code-rover/hotswap/results/mixtral/only_fl_{i}/no_patch'
            dest_dir = f'/home/kimnal0/auto-code-rover/hotswap/results/sequential_hotswap/{k}/only_fl_{i}/no_patch'
            source_path = get_source_dir(source_dir, task_name)
            task_dir = source_path.split('/')[-1]
            dest_path = os.path.join(dest_dir, task_dir)
            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
    
        for i in range(k+1, 6):
            dest_dir = f'/home/kimnal0/auto-code-rover/hotswap/results/sequential_hotswap/{k}/only_fl_{i}/no_patch'
            if task_name in hotswap_tasks:
                source_dir = f'/home/kimnal0/auto-code-rover/hotswap/results/gpt-4/only_fl_{i}/no_patch'
            else:
                source_dir = f'/home/kimnal0/auto-code-rover/hotswap/results/mixtral/only_fl_{i}/no_patch'

            source_path = get_source_dir(source_dir, task_name)
            task_dir = source_path.split('/')[-1]
            dest_path = os.path.join(dest_dir, task_dir)
            shutil.copytree(source_path, dest_path, dirs_exist_ok=True)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', default=1, type=int)
    args = parser.parse_args()

    copy_results_to_hotswap_dir(args.k)