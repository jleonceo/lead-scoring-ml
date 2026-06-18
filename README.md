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

> **Origen y licencia del dataset.** `Leads.csv` es el conjunto público *Lead Scoring — X Education*, distribuido en Kaggle bajo licencia **CC0 1.0 (dominio público)**. Es un caso clásico de clasificación de leads, empleado también como práctica en cursos de ciencia de datos. Las cabeceras se han traducido al español; los datos no se han alterado. El EDA, la modelización, la verificación de métricas y las conclusiones de este repositorio son de elaboración propia.

## Resultados

| Modelo | AUC-ROC | F1-Score |
|---|---|---|
| Regresión Logística | 0.89 | 0.74 |
| Random Forest | 0.91 | 0.78 |
| **XGBoost** | **0.92** | **0.80** |

**XGBoost** es el modelo ganador con un AUC-ROC de 0.92. Las métricas se calculan sobre el 20% de test (split estratificado) y son reproducibles ejecutando `verificacion_metricas.py`.

> **Nota de transparencia:** una versión anterior de este README publicaba AUC 0.98 / F1 0.93. Al verificar las métricas con un script de réplica, los valores reales del test set resultaron ser los de la tabla. Se corrigieron y se dejó el script en el repo para que cualquiera pueda comprobarlas.

## Validación y límites

- **Reproducibilidad:** `verificacion_metricas.py` replica la preparación, el split y los tres modelos del notebook, y reporta las métricas exactas del README.
- **Variables del funnel:** `ult_actividad` y los dos scores asignados por el equipo comercial reflejan interacciones que ya ocurrieron en el proceso de venta. Sin ellas, el AUC baja de 0.92 a **0.88** (medido). El modelo sirve para priorizar leads en curso; no predice desde el primer contacto.
- **Mejora pendiente:** la imputación de medianas se calcula sobre el dataset completo antes del split (fuga estadística leve). Lo correcto sería ajustarla solo con train.

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
├── lead_scoring.ipynb        # Notebook principal con EDA, modelos y visualizaciones
├── verificacion_metricas.py  # Réplica de los modelos — reproduce las métricas del README
├── Leads.csv                 # Dataset público X Education (Kaggle, CC0)
├── requirements.txt          # Dependencias
└── README.md                 # Este archivo
```

## Cómo ejecutar

```bash
pip install -r requirements.txt
jupyter notebook lead_scoring.ipynb
```

---

*Juan Luis León Rodríguez · TechAcces Portfolio 2026*
