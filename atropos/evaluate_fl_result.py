import json
import re
import os
from typing import List, Dict, Optional
from collections import defaultdict

def extract_hunks_from_diff(diff_file_path):
    hunk_dict = dict()

    with open(diff_file_path, 'r') as f:
        diff_lines = f.read().splitlines()

    in_hunk = False
    for i, line in enumerate(diff_lines):

        if line.startswith('--- '):
            buggy_file = '/'.join(line.split()[1].split('/')[1:])
            hunk_dict[buggy_file] = []

        elif line.startswith('@@ '):
            in_hunk = True

            # buggy_method = line.split('def')[-1].strip()
            # if buggy_method.endswith(':'):
            #     buggy_method = buggy_method[:-1]
            
            hunk_start_lineno, range = line.split()[1][1:].split(',')
            hunk_start_lineno = int(hunk_start_lineno) 
            hunk = []
        
        elif in_hunk:
            hunk.append(line)

            if i == len(diff_lines) -1 or diff_lines[i+1].startswith('diff ') or diff_lines[i+1].startswith('--- ') or diff_lines[i+1].startswith('+++ ') or diff_lines[i+1].startswith('@@ '):
                in_hunk = False
                hunk_dict[buggy_file].append({'hunk': hunk, 'hunk_start_lineno': hunk_start_lineno})
    
    # for file, hunk_list in hunk_dict.items():
    #     for hunk_info in hunk_list:
    #         print('------')
    #         print(file)
    #         print('\n'.join(hunk_info['hunk']))
    #         print(hunk_info['hunk_start_lineno'])
    
    return hunk_dict

"""
- input: hunk dictionary with the key of """
def extract_modificaiton_from_hunk(hunk_dict):
    modif_dict = dict()
    for file, hunk_list in hunk_dict.items():
        modif_dict[file] = []
        for hunk_info in hunk_list:
            start_lineno = hunk_info['hunk_start_lineno']
            hunk = hunk_info['hunk']

            skipped_head_lineno = 0
            while not (hunk[0].startswith('-') or hunk[0].startswith('+')):
                del hunk[0]
                skipped_head_lineno += 1
            
            skipped_tail_lineno = 0
            while not (hunk[-1].startswith('-') or hunk[-1].startswith('+')):
                del hunk[-1]
                skipped_tail_lineno += 1
            
            modif_start_lineno = start_lineno + skipped_head_lineno

            added_lineno = 0
            for line in hunk:
                if line.startswith('+'):
                    added_lineno += 1

            if len(hunk) == added_lineno:
                modif_end_lineno = modif_start_lineno
            else:
                modif_end_lineno = modif_start_lineno + len(hunk) -1 - added_lineno

            modif_dict[file].append({'hunk': hunk, 'start_lineno': modif_start_lineno, 'end_lineno': modif_end_lineno})
            # print('---------')
            # print('\n'.join(hunk))
            # print(start_lineno)
            # print(modif_start_lineno)
            # print(modif_end_lineno)
    return modif_dict


import re

def extract_search_results(text: str) -> List[Dict[str, Optional[str]]]:
    """
    Extract 'Search result N:' blocks and pull out <file>, <class>, and <func>/<function>.
    If <class> or <func> is missing, set it to None.
    """
    # 찾을 블록의 시작 위치들
    header_pat = re.compile(r"Search result\s+\d+:\s*", re.IGNORECASE)
    matches = list(header_pat.finditer(text))

    # 블록 경계 계산
    blocks = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append(text[start:end])

    results: List[Dict[str, Optional[str]]] = []
    for block in blocks:
        # 각 태그는 선택적으로 존재 → 없으면 None
        file_m = re.search(r"<file>(.*?)</file>", block, flags=re.DOTALL | re.IGNORECASE)
        class_m = re.search(r"<class>(.*?)</class>", block, flags=re.DOTALL | re.IGNORECASE)
        func_m  = re.search(r"<(?:func|function)>(.*?)</(?:func|function)>",
                            block, flags=re.DOTALL | re.IGNORECASE)

        file_val  = file_m.group(1).strip()  if file_m  else None
        class_val = class_m.group(1).strip() if class_m else None
        func_val  = func_m.group(1).strip()  if func_m  else None

        results.append({
            "file": file_val,
            "class": class_val,
            "func": func_val,
        })

    return results

