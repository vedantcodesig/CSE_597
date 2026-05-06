import json
import matplotlib.pyplot as plt
import os

INPUT_FILE = "data/evaluation_results.json"
OUTPUT_DIR = "data/figures/"

def create_comparison_chart(metrics):
    baseline_r1 = metrics["baseline_comparison"]["few_shot_rouge1"]
    finetuned_r1 = metrics["baseline_comparison"]["finetuned_rouge1"]
    
    baseline_rl = metrics["baseline_comparison"]["few_shot_rougeL"]
    finetuned_rl = metrics["baseline_comparison"]["finetuned_rougeL"]

    labels = ['ROUGE-1', 'ROUGE-L']
    baseline_scores = [baseline_r1, baseline_rl]
    finetuned_scores = [finetuned_r1, finetuned_rl]

    x = [0, 1]
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar([p - width/2 for p in x], baseline_scores, width, label='Few-Shot Baseline', color='#d3d3d3')
    ax.bar([p + width/2 for p in x], finetuned_scores, width, label='LoRA Fine-Tuned', color='#1f77b4')

    ax.set_ylabel('Score')
    ax.set_title('Prompt Recovery Performance: Baseline vs Fine-Tuned')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 1.0)

    for i, v in enumerate(baseline_scores):
        ax.text(i - width/2, v + 0.02, str(round(v, 4)), ha='center')
    for i, v in enumerate(finetuned_scores):
        ax.text(i + width/2, v + 0.02, str(round(v, 4)), ha='center')

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_DIR, 'baseline_vs_finetuned.png'), dpi=300)
    plt.close()

def main():
    if not os.path.exists(INPUT_FILE):
        return
        
    with open(INPUT_FILE, "r") as f:
        metrics = json.load(f)

    create_comparison_chart(metrics)

if __name__ == "__main__":
    main()