"""
Compare Mixtral k=7 vs GPT-4 k=8 FL results.
"""

import json
import os
from pathlib import Path
from collections import defaultdict


def load_fl_results(output_dir, task_name):
    """
    Load FL results for a task from an output directory.

    Returns:
        {
            'bug_locations_before': [...],
            'bug_locations_after': [...],
            'tool_call_layers': [...],
            'rounds': {0: {...}, 1: {...}, ...}
        }
    """
    # Find task directory
    task_dirs = [d for d in os.listdir(os.path.join(output_dir, 'no_patch'))
                 if d.startswith(task_name)]

    if not task_dirs:
        return None

    task_dir = task_dirs[0]
    search_dir = os.path.join(output_dir, 'no_patch', task_dir, 'output_0', 'search')

    if not os.path.exists(search_dir):
        return None

    result = {
        'bug_locations_before': None,
        'bug_locations_after': None,
        'tool_call_layers': None,
        'rounds': {}
    }

    # Load bug locations
    bug_loc_before = os.path.join(search_dir, 'bug_locations_before_process.json')
    if os.path.exists(bug_loc_before):
        with open(bug_loc_before, 'r') as f:
            result['bug_locations_before'] = json.load(f)

    bug_loc_after = os.path.join(search_dir, 'bug_locations_after_process.json')
    if os.path.exists(bug_loc_after):
        with open(bug_loc_after, 'r') as f:
            result['bug_locations_after'] = json.load(f)

    # Load tool call layers
    tool_call_file = os.path.join(search_dir, 'tool_call_layers.json')
    if os.path.exists(tool_call_file):
        with open(tool_call_file, 'r') as f:
            result['tool_call_layers'] = json.load(f)

    # Load search rounds
    for round_file in sorted(Path(search_dir).glob('search_round_*.json')):
        round_num = int(round_file.stem.replace('search_round_', ''))
        with open(round_file, 'r') as f:
            result['rounds'][round_num] = json.load(f)

    return result


def compare_task(task_name, mixtral_base, gpt4_base):
    """Compare FL results for a single task."""

    print(f"\n{'='*80}")
    print(f"Task: {task_name}")
    print(f"{'='*80}")

    # Load Mixtral results (5 runs, majority voting)
    mixtral_results = []
    for i in range(1, 6):
        mixtral_dir = f"{mixtral_base}_{i}"
        result = load_fl_results(mixtral_dir, task_name)
        if result:
            mixtral_results.append(result)

    # Load GPT-4 results (5 runs, majority voting)
    gpt4_results = []
    for i in range(1, 6):
        gpt4_dir = f"{gpt4_base}_{i}"
        result = load_fl_results(gpt4_dir, task_name)
        if result:
            gpt4_results.append(result)

    if not mixtral_results:
        print("  ⚠️  No Mixtral results found")
    if not gpt4_results:
        print("  ⚠️  No GPT-4 results found")

    if not mixtral_results or not gpt4_results:
        return None

    # Compare rounds
    print("\n📊 Round Comparison:")

    max_mixtral_rounds = max(len(r['rounds']) for r in mixtral_results)
    max_gpt4_rounds = max(len(r['rounds']) for r in gpt4_results)

    print(f"  Mixtral: {max_mixtral_rounds} rounds")
    print(f"  GPT-4:   {max_gpt4_rounds} rounds")

    # Compare tool calls
    print("\n🔧 Tool Call Comparison:")

    for round_num in range(min(max_mixtral_rounds, max_gpt4_rounds)):
        print(f"\n  Round {round_num}:")

        # Get tool calls from both models
        mixtral_calls = []
        for result in mixtral_results:
            if result['tool_call_layers'] and round_num < len(result['tool_call_layers']):
                calls = [tc['func_name'] for tc in result['tool_call_layers'][round_num]]
                mixtral_calls.append(calls)

        gpt4_calls = []
        for result in gpt4_results:
            if result['tool_call_layers'] and round_num < len(result['tool_call_layers']):
                calls = [tc['func_name'] for tc in result['tool_call_layers'][round_num]]
                gpt4_calls.append(calls)

        if mixtral_calls:
            mixtral_calls_str = ', '.join(mixtral_calls[0]) if mixtral_calls[0] else 'None'
            print(f"    Mixtral: {mixtral_calls_str}")
        if gpt4_calls:
            gpt4_calls_str = ', '.join(gpt4_calls[0]) if gpt4_calls[0] else 'None'
            print(f"    GPT-4:   {gpt4_calls_str}")

    # Compare bug locations
    print("\n🎯 Bug Location Comparison:")

    mixtral_locs = [r['bug_locations_after'] for r in mixtral_results if r['bug_locations_after']]
    gpt4_locs = [r['bug_locations_after'] for r in gpt4_results if r['bug_locations_after']]

    if mixtral_locs:
        print(f"  Mixtral: {len(mixtral_locs[0])} locations")
        for loc in mixtral_locs[0][:3]:  # Show first 3
            print(f"    - {loc.get('rel_file_path', 'N/A')}::{loc.get('class_name', 'N/A')}#{loc.get('method_name', 'N/A')}")

    if gpt4_locs:
        print(f"  GPT-4:   {len(gpt4_locs[0])} locations")
        for loc in gpt4_locs[0][:3]:  # Show first 3
            print(f"    - {loc.get('rel_file_path', 'N/A')}::{loc.get('class_name', 'N/A')}#{loc.get('method_name', 'N/A')}")

    return {
        'task': task_name,
        'mixtral_rounds': max_mixtral_rounds,
        'gpt4_rounds': max_gpt4_rounds,
        'mixtral_locations': len(mixtral_locs[0]) if mixtral_locs else 0,
        'gpt4_locations': len(gpt4_locs[0]) if gpt4_locs else 0,
    }


