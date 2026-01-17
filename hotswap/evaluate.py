import os
import json
import subprocess
import sys
from tqdm import tqdm
from collections import defaultdict

sys.path.insert(0, os.path.abspath('..'))
from app.search.search_backend import SearchBackend
from app.data_structures import BugLocation, SearchResult

def checkout_commit(repo_path, commit_hash):
    try:
        subprocess.run(
            ['git', 'checkout', '-f', commit_hash],
            cwd = repo_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError as e:
        return False

def extract_fl_results(model, r_idx):
    result_dir = f'./results/{model}/only_fl_{r_idx}/no_patch'

    instance_dir_list = os.listdir(result_dir)

    filtered_fl_dict = dict()

    with open('../SWE-bench/setup_result/setup_map.json', 'r') as f:
        setup_map = json.load(f)
    with open('../SWE-bench/setup_result/tasks_map.json', 'r') as f:
        tasks_map = json.load(f)
    
    print(f"Filtering fl results for repetition {r_idx}")
    for instance_dir in tqdm(instance_dir_list):
        splited_instance_dir = instance_dir.split('_')
        instance_name = f"{splited_instance_dir[0]}__{splited_instance_dir[2]}"
        filtered_fl_dict[instance_name] = []

        project_path = setup_map[instance_name]["repo_path"]
        if not os.path.exists(project_path):
            continue

        task_info = tasks_map[instance_name]
        task_commit = task_info.get("base_commit") or task_info.get("commit")

        checkout_result = checkout_commit(project_path, task_commit)

        if not checkout_result:
            continue

        fl_before_process_path = os.path.join(result_dir, instance_dir, 'output_0/search/bug_locations_before_process.json')

        try:
            with open(fl_before_process_path, 'r') as f:
                fl_before_process = json.load(f)
        except:
            fl_before_process = []
        
        if not fl_before_process:
            continue

        backend = SearchBackend(project_path)

        res:SearchBackend
        for bug_location_dict in fl_before_process:
            tmp_file_name = bug_location_dict.get("file", "")
            tmp_class_name = bug_location_dict.get("class", "")
            tmp_method_name = bug_location_dict.get("method", "")
            intended_behavior = bug_location_dict.get("intended_behavior", "")

            if not tmp_class_name and tmp_method_name and "." in tmp_method_name:
                fragments = tmp_method_name.split(".")
                if len(fragments) == 2:
                    tmp_class_name, tmp_method_name = fragments
            
            if not (tmp_file_name or tmp_class_name or tmp_method_name):
                continue

            search_res = []
            
            # Case 1: class + method
            if tmp_class_name and tmp_method_name:
                _, curr_search_res, call_ok = backend.search_method_in_class(tmp_method_name, tmp_class_name)
                search_res.extend(curr_search_res)

                res:SearchResult
                if call_ok:
                    for res in curr_search_res:
                        if (res.class_name is None or res.func_name is None or res.file_path is None):
                            continue

                        inherited_output, inherited_search_res, _ = backend._get_inherited_methods(res.class_name, res.func_name)
                        search_res.extend(inherited_search_res)
            
            # Case 2: file + method (no class)
            elif tmp_file_name and tmp_method_name and not tmp_class_name:
                _, search_res, call_ok = backend.search_method_in_file(tmp_method_name, tmp_file_name)
            
            # Case 3: file + class (no method)
            elif tmp_file_name and tmp_class_name and not tmp_method_name:
                _, search_res, call_ok = backend.search_class_in_file(tmp_class_name, tmp_file_name)
            
            # Case 4: class only (no file, no method)
            elif tmp_class_name and not tmp_method_name and not tmp_file_name:
                _, search_res, call_ok = backend.get_class_full_snippet(tmp_class_name)
            
            # Case 5: method only (no class, no file)
            elif tmp_method_name and not tmp_class_name and not tmp_file_name:
                _, search_res, call_ok = backend.search_method(tmp_method_name)
            
            # Case 6: file only (no method, no class)
            elif tmp_file_name and not tmp_method_name and not tmp_class_name:
                _, search_res, call_ok = backend.get_file_content(tmp_file_name)
            
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
                    bug_loc_dict["result_dir"] = os.path.join(result_dir, instance_dir)
                    filtered_fl_dict[instance_name].append(bug_loc_dict)
    
    return filtered_fl_dict

def vote_and_ranks_answers(fl_results_for_r):
    def tie_break(task, tie_methods):
        tie_broken_methods = []

        for i in range(1, 6):
            fl_result = fl_results_for_r[str(i)]
            answer_list = fl_result[task]
            for answer in answer_list:
                signature = f"{answer['rel_file_path']}::{answer['class_name']}#{answer['method_name']}_{answer['start']}_{answer['end']}"
                voting_score_dict[task][signature] += 1/len(answer_list)
                if signature in tie_methods:
                    tie_broken_methods.append(signature)
                    tie_methods.remove(signature)

                    if not tie_methods:
                        return tie_broken_methods
    
    test_bug_name_file = f'/home/kimnal0/auto-code-rover/atropos/results/parallel/embedding/fasttext/nhot_normal/sentence_vector/300d/not_add/label_criteria_1/test_bug_names2.json'
    with open(test_bug_name_file, 'r') as f:
        test_bug_name = json.load(f)
    task_list = []
    for i, tt in test_bug_name.items():
        task_list.extend(tt)

    voting_score_dict = defaultdict(lambda: defaultdict(float))
    ranking_dict = dict()

    for i in range(1, 6):
        fl_result = fl_results_for_r[str(i)]
        for task in task_list:
            answer_list = fl_result[task]
            for answer in answer_list:
                signature = f"{answer['rel_file_path']}::{answer['class_name']}#{answer['method_name']}_{answer['start']}_{answer['end']}"
                voting_score_dict[task][signature] += 1/len(answer_list)
    
    for task, scores_dict in voting_score_dict.items():
        for signature in scores_dict.keys():
            scores_dict[signature] /= 5
    
    for task, voting_scores in voting_score_dict.items():
        ranking = []
        groups = defaultdict(list)
        for m, s in voting_scores.items():
            groups[s].append(m)
        sorted_group = sorted(groups.items(), key = lambda x: x[0], reverse=True)

        for s, m in sorted_group:
            if len(m) < 2:
                ranking.extend(m)
            else:
                ranking.extend(tie_break(task, m))
        ranking_dict[task] = ranking
    
    combined_result_dict = {'ranking': ranking_dict, 'confidence_score': voting_score_dict}

    return combined_result_dict


def evaluate(model):
    if model == 'hotswap':
        filtered_result_file = './filtered_fl_results_hotswap.json'
    elif model == 'mixtral':
        filtered_result_file = './filtered_fl_results_mixtral.json'
    elif model == 'gpt-4':
        filtered_result_file = './filtered_fl_results_gpt-4.json'
    

    with open(filtered_result_file, 'r') as f:
        fl_results_for_r = json.load(f)
    
    with open('../atropos/modif_from_developer_patch_1000size.json', 'r') as f:
        modif_from_diff_dict = json.load(f)
    
    combined_result = vote_and_ranks_answers(fl_results_for_r)

    correctness_each_answer_dict = defaultdict(list)

    for task, ranked_answers in combined_result['ranking'].items():
        if ranked_answers:
            for answer in ranked_answers:
                correctness = False

                rel_file_path = answer.split('::')[0]
                start, end = answer.split('_')[-2:]
                start, end = int(start), int(end)
                if rel_file_path in modif_from_diff_dict[task].keys():
                    for modif in modif_from_diff_dict[task][rel_file_path]:
                        if start <= modif["start_lineno"] and end >= modif["end_lineno"]:
                            correctness = True
                            break
                correctness_each_answer_dict[task].append(correctness)
    
    
    acc_dict = defaultdict(int)
    for task, correctness_list in correctness_each_answer_dict.items():
        for i, correctness in enumerate(correctness_list):
            if correctness:
                for j in range(i+1, 11):
                    acc_dict[j] += 1
    
    return acc_dict

def get_cost(model):
    total_time_cost = 0
    total_input_tokens = 0
    total_output_tokens = 0
    for i in range(1, 6):
        result_dir = f'./results/{model}/only_fl_{i}/no_patch'
        
        instance_dir_list = os.listdir(result_dir)
        for instance_dir in instance_dir_list:
            cost_file = os.path.join(result_dir, instance_dir, 'cost.json')
            if os.path.exists(cost_file):
                with open(cost_file, 'r') as f:
                    cost = json.load(f)
                total_time_cost += cost["elapsed_seconds"]
                total_input_tokens += cost["total_input_tokens"]
                total_output_tokens += cost["total_output_tokens"]
            
    
    return total_time_cost, total_input_tokens, total_output_tokens
                    
def evaluate_hotswap():
    # hotswap_fl_results_for_r = dict()
    # mixtral_fl_results_for_r = dict()
    # gpt4_fl_results_for_r = dict()
    # for i in range(1, 6):
    #     hotswap_fl_results_for_r[i] = extract_fl_results("hotswap", i)
    #     mixtral_fl_results_for_r[i] = extract_fl_results("mixtral", i)
    #     # gpt4_fl_results_for_r[i] = extract_fl_results("gpt-4", i)
        
    # fl_results_output_file = './filtered_fl_results_hotswap.json'
    # with open(fl_results_output_file, 'w') as f:
    #     json.dump(hotswap_fl_results_for_r, f, indent = 4)
    
    # fl_results_output_file = './filtered_fl_results_mixtral.json'
    # with open(fl_results_output_file, 'w') as f:
    #     json.dump(mixtral_fl_results_for_r, f, indent = 4)

    # fl_results_output_file = './filtered_fl_results_gpt-4.json'
    # with open(fl_results_output_file, 'w') as f:
    #     json.dump(gpt4_fl_results_for_r, f, indent = 4)
    
    # hotswap_filtered_result_file = './filtered_fl_results_hotswap.json'
    # mixtral_filtered_result_file = './filtered_fl_results_mixtral.json'
    # gpt4_filtered_result_file = './filtered_fl_results_gpt-4.json'

    # with open(hotswap_filtered_result_file, 'r') as f:
    #     hotswap_fl_results_for_r = json.load(f)
    # with open(mixtral_filtered_result_file, 'r') as f:
    #     mixtral_fl_results_for_r = json.load(f)
    # with open(gpt4_filtered_result_file, 'r') as f:
    #     gpt4_fl_results_for_r = json.load(f)

    evaluation_result = dict()

    # =================== Evaluation ====================
    
    hotswap_evaluation_result = evaluate("hotswap")
    mixtral_evaluation_result = evaluate("mixtral")
    gpt4_evaluation_result = evaluate("gpt-4")

    print(f"Mixtral: {mixtral_evaluation_result}")
    print(f"Hotswap: {hotswap_evaluation_result}")
    print(f"gpt-4: {gpt4_evaluation_result}")

    evaluation_result['hotswap'] = {'acc': hotswap_evaluation_result}
    evaluation_result['mixtral'] = {'acc': mixtral_evaluation_result}
    evaluation_result['gpt-4'] = {'acc': gpt4_evaluation_result}

    # =================== Cost Calculation =====================
    gpt4_input_price_per_1m = 10
    gpt4_output_price_per_1m = 30
    mixtral_time_cost, mixtral_input_tokens, mixtral_output_tokens = get_cost("mixtral")
    mixtral_monetary_cost = 0

    evaluation_result["mixtral"]['cost'] = {
        'time_cost': mixtral_time_cost,
        'input_tokens': mixtral_input_tokens,
        'output_tokens': mixtral_output_tokens,
        'monetary_cost': mixtral_monetary_cost
    }

    hotswap_time_cost, hotswap_input_tokens, hotswap_output_tokens = get_cost("hotswap")
    hotswap_monetary_cost = ((hotswap_input_tokens / 1_000_000) * gpt4_input_price_per_1m) + ((hotswap_output_tokens / 1_000_000) * gpt4_output_price_per_1m)

    evaluation_result["hotswap"]['cost'] = {
        'time_cost': hotswap_time_cost,
        'input_tokens': hotswap_input_tokens,
        'output_tokens': hotswap_output_tokens,
        'monetary_cost': hotswap_monetary_cost
    }

    gpt4_time_cost, gpt4_input_tokens, gpt4_output_tokens = get_cost("gpt-4")
    gpt4_monetary_cost = ((gpt4_input_tokens / 1_000_000) * gpt4_input_price_per_1m) + ((gpt4_output_tokens / 1_000_000) * gpt4_output_price_per_1m)

    evaluation_result["gpt-4"]['cost'] = {
        'time_cost': gpt4_time_cost,
        'input_tokens': gpt4_input_tokens,
        'output_tokens': gpt4_output_tokens,
        'monetary_cost': gpt4_monetary_cost
    }

    print(f"Mixtral - time cost: {mixtral_time_cost:.4f}, monetary cost: {mixtral_monetary_cost:.4f}, input tokens: {mixtral_input_tokens}, output tokens: {mixtral_output_tokens}")
    print(f"Hotswap - time cost: {hotswap_time_cost:.4f}, monetary cost: {hotswap_monetary_cost:.4f}, input tokens: {hotswap_input_tokens}, output tokens: {hotswap_output_tokens}")
    print(f"Gpt-4 - time cost: {gpt4_time_cost:.4f}, monetary cost: {gpt4_monetary_cost:.4f}, input tokens: {gpt4_input_tokens}, output_tokens: {gpt4_output_tokens}")

    with open('parallel_hotswap_result_and_cost.json', 'w') as f:
        json.dump(evaluation_result, f, indent=4)


if __name__ == '__main__':
    evaluate_hotswap()
    