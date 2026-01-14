import os
import json
import argparse
import copy
import ast
import torch
import subprocess
import sys
import fasttext
import fasttext.util
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from tqdm import tqdm
from torch_geometric.utils import from_networkx

sys.path.insert(0, os.path.abspath('../..'))
from app.search.search_backend import SearchBackend
from app.data_structures import BugLocation, SearchResult

# fasttext.util.download_model('en', if_exists='ignore')
# fasttext_model = fasttext.load_model('cc.en.300.bin')
# embedding_size = 300

def checkout_commit(repo_path, commit_hash):
    try:
        subprocess.run(
            ['git', 'checkout', '-f', commit_hash],
            cwd=repo_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError as e:
        return False


class Data_generater():
    def __init__(self, repetition, label_criteria):
        self.repetition = repetition
        self.label_criteria = label_criteria
        self.function_types = ['search_class', 'search_class_in_file', 'search_method_in_file', 'search_method_in_class', 'search_method', 'search_code', 'search_code_in_file', 'get_code_around_line']
        self.ks = list(range(1, 11))
        self.ks.extend([15, 16])


        task_list_file = '../sampled_tasks_1_and_2.txt'
        with open(task_list_file, 'r') as f:
            self.task_list = f.read().splitlines()
        # self.task_list = ['astropy__astropy-6938']
        # self.task_list = ['django__django-17066']
        # self.task_list = ['astropy__astropy-6938', 'django__django-17066']
        # self.task_list = ['scikit-learn__scikit-learn-26400']
        ########## Filtering fl results directly and save ##############
        self.fl_results = dict()
        for i in range(1, self.repetition+1):
            self.fl_results[i] = self.extract_fl_results(i)
        self.check_granuarity()
        # fl_results_output_file = "../fl_results/filtered_fl_results_mixtral.json"
        # with open(fl_results_output_file, 'w') as f:
        #     json.dump(self.fl_results, f, indent=4)
        ################################################################

        # ################ Load the filtered_fl_results ###############
        # with open("../fl_results/filtered_fl_results_mixtral.json", 'r') as f:
        #     filtered_fl_results = json.load(f)
        # self.fl_results = {int(k): v for k, v in filtered_fl_results.items()}
        # #############################################################
    
    def check_granuarity(self):
        num_file = 0
        num_class = 0
        num_method = 0
        for i in range(1, self.repetition+1):
            for task, fl_result_list in self.fl_results[i].items():
                for fl_result in fl_result_list:
                    if not fl_result["class_name"] and fl_result["method_name"]:
                        num_file += 1
                    elif fl_result["method_name"]:
                        num_method += 1
                    else:
                        num_class += 1
        print(f"Num file: {num_file}")
        print(f"Num class: {num_class}")
        print(f"Num method: {num_method}")
                        

    
    def extract_fl_results(self, idx):
        result_dir = f'../../fl_outputs/only_fl_output_mixtral_{idx}'
        instance_dir_list = os.listdir(os.path.join(result_dir, 'no_patch'))

        filtered_fl_dict = dict()

        with open('../../SWE-bench/setup_result/setup_map.json', 'r') as f:
            setup_map = json.load(f)
        with open('../../SWE-bench/setup_result/tasks_map.json', 'r') as f:
            tasks_map = json.load(f)

        print(f"Filtering fl results for repetition {idx}")
        for instance_dir in tqdm(instance_dir_list):
            splited_instance_dir = instance_dir.split('_')
            instance_name = f"{splited_instance_dir[0]}__{splited_instance_dir[2]}"
            filtered_fl_dict[instance_name] = []

            project_path = setup_map[instance_name]["repo_path"]
            if not os.path.exists(project_path):
                continue

            task_info = tasks_map[instance_name]
            task_commit = task_info.get("base_commit") or task_info.get("commit")

            checkout_result = checkout_commit(project_path, task_commit) # returns True if checked out successfully, False otherwise
            if not checkout_result:
                continue

            fl_before_process_path = os.path.join(result_dir, 'no_patch', instance_dir, 'output_0/search/bug_locations_before_process.json')

            try:
                with open(fl_before_process_path, 'r') as f:
                    fl_before_process = json.load(f)
            except:
                fl_before_process = []
            
            if not fl_before_process:
                continue

            backend = SearchBackend(project_path)

            res: SearchBackend
            for bug_location_dict in fl_before_process:
                tmp_file_name = bug_location_dict.get("file", "")
                tmp_class_name = bug_location_dict.get("class", "")
                tmp_method_name = bug_location_dict.get("method", "")
                intended_behavior = bug_location_dict.get("intended_behavior", "")

                # Handle Class.method format
                if not tmp_class_name and tmp_method_name and "." in tmp_method_name:
                    fragments = tmp_method_name.split(".")
                    if len(fragments) == 2:
                        tmp_class_name, tmp_method_name = fragments
                
                if not (tmp_file_name or tmp_class_name or tmp_method_name):
                    continue

                search_res = []

                # Case 1: class + method
                if tmp_class_name and tmp_method_name:
                    output, curr_search_res, call_ok = backend.search_method_in_class(tmp_method_name, tmp_class_name)
                    search_res.extend(curr_search_res)

                    res: SearchResult
                    if call_ok:
                        for res in curr_search_res:
                            if (res.class_name is None or res.func_name is None or res.file_path is None):
                                continue

                            inherited_output, inherited_search_res, _ = backend._get_inherited_methods(res.class_name, res.func_name)
                            search_res.extend(inherited_search_res)
                
                # Case 2: file + method (no class)
                elif tmp_file_name and tmp_method_name and not tmp_class_name:
                    output, search_res, call_ok = backend.search_method_in_file(tmp_method_name, tmp_file_name)
                
                # Case 3: file + class (no method)
                elif tmp_file_name and tmp_class_name and not tmp_method_name:
                    output, search_res, call_ok = backend.search_class_in_file(tmp_class_name, tmp_file_name)
                
                # Case 4: class only (no file, no method)
                elif tmp_class_name and not tmp_method_name and not tmp_file_name:
                    output, search_res, call_ok = backend.get_class_full_snippet(tmp_class_name)
                
                # Case 5: method only (no class, no file)
                elif tmp_method_name and not tmp_class_name and not tmp_file_name:
                    output, search_res, call_ok = backend.search_method(tmp_method_name)
                
                # Case 6: file only (no method, no class)
                elif tmp_file_name and not tmp_method_name and not tmp_class_name:
                    output, search_res, call_ok = backend.get_file_content(tmp_file_name)
                
                res: SearchResult
                final_bug_locs: list[BugLocation] = []
                for res in search_res:
                    if not hasattr(res, 'start') or not hasattr(res, 'end'):
                        continue
                    if res.start is None or res.end is None:
                        continue
                    new_bug_loc = BugLocation(res, project_path, intended_behavior)
                    final_bug_locs.append(new_bug_loc)
                
                unique_bug_locations = []
                for loc in final_bug_locs:
                    if loc not in unique_bug_locations:
                        unique_bug_locations.append(loc)
                
                if unique_bug_locations:
                    for loc in unique_bug_locations:
                        bug_loc_dict = loc.to_dict()
                        bug_loc_dict["result_dir"] = os.path.join(result_dir, 'no_patch', instance_dir)
                        filtered_fl_dict[instance_name].append(bug_loc_dict)
        
        return filtered_fl_dict
    
    def vote_and_ranks_answers(self):
        def tie_break(task, tie_methods):
            tie_broken_methods = []

            for i in range(1, self.repetition+1):
                fl_result = self.fl_results[i]
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

        for i in range(1, self.repetition+1):
            fl_result = self.fl_results[i]
            for task in self.task_list:
                answer_list = fl_result[task]
                for answer in answer_list:
                    signature = f'{answer["rel_file_path"]}::{answer["class_name"]}#{answer["method_name"]}_{answer["start"]}_{answer["end"]}'
                    voting_score_dict[task][signature] += 1/len(answer_list)

        for task, scores_dict in voting_score_dict.items():
            for signature in scores_dict.keys():
                # voting_score_dict[task][signature] /= 5
                scores_dict[signature] /= self.repetition
        # print(voting_score_dict['sphinx-doc__sphinx-9461'])
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
        
        combined_result_dict = {'ranking': ranking_dict, 'confidence_score': voting_score_dict}

        return combined_result_dict


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repetition', default=5, type=int)
    parser.add_argument('-l', '--label_criteria', default=1, type=int)
    args = parser.parse_args()

    data_generater = Data_generater(args.repetition, args.label_criteria)



    