def main():
    """Main comparison function."""

    # Paths
    mixtral_base = '/home/kimnal0/auto-code-rover/fl_outputs/only_fl_output_mixtral'
    gpt4_base = '/home/kimnal0/auto-code-rover/hotswap/fl_outputs/gpt4_k8_run'

    # Load task list
    tasks_file = '/home/kimnal0/auto-code-rover/hotswap/predictions/k8_tasks_to_rerun.json'

    if not os.path.exists(tasks_file):
        print("❌ Task list not found. Run predict_correctness.py first.")
        return

    with open(tasks_file, 'r') as f:
        tasks_dict = json.load(f)

    # Flatten tasks
    all_tasks = set()
    for fold, tasks in tasks_dict.items():
        all_tasks.update(tasks)

    all_tasks = sorted(list(all_tasks))

    print(f"Comparing {len(all_tasks)} tasks...")
    print(f"Mixtral base: {mixtral_base}")
    print(f"GPT-4 base:   {gpt4_base}")

    # Compare each task
    results = []
    for task in all_tasks[:5]:  # Start with first 5 for testing
        result = compare_task(task, mixtral_base, gpt4_base)
        if result:
            results.append(result)

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")

    if results:
        avg_mixtral_rounds = sum(r['mixtral_rounds'] for r in results) / len(results)
        avg_gpt4_rounds = sum(r['gpt4_rounds'] for r in results) / len(results)
        avg_mixtral_locs = sum(r['mixtral_locations'] for r in results) / len(results)
        avg_gpt4_locs = sum(r['gpt4_locations'] for r in results) / len(results)

        print(f"Average rounds:")
        print(f"  Mixtral: {avg_mixtral_rounds:.2f}")
        print(f"  GPT-4:   {avg_gpt4_rounds:.2f}")
        print(f"\nAverage bug locations:")
        print(f"  Mixtral: {avg_mixtral_locs:.2f}")
        print(f"  GPT-4:   {avg_gpt4_locs:.2f}")

    # Save results
    output_file = '/home/kimnal0/auto-code-rover/hotswap/comparison_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
