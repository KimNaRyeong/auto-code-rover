import os
import json
import argparse
import copy
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from tqdm import tqdm

class Data_generater():
    def __init__(self, repetition, nhot = True, including_answer = True, one_arg_vector_size = False):
        self.repetition = repetition
        self.nhot = nhot
        self.including_answer = including_answer
        self.one_arg_vector_size = one_arg_vector_size
        self.function_types = ['search_class', 'search_class_in_file', 'search_method_in_file', 'search_method_in_class', 'search_method', 'search_code', 'search_code_in_file', 'get_code_around_line']
        if nhot:
            self.ks = list(range(1, 11))
            if self.including_answer:
                self.ks.append(15)
            else:
                self.ks.extend([15, 16])
        else:
            self.ks = list(range(1, 11))
            if self.including_answer:
                self.ks.append(15)
            else:
                self.ks.extend([15, 32])

        self.max_length_for_each_traj = None

        task_list_file = './sampled_tasks.txt'
        with open(task_list_file, 'r') as f:
            self.task_list = f.read().splitlines()
        self.task_list = ['astropy__astropy-6938']
        # self.task_list = ['django__django-17066']
        # self.task_list = ['astropy__astropy-6938', 'django__django-17066']
        self.trajs_dict = self.extract_trajs_from_logs()
        self.reasoning_paths_dict = self.generate_reasoning_paths_dict()

        print(self.trajs_dict)
        print()
        print(self.reasoning_paths_dict)
        print(len(self.trajs_dict['astropy__astropy-6938'][1]))
        print(len(self.reasoning_paths_dict['astropy__astropy-6938'][0]))
        self.args_dict = self.get_args_dict_for_k()
        self.arg_vector_size_dict = self.get_arg_vector_size()
        self.label_dict = self.get_labels_dict()
    
    def extract_trajs_from_logs(self):
        trajs_dict = defaultdict(dict)

        print("Collecting the reasoning trajectories...")
        for task in tqdm(self.task_list):
            for i in range(1, self.repetition+1):

                if i == 1:
                    output_dir = '../only_fl_output/no_patch'
                else:
                    output_dir = f'../only_fl_output{i}/no_patch'
                instance_list = os.listdir(output_dir)

                tool_call_layer_file = None
                for instance in instance_list:
                    if instance.startswith(task):
                        tool_call_layer_file = os.path.join(output_dir, instance, 'output_0/search/tool_call_layers.json')
                        break
                
                if not os.path.exists(tool_call_layer_file):
                    trajs_dict[task][i] = []
                else:
                    with open(tool_call_layer_file, 'r') as f:
                        trajs_dict[task][i] = json.load(f)
        
        return trajs_dict
    
    def generate_reasoning_paths_dict(self):
        reasoning_paths_dict = defaultdict(list)

        for i in range(1, self.repetition+1):
            fl_result_file = f'./fl_results/filtered_fl_result_{i}.json'
            with open(fl_result_file, 'r') as f:
                fl_results_dict = json.load(f)
                for task in self.task_list:
                    traj = self.trajs_dict[task][i]
                    if self.nhot:
                        reasoning_path = copy.deepcopy(traj)
                    else:
                        reasoning_path = []
                        for reasoning_step in traj:
                            if reasoning_step:
                                for fc in reasoning_step:
                                    reasoning_path.append(fc)
                            else:
                                reasoning_path.append([])
                    
                    if self.including_answer:
                        answer_list = []

                        for fl in fl_results_dict[task]:
                            answer = set()
                            if fl["rel_file_path"]:
                                answer.add(fl["rel_file_path"])
                            if fl["class_name"]:
                                answer.add(fl["class_name"])
                            if fl["method_name"]:
                                answer.add(fl["rel_file_path"])
                            answer_list.append(list(answer))
                        
                        if self.nhot:
                            reasoning_path.append([{'answers': answer_list}])
                        else:
                            reasoning_path.append({'answers': answer_list})
                    reasoning_paths_dict[task].append(reasoning_path)
        return reasoning_paths_dict
                
    
    def get_args_dict_for_k(self):

        args_dict = defaultdict(lambda: defaultdict(set))

        for task, reasoning_paths in self.reasoning_paths_dict.items():
            for i, path in enumerate(reasoning_paths):
                for reasoning_step in path:
                    if self.nhot:
                        다시짜기



                        for function_call in reasoning_step:
                            for k in range(self.ks[i], self.ks[-1]):
                                args_dict[task][k] = args_dict[task][k].union(set(function_call["arguments"].values()))

                    else:
                        if reasoning_step:
                            for function_call in reasoning_step:
                                for k in self.ks:
                                    if num_fc < k:
                                        args_dict[task][k] = args_dict[task][k].union(set(function_call["arguments"].values()))
                                num_fc += 1
                        else:
                            num_fc += 1
                
                if self.including_answer:
                    fl_result_file = f'./fl_results/filtered_fl_result_{idx}.json'
                    with open(fl_result_file, 'r') as f:
                        fl_results_dict = json.load(f)

                    for k in self.ks:
                        if num_fc < k:
                            for one_fl in fl_results_dict[task]:
                                if one_fl["rel_file_path"]:
                                    args_dict[task][k].add(one_fl["rel_file_path"])
                                if one_fl["class_name"]:
                                    args_dict[task][k].add(one_fl["class_name"])
                                if one_fl["method_name"]:
                                    args_dict[task][k].add(one_fl["method_name"])
                                


        return args_dict
    
    def get_labels_dict(self):
        combined_result_file = './combined_fl_results.json'
        with open(combined_result_file, 'r') as f:
            combined_result = json.load(f)

        with open('./modif_from_developer_patch.json', 'r') as f:
            modif_from_diff_dict = json.load(f)

        labels_dict = dict()

        for task in self.task_list:
            labels_dict[task] = 0
        for task, ranking in combined_result.items():
            if ranking:
                final_answer = ranking[0]
                rel_file_path = final_answer.split('::')[0]
                start, end = final_answer.split('_')[-2:]
                start, end = int(start), int(end)
                if rel_file_path in modif_from_diff_dict[task].keys():
                    for modif in modif_from_diff_dict[task][rel_file_path]:
                        if start <= modif["start_lineno"] and end >= modif["end_lineno"]:
                            labels_dict[task] = 1
        return labels_dict
    
    def get_arg_vector_size(self):
        arg_vector_size_dict = defaultdict(int)
        for k in self.ks:
            max_arg_size = 0
            for _, arg_for_k in self.args_dict.items():
                if len(arg_for_k[k]) > max_arg_size:
                    max_arg_size = len(arg_for_k[k])
            arg_vector_size_dict[k] = max_arg_size
        return arg_vector_size_dict

    def generate_LIG(self, generate_S = True, generate_F = True, generate_FA = True):
        def add_weight_edge(G, u, v, weight=1):
            if G.has_edge(u, v):
                G[u][v]['weight'] += 1
            else:
                G.add_edge(u, v, weight = weight)
        
        dataset_S = []
        dataset_F = []
        dataset_FA = []

        for task, trajs_with_idx in self.reasoning_paths_dict.items():
            pass


        


    def draw_length_distribution_graphs(self):
        length_dict_nhot = defaultdict(int)
        length_dict_onehot = defaultdict(int)
        
        for task_name, trajs in self.reasoning_paths_dict.items():
            for traj in trajs:
                num_fc = 0
                for reasoning_step in traj:
                    num_fc += len(reasoning_step)
                    if not reasoning_step:
                        num_fc += 1
                length_dict_nhot[len(traj)] += 1
                length_dict_onehot[num_fc] += 1
        if self.nhot:
            self.max_length_for_each_traj = max(length_dict_nhot.keys())
        else:
            self.max_length_for_each_traj = max(length_dict_onehot.keys())

        print(max(length_dict_nhot.keys()))
        print(max(length_dict_onehot.keys()))
        
        # Draw the length distibution graphs
        plt.bar(list(length_dict_nhot.keys()), list(length_dict_nhot.values()), color='skyblue')
        plt.title('The length distribution of each traj. (nhot ver.)')
        plt.xlabel('Length')
        plt.grid(axis='y')
        plt.savefig('./graphs/length_distribution_nhot')

        plt.bar(list(length_dict_onehot.keys()), list(length_dict_onehot.values()), color='skyblue')
        plt.title('The length distribution of each traj. (onehot ver.)')
        plt.xlabel('Length')
        plt.grid(axis='y')
        plt.savefig('./graphs/length_distribution_onehot')

    def generate_vector_for_all_tasks(self):
        args_dict = defaultdict(set)
        length_dict_nhot = defaultdict(int)
        length_dict_onehot = defaultdict(int)
        
        for task_name, trajs in self.reasoning_paths_dict.items():
            for traj in trajs:
                vector_for_traj = []
                num_fc = 0
                for reasoning_step in traj:
                    if self.nhot:
                        func_vector = [0] * (len(self.function_types) + 1)
                        for function_call in reasoning_step:
                            if function_call in self.function_types:
                                func_idx = self.function_types.index(function_call)
                            else:
                                func_idx = -1
                            func_vector[func_idx] += 1 ## modify here!!
                            func_vector[func_idx] = 1

                        for function_call in reasoning_step:
                            func_vector = [0] * (len(self.function_types) + 1)
                
