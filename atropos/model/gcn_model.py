import torch.nn as nn
import os
import torch
import numpy as np
import argparse
import matplotlib.pyplot as plt
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.loader import DataLoader
from sklearn.model_selection import KFold
from tqdm import tqdm
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.metrics import precision_score, recall_score, confusion_matrix
import random

def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.use_deterministic_algorithms(True)
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
    
def data_load(data_dir):
    dataset_S = dict()
    dataset_F = dict()
    dataset_FA = dict()
    
    ks = [int(k) for k in os.listdir(data_dir)]
    for k in ks:
        data_for_k = torch.load(os.path.join(data_dir, str(k), 'gcn_dataset.pth'), weights_only=False)

        dataset_S[k] = data_for_k["dataset_S"]
        dataset_F[k] = data_for_k["dataset_F"]
        dataset_FA[k] = data_for_k["dataset_FA"]
    
    print("Datasets loaded successfully")

    return dataset_S, dataset_F, dataset_FA


def print_metadata(dataset, ks, dataset_name):
    print(f"About {dataset_name}")
    print(f"Data size: {len(dataset[1])}")

    for k in sorted(ks):
        print(f"------------{k}------------")
        print(f".   Size: {len(dataset[k])}")
        print(f".   x shape: {dataset[k][0].x.shape}")


def get_baseline_acc(dataset, result_file):
    num_total = len(dataset[1])

    num_true = 0
    for data in dataset[1]:
        if data.y:
            num_true += 1
    baseline_acc = num_true / num_total
    print(f"Baseline accuracy: {baseline_acc}")

    with open(result_file, 'a+') as rf:
        rf.write(f'baseline accuracy: {baseline_acc:.4f}\n')


class GCN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, dropout_p, num_layers):
        super(GCN, self).__init__()
        self.num_layers = num_layers
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.convs = torch.nn.ModuleList([
            GCNConv(hidden_dim, hidden_dim) for _ in range(num_layers - 2)
        ])
        self.conv_out = GCNConv(hidden_dim, hidden_dim)
        self.fc = torch.nn.Linear(hidden_dim, output_dim)
        self.dropout_p = dropout_p

    def forward(self, data):
        x, edge_index, edge_weight, batch = data.x, data.edge_index, data.edge_weight, data.batch
        x = self.conv1(x, edge_index, edge_weight)
        x = F.relu(x)
        x = F.dropout(x, p=self.dropout_p, training=self.training)
        for i, conv in enumerate(self.convs):
            x = conv(x, edge_index, edge_weight)
            x = F.relu(x)
            x = F.dropout(x, p = self.dropout_p, training=self.training)
        x = self.conv_out(x, edge_index, edge_weight)
        x = global_mean_pool(x, batch) 
        x = self.fc(x)
        return x
    



def train(model, optimizer, criterion, train_loader, device):
    model.train()
    total_loss = 0
    
    for data in train_loader:
        try:
            data = data.to(device)
            optimizer.zero_grad()
            out = model(data)
            if out.dim() == 2 and out.size(1) == 1:
                out = out.view(-1)
            loss = criterion(out, data.y.float())
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        except:
            print(data.task)
    return total_loss / len(train_loader)

def test(model, loader, device):
    model.eval()
    correct = 0
    for data in loader:
        data = data.to(device)
        out = model(data).squeeze()
        pred = (torch.sigmoid(out) >= 0.5).int()
        correct += int((pred == data.y).sum())
    return correct / len(loader.dataset)


def test_with_auc(model, loader, device):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for data in loader:
            data = data.to(device)
            out = model(data)
            if out.dim() == 2 and out.size(1) == 1:
                out = out.view(-1)

            preds = torch.sigmoid(out).cpu().numpy()
            
            labels = data.y.cpu().numpy()

            all_preds.extend(preds)
            all_labels.extend(labels)
    
    fpr, tpr, thresholds = roc_curve(all_labels, all_preds)
    auc = roc_auc_score(all_labels, all_preds)
    return fpr, tpr, auc

