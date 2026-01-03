"""
Script to reuse FL results from k=1 to k=7 for tasks predicted as incorrect.
This copies the existing FL outputs from only_fl_output_mixtral_{1-5} directories.
"""

import os
import sys
import json
import shutil
from tqdm import tqdm
from collections import defaultdict

def load_tasks_to_rerun(predictions_file):
    """Load tasks that were predicted as incorrect and need to be re-run."""
    with open(predictions_file, 'r') as f:
        tasks_to_rerun = json.load(f)
    return tasks_to_rerun

def copy_fl_results_for_task(task_name, repetition, source_base, dest_base, k_max=7):
    """
    Copy FL results for a task from existing outputs (k=1 to k_max).

    Args:
        task_name: Name of the task (e.g., "django__django-12345")
        repetition: Repetition number (1-5)
        source_base: Base directory for source FL outputs
        dest_base: Base directory for destination outputs
        k_max: Maximum k to copy (default 7, since k=8 will be re-run)
    """
    source_dir = os.path.join(source_base, f'only_fl_output_mixtral_{repetition}', 'no_patch')

    # Find the instance directory for this task
    if not os.path.exists(source_dir):
        print(f"Warning: Source directory not found: {source_dir}")
        return False

    instance_dirs = os.listdir(source_dir)
    task_instance_dir = None

    for instance_dir in instance_dirs:
        if instance_dir.startswith(task_name):
            task_instance_dir = instance_dir
            break

    if not task_instance_dir:
        print(f"Warning: No instance directory found for task {task_name} in repetition {repetition}")
        return False

    source_task_dir = os.path.join(source_dir, task_instance_dir)

    # Copy to destination
    dest_dir = os.path.join(dest_base, f'rerun_output_{repetition}', 'no_patch', task_instance_dir)
    os.makedirs(os.path.dirname(dest_dir), exist_ok=True)

    # Copy the entire directory
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    shutil.copytree(source_task_dir, dest_dir)

    return True

def main():
    # Configuration
    k = 8
    predictions_dir = '/home/kimnal0/auto-code-rover/hotswap/predictions'
    tasks_to_rerun_file = os.path.join(predictions_dir, f'k{k}_tasks_to_rerun.json')

    source_base = '/home/kimnal0/auto-code-rover/fl_outputs'
    dest_base = '/home/kimnal0/auto-code-rover/hotswap/fl_outputs'

    # Load tasks to re-run
    print(f"Loading tasks to re-run from {tasks_to_rerun_file}")
    tasks_to_rerun = load_tasks_to_rerun(tasks_to_rerun_file)

    # Flatten all tasks across folds
    all_tasks = set()
    for fold, tasks in tasks_to_rerun.items():
        all_tasks.update(tasks)

    print(f"Total unique tasks to re-run: {len(all_tasks)}")

    # Copy FL results for each repetition (1-5)
    print("\nCopying FL results for k=1 to k=7 from existing outputs...")

    stats = defaultdict(lambda: {'success': 0, 'failed': 0})

    for repetition in range(1, 6):
        print(f"\nProcessing repetition {repetition}...")

        for task_name in tqdm(all_tasks, desc=f"Rep {repetition}"):
            success = copy_fl_results_for_task(
                task_name,
                repetition,
                source_base,
                dest_base,
                k_max=7
            )

            if success:
                stats[repetition]['success'] += 1
            else:
                stats[repetition]['failed'] += 1

    # Print summary
    print("\n" + "="*60)
    print("COPY SUMMARY")
    print("="*60)

    for repetition in range(1, 6):
        print(f"Repetition {repetition}:")
        print(f"  Successfully copied: {stats[repetition]['success']}")
        print(f"  Failed: {stats[repetition]['failed']}")

    print("\n" + "="*60)
    print("FL results for k=1-7 have been reused from existing outputs.")
    print("Next step: Run ACR for k=8 with gpt-4-0125-preview")
    print("="*60)

    # Save copy log
    log_file = os.path.join(dest_base, 'copy_log.json')
    with open(log_file, 'w') as f:
        json.dump({
            'total_tasks': len(all_tasks),
            'stats': dict(stats),
            'tasks_list': list(all_tasks)
        }, f, indent=4)

    print(f"\nCopy log saved to {log_file}")

if __name__ == "__main__":
    main()
