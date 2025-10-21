import os
import json
import argparse
import copy
import ast
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from tqdm import tqdm
from torch_geometric.utils import from_networkx

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
                self.ks.extend([15, 16])
            else:
                self.ks.append(15)
        else:
            self.ks = list(range(1, 11))
            if self.including_answer:
                self.ks.extend([15, 20, 38])
            else:
                self.ks.extend([15, 20, 37])

        task_list_file = './sampled_tasks.txt'
        with open(task_list_file, 'r') as f:
            self.task_list = f.read().splitlines()
        # self.task_list = ['astropy__astropy-6938']
        # self.task_list = ['django__django-17066']
        # self.task_list = ['astropy__astropy-6938', 'django__django-17066']
        self.trajs_dict = self.extract_trajs_from_logs()
        self.reasoning_paths_dict = self.generate_reasoning_paths_dict()

        # print(self.trajs_dict)
        # print()
        # print(self.reasoning_paths_dict)
        # print(len(self.trajs_dict['astropy__astropy-6938'][1]))
        # print(len(self.reasoning_paths_dict['astropy__astropy-6938'][0]))
        self.args_dict = self.get_args_dict_for_k()
        self.arg_vector_size_dict = self.get_arg_vector_size()
        self.label_dict = self.get_labels_dict()
    
    def extract_trajs_from_logs(self):
        trajs_dict = defaultdict(dict)

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
                                answer.add(fl["method_name"])
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
            for idx, path in enumerate(reasoning_paths):
                for i, reasoning_step in enumerate(path):
                    if self.nhot:
                        for func_call in reasoning_step:
                            for k in self.ks:
                                if i < k:
                                    if "arguments" in func_call.keys():
                                        args_dict[task][k] = args_dict[task][k].union(set(func_call["arguments"].values()))
                                    elif "answers" in func_call.keys():
                                        for one_fl in func_call["answers"]:
                                            args_dict[task][k] = args_dict[task][k].union(set(one_fl))
                    
                    else:
                        for k in self.ks:
                            if reasoning_step != [] and i < k:
                                if "arguments" in reasoning_step.keys():
                                    args_dict[task][k] = args_dict[task][k].union(set(reasoning_step["arguments"].values()))
                                elif "answers" in reasoning_step.keys():
                                    for one_fl in reasoning_step["answers"]:
                                        args_dict[task][k] = args_dict[task][k].union(set(one_fl))

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
    
    def save_graph_image(self, graph, filename):
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=False, node_size=700, node_color='lightblue', font_size=10, font_weight='bold')

        edge_labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=9)

        plt.savefig(filename, format='png')
        plt.close()



    def generate_LIG_for_all_k(self, generate_S = True, generate_F = True, generate_FA = True):
        def add_weight_edge(G, u, v, weight=1):
            if G.has_edge(u, v):
                G[u][v]['weight'] += 1
            else:
                G.add_edge(u, v, weight = weight)
        
        dataset_S = []
        dataset_F = []
        dataset_FA = []

        # for k in self.ks:
        print("Generating the graphs for all tasks and ks")
        for k in [37]:
            for task in tqdm(self.task_list):
                graph = nx.DiGraph()
                for _, rp in enumerate(self.reasoning_paths_dict[task]):
                    if not rp:
                        graph.add_node('[]')
                        continue
                    if self.nhot and rp[0] and 'answers' in rp[0][0].keys():
                        for fl in rp[0][0]['answers']:
                            graph.add_node(str(fl))
                    else:
                        graph.add_node(str(rp[0]))

                for _, rp in enumerate(self.reasoning_paths_dict[task]):
                    if not rp:
                        continue
                    for i, rs in enumerate(rp[1:]):
                        if i + 1 < k:
                            if self.nhot:
                                if self.including_answer and rs and 'answers' in rs[0].keys():
                                    for fl in rs[0]['answers']:
                                        if not graph.has_node(str(fl)):
                                            graph.add_node(str(fl))

                                        add_weight_edge(graph, str(rp[i]), str(fl))
                                else:
                                    if not graph.has_node(str(rs)):
                                        graph.add_node(str(rs))
                                    add_weight_edge(graph, str(rp[i]), str(rs))
                            else:
                                if self.including_answer and rs and 'answers' in rs.keys():
                                    for fl in rs['answers']:
                                        if not graph.has_node(str(fl)):
                                            graph.add_node(str(fl))

                                        add_weight_edge(graph, str(rp[i]), str(fl))
                                else:
                                    if not graph.has_node(str(rs)):
                                        graph.add_node(str(rs))
                                    add_weight_edge(graph, str(rp[i]), str(rs))

                            # for node in graph.nodes():
                            #     print(node)
                            # for edge in graph.edges():
                            #     print(edge)


                if self.nhot:
                    if self.including_answer:
                        graph_dir = f'./graphs/lig/nhot/including_answer/{k}'
                    else:
                        graph_dir = f'./graphs/lig/nhot/no_answer/{k}'
                else:
                    if self.including_answer:
                        graph_dir = f'./graphs/lig/onehot/including_answer/{k}'
                    else:
                        graph_dir = f'./graphs/lig/onehot/no_answer/{k}'

                os.makedirs(graph_dir, exist_ok=True)
                try:
                    self.save_graph_image(graph, os.path.join(graph_dir, f'{task}.png'))
                except:
                    print(f"Failed to save the graph: {os.path.join(graph_dir, f'{task}.png')}")
            
                # S_data = from_networkx(graph)
                # F_data = from_networkx(graph)
                # FA_data = from_networkx(graph)

                # S_node_x = []
                # F_node_x = []
                # FA_node_x = []

                # for node_str in graph.nodes():
                #     func_vector = [0] * (len(self.function_types) + 1)
                #     if self.nhot:
                #         if 'answers' in node_str:

                    # else:
                    #     if "'answers'" in node_str and self.including_answer:
                    #         pass
                    #     else:
                    #         if node_str == '[]':
                    #             func_vector[-1] = 1
                    #         else:
                    #             node = ast.literal_eval(node_str)

                    

                


                    

            
        


                

                

                
        test_graph_list = []
        test_graph = nx.DiGraph()
        test_graph.add_node('a')
        test_graph.add_node('b')
        add_weight_edge(test_graph, 'a', 'b')

        test_graph_list.append(test_graph)

        test_graph = copy.deepcopy(test_graph)
        test_graph.add_node('c')
        test_graph.add_node(str([]))
        add_weight_edge(test_graph, 'b', 'c')

        test_graph_list.append(test_graph)
        
        for graph in test_graph_list:
            print(graph.nodes())
        print(test_graph.nodes())

        


            


    def draw_length_distribution_graphs(self):
        length_dict = defaultdict(int)
        
        for task_name, trajs in self.reasoning_paths_dict.items():
            for traj in trajs:
                length_dict[len(traj)] += 1
        max_length = max(length_dict.keys())
        print(max_length)
        
        # Draw the length distibution graphs
        plt.bar(list(length_dict.keys()), list(length_dict.values()), color='skyblue')

        title = 'The length distribution of each traj.'
        if self.nhot:
            title += ' (nhot,'
        else:
            title += ' (onehot,'
        if self.including_answer:
            title += ' answer)'
        else:
            title += ' no answer)'

        plt.title(title)
        plt.xlabel('Length')
        plt.grid(axis='y')

        fig_name = 'length_distribution'
        if self.nhot:
            fig_name += '_nhot'
        else:
            fig_name += '_onehot'
        if self.including_answer:
            fig_name += '_answer'
        else:
            fig_name += '_no_answer'
        plt.savefig(f"./graphs/{fig_name}")


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

    # data_generater.draw_length_distribution_graphs()


    #=================================================================
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
    data_generater.generate_LIG_for_all_k()



    



