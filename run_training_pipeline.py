#!/usr/bin/env python
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List

# === RUTAS BASE (ajusta si tu estructura es distinta) ===
ROOT_DIR = Path(__file__).resolve().parent              # carpeta donde está este .py
ENGINE_DIR = ROOT_DIR / "engine"                        # carpeta donde está el código de nanochat
CONFIG_DIR = ROOT_DIR / "model_configurations"          # carpeta con tus configs

# Nombre del JSON de configuración a usar
DEFAULT_CONFIG_NAME = "config_lite.json"                # cámbialo si quieres otra config por defecto
DEFAULT_CONFIG_PATH = CONFIG_DIR / DEFAULT_CONFIG_NAME


def run_cmd(cmd: List[str], desc: str = ""):
    """Ejecuta un comando en un subprocess dentro de ENGINE_DIR."""
    print("\n" + "=" * 80)
    if desc:
        print(f"[RUN] {desc}")
    print(" ".join(cmd))
    print(f"[CWD] {ENGINE_DIR}")
    print("=" * 80)

    # Nos aseguramos de ejecutar dentro de engine/, para que `python -m nanochat...` funcione.
    result = subprocess.run(cmd, cwd=str(ENGINE_DIR))
    if result.returncode != 0:
        print(f"[ERROR] Command failed with code {result.returncode}: {' '.join(cmd)}")
        sys.exit(result.returncode)


def build_args_from_dict(base: List[str], args_dict: Dict[str, Any]) -> List[str]:
    """
    Convierte un dict tipo {"depth": 4, "max_seq_len": 1024}
    en ["--depth=4", "--max-seq-len=1024"], ignorando valores None.
    """
    cmd = base[:]
    for k, v in args_dict.items():
        if v is None:
            continue
        flag = f"--{k.replace('_', '-')}"
        if isinstance(v, bool):
            # si es bool=True -> --flag, si es False no se añade
            if v:
                cmd.append(flag)
        else:
            cmd.append(f"{flag}={v}")
    return cmd


def main():
    # === 1) Cargar config por defecto ===
    config_path = DEFAULT_CONFIG_PATH
    print(f"[INFO] Usando configuración: {config_path}")

    if not config_path.exists():
        print(f"[ERROR] No se encontró el archivo de configuración: {config_path}")
        print("       Asegúrate de que existe y de que DEFAULT_CONFIG_NAME es correcto.")
        sys.exit(1)

    with open(config_path, "r") as f:
        cfg = json.load(f)

    # === 2) Config global opcional ===
    nanochat_base_dir = cfg.get("nanochat_base_dir")
    if nanochat_base_dir:
        os.environ["NANOCHAT_BASE_DIR"] = nanochat_base_dir
        print(f"[INFO] NANOCHAT_BASE_DIR = {nanochat_base_dir}")

    stages = cfg.get("stages", {})

    # ====== 3) DATASET (shards) ======
    if stages.get("dataset", False):
        ds_cfg = cfg.get("dataset", {})
        n_shards = ds_cfg.get("num_shards", 4)
        cmd = ["python", "-m", "nanochat.dataset", "-n", str(n_shards)]
        run_cmd(cmd, desc=f"Crear dataset con {n_shards} shards")

    # ====== 4) TOKENIZER TRAIN ======
    if stages.get("tokenizer_train", False):
        tok_cfg = cfg.get("tokenizer", {})
        max_chars = tok_cfg.get("max_chars", 1_000_000_000)
        cmd = [
            "python", "-m", "scripts.tok_train",
            f"--max_chars={max_chars}",
        ]
        run_cmd(cmd, desc=f"Entrenar tokenizer (max_chars={max_chars})")

    # ====== 5) TOKENIZER EVAL ======
    if stages.get("tokenizer_eval", False):
        cmd = ["python", "-m", "scripts.tok_eval"]
        run_cmd(cmd, desc="Evaluar tokenizer")

    # ====== 6) BASE TRAIN ======
    if stages.get("base_train", False):
        base_train_cfg = cfg.get("base_train", {})
        cmd = build_args_from_dict(
            ["python", "-m", "scripts.base_train"],
            base_train_cfg
        )
        run_cmd(cmd, desc="Entrenar modelo base")

    # ====== 7) BASE LOSS (eval rápida de pérdida) ======
    if stages.get("base_loss_eval", False):
        base_loss_cfg = cfg.get("base_loss", {})
        cmd = build_args_from_dict(
            ["python", "-m", "scripts.base_loss"],
            base_loss_cfg
        )
        run_cmd(cmd, desc="Evaluar base_loss sobre valid")

    # ====== 8) BASE EVAL (CORE metric / benchmarks clásicos) ======
    if stages.get("base_core_eval", False):
        base_eval_cfg = cfg.get("base_eval", {})
        cmd = build_args_from_dict(
            ["python", "-m", "scripts.base_eval"],
            base_eval_cfg
        )
        run_cmd(cmd, desc="Evaluar modelo base en CORE benchmarks")

    # ====== 9) MID TRAIN ======
    if stages.get("mid_train", False):
        mid_train_cfg = cfg.get("mid_train", {})
        cmd = build_args_from_dict(
            ["python", "-m", "scripts.mid_train"],
            mid_train_cfg
        )
        run_cmd(cmd, desc="Entrenamiento mid (continuación pretraining + eval CORE)")

    # ====== 10) CHAT EVAL (mid) ======
    if stages.get("chat_eval_mid", False):
        chat_eval_mid_cfg = cfg.get("chat_eval_mid", {})
        cmd = build_args_from_dict(
            ["python", "-m", "scripts.chat_eval"],
            chat_eval_mid_cfg
        )
        run_cmd(cmd, desc="Evaluación chat_eval sobre modelo mid")

    # ====== 11) SFT TRAIN ======
    if stages.get("sft_train", False):
        sft_cfg = cfg.get("sft_train", {})
        cmd = build_args_from_dict(
            ["python", "-m", "scripts.chat_sft"],
            sft_cfg
        )
        run_cmd(cmd, desc="Entrenamiento SFT (instruct/chat finetuning)")

    # ====== 12) REPORT ======
    if stages.get("report", False):
        cmd = ["python", "-m", "nanochat.report", "generate"]
        run_cmd(cmd, desc="Generar report.md de todo el pipeline")

    print("\n✅ Pipeline completado correctamente.")


if __name__ == "__main__":
    main()
