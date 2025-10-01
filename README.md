# micelle-free-energy

**Automated Free Energy Analysis for Micellization using Molecular Dynamics**

Este repositorio contiene una herramienta desarrollada para **automatizar el análisis de simulaciones moleculares alquímicas** enfocadas en la **micelización de tensoactivos no iónicos**.
La metodología integra **alchemlyb** y **pymbar** para calcular diferencias de energía libre (ΔG) mediante los enfoques:

* **TI (Thermodynamic Integration)**
* **BAR (Bennett Acceptance Ratio)**
* **MBAR (Multistate Bennett Acceptance Ratio)**

El flujo de trabajo está diseñado para ser **reproducible, modular y extensible**, reduciendo la barrera técnica para investigadores que deseen implementar análisis termodinámicos avanzados.

---

## ✨ Características principales

* Procesa automáticamente archivos de salida (`.xvg`) de GROMACS.
* Implementa y compara **TI, BAR y MBAR** en un mismo marco.
* Incluye rutinas de preprocesamiento (decorrelación y subsampling).
* Genera gráficos comparativos de ΔG vs. λ de forma automática.
* Validado con simulaciones de micelas de **pentaetilenglicol monoéster de octilo (C8E5)**.

---

## 📦 Instalación

Requiere **Python 3.10+**. Se recomienda usar un entorno virtual:

```bash
git clone https://github.com/tuusuario/micelle-free-energy.git
cd micelle-free-energy
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Uso básico

Coloca tus archivos `md0.xvg, md1.xvg, ..., md20.xvg` en una carpeta y ejecuta:

```bash
python analyze_free_energy.py --input ./xvg_files --output results/
```

El programa generará:

* `results_summary.csv` con ΔG calculados por TI, BAR y MBAR.
* Gráficas comparativas (`.png`).

---

## 📊 Ejemplo de salida

| Método | ΔG° (kJ/mol) | Tiempo de cómputo |
| ------ | ------------ | ----------------- |
| TI     | -18.7 ± 0.6  | ~2 min            |
| BAR    | -18.8 ± 0.5  | ~5 s              |
| MBAR   | -18.6 ± 0.5  | ~4 min            |

*(valores ilustrativos basados en C8E5)*

---

## 🔮 Futuro

* Extender soporte a otros tensoactivos (iónicos y no iónicos).
* Implementación en **Rust** para mejorar rendimiento y portabilidad.
* Integración con interfaces gráficas y notebooks para enseñanza.

---

## 📚 Referencias

* Navarro-Aquino, D., & Medeiros, M. (2022). *Molecular simulation of pentaethylene glycol monooctyl ether micelles in water: Prediction of the micellization Gibbs energy*. **Colloids and Surfaces A**, 640, 128406.
* [alchemlyb documentation](https://alchemlyb.readthedocs.io/)

---
