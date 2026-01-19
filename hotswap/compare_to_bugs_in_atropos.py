import json

original_file = '/home/kimnal0/auto-code-rover/hotswap/predictions/k8_tasks_to_rerun.json'
new_file = '/home/kimnal0/atropos/hotswap/auto-code-rover/parallel_predictions/k8_tasks_to_rerun.json'

with open(original_file, 'r') as f:
    original_results = json.load(f)
with open(new_file, 'r') as f:
    new_results = json.load(f)

original_bugs = []
for _, bugs in original_results.items():
    original_bugs.extend(bugs)

new_bugs = []
for _, bugs in new_results.items():
    new_bugs.extend(bugs)

for new_bug in new_bugs:
    if new_bug not in original_bugs:
        print(new_bug)