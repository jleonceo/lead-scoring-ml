# Lead Scoring con Machine Learning

**Proyecto de Data Science · Portfolio TechAcces · 2026**

[Español](#español) · [English](#english)

---

## Español

### Qué problema resuelve

Una empresa que capta clientes por internet acaba con una lista de contactos mucho mayor de lo que su equipo comercial puede atender. En este proyecto hay 9.093 personas que dejaron sus datos en un formulario, y 3.418 de ellas acabaron comprando: algo menos de cuatro de cada diez. Llamar por orden de llegada gasta la misma media hora con quien iba a comprar de todas formas que con quien entró en la web por error. A mitad de lista se ha terminado el trimestre.

Este repositorio le pone a cada contacto una nota entre cero y uno. Con esa nota ordena la lista de arriba abajo. En el oficio comercial ese contacto se llama **lead**: alguien que ha mostrado interés y todavía no ha comprado, porque rellenó un formulario, descargó un documento o pidió información.

Un comercial con años encima tiene su intuición para esto y suele acertar. Lo que una intuición no puede hacer es aplicarse a nueve mil fichas cada mañana, ni explicarle a la dirección en qué se basa, ni quedarse escrita en algún sitio el día que esa persona cambia de empresa.

### El ejemplo en llamadas

El proyecto aparta 1.819 fichas para examinarse a sí mismo. Dentro de ellas había 684 compradores. Ordenada la lista por la nota del modelo, llamando solo al veinte por ciento de arriba, es decir a las 363 primeras, se alcanza a 338 de esos 684 compradores. Sale prácticamente la mitad de las ventas con una quinta parte de las llamadas.

Visto llamada a llamada: de cada cien de ese tramo, 93 caen en alguien que acabó comprando, mientras que llamando al azar habrían caído 38. Ahí está el valor de este trabajo, en el reparto del esfuerzo comercial. Cuenta bastante más que el porcentaje de aciertos del modelo tomado por su cuenta.

### Los datos de partida

| Parámetro | Valor |
|---|---|
| Registros | 9.093 leads |
| Variables | 21 columnas |
| Variable objetivo | `compra` (vale 1 o vale 0) |
| Tasa de conversión | 37,6 % |

Cada fila del fichero `Leads.csv` recoge por dónde entró la persona, cuántas veces volvió a la web, cuántos minutos pasó en ella, su ocupación y si pidió que no la llamaran. Al final hay una columna `compra` que dice si compró. Esa última columna es la respuesta correcta. Existe porque estos 9.093 casos ya pasaron.

> **Origen y licencia del dataset.** `Leads.csv` es el conjunto público *Lead Scoring · X Education*, distribuido en Kaggle bajo licencia **CC0 1.0 (dominio público)**. Es un caso clásico de clasificación de leads. También se emplea como práctica en cursos de ciencia de datos. Las cabeceras se han traducido al español y los datos no se han alterado. El análisis, la modelización, la verificación de métricas y las conclusiones de este repositorio son de elaboración propia.

### Cómo funciona por dentro

Un **modelo** es un conjunto de reglas que el ordenador deduce de los datos. Nadie se las dicta. Aquí nadie escribió que los contactos llegados por recomendación de otro cliente valgan mucho: la máquina lo encontró sola. **Entrenar** es el proceso por el que esas reglas se ajustan mirando casos con la respuesta ya conocida. El programa propone, mide su error y se corrige cientos de veces seguidas.

Una ficha recorre cinco pasos hasta convertirse en una nota:

1. **Se tapan los huecos.** La puntuación que el equipo comercial asigna a mano falta en 4.149 de las 9.093 fichas, casi la mitad. El hueco se rellena con el valor central que tienen las demás fichas. Donde lo que falta es un texto, se escribe la palabra `Desconocido`.
2. **Las palabras se vuelven números.** Un ordenador no compara `Chat` con `Google`, así que cada respuesta posible pasa a ser una columna que vale 0 o 1.
3. **Se parte la lista en dos montones**, 7.274 fichas para aprender y 1.819 guardadas para el examen final.
4. **Se entrenan tres modelos** de complejidad creciente para poder compararlos. La regresión logística traza una frontera recta entre compradores y no compradores. El bosque aleatorio promedia cientos de árboles de decisión construidos sobre trozos distintos de los datos. **XGBoost** encadena 300 reglas donde cada una arregla los fallos que dejó la anterior.
5. **Se examinan con el montón apartado.** De ahí salen las cifras de la tabla de resultados.

Entrenar los tres modelos en un portátil normal lleva cuatro segundos.

### Por qué se aparta un montón de fichas

Los dos montones se separan antes de tocar nada, y el reparto es **estratificado**: ambos conservan la misma proporción de compradores, el 37,6 %. Así el examen no sale más fácil ni más difícil que la clase. Con el primer montón se ajusta el modelo y con el segundo, que no ha visto nunca, se le toma la lección.

La razón de examinarlo con fichas nuevas se puede medir en este mismo repositorio. Un programa así tiene memoria de sobra para quedarse con los casos concretos en lugar de con el criterio, igual que el alumno que se aprende las diez preguntas del examen del año pasado. El modelo ganador saca 0,9648 sobre las fichas que ya había visto y 0,9210 sobre las 1.819 apartadas. Esos cuatro puntos de diferencia son exactamente lo aprendido de memoria, que no sirve para nadie nuevo.

### Qué mide el AUC

**AUC** son las iniciales de una medida que puntúa lo bien ordenada que queda la lista. Se lee sin fórmula ninguna. Coge un comprador al azar y un no comprador al azar. Mira si el modelo le puso más nota al comprador. El AUC es la proporción de veces que gana esa comparación. Sorteando 400.000 parejas del conjunto de prueba, el comprador iba por delante en 92 de cada 100.

Esa escala tiene dos anclas comprobables. Un modelo que reparta notas al azar saca 0,50, cifra que tampoco hay que creerse de palabra: puntuando al azar las 1.819 fichas de prueba salió 0,4994. Ordenar a la perfección, con todos los compradores por encima de todos los demás, daría 1,00. El 0,92 no significa que el modelo acierte el 92 % de las ventas, que es la confusión más extendida en este oficio. Significa que el orden de la lista es fiable; lo que ese orden vale se ve en las 363 llamadas de más arriba.

### Resultados medidos

Todas estas cifras salen de ejecutar el repositorio el 22/07/2026. Ninguna sale de leer lo que promete su documentación.

| Modelo | AUC sobre el conjunto de prueba |
|---|---|
| Regresión Logística | 0,8936 |
| Bosque Aleatorio | 0,9147 |
| **XGBoost** | **0,9210** |

| Comprobación de control | Resultado |
|---|---|
| El AUC de XGBoost recalculado por otras dos vías | 0,9210 y 0,9214 |
| El mismo modelo sobre las fichas que ya había visto | 0,9648 |
| Un modelo que puntúa al azar | 0,4994 |
| `verificacion_metricas.py` se ejecuta hoy | sí, en 4 segundos |

### Lo que hoy no cuadra

**El F1 publicado no sale del script que reproduce las métricas.** El **F1** es una medida distinta del AUC. Resume en un número el equilibrio entre dos cosas. La precisión dice cuántos de los que el modelo señala como compradores lo eran de verdad. La exhaustividad dice cuántos de los compradores reales llega a señalar. Una versión anterior de este README publicaba un F1 de 0,80 en la misma tabla que el AUC. Al ejecutar `verificacion_metricas.py` sale 0,7883. El 0,80 aparece dentro del cuaderno, en un apartado posterior donde se prueban distintos puntos de corte y se elige el más favorable, así que aquella tabla juntaba dos cifras medidas de forma distinta. La diferencia es de un punto en una cifra secundaria; aun así queda dicha, porque la razón de ser de este repositorio es justamente comprobar lo que publica.

**El cuaderno grande ya no se ejecuta.** Rellena sus huecos con una instrucción que las versiones actuales de la biblioteca de datos aceptan sin protestar y ya no obedecen. Así que los 8.544 huecos siguen ahí, salen menos columnas de las que deberían y el primero de los tres modelos se detiene con un error. El programa de comprobación escribe esa misma operación de otra manera y funciona sin tocar nada, que es de donde salen las cifras de la tabla de arriba. Quien clone el repositorio hoy debería empezar por `verificacion_metricas.py` en vez de por el cuaderno.

Esta no es la primera corrección del proyecto. Una versión anterior publicaba un AUC de 0,98 y un F1 de 0,93. Aquellas cifras no coincidían con los gráficos del propio cuaderno. Se corrigieron, se dejó escrita la nota de transparencia y se añadió el programa de réplica. Ese programa es el que ha cazado hoy el punto que faltaba.

### Cuándo no sirve

Tres de las 21 columnas recogen cosas que ocurrieron durante el proceso de venta, como la última interacción registrada o la puntuación que el comercial le puso a la ficha. Quitándolas, el AUC baja de 0,9210 a 0,875. El modelo sirve para ordenar leads que ya están en marcha. Con alguien que acaba de rellenar el formulario hace un minuto tiene bastante menos que decir.

El repositorio arrastra un defecto propio que no ha corregido. El valor con el que se tapan los huecos se calcula sobre las 9.093 fichas juntas, antes de partirlas. Así que una pizca de información del montón de examen se cuela en el de entrenamiento.

Es leve. Queda declarada.

Cuidado con los grupos pequeños. Entre las ocupaciones aparece «Housewife» con el cien por cien de conversión. Impresiona. Luego se mira el tamaño del grupo: diez personas.

Y estos datos son un conjunto público de una empresa de formación, con su época y su mercado. Quien quisiera usar esto de verdad tendría que entrenar el modelo con sus propias ventas y repetir el entrenamiento cada temporada, porque el comportamiento de los clientes cambia y las reglas aprendidas caducan.

### Recomendaciones comerciales con su tamaño de muestra

- **Los leads llegados por recomendación (`Reference`) convierten al 91,8 %**, medido sobre 534 leads. Es el grupo que primero hay que llamar.
- **Los profesionales en activo (`Working Professional`) convierten al 91,6 %**, medido sobre 706 leads.

Otras dos recomendaciones que figuraban aquí antes se han retirado. Una señalaba el `SMS Sent` como última actividad y otra daba menos del 26 % de conversión a los canales de chat y Facebook. Ninguna de las dos llevaba escrito el número de casos sobre el que estaba medida ni se ha podido reproducir al ejecutar el repositorio. Una recomendación para un equipo comercial sin su tamaño de muestra detrás no se sostiene.

### Qué abrir y en qué orden

| Orden | Fichero | Qué encontrarás |
|---|---|---|
| 1 | `verificacion_metricas.py` | El programa que recalcula las cifras publicadas, 84 líneas |
| 2 | `Leads.csv` | Los datos: 9.093 filas y 21 columnas |
| 3 | `lead_scoring.ipynb` | El cuaderno largo, con los gráficos y el análisis. Hoy no se ejecuta entero |
| 4 | `requirements.txt` | Las bibliotecas auxiliares que hacen falta |

### Stack técnico

`Python` · `Pandas` · `Scikit-learn` · `XGBoost` · `Matplotlib` · `Seaborn`

### Cómo ejecutarlo

```bash
pip install -r requirements.txt
python verificacion_metricas.py
```

Tarda cuatro segundos y escribe en pantalla las mismas cifras que este README promete. Es la única forma razonable de creérselas.

### Repos relacionados

Este análisis es una pieza de un portfolio de casos de analítica. Las piezas hermanas:

- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): segmentación de clientes por recencia, frecuencia e importe.
- [accident-intelligent-agent](https://github.com/jleonceo/accident-intelligent-agent): ETL, exploración y modelo sobre los accidentes de tráfico de Madrid, con sus errores documentados.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): análisis financiero de una empresa con Python, del libro diario a las conclusiones.

---

## English

### The problem it solves

A company that brings in customers through the internet ends up with a contact list far longer than its sales team can work through. This project starts from 9,093 people who left their details on a form, of whom 3,418 went on to buy, a little under four in ten. Calling them in the order they arrived spends the same half hour on someone who was going to buy anyway as on someone who landed on the website by mistake. The quarter runs out halfway down the list.

This repository gives every contact a score between zero and one. That score sorts the list from top to bottom. Sales people call that contact a **lead**: someone who has shown interest and has not bought yet, because they filled in a form, downloaded a document or asked for information.

An experienced sales rep has an instinct for this and is often right. What an instinct cannot do is work through nine thousand records every morning, explain to management what it rests on, or stay written down anywhere the day that person leaves the company.

### The example in phone calls

The project sets aside 1,819 records to examine itself. There were 684 buyers inside them. Sorting the list by the model's score and calling only the top twenty per cent, that is the first 363, reaches 338 of those 684 buyers. That is roughly half the sales for a fifth of the calls.

Call by call: out of every hundred in that band, 93 land on someone who ended up buying, against 38 for calls made at random. The value of this work lies in that allocation of effort. It counts for more than the model's hit rate on its own.

### The starting data

| Item | Value |
|---|---|
| Records | 9,093 leads |
| Variables | 21 columns |
| Target | `compra` (1 or 0) |
| Conversion rate | 37.6% |

Every row in `Leads.csv` records how the person arrived, how often they came back to the site, how many minutes they spent on it, their occupation and whether they asked not to be called. The last column, `compra`, says whether they bought. That column is the right answer. It is here because all 9,093 of these cases already happened.

> **Dataset origin and licence.** `Leads.csv` is the public *Lead Scoring · X Education* set, distributed on Kaggle under a **CC0 1.0 (public domain)** licence. It is a classic lead classification case. It is also used as practice work on data science courses. The headers were translated into Spanish and the data itself was left untouched. The analysis, the modelling, the metric checks and the conclusions in this repository are my own work.

### How it works inside

A **model** is a set of rules the computer works out from the data, with nobody dictating them. Nothing here says that contacts arriving through a referral are worth a lot: the machine found that on its own. **Training** is the process by which those rules are tuned by looking at cases whose answer is already known. The program proposes, measures its error and corrects itself hundreds of times over.

A record goes through five steps on its way to a score:

1. **The gaps get filled.** The score the sales team assigns by hand is missing in 4,149 of the 9,093 records, close to half. The gap is filled with the middle value taken from the remaining records. Where the missing item is a piece of text, the word `Desconocido` goes in instead.
2. **Words become numbers.** A computer cannot compare `Chat` with `Google`, so every possible answer becomes a column holding 0 or 1.
3. **The list is split into two piles**, 7,274 records to learn from and 1,819 kept back for the final exam.
4. **Three models are trained**, growing in complexity so they can be compared. A logistic regression draws a straight boundary between buyers and non-buyers. A random forest averages hundreds of decision trees built on different slices of the data. **XGBoost** chains 300 rules where each one repairs the mistakes left by the one before.
5. **They sit the exam with the pile that was set aside.** That is where the results table further down comes from.

Training all three models on an ordinary laptop takes four seconds.

### Why a pile of records is set aside

The two piles are separated before anything else is touched, and the split is **stratified**: both keep the same share of buyers, 37.6%. So the exam is neither easier nor harder than the class. The first pile tunes the model and the second, which it has never seen, tests it.

The reason for testing on fresh records can be measured in this very repository. A program like this has memory to spare for holding on to individual cases rather than the underlying criterion, in the same way a student memorises last year's ten exam questions. The winning model scores 0.9648 on records it had already seen and 0.9210 on the 1,819 set aside. Those four points of difference are exactly what the model memorised, which is of no use whatsoever for anyone new.

### What AUC measures

**AUC** stands for a measure that scores how well the list ends up sorted. It reads without any formula at all. Take a buyer at random and a non-buyer at random. See whether the model gave the buyer the higher score. The AUC is how often that comparison goes the right way. Drawing 400,000 such pairs from the test set, the buyer came out ahead in 92 out of 100.

That scale has two anchors you can check. A model handing out scores at random gets 0.50, a figure not to be taken on trust either: scoring the 1,819 test records at random gave 0.4994. Sorting them perfectly, with every buyer above every non-buyer, would give 1.00. The 0.92 does not mean the model gets 92% of the sales right, which is the most common confusion in this field. It means the ordering of the list is reliable; what that ordering is worth shows up in the 363 calls above.

### Measured results

Every figure below comes from running the repository on 22/07/2026. None of it comes from reading what the documentation promises.

| Model | AUC on the test set |
|---|---|
| Logistic Regression | 0.8936 |
| Random Forest | 0.9147 |
| **XGBoost** | **0.9210** |

| Control check | Result |
|---|---|
| The XGBoost AUC recomputed by two other routes | 0.9210 and 0.9214 |
| The same model on records it had already seen | 0.9648 |
| A model scoring at random | 0.4994 |
| `verificacion_metricas.py` runs today | yes, in 4 seconds |

### What does not add up today

**The published F1 does not come out of the script that reproduces the metrics.** **F1** is a different measure from AUC. It sums up in one number the balance between two things. Precision says how many of those the model flags as buyers really were. Recall says how many of the real buyers it manages to flag. An earlier version of this README published an F1 of 0.80 in the same table as the AUC. Running `verificacion_metricas.py` gives 0.7883. The 0.80 does appear inside the notebook, in a later section that tries different cut-off points and picks the most favourable one, so that table was putting together two figures measured in different ways. It is a one-point gap in a secondary figure; it is said out loud anyway, because checking what it publishes is the whole point of this repository.

**The long notebook no longer runs.** It fills its gaps with an instruction that current versions of the data library accept without complaint and no longer obey. So the 8,544 gaps are still there, fewer columns come out than there should be, and the first of the three models stops with an error. The verification program writes that same operation a different way and works untouched, which is why the figures in the table above exist at all. Anyone cloning the repository today should start with `verificacion_metricas.py` rather than the notebook.

This is not the project's first correction. An earlier version published an AUC of 0.98 and an F1 of 0.93. Those figures did not match the charts in its own notebook. They were corrected, the transparency note was written down and the replication script was added. That script is precisely the tool that caught today's missing point.

### When it does not apply

Three of the 21 columns hold things that happened during the sales process, such as the last recorded interaction or the score the rep gave the record. Take them out and the AUC drops from 0.9210 to 0.875. The model is there to rank leads already in play. It has considerably less to say about someone who filled in the form a minute ago.

The repository carries a flaw of its own that it has not fixed. The value used to fill the gaps is computed over all 9,093 records together, before they are split. So a trace of information from the exam pile leaks into the training pile.

It is mild. It is declared.

Watch out for small groups. Among the occupations, `Housewife` shows a hundred per cent conversion. It is impressive. Then you look at the size of the group: ten people.

And this data is a public set from a training company, with its own period and its own market. Anyone wanting to use this for real would have to train the model on their own sales and retrain it every season, because customer behaviour shifts and learned rules expire.

### Sales recommendations with their sample size

- **Leads arriving through a referral (`Reference`) convert at 91.8%**, measured over 534 leads. That is the group to call first.
- **People in work (`Working Professional`) convert at 91.6%**, measured over 706 leads.

Two other recommendations that used to sit here have been withdrawn. One pointed at `SMS Sent` as the last activity and the other gave chat and Facebook channels under 26% conversion. Neither of them carried the number of cases it was measured over, nor could either be reproduced by running the repository today. A recommendation handed to a sales team without a sample size behind it does not hold.

### What to open and in what order

| Order | File | What you will find |
|---|---|---|
| 1 | `verificacion_metricas.py` | The program that recomputes the published figures, 84 lines |
| 2 | `Leads.csv` | The data: 9,093 rows and 21 columns |
| 3 | `lead_scoring.ipynb` | The long notebook, with the charts and the analysis. It does not run all the way through today |
| 4 | `requirements.txt` | The supporting libraries it needs |

### Tech stack

`Python` · `Pandas` · `Scikit-learn` · `XGBoost` · `Matplotlib` · `Seaborn`

### How to run it

```bash
pip install -r requirements.txt
python verificacion_metricas.py
```

It takes four seconds and prints the same figures this README promises. That is the only sensible way to believe them.

### Related repositories

This analysis is one piece of an analytics portfolio. Its sibling projects:

- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): customer segmentation by recency, frequency and monetary value.
- [accident-intelligent-agent](https://github.com/jleonceo/accident-intelligent-agent): ETL, exploration and a model over Madrid road accident data, with its errors documented.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): financial analysis of a company with Python, from the ledger to the conclusions.

---

*Parte del portfolio de / Part of [Juan Luis León](https://github.com/jleonceo)'s portfolio · [juanluisleon.vercel.app](https://juanluisleon.vercel.app) · Licencia / License: [MIT](LICENSE)*