def evaluate_with_fixed_threshold_precision(model, loader, device):
    threshold=0.5
    model.eval()
    all_preds, all_labels = [], []
    
    with torch.no_grad():
        for data in loader:
            data = data.to(device)
            out = model(data)
            if out.dim() == 2 and out.size(1) == 1:
                out = out.view(-1)
                
            pred = (torch.sigmoid(out) >= threshold).int()

            if pred.ndim == 0:
                pred = torch.tensor(pred.item())
            labels = data.y.cpu().numpy()

            all_preds.extend(pred.cpu().numpy())
            all_labels.extend(labels)

    precision = precision_score(all_labels, all_preds, zero_division=0)
    
    return precision

def evaluate_with_fixed_threshold_recall(model, loader, device):
    threshold = 0.5
    model.eval()
    all_preds, all_labels = [], []
    
    with torch.no_grad():
        for data in loader:
            data = data.to(device)
            out = model(data)
            if out.dim() == 2 and out.size(1) == 1:
                out = out.view(-1)
            pred = (torch.sigmoid(out) >= threshold).int()
            labels = data.y.cpu().numpy()

            all_preds.extend(pred.cpu().numpy())
            all_labels.extend(labels)
    
    recall = recall_score(all_labels, all_preds, zero_division=0)
    
    return recall

def evaluate_with_npv(model, loader, device):
    threshold = 0.5
    model.eval()
    all_preds, all_labels = [], []
    
    with torch.no_grad():
        for data in loader:
            data = data.to(device)
            out = model(data)
            if out.dim() == 2 and out.size(1) == 1:
                out = out.view(-1)
            pred = (torch.sigmoid(out) >= threshold).int()
            labels = data.y.cpu().numpy()

            all_preds.extend(pred.cpu().numpy())
            all_labels.extend(labels)
    
    # Confusion matrix에서 True Negative와 False Negative 값을 추출
    tn, fp, fn, tp = confusion_matrix(all_labels, all_preds).ravel()
    
    # Negative Predictive Value (NPV) 계산
    npv = tn / (tn + fn) if (tn + fn) > 0 else 0  # 나누는 값이 0이 아닐 경우에만 계산
    
    return npv

def evaluate_with_specificity(model, loader, device):
    threshold = 0.5
    model.eval()
    all_preds, all_labels = [], []
    
    with torch.no_grad():
        for data in loader:
            data = data.to(device)
            out = model(data)
            if out.dim() == 2 and out.size(1) == 1:
                out = out.view(-1)
            pred = (torch.sigmoid(out) >= threshold).int()
            labels = data.y.cpu().numpy()

            all_preds.extend(pred.cpu().numpy())
            all_labels.extend(labels)
    
    # Confusion matrix에서 True Negative와 False Positive 값을 추출
    tn, fp, fn, tp = confusion_matrix(all_labels, all_preds).ravel()
    
    # Specificity (True Negative Rate) 계산
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0  # 나누는 값이 0이 아닐 경우에만 계산
    
    return specificity

