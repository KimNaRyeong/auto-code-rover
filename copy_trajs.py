import shutil

for i in range(1, 6):
    source_dir = f'/home/kimnal0/auto-code-rover/fl_outputs/only_fl_output_mixtral_{i}'
    dest_dir = f'/home/kimnal0/atropos/trajectories/auto-code-rover/only_fl_output_mixtral_{i}'
    shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)

    source_dir = f'/home/kimnal0/auto-code-rover/fl_outputs/only_fl_output{i}'
    dest_dir = f'/home/kimnal0/atropos/trajectories/auto-code-rover/only_fl_output_gpt-4_{i}'
    shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)