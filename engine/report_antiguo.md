# nanochat training report

Generated: 2025-12-01 14:05:18

## Environment

### Git Information
- Branch: master
- Commit: 4a87a0d (dirty)
- Message: Merge pull request #299 from samjabrahams/rotary_embedding_head_dim_comment_clea

### Hardware
- Platform: Linux
- CPUs: 8 cores (16 logical)
- Memory: 15.5 GB
- GPUs: None available

### Software
- Python: 3.10.19
- PyTorch: 2.9.0+cpu


### Bloat
- Characters: 409,031
- Lines: 9,969
- Files: 49
- Tokens (approx): 102,257
- Dependencies (uv.lock lines): 2,218

Run started: 2025-12-01 14:05:18

---

## Tokenizer training
timestamp: 2025-12-01 14:05:41

- max_chars: 1,000,000,000
- doc_cap: 10,000
- vocab_size: 65,536
- train_time: 19.5805
- num_special_tokens: 9
- token_bytes_min: 1
- token_bytes_max: 32
- token_bytes_mean: 6.9201
- token_bytes_std: 2.8729


## Tokenizer evaluation
timestamp: 2025-12-01 14:05:44

### Comparison with GPT-2

| Text Type | Bytes | GPT-2 Tokens | GPT-2 Ratio | Ours Tokens | Ours Ratio | Relative Diff % |
|-----------|-------|--------------|--------------|-------------|------------|-----------------|
| news | 1819 | 404 | 4.50 | 375 | 4.85 | +7.2% |
| korean | 893 | 745 | 1.20 | 731 | 1.22 | +1.9% |
| code | 1259 | 576 | 2.19 | 494 | 2.55 | +14.2% |
| math | 1834 | 936 | 1.96 | 971 | 1.89 | -3.7% |
| science | 1112 | 260 | 4.28 | 227 | 4.90 | +12.7% |
| fwe-train | 4208518 | 900364 | 4.67 | 856776 | 4.91 | +4.8% |
| fwe-val | 4400098 | 954009 | 4.61 | 908625 | 4.84 | +4.8% |

### Comparison with GPT-4

| Text Type | Bytes | GPT-4 Tokens | GPT-4 Ratio | Ours Tokens | Ours Ratio | Relative Diff % |
|-----------|-------|--------------|--------------|-------------|------------|-----------------|
| news | 1819 | 387 | 4.70 | 375 | 4.85 | +3.1% |
| korean | 893 | 364 | 2.45 | 731 | 1.22 | -100.8% |
| code | 1259 | 309 | 4.07 | 494 | 2.55 | -59.9% |
| math | 1834 | 832 | 2.20 | 971 | 1.89 | -16.7% |
| science | 1112 | 249 | 4.47 | 227 | 4.90 | +8.8% |
| fwe-train | 4208518 | 874799 | 4.81 | 856776 | 4.91 | +2.1% |
| fwe-val | 4400098 | 927977 | 4.74 | 908625 | 4.84 | +2.1% |


## Base model training
timestamp: 2025-12-01 14:19:50

- run: dummy
- device_type: 
- depth: 4
- max_seq_len: 1024
- num_iterations: 50
- target_flops: -1.0000
- target_param_data_ratio: 20
- device_batch_size: 1
- total_batch_size: 1024
- embedding_lr: 0.2000
- unembedding_lr: 0.0040
- weight_decay: 0.0000
- matrix_lr: 0.0200
- grad_clip: 1.0000
- warmup_ratio: 0.0000
- warmdown_ratio: 0.2000
- final_lr_frac: 0.0000
- resume_from_step: -1
- eval_every: 50
- eval_tokens: 4096
- core_metric_every: 50
- core_metric_max_per_task: 12
- sample_every: 50
- save_every: -1
- model_tag: 
- Number of parameters: 36,700,160
- Number of FLOPs per token: 1.321206e+08
- Calculated number of iterations: 50
- Number of training tokens: 51,200
- Tokens : Params ratio: 0.0014
- DDP world size: 1
- warmup_ratio: 0.0000
- warmdown_ratio: 0.2000
- final_lr_frac: 0.0000
- Minimum validation bpb: 2.1030
- Final validation bpb: 2.1030
- CORE metric estimate: -0.0530
- MFU %: 0.00%
- Total training flops: 6.764573e+12
- Total training time: 6.11m
- Peak memory usage: 0.00MiB


