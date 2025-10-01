# 🔬 Flujo de trabajo: Simulaciones de Energía Libre

Este documento describe el uso de los **scripts auxiliares** incluidos en este repositorio para preparar, ejecutar y recolectar simulaciones de energía libre con **GROMACS**.

El flujo completo consta de tres pasos:

1. **Generación de archivos `.mdp` por λ** → `generate_mdp.py`
2. **Ejecución de simulaciones en GROMACS** → `run_free_energy.sh`
3. **Recolección de resultados (`.xvg`) y análisis BAR** → `collect_free.sh`

---

## 1️⃣ Generación de archivos `.mdp` por λ

Script: [`generate_mdp.py`](generate_mdp.py)

Este script lee los archivos base (`md.mdp`, `nvt.mdp`, `npt.mdp`, `em_steep.mdp`) en la carpeta `MDP/` y genera automáticamente los archivos para cada valor de **λ**.

```bash
python generate_mdp.py --n 21
```

* Entrada:

  * `MDP/md.mdp`, `MDP/nvt.mdp`, `MDP/npt.mdp`, `MDP/em_steep.mdp`
* Salida:

  * `MDP/md_0.mdp ... md_20.mdp`
  * `MDP/nvt_0.mdp ... nvt_20.mdp`
  * etc.

---

## 2️⃣ Ejecución de simulaciones

Script: [`run_free_energy.sh`](run_free_energy.sh)

Este script corre de manera organizada las simulaciones para cada λ, generando las carpetas `Lambda_0`, `Lambda_1`, … con la jerarquía:

```
Lambda_X/
 ├── EM/
 ├── NVT/
 ├── NPT/
 └── Production_MD/
```

Ejemplo de uso:

```bash
./run_free_energy.sh
```

El número de λ se detecta automáticamente en función de los archivos generados en `MDP/`.

---

## 3️⃣ Recolección de resultados y análisis BAR

Script: [`collect_free.sh`](collect_free.sh)

Este script recopila todos los archivos `md*.xvg` de cada `Lambda_X/Production_MD/` en una carpeta `Free/`.
Luego ejecuta el análisis de energía libre con el método **BAR** nativo de GROMACS.

```bash
./collect_free.sh
```

* Entrada:

  * `Lambda_X/Production_MD/mdX.xvg` (uno por cada λ)
* Salida:

  * Carpeta `Free/` con todos los `.xvg` copiados
  * Resultados de GROMACS BAR:

    * `gromacs-bar.xvg`
    * `gromacs-bar-int.xvg`

---

## 🔗 Flujo completo resumido

```bash
# 1. Generar .mdp para N lambdas
python generate_mdp.py --n 21

# 2. Ejecutar simulaciones
./run_free_energy.sh

# 3. Recolectar resultados y correr BAR
./collect_free.sh
```

Al final tendrás en `Free/` los archivos listos para análisis comparativo (BAR vs TI vs MBAR) con el script `analyze_free_energy.py`.

---