import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

BASE_MODEL = "microsoft/phi-3-mini-4k-instruct"
INPUT_DATA = "data/dataset.json"
OUTPUT_DATA = "data/baseline_inference_results.json"

FEW_SHOT_PREFIX = """Code:
def celsius_to_fahrenheit(c):
    return (c * 9/5) + 32

Prompt:
Convert temperature from Celsius to Fahrenheit

Code:
def reverse_string(s):
    return s[::-1]

Prompt:
Reverse a string

"""

def main():
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=False)
    tokenizer.pad_token = tokenizer.eos_token
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL, quantization_config=bnb_config, device_map="auto"
    )
    model.eval()

    with open(INPUT_DATA, "r") as f:
        data = json.load(f)

    results = []
    
    for i, pair in enumerate(data):
        if not pair.get("hard", False):
            continue 
            
        full_prompt = FEW_SHOT_PREFIX + f"Code:\n{pair['code']}\n\nPrompt:\n"
        inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs, max_new_tokens=60, temperature=0.1,
                do_sample=False, pad_token_id=tokenizer.eos_token_id
            )
            
        decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response_part = decoded[len(full_prompt):].strip().split("\n")[0]
        
        results.append({
            "id": pair["id"],
            "original_prompt": pair["prompt"],
            "recovered_prompt": response_part,
            "is_hard": True
        })

    with open(OUTPUT_DATA, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()