def save_bug_locations():
    with open('./sampled_tasks.txt', 'r') as f:
        sampled_tasks = f.read().splitlines()
    # sampled_tasks = ['astropy__astropy-14413']

    exists_result_dirs = ['acr-run-1', 'acr-run-2', 'acr-run-3']
    sub_dirs = ['applicable_patch', 'matched_but_empty_diff', 'matched_but_empty_origin', 'raw_patch_but_unmatched', 'raw_patch_but_unparsed']

    for result_dir in exists_result_dirs:
        matched_task = []
        for task in sampled_tasks:
            # print(task)
            num_match = 0
            for sub_dir in sub_dirs:
                dir_path = os.path.join('../results', result_dir, sub_dir)
                # print(dir_path)
                if os.path.exists(dir_path):
                    results_list = os.listdir(dir_path)
                    for instance_result in results_list:
                        if instance_result.startswith(task):
                            num_match += 1
            
            if num_match == 1:
                matched_task.append(task)
        print('----------------')
        print(result_dir)
        print(len(matched_task))
        print(matched_task)
    
    for result_dir in exists_result_dirs:
        instances = []
        for sub_dir in sub_dirs:
            dir_path = os.path.join('../results', result_dir, sub_dir)
            # print(dir_path)
            if os.path.exists(dir_path):
                results_list = os.listdir(dir_path)
                instances.extend(results_list)
        
        print(len(instances))

"""
- input: the path of result directory
- output: the dictionary of filtered fault location (the final answer of the fl part of ACR)

Comparing the intended_behavior of before_process and after_process and filtering the matched ones.
"""
def extract_fl_results(result_dir):
    instance_dir_list = os.listdir(os.path.join(result_dir, 'no_patch'))

    filtered_fl_dict = defaultdict(list)

    # instance_dir_list = ['astropy__astropy-6938_2025-10-15_02-57-48']
    for instance_dir in instance_dir_list:
        splited_instance_dir = instance_dir.split('_')
        instance_name = f"{splited_instance_dir[0]}__{splited_instance_dir[2]}"

        fl_before_process_path = os.path.join(result_dir, 'no_patch', instance_dir, 'output_0/search/bug_locations_before_process.json')
        fl_after_process_path = os.path.join(result_dir, 'no_patch', instance_dir, 'output_0/search/bug_locations_after_process.json')
        try:
            with open(fl_before_process_path, 'r') as f:
                fl_before_process = json.load(f)
        except:
            fl_before_process = []
        
        try:
            with open(fl_after_process_path, 'r') as f:
                fl_after_process = json.load(f)
        except:
            fl_after_process = []
        
        if not fl_before_process or not fl_after_process:
            filtered_fl_dict[instance_name] = []

        
        for raw_fl in fl_before_process:
            intended_behavior = raw_fl["intended_behavior"]

            for searched_fl in fl_after_process:
                searched_fl_intended_behavior = searched_fl["intended_behavior"]
                if intended_behavior == searched_fl_intended_behavior:
                    searched_fl["result_dir"] = os.path.join(result_dir, 'no_patch', instance_dir)
                    filtered_fl_dict[instance_name].append(searched_fl)
    
    return filtered_fl_dict

        
def save_diff_modif_dict(result_dir):
    instance_dir_list = os.listdir(os.path.join(result_dir, 'no_patch'))

    modif_from_diff_dict = dict()

    # instance_dir_list = ['astropy__astropy-6938_2025-10-15_02-57-48']
    for instance_dir in instance_dir_list:
        splited_instance_dir = instance_dir.split('_')
        instance_name = f"{splited_instance_dir[0]}__{splited_instance_dir[2]}"

        developer_patch_path = os.path.join(result_dir, 'no_patch', instance_dir, 'developer_patch.diff')
        hunk_dict = extract_hunks_from_diff(developer_patch_path)
        modif_dict = extract_modificaiton_from_hunk(hunk_dict)

        modif_from_diff_dict[instance_name] = modif_dict
    
    with open('./modif_from_developer_patch.json', 'w') as f:
        json.dump(modif_from_diff_dict, f, indent=4)

