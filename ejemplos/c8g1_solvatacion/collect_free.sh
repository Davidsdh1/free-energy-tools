#!/bin/bash
# =========================================================
# collect_free.sh
#
# Copia archivos .xvg de todas las simulaciones en una
# carpeta "Free" y ejecuta gmx bar de manera automática.
#
# Requiere:
#   - Carpetas Lambda_0, Lambda_1, ..., Lambda_N
#   - Archivos mdX.xvg dentro de cada Production_MD/
# =========================================================

FREE_ENERGY=$(pwd)
echo "Free energy home directory set to $FREE_ENERGY"

# Crear carpeta Free si no existe
FREE_DIR=$FREE_ENERGY/Free
mkdir -p $FREE_DIR
echo "Output directory: $FREE_DIR"

# Detectar número de lambdas en función de md_*.mdp
N_LAMBDAS=$(ls MDP/md_*.mdp | wc -l)
echo "Detected $N_LAMBDAS lambda states."

# Copiar archivos .xvg a Free/
for (( i=0; i<$N_LAMBDAS; i++ ))
do
    LAMBDA=$i
    SRC=$FREE_ENERGY/Lambda_$LAMBDA/Production_MD/md${LAMBDA}.xvg
    if [[ -f $SRC ]]; then
        cp $SRC $FREE_DIR/
        echo "[OK] Copied: $SRC"
    else
        echo "[WARN] File not found: $SRC"
    fi
done

# Construir lista de archivos md*.xvg en orden correcto
cd $FREE_DIR
FILES=$(ls md*.xvg | sort -V)

echo "Running gmx bar with files:"
echo $FILES

# Ejecutar gmx bar
gmx bar -f $FILES -o gromacs-bar.xvg -oi gromacs-bar-int.xvg

echo "=== Free energy analysis (BAR) complete ==="
