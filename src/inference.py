import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

BASE_MODEL = "microsoft/phi-3-mini-4k-instruct"
ADAPTER_PATH = "models/prompt_archaeology_lora"
INPUT_DATA = "data/dataset.json"
OUTPUT_DATA = "data/inference_results.json"

def main():
    tokenizer = AutoTokenizer.from_pretrained(ADAPTER_PATH)
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16
    )
    
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL, quantization_config=bnb_config, device_map="auto"
    )
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)
    model.eval()

    with open(INPUT_DATA, "r") as f:
        data = json.load(f)

    results = []
    
    for i, pair in enumerate(data):
        prefix = f"Code:\n{pair['code']}\n\nPrompt:\n"
        inputs = tokenizer(prefix, return_tensors="pt").to(model.device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs, max_new_tokens=120, temperature=0.3,
                top_p=0.9, do_sample=True, pad_token_id=tokenizer.eos_token_id
            )
            
        full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        marker = "Prompt:\n"
        recovered = full_text[full_text.rfind(marker) + len(marker):].strip().split("\n")[0] if marker in full_text else full_text.strip()
        
        results.append({
            "id": pair["id"],
            "task": pair["task"],
            "original_prompt": pair["prompt"],
            "recovered_prompt": recovered,
            "is_hard": pair.get("hard", False)
        })

    with open(OUTPUT_DATA, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()