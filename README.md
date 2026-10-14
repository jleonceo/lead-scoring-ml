English version: [README.en.md](README.en.md)

# Puntuación de clientes potenciales con aprendizaje automático

Un modelo que ordena una lista de contactos comerciales por su probabilidad de compra, para que el equipo de ventas
llame primero a quien más probabilidades tiene de comprar.

**Resultado:** llamando solo al 20 % de la lista mejor puntuado se llega a la mitad de los compradores. De cada 100
llamadas de ese tramo, 93 acaban en venta, frente a 38 llamando al azar.

```bash
pip install -r requirements.txt
python verificacion_metricas.py
jupyter notebook lead_scoring.ipynb
```

El script recalcula en unos segundos todas las cifras de esta página. El cuaderno contiene el análisis completo con
sus gráficos y se ejecuta de principio a fin.

## El problema

Una empresa que capta clientes por internet acumula más contactos de los que su equipo comercial puede atender. En
estos datos hay 9.093 personas que dejaron sus datos en un formulario, y el 37,6 % acabó comprando. Llamar por orden
de llegada dedica el mismo tiempo a quien iba a comprar que a quien entró por error.

El modelo da a cada contacto una nota entre cero y uno, y con ella se ordena la lista.

## El ejemplo

Se apartaron 1.819 contactos que el modelo no vio al aprender, con 684 compradores dentro. Ordenados por la nota del
modelo, las 363 primeras llamadas alcanzan a 338 de esos compradores.

Dos grupos destacan por su conversión, medida sobre todo el fichero:
- los que llegan por recomendación de otro cliente compran en el 91,8 % de los casos, sobre 534 contactos;
- los profesionales en activo compran en el 91,6 %, sobre 706.

## Cómo funciona

1. Los huecos de texto se rellenan con «Desconocido».
2. Cada categoría pasa a una columna de ceros y unos.
3. Se separan 7.274 contactos para aprender y 1.819 para el examen, con la misma proporción de compradores en los
   dos grupos.
4. Los huecos numéricos se rellenan con la mediana del grupo de aprendizaje, para que nada del examen se cuele en el
   entrenamiento.
5. Se entrenan tres modelos y se comparan sobre el examen.

| Modelo | AUC | F1 |
|---|---|---|
| Regresión logística | 0,8936 | 0,7422 |
| Bosque aleatorio | 0,9147 | 0,7773 |
| **XGBoost** | **0,9210** | **0,7883** |

El **AUC** mide lo bien ordenada que queda la lista: es la probabilidad de que un comprador tomado al azar reciba
más nota que un no comprador. Un modelo que puntuara al azar sacaría 0,50. El **F1** resume en una cifra cuántos de
los señalados compran de verdad y cuántos compradores se llegan a señalar.

## Datos

`Leads.csv` es el conjunto público *Lead Scoring · X Education* de Kaggle, con licencia CC0 1.0 (dominio público).
Tiene 9.093 filas y 21 columnas; se tradujeron las cabeceras al español y los datos no se han tocado. El análisis, el
modelo y la verificación son de elaboración propia.

## Límites

- Tres de las columnas recogen lo que pasó durante la venta, como la última interacción o la puntuación que puso el
  comercial. Sin ellas, el AUC baja a 0,875. El modelo sirve para ordenar contactos que ya están en marcha y dice
  menos de quien acaba de rellenar el formulario.
- Los grupos pequeños engañan: una ocupación con el 100 % de conversión tiene solo 10 contactos, y por eso no figura
  entre las recomendaciones.
- Son datos públicos de una empresa de formación, de su época y su mercado. Para usarlo en otra empresa habría que
  entrenarlo con sus ventas y repetir el entrenamiento cada temporada.

## Ficheros

| Fichero | Qué contiene |
|---|---|
| `verificacion_metricas.py` | el programa que recalcula las cifras de esta página |
| `lead_scoring.ipynb` | el análisis completo, con los gráficos |
| `Leads.csv` | los datos |
| `requirements.txt` | las bibliotecas necesarias |

## Repositorios relacionados

- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): segmentación de clientes por
  recencia, frecuencia e importe.
- [de-datos-en-bruto-a-decisiones](https://github.com/jleonceo/de-datos-en-bruto-a-decisiones): un fichero de ventas
  en bruto convertido en respuestas de negocio y en un cuadro de mando.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): análisis financiero de una empresa, del libro
  diario a las conclusiones.

---

*Parte del portfolio de [Juan Luis León](https://github.com/jleonceo) · [juanluisleon.vercel.app](https://juanluisleon.vercel.app) · Licencia [MIT](LICENSE)*
