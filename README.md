# free-energy-tools

**Automated Free Energy Analysis with Molecular Dynamics**

Este repositorio proporciona una herramienta para **automatizar el cálculo de diferencias de energía libre (ΔG)** en procesos moleculares como la **micelización de tensoactivos**, a partir de simulaciones realizadas con **GROMACS**.

Integra y compara tres métodos:

* **TI (Thermodynamic Integration)**
* **BAR (Bennett Acceptance Ratio)**
* **MBAR (Multistate Bennett Acceptance Ratio)**

El flujo de trabajo automatiza la lectura de salidas de GROMACS (`.xvg`), aplica preprocesamiento estadístico con **alchemlyb** y genera reportes comparativos en tablas y gráficas.

---

## ⚙️ Requisitos previos

### 1. **GROMACS**

Necesario para correr las simulaciones y generar los archivos de entrada (`.xvg`).

En Ubuntu/Debian se instala con:

```bash
sudo apt update
sudo apt install gromacs
```

Verifica la instalación:

```bash
gmx --version
```

> Recomendado: versión ≥ **2021**.

---

### 2. **Python 3**

La mayoría de distribuciones ya lo incluyen. Verifica con:

```bash
python3 --version
```

Si no está instalado:

```bash
sudo apt install python3 python3-venv python3-pip
```

---

### 3. **Entorno virtual y dependencias**

Para mantener el sistema limpio, crea un entorno virtual en la carpeta del proyecto:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Contenido de `requirements.txt`:

```
numpy
pandas
matplotlib
alchemlyb
pymbar
```

---

## 🚀 Uso básico

1. Corre tus simulaciones de energía libre en GROMACS.
   Obtendrás archivos tipo:

   ```
   md0.xvg, md1.xvg, ..., md20.xvg
   ```

2. Clona este repositorio:

```bash
git clone https://github.com/Davidsdh1/free-energy-tools.git
cd free-energy-tools
```

3. Activa el entorno virtual y corre el análisis:

```bash
source env/bin/activate
python analyze_free_energy.py --input ./xvg_files --output results/
```

4. Resultados generados:

   * `results_summary.csv` con ΔG de TI, BAR y MBAR.
   * Gráficas comparativas en `results/plots/`.

---

## 📊 Ejemplo de resultados

| Método | ΔG° (kJ/mol) | Tiempo de cómputo |
| ------ | ------------ | ----------------- |
| TI     | -18.7 ± 0.6  | ~2 min            |
| BAR    | -18.8 ± 0.5  | ~5 s              |
| MBAR   | -18.6 ± 0.5  | ~4 min            |

*(valores ilustrativos)*

---

