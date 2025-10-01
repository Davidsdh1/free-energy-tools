import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from alchemlyb.parsing.gmx import extract_u_nk, extract_dHdl
from alchemlyb.preprocessing.subsampling import decorrelate_u_nk, decorrelate_dhdl
from alchemlyb import concat
from alchemlyb.estimators import MBAR, BAR, TI

# === Configuración general ===
data_dir = 'Free'  # carpeta donde están los md0.xvg ... md20.xvg
temperature = 300  # Kelvin
file_pattern = os.path.join(data_dir, 'md*.xvg')
file_list = sorted(glob.glob(file_pattern))
print(f'Archivos encontrados: {file_list}')

# === Extracción y preprocesamiento ===
u_nk_list = []
dhdl_list = []

for file_path in file_list:
    print(f'Procesando archivo: {file_path}')
    u_nk = extract_u_nk(file_path, T=temperature)
    dhdl = extract_dHdl(file_path, T=temperature)

    u_nk = decorrelate_u_nk(u_nk, method='dhdl', remove_burnin=True)
    dhdl = decorrelate_dhdl(dhdl, remove_burnin=True)

    u_nk_list.append(u_nk)
    dhdl_list.append(dhdl)

u_nk_all = concat(u_nk_list)
dhdl_all = concat(dhdl_list)
print("Datos concatenados y decorrelacionados.")

# === Estimación de energía libre ===
results = {}

# MBAR
mbar = MBAR()
mbar.fit(u_nk_all)
results['MBAR'] = {
    'deltaF': mbar.delta_f_,
    'dF_err': mbar.d_delta_f_,
}

# BAR
bar = BAR()
bar.fit(u_nk_all)
results['BAR'] = {
    'deltaF': bar.delta_f_,
    'dF_err': bar.d_delta_f_,
}

# TI
ti = TI()
ti.fit(dhdl_all)
results['TI'] = {
    'deltaF': ti.delta_f_,
    'dF_err': ti.d_delta_f_,
}

# === Mostrar resultados por intervalo ===
for method, res in results.items():
    print(f"\n===== {method} =====")
    deltaF = res['deltaF'].values.flatten()
    dF_err = res['dF_err'].values.flatten()
    total = deltaF.sum()
    total_err = (dF_err ** 2).sum() ** 0.5

    print("Intervalo λ     ΔG (kT)       ± error")
    print("------------- ------------- -------------")
    for i, (df, err) in enumerate(zip(deltaF, dF_err)):
        print(f"{i} → {i+1:2d}      {df:10.3f}     ± {err:.3f}")
    print(f"TOTAL {method}:  {total:.3f} ± {total_err:.3f} kT")

# === Tabla comparativa acumulada para graficar ===
num_points = len(results['MBAR']['deltaF']) + 1
df_comparison = pd.DataFrame({'lambda_index': list(range(num_points))})

for method in results:
    deltaF = results[method]['deltaF'].values.flatten()
    dF_err = results[method]['dF_err'].values.flatten()
    full = [0] + list(pd.Series(deltaF).cumsum())
    err = [0] + list((pd.Series(dF_err) ** 2).cumsum().pow(0.5))
    df_comparison[f'{method}_deltaF'] = full
    df_comparison[f'{method}_err'] = err

# === Guardar como CSV y parquet ===
df_comparison.to_csv(f'{data_dir}_comparison.csv', index=False)
u_nk_all.to_parquet(f'{data_dir}_u_nk.parquet')
dhdl_all.to_parquet(f'{data_dir}_dhdl.parquet')
print("Resultados guardados como CSV y Parquet.")

# === Gráfica comparativa ===
plt.figure(figsize=(8, 5))
for method in results:
    plt.errorbar(
        df_comparison['lambda_index'],
        df_comparison[f'{method}_deltaF'],
        yerr=df_comparison[f'{method}_err'],
        label=method,
        marker='o',
        linestyle='-',
        capsize=4,
    )

plt.xlabel('Índice de λ')
plt.ylabel('Energía libre acumulada ΔG (kT)')
plt.title(f'Comparación de energía libre - {data_dir}')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(f'{data_dir}_comparison.png', dpi=300)
plt.show()
