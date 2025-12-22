import os
import json
import argparse
import copy
import ast
import torch
import subprocess
import fasttext
import fasttext.util
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
from tqdm import tqdm
from torch_geometric.utils import from_networkx
import sys

# Add auto-code-rover directory to path
sys.path.insert(0, os.path.abspath('../..'))
from app.search.search_backend import SearchBackend
from app.data_structures import BugLocation, SearchResult

fasttext.util.download_model('en', if_exists='ignore')
fasttext_model = fasttext.load_model('cc.en.300.bin')
embedding_size = 300

def checkout_commit(repo_path, commit_hash):
    """
    해당 레포지토리 경로에서 특정 커밋으로 체크아웃합니다.
    """
    # print(f"    [GIT] Checking out commit {commit_hash} in {repo_path}...")
    try:
        # 강제로 체크아웃 (기존 변경사항 무시)
        subprocess.run(
            ['git', 'checkout', '-f', commit_hash], 
            cwd=repo_path, 
            check=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.PIPE
        )
        # print(f"    [GIT] Successfully checked out to {commit_hash}")
        return True
    except subprocess.CalledProcessError as e:
        # print(f"    [GIT ERROR] Failed to checkout: {e.stderr.decode().strip()}")
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
        self.fl_results = dict()
        for i in range(1, self.repetition+1):
            self.fl_results[i] = self.extract_fl_results(i)
        output_file = "/tmp/test_fl_results.json"
        with open(output_file, 'w') as f:
            json.dump(self.fl_results, f, indent=2)

        self.trajs_dict = self.extract_trajs_from_logs()
        self.reasoning_paths_dict = self.generate_reasoning_paths_dict()

        # print(self.trajs_dict)
        # print()
        # print(self.reasoning_paths_dict)
        # print(len(self.trajs_dict['astropy__astropy-6938'][1]))
        # print(len(self.reasoning_paths_dict['astropy__astropy-6938'][0]))
        self.max_num_args = self.get_max_num_args_per_step()
        self.args_dict = self.get_args_dict_for_k()
        # # print(self.args_dict)
        self.label_dict = self.get_labels_dict()
        # # self.task_list = ['scikit-learn__scikit-learn-26400']
        # # self.task_list = ['astropy__astropy-6938']
    
    def get_max_num_args_per_step(self):

        num_args_list = []

        for task, reasoning_paths in self.reasoning_paths_dict.items():
            for idx, path in enumerate(reasoning_paths):
                for i, reasoning_step in enumerate(path):
                    num_args = 0
                    for func_call in reasoning_step:
                        if "arguments" in func_call.keys():
                            
                            num_args += len(func_call["arguments"].keys())
                        elif "answers" in func_call.keys():
                            for one_fl in func_call["answers"]:
                                num_args += len(one_fl)
                            
                    num_args_list.append(num_args)
                    if num_args == 682:
                        print(task, idx)
        max_num_args = max(num_args_list)
        return max_num_args

    def extract_fl_results(self, idx):
        """
        Re-process FL results using SearchBackend.
        Matches the transformation logic of auto-code-rover but excludes class context.
        """
        result_dir = f'../../fl_outputs/only_fl_output_mixtral_{idx}'
        instance_dir_list = os.listdir(os.path.join(result_dir, 'no_patch'))

        filtered_fl_dict = defaultdict(list)

        with open('../../SWE-bench/setup_result/setup_map.json', 'r') as f:
            setup_map = json.load(f)

        with open('../../SWE-bench/setup_result/tasks_map.json', 'r') as f:
            tasks_map = json.load(f)

        for instance_dir in instance_dir_list:
            # Parse instance_dir: e.g., "astropy__astropy-6938_2025-12-05_14-26-01"
            # Extract instance_name: "astropy__astropy-6938"
            splited_instance_dir = instance_dir.split('_')
            instance_name = f"{splited_instance_dir[0]}__{splited_instance_dir[2]}"

            potential_path = setup_map[instance_name]["repo_path"]
            if not os.path.exists(potential_path):
                filtered_fl_dict[instance_name] = []
                continue
            task_info = tasks_map[instance_name]
            task_commit = task_info.get("base_commit") or task_info.get("commit")

            checkout_commit(potential_path, task_commit)

            project_path = None

            if os.path.exists(potential_path):
                project_path = potential_path

            # Read before_process
            fl_before_process_path = os.path.join(result_dir, 'no_patch', instance_dir, 'output_0/search/bug_locations_before_process.json')
            try:
                with open(fl_before_process_path, 'r') as f:
                    fl_before_process = json.load(f)
            except:
                fl_before_process = []

            if not fl_before_process:
                filtered_fl_dict[instance_name] = []
                continue

            # 수정사항 1: project_path를 못찾으면 빈 리스트
            if not project_path or not os.path.exists(project_path):
                print("No project path")
                filtered_fl_dict[instance_name] = []
                continue

            # Use SearchBackend
            backend = SearchBackend(project_path)

            for bug_location_dict in fl_before_process:
                tmp_file_name = bug_location_dict.get("file", "")
                tmp_method_name = bug_location_dict.get("method", "")
                tmp_class_name = bug_location_dict.get("class", "")
                intended_behavior = bug_location_dict.get("intended_behavior", "")

                # Handle Class.method format
                if not tmp_class_name and tmp_method_name and "." in tmp_method_name:
                    fragments = tmp_method_name.split(".")
                    if len(fragments) == 2:
                        tmp_class_name, tmp_method_name = fragments

                if not (tmp_method_name or tmp_class_name or tmp_file_name):
                    continue

                call_ok = False
                search_res = []

                # 수정사항 3: 정확한 조건에서만 검색
                # Case 1: method + class
                if tmp_method_name and tmp_class_name:
                    output, curr_search_res, call_ok = backend.search_method_in_class(
                        tmp_method_name, tmp_class_name
                    )
                    search_res.extend(curr_search_res)

                    # 수정사항 2: inherited methods는 포함하지만 class context는 제외
                    res: SearchResult
                    if call_ok:
                        for res in curr_search_res:
                            if (res.class_name is None or
                                res.func_name is None or
                                res.file_path is None):
                                continue

                            inherited_output, inherited_search_res, _ = (
                                backend._get_inherited_methods(res.class_name, res.func_name)
                            )
                            search_res.extend(inherited_search_res)

                # Case 2: method + file (no class)
                elif tmp_method_name and tmp_file_name and not tmp_class_name:
                    output, search_res, call_ok = backend.search_method_in_file(
                        tmp_method_name, tmp_file_name
                    )

                # Case 3: class + file (no method)
                elif tmp_class_name and tmp_file_name and not tmp_method_name:
                    output, search_res, call_ok = backend.search_class_in_file(
                        tmp_class_name, tmp_file_name
                    )

                # Case 4: class only (no file, no method)
                elif tmp_class_name and not tmp_file_name and not tmp_method_name:
                    output, search_res, call_ok = backend.get_class_full_snippet(tmp_class_name)

                # Case 5: method only (no file, no class)
                elif tmp_method_name and not tmp_file_name and not tmp_class_name:
                    output, search_res, call_ok = backend.search_method(tmp_method_name)

                # Case 6: file only (no method, no class)
                elif tmp_file_name and not tmp_method_name and not tmp_class_name:
                    output, search_res, call_ok = backend.get_file_content(tmp_file_name)

                # Convert SearchResult to BugLocation
                res: SearchResult
                final_bug_locs: list[BugLocation] = []
                for res in search_res:
                    # Skip if not a SearchResult object (defensive programming)
                    if not hasattr(res, 'start') or not hasattr(res, 'end'):
                        print(res)
                        continue
                    if res.start is None or res.end is None:
                        continue
                    new_bug_loc = BugLocation(res, project_path, intended_behavior)
                    final_bug_locs.append(new_bug_loc)

                # Remove duplicates
                unique_bug_locations = []
                for loc in final_bug_locs:
                    if loc not in unique_bug_locations:
                        unique_bug_locations.append(loc)

                # Add to result
                if unique_bug_locations:
                    for loc in unique_bug_locations:
                        bug_loc_dict = loc.to_dict()
                        bug_loc_dict["result_dir"] = os.path.join(result_dir, 'no_patch', instance_dir)
                        filtered_fl_dict[instance_name].append(bug_loc_dict)
                

        return filtered_fl_dict
    
    def extract_fl_results_old(self, idx):
        result_dir = f'../../fl_outputs/only_fl_output_mixtral_{idx}'
        instance_dir_list = os.listdir(os.path.join(result_dir, 'no_patch'))

        filtered_fl_dict = defaultdict(list)

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
                continue

            
            for raw_fl in fl_before_process:
                intended_behavior = raw_fl.get("intended_behavior", "")
                search=False
                for searched_fl in fl_after_process:
                    searched_fl_intended_behavior = searched_fl["intended_behavior"]
                    if intended_behavior == searched_fl_intended_behavior:
                        searched_fl["result_dir"] = os.path.join(result_dir, 'no_patch', instance_dir)
                        filtered_fl_dict[instance_name].append(searched_fl)
                        # if search:
                        #     print(instance_dir, idx)
                        #     print(intended_behavior)
                        # search = True
        
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


    def extract_trajs_from_logs(self):
        trajs_dict = defaultdict(dict)

        print("Extracting trajectories...")
        for task in tqdm(self.task_list):
            for i in range(1, self.repetition+1):
                output_dir = f'../../fl_outputs/only_fl_output_mixtral_{i}/no_patch'
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
            fl_results_dict = self.extract_fl_results(i)

            for task in self.task_list:
                traj = self.trajs_dict[task][i]
                reasoning_path = copy.deepcopy(traj)
                
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
                
                reasoning_path.append([{'answers': answer_list}])

                reasoning_paths_dict[task].append(reasoning_path)
        return reasoning_paths_dict
                
    
    def get_args_dict_for_k(self):

        args_dict = defaultdict(lambda: defaultdict(set))

        for task, reasoning_paths in self.reasoning_paths_dict.items():
            for idx, path in enumerate(reasoning_paths):
                for i, reasoning_step in enumerate(path):
                    for func_call in reasoning_step:
                        for k in self.ks:
                            if i < k:
                                if "arguments" in func_call.keys():
                                    args_dict[task][k] = args_dict[task][k].union(set(func_call["arguments"].values()))
                                elif "answers" in func_call.keys():
                                    for one_fl in func_call["answers"]:
                                        args_dict[task][k] = args_dict[task][k].union(set(one_fl))
                    
        return args_dict
    
    def get_labels_dict(self):
        combined_result = self.vote_and_ranks_answers()
        with open('../combined_fl_results_mixtral.json', 'w') as f:
            json.dump(combined_result, f, indent=4)

        with open('../modif_from_developer_patch_1000size.json', 'r') as f:
            modif_from_diff_dict = json.load(f)

        labels_dict = dict()

        for task in self.task_list:
            labels_dict[task] = 1
        for task, ranking in combined_result["ranking"].items():
            if ranking:
                for answer in ranking[:self.label_criteria]:
                    rel_file_path = answer.split('::')[0]
                    start, end = answer.split('_')[-2:]
                    start, end = int(start), int(end)
                    if rel_file_path in modif_from_diff_dict[task].keys():
                        for modif in modif_from_diff_dict[task][rel_file_path]:
                            if start <= modif["start_lineno"] and end >= modif["end_lineno"]:
                                labels_dict[task] = 0
                                break
                    if labels_dict[task] == 0:
                        break

        return labels_dict
    
    def save_graph_image(self, graph, filename):
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=False, node_size=700, node_color='lightblue', font_size=10, font_weight='bold')

        edge_labels = nx.get_edge_attributes(graph, "weight")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=9)

        plt.savefig(filename, format='png')
        plt.close()

    def embed_with_fasttext(self, text):
        text_str = str(text)
        embedding = fasttext_model.get_sentence_vector(text_str)

        return torch.from_numpy(embedding).float()

    def generate_LIG_for_all_k(self, save_data, save_dir):
        def add_weight_edge(G, u, v, weight=1):
            if G.has_edge(u, v):
                G[u][v]['weight'] += 1
            else:
                G.add_edge(u, v, weight = weight)

        print("Generating the graphs for all tasks and ks")

        # for k in [5]:
        for k in self.ks:
            dataset = []
            for task in tqdm(self.task_list):
                graph = nx.DiGraph()

                for _, rp in enumerate(self.reasoning_paths_dict[task]):
                    if not rp:
                        continue
                    if rp[0] and 'answers' in rp[0][0].keys():
                        for fl in rp[0][0]['answers']:
                            graph.add_node(str(fl))
                    else:
                        graph.add_node(str(rp[0]))
                if not graph.nodes():
                    graph.add_node('None')

                for _, rp in enumerate(self.reasoning_paths_dict[task]):
                    if not rp:
                        continue
                    for i, rs in enumerate(rp[1:]):
                        if i + 1 < k:
                            if rs and 'answers' in rs[0].keys():
                                for fl in rs[0]['answers']:
                                    if not graph.has_node(str(fl)):
                                        graph.add_node(str(fl))

                                    add_weight_edge(graph, str(rp[i]), str(fl))
                            else:
                                if not graph.has_node(str(rs)):
                                    graph.add_node(str(rs))
                                add_weight_edge(graph, str(rp[i]), str(rs))

                            # for edge in graph.edges():
                            #     print(edge)

                ################################################################
                ############Draw and save the graphs in ./graphs/lig############
                # if self.nhot:
                #     if self.including_answer:
                #         graph_dir = f'./graphs/lig/nhot/including_answer/{k}'
                #     else:
                #         graph_dir = f'./graphs/lig/nhot/no_answer/{k}'
                # else:
                #     if self.including_answer:
                #         graph_dir = f'./graphs/lig/onehot/including_answer/{k}'
                #     else:
                #         graph_dir = f'./graphs/lig/onehot/no_answer/{k}'

                # os.makedirs(graph_dir, exist_ok=True)
                # try:
                #     self.save_graph_image(graph, os.path.join(graph_dir, f'{task}.png'))
                # except:
                #     print(f"Failed to save the graph: {os.path.join(graph_dir, f'{task}.png')}")
                ################################################################
            
                data = from_networkx(graph)
                node_embeddings = []
              
                for node_str in graph.nodes():
                    # print(node_str)
                    node = ast.literal_eval(node_str)
                    
                    if not node:
                        func_vector = torch.zeros(len(self.function_types) + 1, dtype=torch.float)
                        func_vector[-1] = 1
                        arg_embedding = torch.zeros(embedding_size, dtype=torch.float)
                    elif isinstance(node[0], str): 
                        func_vector = torch.ones(len(self.function_types) + 1, dtype=torch.float)
                        arg_embedding = self.embed_with_fasttext(str(node))
                    else:
                        func_vector = torch.zeros(len(self.function_types) + 1, dtype=torch.float)
                        arguments = []
                        for func_call in node:
                            if func_call['func_name'] in self.function_types:
                                func_idx = self.function_types.index(func_call['func_name'])
                            else:
                                func_idx = -1
                            func_vector[func_idx] = 1
                        
                            for arg in func_call['arguments'].values():
                                arguments.append(arg)
                        arg_embedding = self.embed_with_fasttext(str(arguments))

                    embedding = torch.cat([func_vector, arg_embedding], dim=0)
                    node_embeddings.append(embedding)

                node_x_stack = torch.stack(node_embeddings)
                data.x = node_x_stack
                data.y = torch.tensor([self.label_dict[task]], dtype=float)
                data.task = task
                data.edge_weight = torch.tensor([graph[u][v]['weight'] for u, v in graph.edges()], dtype = torch.float)
                if hasattr(data, 'weight'):
                    delattr(data, 'weight')

                dataset.append(data)

            if save_data:
                save_dir_with_k = os.path.join(save_dir, str(k))
                os.makedirs(save_dir_with_k, exist_ok=True)
                torch.save({
                    "dataset": dataset,
                }, os.path.join(save_dir_with_k, 'gcn_dataset.pth'))
                print(f"{k}th GCN dataset saved in {save_dir_with_k}")

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

                
def examine_tool_call_layers():
    task_list_file = './sampled_tasks_1_and_2.txt'
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

def get_save_dir(label_criteria, embedding_length):
    save_dir = f'../data/parallel/embedding/fasttext/nhot_normal/sentence_vector/{embedding_length}d/label_criteria_{label_criteria}'
    return save_dir

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repetition', default=5, type=int)
    parser.add_argument('-l', '--label_criteria', default=1, type=int)
    args = parser.parse_args()

    save_dir = get_save_dir(args.label_criteria, embedding_size)

    data_generater = Data_generater(args.repetition, args.label_criteria)

    print("The number of tasks: ", len(data_generater.label_dict.values()))
    print("The number of tasks with positive labels: ", sum(data_generater.label_dict.values()))

    print(data_generater.max_num_args)

    data_generater.generate_LIG_for_all_k(save_data=True, save_dir=save_dir)



    



