# Training Infrastructure Activation Guide
*Audited: 2026-03-25 UTC*

---

## Current State: ✅ OPERATIONAL (Inference) / ⚠️ NOT YET (Fine-tuning)

---

## What's Present

| Component | Location | Status |
|-----------|----------|--------|
| llama.cpp binaries (full suite) | `/bitnet/build/bin/` | ✅ Built, runnable |
| BitNet-b1.58-2B-4T GGUF model | `/bitnet/models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf` | ✅ 1.2 GB, i2_s quantized |
| Training data generator | `/training/generate-training-data.py` | ✅ Built 2026-03-25 |
| Agency instruction JSONL | `/training/agency-instruct.jsonl` | ✅ 42 examples, 48 KB |
| LoRA export binary | `/bitnet/build/bin/llama-export-lora` | ✅ Compiled |

---

## Inference: READY NOW

```bash
/root/.openclaw/workspace/bitnet/build/bin/llama-cli \
  -m /root/.openclaw/workspace/bitnet/models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
  -p "Your prompt here" \
  -n 200 \
  -t 4
```

**Measured performance (2026-03-25):**
- Load time: ~1.16 seconds
- Inference speed: ~21.4 tokens/sec (CPU, 4 threads, x86_64)
- RAM usage: ~1.5 GB (fits in 7.2 GB available)

---

## Training Data: READY

The generator at `/training/generate-training-data.py` fetches articles from
`dollaragency.hashnode.dev` via Hashnode GraphQL and converts them to
instruction-tuning format. Run to refresh:

```bash
python3 /root/.openclaw/workspace/training/generate-training-data.py
```

Output: `/root/.openclaw/workspace/training/agency-instruct.jsonl`

Format:
```json
{"instruction": "What is X?", "input": "", "output": "..."}
```

---

## Fine-tuning: NOT ACTIVE (Missing Components)

To fine-tune on CPU you need:

### 1. Fine-tuning binary
llama.cpp's `llama-finetune` was removed from newer builds. BitNet's build
does not include it. You have two options:

**Option A — Build llama-finetune from source:**
```bash
# Clone the older llama.cpp branch that includes finetune
git clone https://github.com/ggerganov/llama.cpp /tmp/llama-finetune-src
cd /tmp/llama-finetune-src
git checkout b2408  # last commit with finetune
cmake -B build -DLLAMA_CURL=OFF
cmake --build build --target llama-finetune -j4
# binary: /tmp/llama-finetune-src/build/bin/llama-finetune
```

**Option B — Use mlx or trl (Python-based LoRA):**
```bash
pip install trl peft transformers
# Run LoRA fine-tune from the JSONL using a HuggingFace base model
```

### 2. Base model in full precision (for LoRA)
The current GGUF (i2_s) is 2-bit quantized — inference only.
LoRA requires at minimum a 4-bit or fp16 version:

```bash
# Download from HuggingFace
pip install huggingface_hub
python3 -c "
from huggingface_hub import snapshot_download
snapshot_download('microsoft/bitnet-b1.58-2B-4T', local_dir='/bitnet/models/bitnet-full')
"
# WARNING: Full bf16 model = ~4-5 GB RAM just for weights
```

### 3. Training script
Suggested: use `trl` (Transformer Reinforcement Learning library):

```python
from trl import SFTTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig
import datasets

dataset = datasets.load_dataset("json", 
    data_files="/root/.openclaw/workspace/training/agency-instruct.jsonl")

model = AutoModelForCausalLM.from_pretrained("microsoft/bitnet-b1.58-2B-4T")
tokenizer = AutoTokenizer.from_pretrained("microsoft/bitnet-b1.58-2B-4T")

lora_config = LoraConfig(r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"])

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset["train"],
    peft_config=lora_config,
)
trainer.train()
trainer.model.save_pretrained("/root/.openclaw/workspace/training/lora-agency-adapter")
```

---

## Resource Reality Check

| Task | RAM Required | Time Estimate | Feasible on VPS? |
|------|-------------|---------------|-----------------|
| Inference (2B model, i2_s) | ~1.5 GB | ~21 tok/s | ✅ Yes |
| LoRA fine-tune (2B, 4-bit) | ~6+ GB | Hours for 42 examples | ⚠️ Marginal |
| Full fine-tune (2B, bf16) | ~16+ GB | Days | ❌ OOM |
| JSONL data generation | <100 MB | Seconds | ✅ Yes |

**Bottom line:** This VPS can run inference immediately. LoRA fine-tuning is
theoretically possible but will strain the 7.2 GB RAM. Add more data first
(run the generator on more content sources), then attempt LoRA with a 4-bit
quantized adapter.

---

## Next Steps (Priority Order)

1. **Expand training data** — rerun `generate-training-data.py` after adding
   more Hashnode articles or doctrine files. Target: 200+ examples.

2. **Test inference serving** — `llama-server` binary is present. Start it:
   ```bash
   /root/.openclaw/workspace/bitnet/build/bin/llama-server \
     -m /root/.openclaw/workspace/bitnet/models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf \
     --port 8080 -t 4
   ```
   Note: Not accessible externally (HR-009 — no public ports on Ampere).
   Route through a tunnel (ngrok/cloudflared) if external access needed.

3. **Install trl/peft for LoRA** — `pip install trl peft transformers`
   (~500 MB). This enables fine-tuning without a GPU.

4. **Download bf16 checkpoint** (when RAM allows or machine is upgraded).

---

*File generated by subagent audit. Last updated: 2026-03-25.*
