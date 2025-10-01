#!/usr/bin/env python3
"""
generate_mdp.py

Genera múltiples archivos .mdp a partir de archivos base en la carpeta MDP,
cambiando el valor de 'init_lambda_state' de 0 a N.

Uso:
    python generate_mdp.py --n 21
"""

import argparse
from pathlib import Path

def generate_mdp(base_file: Path, n: int):
    with open(base_file, "r") as f:
        lines = f.readlines()

    for i in range(n):
        output_file = base_file.parent / f"{base_file.stem}_{i}.mdp"
        with open(output_file, "w") as out:
            for line in lines:
                if line.strip().startswith("init_lambda_state"):
                    out.write(f"init_lambda_state        = {i}\n")
                else:
                    out.write(line)
        print(f"[OK] Generado: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Genera múltiples .mdp con init_lambda_state modificado."
    )
    parser.add_argument("--n", type=int, default=21,
                        help="Número de lambdas (default: 21 → 0 a 20)")
    parser.add_argument("--mdpdir", default="MDP",
                        help="Carpeta con archivos .mdp base (default: MDP)")
    args = parser.parse_args()

    mdpdir = Path(args.mdpdir)

    for base_file in mdpdir.glob("*.mdp"):
        generate_mdp(base_file, args.n)
