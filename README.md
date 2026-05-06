```markdown
# PROMPT.ARCHAEOLOGY

Prompt.Archaeology is the first system designed to systematically recover the original natural language instructions (prompts) used to generate AI-authored Python code. While prior work focuses on detecting AI code or attributing it to specific models, this project tackles the generative task of Intent Reconstruction.

By using Low-Rank Adaptation (LoRA) on microsoft/phi-3-mini-4k-instruct, this system proves that sensitive business logic, constraints, and operational context can be reverse-engineered directly from pure code structure.

## Repository Structure

```text
prompt-archaeology/
├── data/
│   ├── .gitkeep
├── models/
│   ├── .gitkeep
├── src/
│   ├── 01_generate_dataset.py
│   ├── 02_train.py
│   ├── 03_inference.py
│   └── 04_evaluate.py
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

1. Generate the Dataset
```bash
python src/01_generate_dataset.py
```
This creates the data/dataset.json file containing 200 code-to-prompt pairs (13 easy named functions, 187 hard structurally obfuscated functions).

2. Fine-Tune the Model
```bash
python src/02_train.py
```
This script loads Phi-3-mini in 4-bit quantization, applies LoRA to the attention and MLP projections, trains for 5 epochs using paged_adamw_8bit, and saves the adapters to models/prompt_archaeology_lora.

3. Run Inference
```bash
python src/03_inference.py
```
This script loads the fine-tuned model and reconstructs prompts for the dataset, saving the output to data/inference_results.json.

4. Evaluate Metrics
```bash
python src/04_evaluate.py
```
This calculates BLEU, ROUGE-1, ROUGE-L, and Semantic Similarity (using all-MiniLM-L6-v2) against the ground truth, saving the final report to data/evaluation_results.json.

## Threat Model Context

This tool demonstrates that AI-generated code inadvertently acts as a side-channel, leaking the operational constraints, compliance rules, and cryptographic decisions provided by developers during prompting. 

```