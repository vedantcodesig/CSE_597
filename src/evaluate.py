import json
import numpy as np
from rouge_score import rouge_scorer as rs
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

INPUT_FILE = "data/inference_results.json"
OUTPUT_FILE = "data/evaluation_results.json"

def score_set(result_list, sem_model, rouge, smoother):
    if not result_list: return {}
    bleu_s = []; sem_s = []; r1_s = []; rl_s = []; exact = 0
    
    for r in result_list:
        ref = r["original_prompt"]
        hyp = r["recovered_prompt"]
        
        bleu_s.append(sentence_bleu([ref.lower().split()], hyp.lower().split(), smoothing_function=smoother))
        sem_s.append(float(cosine_similarity([sem_model.encode(ref)], [sem_model.encode(hyp)])[0][0]))
        
        sc = rouge.score(ref, hyp)
        r1_s.append(sc["rouge1"].fmeasure)
        rl_s.append(sc["rougeL"].fmeasure)
        
        if ref.lower().strip() == hyp.lower().strip():
            exact += 1
            
    return {
        "avg_bleu": round(float(np.mean(bleu_s)), 4),
        "avg_semantic_similarity": round(float(np.mean(sem_s)), 4),
        "avg_rouge1": round(float(np.mean(r1_s)), 4),
        "avg_rougeL": round(float(np.mean(rl_s)), 4),
        "exact_match_rate": round(exact / len(result_list), 4),
        "sample_size": len(result_list)
    }

def main():
    sem_model = SentenceTransformer("all-MiniLM-L6-v2")
    rouge = rs.RougeScorer(["rouge1", "rougeL"], use_stemmer=True)
    smoother = SmoothingFunction().method1

    with open(INPUT_FILE, "r") as f:
        results = json.load(f)

    hard_results = [r for r in results if r["is_hard"]]
    easy_results = [r for r in results if not r["is_hard"]]

    metrics = {
        "metrics_all": score_set(results, sem_model, rouge, smoother),
        "metrics_hard": score_set(hard_results, sem_model, rouge, smoother),
        "metrics_easy": score_set(easy_results, sem_model, rouge, smoother)
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    main()