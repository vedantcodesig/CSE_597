```markdown
# PROMPT.ARCHAEOLOGY

Prompt.Archaeology is the first system designed to systematically recover the original natural language instructions (prompts) used to generate AI-authored Python code. While prior work focuses on detecting AI code or attributing it to specific models, this project tackles the generative task of Intent Reconstruction. The data and models directory are created on running the code.

By using Low-Rank Adaptation (LoRA) on `microsoft/phi-3-mini-4k-instruct`, this system proves that sensitive business logic, constraints, and operational context can be reverse-engineered directly from pure code structure.

## Repository Structure

```text
prompt-archaeology/
├── data/
│   ├── figures/
│   └── .gitkeep
├── models/
│   └── .gitkeep
├── src/
│   ├── data_validation_eda.py
│   ├── evaluate.py
│   ├── few_shot_baseline.py
│   ├── forensic_scanner.py
│   ├── generate_dataset.py
│   ├── inference.py
│   ├── train.py
│   └── visualize_metrics.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
```bash
git clone [https://github.com/yourusername/prompt-archaeology.git](https://github.com/yourusername/prompt-archaeology.git)
cd prompt-archaeology
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Pipeline

Execute the pipeline scripts in sequential order from the root directory. Hardware Requirement: NVIDIA GPU with at least 16GB VRAM (e.g., T4, RTX 3090/4090, A100).

**1. Generate the Dataset**
```bash
python src/generate_dataset.py
```
This creates the `data/dataset.json` file containing 200 code-to-prompt pairs (13 easy named functions, 187 hard structurally obfuscated functions).

**2. Validate the Dataset (Exploratory Data Analysis)**
```bash
python src/data_validation_eda.py
```
Performs rigorous Abstract Syntax Tree (AST) validation and regex credential scanning to guarantee the dataset contains no syntax errors or hardcoded secrets prior to training.

**3. Fine-Tune the Model**
```bash
python src/train.py
```
Loads Phi-3-mini in 4-bit quantization, applies LoRA to the attention and MLP projections, trains for 5 epochs using `paged_adamw_8bit`, and saves the trained adapters to `models/prompt_archaeology_lora`.

**4. Generate Few-Shot Baseline**
```bash
python src/few_shot_baseline.py
```
Establishes a zero-gradient, few-shot baseline against the dataset to isolate and measure the exact performance gains provided by the LoRA fine-tuning.

**5. Run Inference**
```bash
python src/inference.py
```
Loads the fine-tuned model and reconstructs prompts for the validation dataset, saving the raw output to `data/inference_results.json`.

**6. Evaluate Metrics**
```bash
python src/evaluate.py
```
Calculates BLEU, ROUGE-1, ROUGE-L, and Semantic Similarity (using `all-MiniLM-L6-v2`) against the ground truth, saving the final report to `data/evaluation_results.json`.

**7. Visualize Results**
```bash
python src/visualize_metrics.py
```
Parses the evaluation metrics and generates publication-ready bar charts in `data/figures/` comparing the baseline model against the fine-tuned model.

**8. Run Forensic Scanner (Applied Tooling)**
```bash
python src/forensic_scanner.py <path_to_scan>
```
Elevates the model into an applied forensic CLI tool. It recursively parses a target directory of Python files, extracts function definitions via AST, and attempts to reconstruct the original developer prompts in the wild, outputting a `forensic_scan_report.json`.

## Threat Model Context

This tool demonstrates that AI-generated code inadvertently acts as a side-channel, leaking the operational constraints, compliance rules, and cryptographic decisions provided by developers during prompting. 
```
