"""
FILE: finetune_lora_colab.py
CREATED: 2025-11-04 20:08:56
DESCRIPTION: Colab-ready LoRA fine-tuning script for small models (3B–7B). Uses PEFT + Transformers.
DEPENDENCIES: transformers, peft, datasets, accelerate, bitsandbytes, trl (optional)
NOTE: This expects a GPU environment. On CPU with 8GB RAM, prefer RAG instead of fine-tuning.
"""
import argparse, json, os
from pathlib import Path

def main():
    import torch
    from datasets import load_dataset
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, DataCollatorForLanguageModeling, Trainer
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    import bitsandbytes as bnb

    parser = argparse.ArgumentParser()
    parser.add_argument("--base-model", default="mistralai/Mistral-7B-v0.1", help="Try smaller models if OOM, e.g., 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'")
    parser.add_argument("--dataset", default=None, help="Path to JSONL with fields 'input' and 'output'")
    parser.add_argument("--output-dir", default="./lora_out")
    parser.add_argument("--micro-batch", type=int, default=1)
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--lora-r", type=int, default=8)
    parser.add_argument("--lora-alpha", type=int, default=16)
    parser.add_argument("--lora-dropout", type=float, default=0.05)
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print("GPU not found. This script is intended for Colab/GPUs.")
        return

    tokenizer = AutoTokenizer.from_pretrained(args.base_model, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        load_in_4bit=True,
        torch_dtype=torch.float16,
        device_map="auto",
        quantization_config=bnb.nn.utils.Params4bitConfig(load_in_4bit=True)
    )
    model = prepare_model_for_kbit_training(model)

    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        lora_dropout=args.lora_dropout,
        target_modules=["q_proj","v_proj","k_proj","o_proj"],
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, peft_config)

    # Load dataset
    data = []
    ds_path = Path(args.dataset) if args.dataset else (Path(__file__).resolve().parents[1] / "data" / "pattern_dataset.jsonl")
    for line in open(ds_path, "r", encoding="utf-8"):
        ex = json.loads(line)
        prompt = ex.get("input","")
        completion = ex.get("output","")
        if not prompt or not completion: 
            continue
        data.append({"text": f"Instruction:\n{prompt}\n\nAnswer:\n{completion}"})
    from datasets import Dataset
    dataset = Dataset.from_list(data)

    def tokenize(batch):
        toks = tokenizer(batch["text"], truncation=True, padding="max_length", max_length=1024)
        toks["labels"] = toks["input_ids"].copy()
        return toks

    tokenized = dataset.map(tokenize, batched=True, remove_columns=["text"])

    args_train = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.micro_batch,
        gradient_accumulation_steps=8,
        learning_rate=args.lr,
        fp16=True,
        logging_steps=10,
        save_steps=200,
        save_total_limit=2,
        optim="paged_adamw_8bit",
        report_to=[],
    )
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
    trainer = Trainer(model=model, args=args_train, train_dataset=tokenized, data_collator=data_collator)
    trainer.train()
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print(f"Saved LoRA adapter to {args.output_dir}")

if __name__ == "__main__":
    main()
