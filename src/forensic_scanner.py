import os
import ast
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

BASE_MODEL = "microsoft/phi-3-mini-4k-instruct"
ADAPTER_PATH = "models/prompt_archaeology_lora"

def extract_functions_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_code = ast.get_source_segment(content, node)
            if func_code:
                functions.append({"file": filepath, "name": node.name, "code": func_code})
    return functions

def main(target_directory):
    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH)
    bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
    base_model = AutoModelForCausalLM.from_pretrained(BASE_MODEL, quantization_config=bnb_config, device_map="auto")
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
    model.eval()

    forensic_report = []

    for root, _, files in os.walk(target_directory):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                extracted_funcs = extract_functions_from_file(filepath)
                
                for func in extracted_funcs:
                    prefix = f"Code:\n{func['code']}\n\nPrompt:\n"
                    inputs = tokenizer(prefix, return_tensors="pt").to(model.device)
                    
                    with torch.no_grad():
                        outputs = model.generate(**inputs, max_new_tokens=100, temperature=0.1)
                        
                    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
                    marker = "Prompt:\n"
                    recovered = full_text[full_text.rfind(marker) + len(marker):].strip().split("\n")[0] if marker in full_text else ""
                    
                    forensic_report.append({
                        "target_file": func["file"],
                        "function_name": func["name"],
                        "reconstructed_intent": recovered
                    })

    with open("data/forensic_scan_report.json", "w") as f:
        json.dump(forensic_report, f, indent=2)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Usage: python src/06_forensic_scanner.py <path_to_scan>")