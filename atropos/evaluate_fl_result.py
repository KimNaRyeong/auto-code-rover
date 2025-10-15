import json
import re
import os

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


            
# def evaluate_fl_result(diff_path):

            


hunk_dict = extract_hunks_from_diff('/home/kimnal0/auto-code-rover/only_fl_output/django__django-11991_2025-10-15_04-38-30/developer_patch.diff')
modif_dict = extract_modificaiton_from_hunk(hunk_dict)



# output_dir = '../only_fl_output'
# instances_dir = os.listdir(output_dir)
# for instance in instances_dir:
#     diff_path = os.path.join(output_dir, instance, 'developer_patch.diff')
#     fault_location = extract_gt_fl_from_diff(diff_path)