# def vote_fl(filtered_result_dir):
#     filtered_result_files = os.listdir(filtered_result_dir)



    

def verify_difficulty_of_benchmark():
    with open('../conf/swe_lite_tasks.txt', 'r') as f:
        swe_lite_tasks = f.read().splitlines()
    
    with open('./fl_results/filtered_fl_result_1.json', 'r') as f:
        fl_result1 = json.load(f)

    with open('./fl_results/filtered_fl_result_2.json', 'r') as f:
        fl_result2 = json.load(f)
    
    with open('./modif_from_developer_patch.json', 'r') as f:
        modif_from_diff_dict = json.load(f)
    
    num_success = 0
    num_lite = 0
    num_success_lite = 0
    num_total = 0

    for instance, fl_list in fl_result1.items():
        num_total += 1
        success = False
        if instance in swe_lite_tasks:
            num_lite += 1
        for fl in fl_list:
            if fl["rel_file_path"] in modif_from_diff_dict[instance].keys():
                for modif in modif_from_diff_dict[instance][fl["rel_file_path"]]:
                    if fl["start"] <= modif["start_lineno"] and fl["end"] >= modif["end_lineno"]:
                        success = True
                        break
                
            if success:
                break
        
        if success:
            num_success += 1
            if instance in swe_lite_tasks:
                num_success_lite += 1
    
    for instance, fl_list in fl_result2.items():
        num_total += 1
        success = False
        if instance in swe_lite_tasks:
            num_lite += 1
        for fl in fl_list:
            if fl["rel_file_path"] in modif_from_diff_dict[instance].keys():
                for modif in modif_from_diff_dict[instance][fl["rel_file_path"]]:
                    if fl["start"] <= modif["start_lineno"] and fl["end"] >= modif["end_lineno"]:
                        success = True
                        break
                
            if success:
                break
        
        if success:
            num_success += 1
            if instance in swe_lite_tasks:
                num_success_lite += 1

    print(f"Num total: {num_total}")
    print(f"Num swe-bench-lite: {num_lite}")
    print(f"Num success: {num_success}")
    print(f"Num success in swe-bench-lite: {num_success_lite}")

def analysis_result_type():
    with open('../conf/swe_lite_tasks.txt', 'r') as f:
        swe_lite_tasks = f.read().splitlines()
    with open('./fl_results/filtered_fl_result_1.json', 'r') as f:
        fl_result1 = json.load(f)
    
    class_method = 0
    only_class = 0
    only_method = 0
    only_file =0


    for instance, fl_list in fl_result1.items():
        if instance not in swe_lite_tasks:
            continue
        for fl in fl_list:
            if fl["class_name"]:
                if fl["method_name"]:
                    class_method += 1
                else:
                    only_class += 1
            else:
                if fl["method_name"]:
                    only_method += 1
                else:
                    only_file += 1
    
    print(f"Num class_method: {class_method}")
    print(f"Num only file: {only_file}")
    print(f"Num only class: {only_class}")
    print(f"Num only method: {only_method}")


def vote_and_ranks_final_answers():
    def tie_break(task, tie_methods):
        tie_broken_methods = []

        for i in range(1, 6):
            filtered_fl_result_file = f'./fl_results/filtered_fl_result_{i}.json'
            with open(filtered_fl_result_file, 'r') as f:
                fl_result = json.load(f)
            answer_list = fl_result[task]
            for answer in answer_list:
                signature = f'{answer["rel_file_path"]}::{answer["class_name"]}#{answer["method_name"]}_{answer["start"]}_{answer["end"]}'
                if signature in tie_methods:
                    tie_broken_methods.append(signature)
                    tie_methods.remove(signature)

                    if not tie_methods:
                        return tie_broken_methods

    
    voting_score_dict = defaultdict(lambda: defaultdict(float))
    ranking_dict = dict()

    task_list_file = './sampled_tasks.txt'
    with open(task_list_file, 'r') as f:
        task_list = f.read().splitlines()

    for i in range(1, 6):
        filtered_fl_result_file = f'./fl_results/filtered_fl_result_{i}.json'
        with open(filtered_fl_result_file, 'r') as f:
            fl_result = json.load(f)
        for task in task_list:
            answer_list = fl_result[task]
            for answer in answer_list:
                signature = f'{answer["rel_file_path"]}::{answer["class_name"]}#{answer["method_name"]}_{answer["start"]}_{answer["end"]}'
                voting_score_dict[task][signature] += 1/len(answer_list)


    for task, voting_scores in voting_score_dict.items():
        ranking = []
        groups = defaultdict(list)
        for m, s in voting_scores.items():
            groups[s].append(m)
        sorted_groups = sorted(groups.items(), key=lambda x: x[0], reverse=True)

        for s, m in sorted_groups:
            if len(m) < 2:
                ranking.extend(m)
            else:
                ranking.extend(tie_break(task, m))
        ranking_dict[task] = ranking

    return ranking_dict
        

    

        


    


            
            



