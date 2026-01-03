"""
Script to re-run ACR for k=8 with gpt-4-0125-preview model.
This script will run ACR 5 times for each task predicted as incorrect.
"""

import os
import sys
import json
import subprocess
from tqdm import tqdm
from datetime import datetime

def load_tasks_to_rerun(predictions_file):
    """Load tasks that were predicted as incorrect and need to be re-run."""
    with open(predictions_file, 'r') as f:
        tasks_to_rerun = json.load(f)
    return tasks_to_rerun

def create_task_list_file(tasks, output_file):
    """Create a task list file for ACR."""
    with open(output_file, 'w') as f:
        for task in tasks:
            f.write(f"{task}\n")

def run_acr_for_repetition(task_list_file, repetition, output_dir, model="gpt-4-0125-preview"):
    """
    Run ACR for a given repetition.

    Args:
        task_list_file: Path to file containing list of tasks
        repetition: Repetition number (1-5)
        output_dir: Base output directory
        model: Model to use for ACR
    """
    rep_output_dir = os.path.join(output_dir, f'rerun_output_{repetition}')

    # Prepare ACR command
    cmd = [
        'python',
        'app/main.py',
        'swe-bench',
        '--model', model,
        '--setup-map', 'SWE-bench/setup_result/setup_map.json',
        '--tasks-map', 'SWE-bench/setup_result/tasks_map.json',
        '--output-dir', rep_output_dir,
        '--task-list-file', task_list_file
    ]

    # Set environment variables
    env = os.environ.copy()
    env['PYTHONPATH'] = '.'

    print(f"\nRunning ACR repetition {repetition}...")
    print(f"Command: {' '.join(cmd)}")
    print(f"Output directory: {rep_output_dir}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        result = subprocess.run(
            cmd,
            cwd='/home/kimnal0/auto-code-rover',
            env=env,
            capture_output=True,
            text=True,
            check=True
        )

        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Status: SUCCESS")

        return True, result.stdout, result.stderr

    except subprocess.CalledProcessError as e:
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Status: FAILED")
        print(f"Error: {e}")

        return False, e.stdout, e.stderr

def main():
    # Configuration
    k = 8
    model = "gpt-4-0125-preview"
    predictions_dir = '/home/kimnal0/auto-code-rover/hotswap/predictions'
    tasks_to_rerun_file = os.path.join(predictions_dir, f'k{k}_tasks_to_rerun.json')

    output_dir = '/home/kimnal0/auto-code-rover/hotswap/fl_outputs'
    os.makedirs(output_dir, exist_ok=True)

    # Load tasks to re-run
    print(f"Loading tasks to re-run from {tasks_to_rerun_file}")
    tasks_to_rerun = load_tasks_to_rerun(tasks_to_rerun_file)

    # Flatten all tasks across folds
    all_tasks = set()
    for fold, tasks in tasks_to_rerun.items():
        all_tasks.update(tasks)

    all_tasks = sorted(list(all_tasks))

    print(f"\n{'='*60}")
    print(f"Total unique tasks to re-run: {len(all_tasks)}")
    print(f"Model: {model}")
    print(f"Repetitions: 5")
    print(f"{'='*60}\n")

    # Create task list file
    task_list_file = os.path.join(output_dir, 'tasks_to_rerun.txt')
    create_task_list_file(all_tasks, task_list_file)
    print(f"Task list file created: {task_list_file}")

    # Run ACR for each repetition (5 times)
    run_log = {
        'model': model,
        'k': k,
        'total_tasks': len(all_tasks),
        'tasks': all_tasks,
        'repetitions': {}
    }

    for repetition in range(1, 6):
        print(f"\n{'='*80}")
        print(f"REPETITION {repetition}/5")
        print(f"{'='*80}")

        success, stdout, stderr = run_acr_for_repetition(
            task_list_file,
            repetition,
            output_dir,
            model
        )

        run_log['repetitions'][repetition] = {
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'output_dir': os.path.join(output_dir, f'rerun_output_{repetition}')
        }

        # Save logs
        log_dir = os.path.join(output_dir, f'rerun_output_{repetition}', 'logs')
        os.makedirs(log_dir, exist_ok=True)

        with open(os.path.join(log_dir, 'stdout.log'), 'w') as f:
            f.write(stdout)

        with open(os.path.join(log_dir, 'stderr.log'), 'w') as f:
            f.write(stderr)

        if not success:
            print(f"\n!!! WARNING: Repetition {repetition} failed !!!")
            print(f"Check logs at: {log_dir}")

    # Save overall run log
    log_file = os.path.join(output_dir, 'acr_run_log.json')
    with open(log_file, 'w') as f:
        json.dump(run_log, f, indent=4)

    print(f"\n{'='*80}")
    print("ACR RE-RUN COMPLETE")
    print(f"{'='*80}")
    print(f"Run log saved to: {log_file}")

    # Print summary
    successful_reps = sum(1 for rep_info in run_log['repetitions'].values() if rep_info['success'])
    print(f"\nSuccessful repetitions: {successful_reps}/5")

    if successful_reps < 5:
        print("\n!!! WARNING: Some repetitions failed. Check the logs for details.")
    else:
        print("\nAll repetitions completed successfully!")

if __name__ == "__main__":
    main()
