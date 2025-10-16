import os, json

def search_instance_with_two_fl(result_dir): # search in the applicable_patch dir in result_dir
    instance_list = os.listdir(os.path.join(result_dir, 'applicable_patch'))
    for instance_dir in instance_list:
        file_list = os.listdir(os.path.join(result_dir, "applicable_patch", instance_dir))

        max_idx = -1
        for file in file_list:
            if file.startswith('conversation_round_'):
                idx = int(file.split('_')[-1].removesuffix('.json'))
                if idx > max_idx:
                    max_idx = idx
        
        if max_idx >= 0:
            last_conversation_file = os.path.join(result_dir, 'applicable_patch', instance_dir, f'conversation_round_{max_idx}.json')
            with open(last_conversation_file, 'r') as f:
                last_conversation = json.load(f)
        
        final_fl_response = last_conversation[-1]["content"]
        if "Found 2 methods with name " in final_fl_response:
            print(instance_dir)

search_instance_with_two_fl('../results/acr-run-1')