# --- example usage ---
if __name__ == "__main__":
    # save_bug_locations()
    # filtered_fl_dict1 = extract_fl_results("../only_fl_output")
    # # print(filtered_fl_dict1)
    # filtered_fl_dict2 = extract_fl_results("../only_fl_output2")
    # # print(filtered_fl_dict2)
    # filtered_fl_dict3 = extract_fl_results("../only_fl_output3")
    # filtered_fl_dict4 = extract_fl_results("../only_fl_output4")
    # filtered_fl_dict5 = extract_fl_results("../only_fl_output5")

    # with open('./fl_results/filtered_fl_result_1.json', 'w') as f:
    #     json.dump(filtered_fl_dict1, f, indent=4)
    # with open('./fl_results/filtered_fl_result_2.json', 'w') as f:
    #     json.dump(filtered_fl_dict2, f, indent=4)
    # with open('./fl_results/filtered_fl_result_3.json', 'w') as f:
    #     json.dump(filtered_fl_dict3, f, indent=4)
    # with open('./fl_results/filtered_fl_result_4.json', 'w') as f:
    #     json.dump(filtered_fl_dict4, f, indent=4)
    # with open('./fl_results/filtered_fl_result_5.json', 'w') as f:
    #     json.dump(filtered_fl_dict5, f, indent=4)

    # # save_diff_modif_dict("../only_fl_output")

    # verify_difficulty_of_benchmark()
    # with open('./sampled_tasks.txt', 'r') as f:
    #     sampled_tasks = f.read().splitlines()
    # with open('./fl_results/filtered_fl_result_1.json', 'r') as f:
    #     fl_result1 = json.load(f)
    # instances_in_fl_result = fl_result1.keys()
    # for task in sampled_tasks:
    #     if task not in instances_in_fl_result:
    #         print(task)

    # analysis_result_type()





            


    # hunk_dict = extract_hunks_from_diff('/home/kimnal0/auto-code-rover/only_fl_output/no_patch/django__django-11991_2025-10-15_04-38-30/developer_patch.diff')
    # print(hunk_dict[0].keys())
    # modif_dict = extract_modificaiton_from_hunk(hunk_dict)
    # print(modif_dict['django/contrib/gis/db/backends/postgis/schema.py'])



    # output_dir = '../only_fl_output'
    # instances_dir = os.listdir(output_dir)
    # for instance in instances_dir:
    #     diff_path = os.path.join(output_dir, instance, 'developer_patch.diff')
    #     fault_location = extract_gt_fl_from_diff(diff_path)

    # instance_dir_list = os.listdir(os.path.join('../only_fl_output', 'no_patch'))
    # for instance in instance_dir_list:
    #     search_files = os.listdir(os.path.join('../only_fl_output/no_patch', instance, 'output_0/search'))

    #     max_idx = 0
    #     for sf in search_files:
    #         if sf.startswith('search_round_'):
    #             idx = int(sf.split('_')[-1].removesuffix('.json'))
    #             if max_idx < idx:
    #                 max_idx = idx
        
    #     if max_idx > 5:
    #         print(instance)

    ranking_dict = vote_and_ranks_final_answers()
    with open('./combined_fl_results.json', 'w') as f:
        json.dump(ranking_dict, f, indent=4)
    


