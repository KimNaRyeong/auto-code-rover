import os
import json
import matplotlib.pyplot as plt

def draw_graph_n_distribution(model):
    interaction_len_dict = {i: 0 for i in range(16)}
    for i in range(1, 6):
        result_dir = f"./results/{model}/only_fl_{i}/no_patch"
        instance_dir_list = os.listdir(result_dir)
        
        for instance_dir in instance_dir_list:
            tool_call_layers_file = os.path.join(result_dir, instance_dir, 'output_0/search/tool_call_layers.json')
            if not os.path.exists(tool_call_layers_file):
                interaction_len_dict[0] += 1
            else:
                with open(tool_call_layers_file, 'r') as f:
                    tool_call_layers = json.load(f)
                    interaction_len_dict[len(tool_call_layers)] += 1
    
    plt.figure(figsize=(10, 6))

    lengths = list(interaction_len_dict.keys())
    counts = list(interaction_len_dict.values())

    bars = plt.bar(lengths, counts, color='skyblue', edgecolor='black')

    plt.title(f"Distribution of interaction length ({model})", fontsize=16)
    plt.xlabel('Interaction Length', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.xticks(lengths)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(f'./distribution_{model}.png')


if __name__ == '__main__':
    # draw_graph_n_distribution("mixtral")
    draw_graph_n_distribution("hotswap")
    draw_graph_n_distribution("gpt-4")