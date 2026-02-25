import os
import json

from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from evaluate import load as load_metric

# ŚCIEŻKI I MODEL
MODEL_NAME = "dkleczek/bert-base-polish-uncased-v1"
DATA_PATH = r"C:\DARK8_MARK01\dataset_intents.jsonl"
OUTPUT_DIR = r"C:\DARK8_MARK01\dark8_mark01\nlp\models\intent_trained"

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Wczytuję dataset...")
dataset = load_dataset("json", data_files=DATA_PATH, split="train")

# ETYKIETY INTENCJI
labels = sorted(list(set(dataset["label"])))
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

print(f"Liczba intencji: {len(labels)}")
print("Intencje:", labels)

with open(os.path.join(OUTPUT_DIR, "labels.json"), "w", encoding="utf-8") as f:
    json.dump(labels, f, ensure_ascii=False, indent=4)

print("Tokenizuję...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def preprocess(example):
    enc = tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=64,
    )
    enc["labels"] = label2id[example["label"]]
    return enc

# MAPOWANIE + USUNIĘCIE STARYCH KOLUMN
tokenized = dataset.map(preprocess)
tokenized = tokenized.remove_columns(["label", "text"])

print("Dzielę na train/validation...")
split = tokenized.train_test_split(test_size=0.1, seed=42)
train_ds = split["train"]
val_ds = split["test"]

print("Ładuję model...")
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(labels),
    id2label=id2label,
    label2id=label2id,
)

# ARGUMENTY TRENINGU – kompatybilne z nowszym transformers
args = TrainingArguments(
    output_dir=os.path.join(OUTPUT_DIR, "checkpoints"),
    eval_strategy="epoch",          # nowe API zamiast evaluation_strategy
    save_strategy="epoch",
    logging_steps=20,
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=5e-5,
    weight_decay=0.01,
    load_best_model_at_end=True,
)

metric = load_metric("accuracy")

def compute_metrics(eval_pred):
    logits, labels_ids = eval_pred
    preds = logits.argmax(axis=-1)
    return metric.compute(predictions=preds, references=labels_ids)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

print("Start treningu...")
trainer.train()

print("Zapisuję wytrenowany model...")
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("Gotowe.")
