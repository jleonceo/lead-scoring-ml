# Lead Scoring con Machine Learning

**Proyecto de Data Science · Portfolio TechAcces · 2026**

[Español](#español) · [English](#english)

---

## Español

### Problema de negocio

Las empresas con modelo inbound generan más leads de los que el equipo comercial puede atender.
Sin priorización, el canal se satura y se pierden oportunidades de venta.

**Lead Scoring** es la técnica que resuelve esto: asigna a cada lead una probabilidad de compra. Así el equipo comercial focaliza el esfuerzo donde el retorno es mayor.

### Objetivo

Construir un modelo de clasificación que prediga si un lead comprará (`compra = 1`) o no (`compra = 0`), y extraer insights accionables para el equipo de ventas.

### Dataset

| Parámetro | Valor |
|---|---|
| Registros | 9.093 leads |
| Variables | 21 columnas |
| Variable objetivo | `compra` (binaria) |
| Tasa de conversión | 37.6% |

> **Origen y licencia del dataset.** `Leads.csv` es el conjunto público *Lead Scoring · X Education*, distribuido en Kaggle bajo licencia **CC0 1.0 (dominio público)**. Es un caso clásico de clasificación de leads, empleado también como práctica en cursos de ciencia de datos. Las cabeceras se han traducido al español; los datos no se han alterado. El EDA, la modelización, la verificación de métricas y las conclusiones de este repositorio son de elaboración propia.

### Resultados

| Modelo | AUC-ROC | F1-Score |
|---|---|---|
| Regresión Logística | 0.89 | 0.74 |
| Random Forest | 0.91 | 0.78 |
| **XGBoost** | **0.92** | **0.80** |

**XGBoost** es el modelo ganador con un AUC-ROC de 0.92. Las métricas se calculan sobre el 20% de test (split estratificado) y son reproducibles ejecutando `verificacion_metricas.py`.

> **Nota de transparencia:** una versión anterior de este README publicaba AUC 0.98 / F1 0.93. Al verificar las métricas con un script de réplica, los valores reales del test set resultaron ser los de la tabla. Se corrigieron y se dejó el script en el repo para que cualquiera pueda comprobarlas.

### Validación y límites

- **Reproducibilidad:** `verificacion_metricas.py` replica la preparación, el split y los tres modelos del notebook, y reporta las métricas exactas del README.
- **Variables del funnel:** `ult_actividad` y los dos scores asignados por el equipo comercial reflejan interacciones que ya ocurrieron en el proceso de venta. Sin ellas, el AUC baja de 0.92 a **0.88** (medido). El modelo sirve para priorizar leads en curso; no predice desde el primer contacto.
- **Mejora pendiente:** la imputación de medianas se calcula sobre el dataset completo antes del split (fuga estadística leve). Lo correcto sería ajustarla solo con train.

### Insights clave

- **Fuente Reference** → 91.8% de conversión (boca a boca convierte casi siempre)
- **Working Professionals** → >90% de conversión
- **SMS Sent como última actividad** → señal clara de interés activo
- **Chat y Facebook** → <26%, baja prioridad para el equipo comercial

### Stack técnico

`Python` · `Pandas` · `Scikit-learn` · `XGBoost` · `Matplotlib` · `Seaborn`

### Estructura del proyecto

```
lead_scoring/
├── lead_scoring.ipynb        # Notebook principal con EDA, modelos y visualizaciones
├── verificacion_metricas.py  # Réplica de los modelos, reproduce las métricas del README
├── Leads.csv                 # Dataset público X Education (Kaggle, CC0)
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo
```

### Cómo ejecutar

```bash
pip install -r requirements.txt
jupyter notebook lead_scoring.ipynb
```

---

### Repos relacionados

Este análisis es una pieza de un portfolio de casos de analítica. Las piezas hermanas:

- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): segmentación de clientes por recencia, frecuencia e importe.
- [accident-intelligent-agent](https://github.com/jleonceo/accident-intelligent-agent): ETL, exploración y modelo para predecir la gravedad de un accidente de tráfico.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): análisis financiero de una empresa con Python, del libro diario a las conclusiones.

## English

### Business problem

Companies running inbound marketing bring in more leads than the sales team can ever work through. With no way to rank them, the funnel backs up and deals are lost.

**Lead scoring** is the technique that fixes this: it puts a probability of buying on every lead, so the sales team spends its time where the return is.

### Goal

Build a classification model that predicts whether a lead will buy (`compra = 1`) or not (`compra = 0`), and pull out insights the sales team can act on.

### Dataset

| Item | Value |
|---|---|
| Records | 9,093 leads |
| Variables | 21 columns |
| Target | `compra` (binary) |
| Conversion rate | 37.6% |

> **Dataset origin and licence.** `Leads.csv` is the public *Lead Scoring · X Education* set, distributed on Kaggle under a **CC0 1.0 (public domain)** licence. It is a classic lead classification case, also used as coursework on data science programmes. The headers were translated into Spanish; the data itself was left untouched. The EDA, the modelling, the metric checks and the conclusions in this repository are my own work.

### Results

| Model | AUC-ROC | F1-Score |
|---|---|---|
| Logistic Regression | 0.89 | 0.74 |
| Random Forest | 0.91 | 0.78 |
| **XGBoost** | **0.92** | **0.80** |

**XGBoost** comes out on top with an AUC-ROC of 0.92. The metrics are measured on the 20% test split (stratified) and can be reproduced by running `verificacion_metricas.py`.

> **Transparency note:** an earlier version of this README published AUC 0.98 / F1 0.93. Checking the metrics with a replication script showed the real test-set values were the ones in the table. They were corrected, and the script was left in the repo so that anyone can verify them.

### Validation and limits

- **Reproducibility:** `verificacion_metricas.py` replicates the data preparation, the split and the three models from the notebook, and reports the exact metrics quoted here.
- **Funnel variables:** `ult_actividad` and the two scores assigned by the sales team capture interactions that already happened during the sale. Take them out and the AUC drops from 0.92 to **0.88** (measured). The model is there to rank leads already in play; it does not predict from first contact.
- **Pending fix:** median imputation is computed over the whole dataset before the split, which is a mild statistical leak. The correct approach is to fit it on the training set alone.

### Key insights

- **Reference as a source** → 91.8% conversion (word of mouth almost always closes)
- **Working Professionals** → over 90% conversion
- **SMS Sent as the last activity** → a clear sign of active interest
- **Chat and Facebook** → under 26%, low priority for the sales team

### Tech stack

`Python` · `Pandas` · `Scikit-learn` · `XGBoost` · `Matplotlib` · `Seaborn`

### Project structure

```
lead_scoring/
├── lead_scoring.ipynb        # Main notebook: EDA, models and charts
├── verificacion_metricas.py  # Replicates the models, reproduces the README metrics
├── Leads.csv                 # Public X Education dataset (Kaggle, CC0)
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

### How to run it

```bash
pip install -r requirements.txt
jupyter notebook lead_scoring.ipynb
```


### Related repositories

This analysis is one piece of an analytics portfolio. Its sibling projects:

- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): customer segmentation by recency, frequency and monetary value.
- [accident-intelligent-agent](https://github.com/jleonceo/accident-intelligent-agent): ETL, exploration and a model to predict how severe a road accident is.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): financial analysis of a company with Python, from the ledger to the conclusions.

---

*Parte del portfolio de [Juan Luis León](https://github.com/jleonceo) · [juanluisleon.vercel.app](https://juanluisleon.vercel.app) · Licencia [MIT](LICENSE)*
