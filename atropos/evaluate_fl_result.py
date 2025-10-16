import json
import re
import os
from typing import List, Dict, Optional

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
            



# --- example usage ---
if __name__ == "__main__":
    save_bug_locations()
    


            


    # hunk_dict = extract_hunks_from_diff('/home/kimnal0/auto-code-rover/only_fl_output/django__django-11991_2025-10-15_04-38-30/developer_patch.diff')
    # modif_dict = extract_modificaiton_from_hunk(hunk_dict)



    # output_dir = '../only_fl_output'
    # instances_dir = os.listdir(output_dir)
    # for instance in instances_dir:
    #     diff_path = os.path.join(output_dir, instance, 'developer_patch.diff')
    #     fault_location = extract_gt_fl_from_diff(diff_path)