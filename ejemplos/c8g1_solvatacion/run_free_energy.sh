#!/bin/bash
# =========================================================
# run_free_energy.sh
#
# Ejecuta simulaciones de energía libre en GROMACS para
# cada valor de lambda (0..N).
#
# Requiere:
#   - Archivos .mdp generados en carpeta MDP/
#   - Archivo inicial de coordenadas (ej. c8g1_water.gro)
#   - Archivo topológico (topol.top)
# =========================================================

FREE_ENERGY=$(pwd)
echo "Free energy home directory set to $FREE_ENERGY"
MDP=$FREE_ENERGY/MDP
echo ".mdp files are stored in $MDP"

# Detectar automáticamente el número de lambdas
N_LAMBDAS=$(ls $MDP/md_*.mdp | wc -l)
echo "Detected $N_LAMBDAS lambda states."

# Usa gmx directamente del PATH
GMX=gmx

for (( i=0; i<$N_LAMBDAS; i++ ))
do
    LAMBDA=$i
    echo "=== Lambda = $LAMBDA ==="

    mkdir -p Lambda_$LAMBDA/EM
    cd Lambda_$LAMBDA/EM

    echo "[INFO] EM (lambda $LAMBDA)"
    $GMX grompp -f $MDP/em_steep_${LAMBDA}.mdp -c $FREE_ENERGY/c8g1_water.gro -p $FREE_ENERGY/topol.top -o min$LAMBDA.tpr
    $GMX mdrun -deffnm min$LAMBDA

    cd ../
    mkdir -p NVT
    cd NVT

    echo "[INFO] NVT (lambda $LAMBDA)"
    $GMX grompp -f $MDP/nvt_${LAMBDA}.mdp -c ../EM/min$LAMBDA.gro -p $FREE_ENERGY/topol.top -o nvt$LAMBDA.tpr
    $GMX mdrun -deffnm nvt$LAMBDA

    cd ../
    mkdir -p NPT
    cd NPT

    echo "[INFO] NPT (lambda $LAMBDA)"
    $GMX grompp -f $MDP/npt_${LAMBDA}.mdp -c ../NVT/nvt$LAMBDA.gro -p $FREE_ENERGY/topol.top -t ../NVT/nvt$LAMBDA.cpt -o npt$LAMBDA.tpr
    $GMX mdrun -deffnm npt$LAMBDA

    cd ../
    mkdir -p Production_MD
    cd Production_MD

    echo "[INFO] Production MD (lambda $LAMBDA)"
    $GMX grompp -f $MDP/md_${LAMBDA}.mdp -c ../NPT/npt$LAMBDA.gro -p $FREE_ENERGY/topol.top -t ../NPT/npt$LAMBDA.cpt -o md$LAMBDA.tpr
    $GMX mdrun -deffnm md$LAMBDA

    cd $FREE_ENERGY
    echo "[DONE] Lambda $LAMBDA completado."
done

echo "=== TODAS LAS SIMULACIONES FINALIZADAS ==="
