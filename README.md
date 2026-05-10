# Lead Scoring con Machine Learning

**Proyecto de Data Science · Portfolio TechAcces · 2026**

---

## Problema de negocio

Las empresas con modelo inbound generan más leads de los que el equipo comercial puede atender.
Sin priorización, el canal se satura y se pierden oportunidades de venta.

**Lead Scoring** es la técnica que resuelve esto: asignar una probabilidad de compra a cada lead para que el equipo comercial focalice su esfuerzo donde el retorno es mayor.

## Objetivo

Construir un modelo de clasificación que prediga si un lead comprará (`compra = 1`) o no (`compra = 0`), y extraer insights accionables para el equipo de ventas.

## Dataset

| Parámetro | Valor |
|---|---|
| Registros | 9.093 leads |
| Variables | 21 columnas |
| Variable objetivo | `compra` (binaria) |
| Tasa de conversión | 37.6% |

## Resultados

| Modelo | AUC-ROC | F1-Score |
|---|---|---|
| Regresión Logística | 0.86 | 0.76 |
| Random Forest | 0.97 | 0.91 |
| **XGBoost** | **0.98** | **0.93** |

**XGBoost** es el modelo ganador con un AUC-ROC de 0.98.

## Insights clave

- **Fuente Reference** → 91.8% de conversión (boca a boca convierte casi siempre)
- **Working Professionals** → >90% de conversión
- **SMS Sent como última actividad** → señal clara de interés activo
- **Chat y Facebook** → <26%, baja prioridad para el equipo comercial

## Stack técnico

`Python` · `Pandas` · `Scikit-learn` · `XGBoost` · `Matplotlib` · `Seaborn`

## Estructura del proyecto

```
lead_scoring/
├── lead_scoring.ipynb   # Notebook principal con EDA, modelos y visualizaciones
├── Leads.csv            # Dataset original
├── requirements.txt     # Dependencias
└── README.md            # Este archivo
```

## Cómo ejecutar

```bash
pip install -r requirements.txt
jupyter notebook lead_scoring.ipynb
```

---

*Juan Luis León Rodríguez · TechAcces Portfolio 2026*
