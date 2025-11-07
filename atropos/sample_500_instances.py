import random

swe_full_tasks_file = '../conf/swe_full_tasks.txt'
swe_old_sampled_tasks_file = './sampled_tasks.txt'

with open(swe_full_tasks_file, 'r') as f:
    swe_full_instances = [line.strip() for line in f if line.strip()]
with open(swe_old_sampled_tasks_file, 'r') as f:
    swe_old_tasks = [line.strip() for line in f if line.strip()]

remaining = list(set(swe_full_instances) - set(swe_old_tasks))
print(len(swe_full_instances))
print(len(swe_old_tasks))
print(len(remaining))
new_sampled_instances = random.sample(remaining, 500)

with open('../conf/sampled_tasks2.txt', 'w') as f:
    f.write('\n'.join(new_sampled_instances))

whole_sampled_tasks = swe_old_tasks + new_sampled_instances
print(whole_sampled_tasks)
with open('../conf/sampled_tasks_1_and_2.txt', 'w') as f:
    f.write('\n'.join(whole_sampled_tasks))