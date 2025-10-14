import random

swe_full_tasks_file = '../conf/swe_full_tasks.txt'

with open(swe_full_tasks_file, 'r') as f:
    swe_full_instances = [line.strip() for line in f if line.strip()]

sampled_instances = random.sample(swe_full_instances, 500)

with open('../conf/sampled_tasks.txt', 'w') as f:
    f.write('\n'.join(sampled_instances))