def train_and_test_model(dataset, criterion, output_dim, K, kf, lr, batch_size, hidden_dim, dropout_p, num_layer, num_epochs, ks, result_file, device, dataset_name, dir_dict):
    print(f"Training and testing with {dataset_name}")
    with open(result_file, "a+") as rf:
        rf.write(f"{dataset_name.split('_')[-1]}\n")
    
    # ks = [2]
    for k in sorted(ks):
        with open(result_file, "a+") as rf:
            rf.write(f'k={k}\n')
        
        ckpt_base = os.path.join(dir_dict['trained_model'], str(k))

        print(f"==================For {k}=======================")
        
        input_dim = dataset[k][0].x.shape[1]
        splits = kf.split(dataset[k])

        train_accs, test_accs = [0] * num_epochs, [0] * num_epochs
        precisions, recalls, npvs, specificities = [0] * num_epochs, [0] * num_epochs, [0] * num_epochs, [0] * num_epochs

        epoch_fprs = [[] for _ in range(num_epochs)]
        epoch_tprs = [[] for _ in range(num_epochs)]
        mean_fpr = np.linspace(0, 1, 100)
        best_acc = -1.0
        best_acc_fold = -1
        best_acc_epoch = -1

        for fold, (train_idx, test_idx) in tqdm(enumerate(splits)):
            train_dataset = [dataset[k][i] for i in train_idx]
            test_dataset = [dataset[k][i] for i in test_idx]
            train_loader = DataLoader(train_dataset, batch_size = batch_size, shuffle=True)
            test_loader = DataLoader(test_dataset, batch_size = batch_size, shuffle = False)

            model = GCN(input_dim, hidden_dim, output_dim, dropout_p, num_layer).to(device)
            optimizer = torch.optim.Adam(model.parameters(), lr = lr)


            for epoch in range(num_epochs):
                loss = train(model, optimizer, criterion, train_loader,device)
                train_acc = test(model, train_loader, device)
                test_acc = test(model, test_loader, device)
                fpr, tpr, _ = test_with_auc(model, test_loader, device)
                precision = evaluate_with_fixed_threshold_precision(model, test_loader, device)
                recall = evaluate_with_fixed_threshold_recall(model, test_loader, device)
                npv = evaluate_with_npv(model, test_loader, device)
                specificity = evaluate_with_specificity(model, test_loader, device)

                train_accs[epoch] += train_acc
                test_accs[epoch] += test_acc
                precisions[epoch] += precision
                recalls[epoch] += recall
                npvs[epoch] += npv
                specificities[epoch] += specificity

                epoch_fprs[epoch].append(fpr)
                epoch_tprs[epoch].append(np.interp(mean_fpr, fpr, tpr))
                epoch_tprs[epoch][-1][0]= 0.0

                if test_acc > best_acc:
                    best_acc = test_acc
                    best_acc_fold = fold
                    best_acc_epoch = epoch
   
                    acc_ckpt = os.path.join(ckpt_base, f'best_acc.pt')
                    save_checkpoint(
                        model,
                        acc_ckpt,
                        meta={
                            "metric": "test_acc",
                            "value": float(best_acc),
                            "fold": int(best_acc_fold),
                            "epoch": int(best_acc_epoch),
                            "k": int(k),
                            "fold": int(fold),
                            "hparams": {
                                "input_dim": int(input_dim),
                                "hidden_dim": int(hidden_dim),
                                "output_dim": int(output_dim),
                                "dropout_p": float(dropout_p),
                                "num_layer": int(num_layer),
                                "lr": float(lr),
                                "batch_size": int(batch_size)
                            }
                        }
                    )
                    print(f"New checkpoint is saved! - Accuracy: {best_acc}")

        mean_train_accs = [acc / K for acc in train_accs]
        mean_test_accs = [acc / K for acc in test_accs]
        mean_precisions = [pre / K for pre in precisions]
        mean_recalls = [recall / K for recall in recalls]
        mean_npvs = [npv / K for npv in npvs]
        mean_specificities = [spec / K for spec in specificities]


        best_mean_accuracy = max(mean_test_accs)
        best_epoch = mean_test_accs.index(best_mean_accuracy)
        mean_tpr = np.mean(epoch_tprs[best_epoch], axis=0)
        std_tpr = np.std(epoch_tprs[best_epoch], axis=0)
        mean_tpr[-1] = 1.0
        mean_roc_auc = auc(mean_fpr, mean_tpr)

        # Plot accuracy graphs over epochs
        graph_dir = dir_dict['graph']
        if not os.path.exists(graph_dir):
            os.makedirs(graph_dir)

        acc_graph_path = os.path.join(graph_dir, f"{k}k_acc.png")
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, num_epochs + 1), mean_train_accs, label='Train Accuracy')
        plt.plot(range(1, num_epochs + 1), mean_test_accs, label='Test Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.title(f'Accuracy per Epoch for {dataset_name} embedding (k={k})')
        plt.legend()
        plt.grid(True)
        plt.savefig(acc_graph_path)

        roc_auc_graph_path = os.path.join(graph_dir, f"{k}k_roc_auc.png")
        plt.figure(figsize=(4.5, 4))
        plt.plot(mean_fpr, mean_tpr, label=f'ROC Curve (AUC = {mean_roc_auc:.4f})', color='blue', linewidth=2)
        plt.fill_between(mean_fpr, np.maximum(mean_tpr-std_tpr, 0), np.minimum(mean_tpr+std_tpr, 1), color = 'blue', alpha=0.2, label = 'Std. Dev.')
        plt.plot([0, 1], [0, 1], linestyle='--', color='red', linewidth=1.5, label='Random Guess')
        plt.xlabel('False Positive Rate (FPR)', fontsize=14)
        plt.ylabel('True Positive Rate (TPR)', fontsize=14)
        plt.title(f'Mean ROC Curve for GCN Model (F+A, k={k})', fontsize=16)
        plt.legend(loc='lower right', fontsize=12)
        plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
        plt.tight_layout()
        plt.savefig(roc_auc_graph_path)
        
        print(f"Epoch = {best_epoch}")
        print(f"Best_mean_accuracy: {mean_test_accs[best_epoch]:.4f}")
        print(f"Best mean_roc_auc: {mean_roc_auc:.4f}")
        print(f"Best mean_precision: {mean_precisions[best_epoch]:.4f}")
        print(f"Best mean_recall: {mean_recalls[best_epoch]:.4f}")
        print(f"Best mean_npv: {mean_npvs[best_epoch]:.4f}")
        print(f"Best mean_specificity: {mean_specificities[best_epoch]:.4f}")
        print('-------------------------------------------------------------------')
        with open(result_file, "a+") as rf:
            rf.write(f"Epoch = {best_epoch}\n")
            rf.write(f"Best_mean_accuracy: {best_mean_accuracy:.4f}\n")
            rf.write(f"Best mean_roc_auc: {mean_roc_auc:.4f}\n")
            rf.write(f"Best mean_precision: {mean_precisions[best_epoch]:.4f}\n")
            rf.write(f"Best mean_recall: {mean_recalls[best_epoch]:.4f}\n")
            rf.write(f"Best mean_npv: {mean_npvs[best_epoch]:.4f}\n")
            rf.write(f"Best mean_specificity: {mean_specificities[best_epoch]:.4f}\n")
    
def save_checkpoint(model, path, meta=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    payload = {"state_dict": model.state_dict()}
    if meta:
        payload.update(meta)
    torch.save(payload, path)



def main(dir_dict):
    set_seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    data_dir = dir_dict['data']
    dataset_S, dataset_F, dataset_FA = data_load(data_dir)

    result_dir = dir_dict['result']
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    result_file = os.path.join(result_dir, 'result.txt')

    if os.path.exists(result_file):
        os.remove(result_file)
        print(f"{result_file} is removed")
    
    ks = [int(k) for k in os.listdir(data_dir)]
    
    get_baseline_acc(dataset_S, result_file)
    print_metadata(dataset_S, ks, "dataset_S")
    print_metadata(dataset_F, ks, "dataset_F")
    print_metadata(dataset_FA, ks, "dataset_FA")

    criterion = nn.BCEWithLogitsLoss()
    output_dim = 1
    K = 5 
    kf = KFold(n_splits=K, shuffle=True, random_state=42)
    lr = 0.001
    batch_size = 32
    hidden_dim = 32
    dropout_p = 0.8
    num_layer = 2
    num_epochs = 150

    train_and_test_model(dataset_S, criterion, output_dim, K, kf, lr, batch_size, hidden_dim, dropout_p, num_layer, num_epochs, ks, result_file, device, "dataset_S", dir_dict)
    train_and_test_model(dataset_F, criterion, output_dim, K, kf, lr, batch_size, hidden_dim, dropout_p, num_layer, num_epochs, ks, result_file, device, "dataset_F", dir_dict)
    train_and_test_model(dataset_FA, criterion, output_dim, K, kf, lr, batch_size, hidden_dim, dropout_p, num_layer, num_epochs, ks, result_file, device, "dataset_FA", dir_dict)

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
            'data': f'../data/{hot_dir}/{answer_dir}/{add_dir}',
            'result': f'../results/{hot_dir}/{answer_dir}/{add_dir}',
            'trained_model': f'../trained_model/{hot_dir}/{answer_dir}/{add_dir}',
            'graph': f'../results/graphs/{hot_dir}/{answer_dir}/{add_dir}'
        }
        
    else:
        dir_dict = {
            'data': f'../data/{hot_dir}/{answer_dir}',
            'result': f'../result/{hot_dir}/{answer_dir}',
            'trained_model': f'../trained_model/{hot_dir}/{answer_dir}',
            'graph': f'../results/graphs/{hot_dir}/{answer_dir}'
        }
    return dir_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--nhot', action='store_true')
    parser.add_argument('--answer', action='store_true', help='including the answer')
    parser.add_argument('--add', action='store_true')
    args = parser.parse_args()

    dir_dict = get_dir_dict(args.nhot, args.answer, args.add)

    main(dir_dict)