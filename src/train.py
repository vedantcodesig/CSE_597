import json
import os
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training

MODEL_NAME = "microsoft/phi-3-mini-4k-instruct"
OUTPUT_DIR = "models/prompt_archaeology_lora"

def main():
    with open("data/dataset.json", "r") as f:
        data = json.load(f)
    
    texts = [f"Code:\n{ex['code']}\n\nPrompt:\n{ex['prompt']}" for ex in data]
    hf_dataset = Dataset.from_dict({"text": texts})
    split = hf_dataset.train_test_split(test_size=0.2, seed=42)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=False)
    tokenizer.pad_token = tokenizer.eos_token

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )
    
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=False
    )

    model = prepare_model_for_kbit_training(model)
    lora_config = LoraConfig(
        r=8, lora_alpha=16,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=0.1, bias="none", task_type=TaskType.CAUSAL_LM
    )
    model = get_peft_model(model, lora_config)
    
    def tokenize_fn(batch):
        out = tokenizer(batch["text"], truncation=True, max_length=512, padding="max_length")
        out["labels"] = out["input_ids"].copy()
        return out
    tokenized = split.map(tokenize_fn, batched=True, remove_columns=["text"])

    training_args = TrainingArguments(
        output_dir="checkpoints",
        num_train_epochs=5,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=20,
        weight_decay=0.01,
        logging_steps=5,
        save_strategy="no",
        fp16=True,
        optim="paged_adamw_8bit",
        learning_rate=2e-4,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        processing_class=tokenizer,
        data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
    )

    trainer.train()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

if __name__ == "__main__":
    main()