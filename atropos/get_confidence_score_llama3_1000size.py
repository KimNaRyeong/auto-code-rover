import argparse, json
from sklearn.metrics import accuracy_score, roc_auc_score
import os

def get_accuracy(dir_dict):
    all_labels = []
    all_preds = []
    all_confidences = []

    combined_result_file = './R5_combined_fl_results_llama3_1000size.json'

    task_list_file = './sampled_tasks_1_and_2.txt'
    with open(task_list_file, 'r') as f:
            task_list = f.read().splitlines()

    with open(combined_result_file, 'r') as f:
        combined_result = json.load(f)

    with open('./modif_from_developer_patch_1000size.json', 'r') as f:
        modif_from_diff_dict = json.load(f)
    
    labels_dict = dict()

    for task in task_list:
        labels_dict[task] = 0
    for task, ranking in combined_result["ranking"].items():
        if ranking:
            final_answer = ranking[0]
            rel_file_path = final_answer.split('::')[0]
            start, end = final_answer.split('_')[-2:]
            start, end = int(start), int(end)
            if rel_file_path in modif_from_diff_dict[task].keys():
                for modif in modif_from_diff_dict[task][rel_file_path]:
                    if start <= modif["start_lineno"] and end >= modif["end_lineno"]:
                        labels_dict[task] = 1
    
    for task in labels_dict.keys():
        all_labels.append(labels_dict[task])
        try:
            answer = combined_result["ranking"][task][0]
            confidence_score = combined_result["confidence_score"][task][answer]
        except:
            confidence_score = 0
        all_preds.append(1 if confidence_score >= 0.5 else 0)
        all_confidences.append(confidence_score)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    print(all_labels)
    print(all_confidences)
    for i in range(len(all_preds)):
        if all_labels[i] == 1 and all_confidences[i] >=0.5:
            tp += 1
        elif all_labels[i] == 1 and all_confidences[i] < 0.5:
            fn += 1
        elif all_labels[i] == 0 and all_confidences[i] >= 0.5:
            fp += 1
        else:
            tn += 1
    print(tp, tn, fp, fn)

    
    accuracy = accuracy_score(all_labels, all_preds)
    roc_auc = roc_auc_score(all_labels, all_confidences)


    return accuracy, roc_auc

def main(dir_dict):
    accuracy, roc_auc = get_accuracy(dir_dict)
    result_file = os.path.join(dir_dict['result'], 'result.txt')

    print(accuracy, roc_auc)

    acc_new_line = f'Confidence-score accuracy: {accuracy:.4f}\n'
    auc_new_line = f'Confidence-score roc-auc: {roc_auc:.4f}\n'
    # with open(result_file, 'r') as rf:
    #     results = rf.read()
    # print(result_file)
    # with open(result_file, 'w') as rf:
    #     rf.write(acc_new_line + auc_new_line + results)

def get_dir_dict(nhot, answer, add):
    if nhot:
        hot_dir = 'nhot'
    else:
        hot_dir = 'onehot'
    
    if answer:
        answer_dir = 'answer'
    else:
        answer_dir = 'no_answer'

    if add:
        add_dir = 'add'
    else:
        add_dir = 'not_add'

    if nhot:
        dir_dict = {
            'data': f'./data/llama3/R5/1000size/{hot_dir}/{answer_dir}/{add_dir}',
            'result': f'./results/llama3/R5/1000size/{hot_dir}/{answer_dir}/{add_dir}',
            'trained_model': f'./llama3/R5/1000size/trained_model/{hot_dir}/{answer_dir}/{add_dir}',
            'graph': f'./results/llama3/R5/1000size/graphs/{hot_dir}/{answer_dir}/{add_dir}'
        }
        
    else:
        dir_dict = {
            'data': f'./data/llama3/R5/1000size/{hot_dir}/{answer_dir}',
            'result': f'./results/llama3/R5/1000size/{hot_dir}/{answer_dir}',
            'trained_model': f'./trained_model/llama3/R5/1000size/{hot_dir}/{answer_dir}',
            'graph': f'./results/llama3/R5/1000size/graphs/{hot_dir}/{answer_dir}'
        }
    return dir_dict
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--nhot', action='store_true')
    parser.add_argument('--answer', action='store_true', help='including the answer')
    parser.add_argument('--add', action='store_true')
    args = parser.parse_args()

    dir_dict = get_dir_dict(args.nhot, args.answer, args.add)

    main(dir_dict)