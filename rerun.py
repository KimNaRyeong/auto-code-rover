import subprocess as sp
import os
import argparse

def main(result_dir):
    done_dirs = os.listdir(result_dir)
    done_tasks = []

    for dir in done_dirs:
        split_dir = dir.split('_')
        done_tasks.append(split_dir[0]+'__'+split_dir[2])

    sampled_tasks_file = './atropos/sampled_tasks2.txt'
    with open(sampled_tasks_file, 'r') as f:
        sampled_tasks = f.read().splitlines()
    
    remain_tasks = list(set(sampled_tasks)- set(done_tasks))
    remain_tasks_file = './atropos/remain_tasks.txt'
    remain_tasks_file_in_swebench = './SWE-bench/remain_tasks.txt'
    with open(remain_tasks_file, 'w') as f:
        f.write('\n'.join(remain_tasks))

    with open(remain_tasks_file_in_swebench, 'w') as f:
        f.write('\n'.join(remain_tasks))
    




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--result_dir')
    args = parser.parse_args()

    main(args.result_dir)