## Base model loss
timestamp: 2025-12-01 14:20:02

- train bpb: 1.8757
- val bpb: 2.1030
- sample 0: <|bos|>The capital of France is a very a very a very a very a very a very a very a very
- sample 1: <|bos|>The chemical symbol of gold is a very a very a very a very a very a very a very a very
- sample 2: <|bos|>If yesterday was Friday, then tomorrow will be a very a very a very a very a very a very a very a very
- sample 3: <|bos|>The opposite of hot is a very a very a very a very a very a very a very a very
- sample 4: <|bos|>The planets of the solar system are: and the body. This is a very very very a very a very a very
- sample 5: <|bos|>My favorite color is a very a very a very a very a very a very a very a very
- sample 6: <|bos|>If 5*x + 3 = 13, then x is a very very very a very a very a very a very a very a very


## Base model evaluation
timestamp: 2025-12-01 14:28:15

- Model: base_model (step 50)
- CORE metric: 0.0025
- hellaswag_zeroshot: 0.1667
- jeopardy: 0.0000
- bigbench_qa_wikidata: 0.0000
- arc_easy: -0.0833
- arc_challenge: -0.1667
- copa: 0.3750
- commonsense_qa: -0.0938
- piqa: -0.2500
- openbook_qa: 0.1667
- lambada_openai: 0.0000
- hellaswag: 0.1667
- winograd: 0.3750
- winogrande: -0.1250
- bigbench_dyck_languages: 0.0000
- agi_eval_lsat_ar: -0.1719
- bigbench_cs_algorithms: 0.0000
- bigbench_operators: 0.0000
- bigbench_repeat_copy_logic: 0.0000
- squad: 0.0000
- coqa: 0.0000
- boolq: -0.4803
- bigbench_language_identification: 0.1749


## Midtraining
timestamp: 2025-12-01 14:42:32

- run: dummy
- device_type: 
- dtype: bfloat16
- num_iterations: 100
- max_seq_len: 1024
- device_batch_size: 1
- unembedding_lr: 0.0040
- embedding_lr: 0.2000
- matrix_lr: 0.0200
- init_lr_frac: 1.0000
- weight_decay: 0.0000
- eval_every: 50
- eval_tokens: 4096
- total_batch_size: 1024
- dry_run: 0
- Number of iterations: 99
- DDP world size: 1
- Minimum validation bpb: 2.0414


## Chat evaluation mid
timestamp: 2025-12-01 14:43:47

- source: mid
- task_name: None
- dtype: bfloat16
- temperature: 0.0000
- max_new_tokens: 128
- num_samples: 1
- top_k: 50
- batch_size: 8
- model_tag: None
- step: None
- max_problems: 20
- device_type: 
- ARC-Easy: 0.2500
- ARC-Challenge: 0.2500
- MMLU: 0.2000
- GSM8K: 0.0000
- HumanEval: 0.0000
- SpellingBee: 0.0000
- ChatCORE metric: -0.0111


## Chat SFT
timestamp: 2025-12-01 15:00:44

- run: dummy
- source: mid
- device_type: 
- dtype: bfloat16
- device_batch_size: 1
- num_epochs: 1
- num_iterations: 100
- target_examples_per_step: 4
- unembedding_lr: 0.0040
- embedding_lr: 0.2000
- matrix_lr: 0.0200
- weight_decay: 0.0000
- init_lr_frac: 0.0200
- eval_every: 100
- eval_steps: 4
- eval_metrics_every: 200
- eval_metrics_max_problems: 16
- Training rows: 21,443
- Number of iterations: 100
- Training loss: 2.1361
- Validation loss: 6.4721


## Summary

- Characters: 409,031
- Lines: 9,969
- Files: 49
- Tokens (approx): 102,257
- Dependencies (uv.lock lines): 2,218

| Metric          | BASE     | MID      | SFT      | RL       |
|-----------------|----------|----------|----------|----------|
| CORE            | 0.0025   | -        | -        | -        |
| ARC-Challenge   | -        | 0.2500   | -        | -        |
| ARC-Easy        | -        | 0.2500   | -        | -        |
| GSM8K           | -        | 0.0000   | -        | -        |
| HumanEval       | -        | 0.0000   | -        | -        |
| MMLU            | -        | 0.2000   | -        | -        |
| ChatCORE        | -        | -0.0111  | -        | -        |

Total wall clock time: 0h55m
