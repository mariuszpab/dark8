import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_NAME = "dkleczek/bert-base-polish-uncased-v1"
OUTPUT_DIR = "C:/DARK8_MARK01/dark8_mark01/nlp/models/intent_onnx"

os.makedirs(OUTPUT_DIR, exist_ok=True)

LABELS = [
    "WRITE_FILE",
    "READ_FILE",
    "LIST_DIR",
    "DELETE_FILE",
    "MAKE_DIR",
    "APPEND_FILE",
    "RUN_UPDATES",
    "LOG"
]

with open(os.path.join(OUTPUT_DIR, "labels.json"), "w", encoding="utf-8") as f:
    json.dump(LABELS, f, indent=4, ensure_ascii=False)

print("Pobieram tokenizer i model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(LABELS)
)

print("Tworzę przykładowe wejście...")
dummy = tokenizer("test", return_tensors="pt")

print("Eksportuję do ONNX...")
torch.onnx.export(
    model,
    (dummy["input_ids"], dummy["attention_mask"]),
    os.path.join(OUTPUT_DIR, "model.onnx"),
    input_names=["input_ids", "attention_mask"],
    output_names=["logits"],
    dynamic_axes={
        "input_ids": {0: "batch", 1: "sequence"},
        "attention_mask": {0: "batch", 1: "sequence"},
        "logits": {0: "batch"}
    },
    opset_version=14
)

print("Zapisuję tokenizer...")
tokenizer.save_pretrained(OUTPUT_DIR)

print("\n======================================")
print(" KONWERSJA ZAKOŃCZONA SUKCESEM")
print("======================================\n")