def examine_tool_call_layers():
    task_list_file = './sampled_tasks.txt'
    with open(task_list_file, 'r') as f:
        task_list = f.read().splitlines()
    
    for task in task_list:
        for i in range(1, 6):
            if i == 1:
                output_dir = '../only_fl_output/no_patch'
            else:
                output_dir = f'../only_fl_output{i}/no_patch'
            instance_list = os.listdir(output_dir)

            tool_call_layer_file = None
            for instance in instance_list:
                if instance.startswith(task):
                    tool_call_layer_file = os.path.join(output_dir, instance, 'output_0/search/tool_call_layers.json')
                    break
            
            if not os.path.exists(tool_call_layer_file):
                print(f"No tool call layer file: {task}, {i}")
            
            else:
                with open(tool_call_layer_file, 'r') as f:
                    tool_call_layer = json.load(f)
            
            if not tool_call_layer:
                print(f"Empty list in tool call layer file: {task}, {i}")
            
            if tool_call_layer[-1]:
                print(f"The last reasoning step is not []: {task}, {i}")
            
            before_fl_file = os.path.join(output_dir, instance, 'output_0/search/bug_locations_before_process.json')

            if not os.path.exists(before_fl_file):
                print(f"No before answer file: {task} {i}")
            else:
                with open(before_fl_file, 'r') as f:
                    before_fls = json.load(f)
                if not before_fls:
                    print(f"No content in the before answer file")

            after_fl_file = os.path.join(output_dir, instance, 'output_0/search/bug_locations_after_process.json')
            if not os.path.exists(after_fl_file):
                print(f"No after answer file: {task} {i}")
            else:
                with open(after_fl_file, 'r') as f:
                    after_fls = json.load(f)
                if not after_fls:
                    print(f"No content in the after answer file")


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repetition', default=5, type=int)
    parser.add_argument('--nhot', action='store_true')
    parser.add_argument('--answer', action='store_true', help='including the answer')
    parser.add_argument('--one_arg_vector_size', action="store_true", help='use unified size for arg vector')
    args = parser.parse_args()

    data_generater = Data_generater(args.repetition, args.nhot, args.answer, args.one_arg_vector_size)
    # reasoning_paths_dict = data_generater.get_reasoning_paths_for_all_tasks()
    # with open('./reasoning_paths.json', 'w') as f:
    #     json.dump(reasoning_paths_dict, f, indent=4)

    
    # with open('./reasoning_paths.json', 'r') as f:
    #     reasoning_paths_dict = json.load(f)
    #     data_generater.reasoning_paths_dict = reasoning_paths_dict
    # print(data_generater.reasoning_paths_dict)
    # for task, trajs_args in data_generater.args_dict.items():
    #     print(task)
    #     for k, traj_args_for_k in trajs_args.items():
    #         print(f"==============={k}===============")
    #         for arg in list(traj_args_for_k):
    #             print(arg)

    # examine_tool_call_layers() 
    # print(len(data_generater.label_dict.values()))
    # print(sum(data_generater.label_dict.values()))

    



