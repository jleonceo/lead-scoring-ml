Versión en español: [README.md](README.md)

# Lead scoring with machine learning

A model that ranks a list of sales contacts by their probability of buying, so the sales team calls first the people
most likely to buy.

**Result:** calling only the top-scored 20 % of the list reaches half of the buyers. Out of every 100 calls in that
band, 93 end in a sale, against 38 when calling at random.

```bash
pip install -r requirements.txt
python verificacion_metricas.py
jupyter notebook lead_scoring.ipynb
```

The script recomputes every figure on this page in a few seconds. The notebook holds the full analysis with its
charts and runs from start to finish.

## The problem

A company that gets customers online collects more contacts than its sales team can handle. This data holds 9,093
people who left their details on a form, and 37.6 % of them ended up buying. Calling in order of arrival spends the
same time on someone who was going to buy as on someone who landed there by mistake.

The model gives every contact a score between zero and one, and the list is sorted by it.

## The example

1,819 contacts the model never saw while learning were set aside, with 684 buyers among them. Sorted by the model's
score, the first 363 calls reach 338 of those buyers.

Two groups stand out for their conversion, measured over the whole file:
- contacts referred by another customer buy in 91.8 % of cases, over 534 contacts;
- working professionals buy in 91.6 % of cases, over 706.

## How it works

1. Text gaps are filled with «Desconocido» (unknown).
2. Every category becomes a column of zeros and ones.
3. 7,274 contacts are kept for learning and 1,819 for the exam, with the same share of buyers in both.
4. Numeric gaps are filled with the median of the learning set, so nothing from the exam leaks into training.
5. Three models are trained and compared on the exam.

| Model | AUC | F1 |
|---|---|---|
| Logistic regression | 0.8936 | 0.7422 |
| Random forest | 0.9147 | 0.7773 |
| **XGBoost** | **0.9210** | **0.7883** |

**AUC** measures how well the list is ordered: it is the probability that a random buyer gets a higher score than a
random non-buyer. A model scoring at random would get 0.50. **F1** sums up in one figure how many of the flagged
contacts really buy and how many buyers get flagged.

## Data

`Leads.csv` is the public *Lead Scoring · X Education* set from Kaggle, under a CC0 1.0 (public domain) licence. It
has 9,093 rows and 21 columns; the headers were translated into Spanish and the data was left untouched. The
analysis, the model and the verification are my own work.

## Limits

- Three of the columns record what happened during the sale, such as the last interaction or the score the sales
  rep gave. Without them, AUC drops to 0.875. The model ranks contacts already in progress and says less about
  someone who has just filled in the form.
- Small groups mislead: one occupation with 100 % conversion has only 10 contacts, which is why it is not among the
  recommendations.
- This is public data from a training company, with its own period and market. To use it elsewhere it would have to
  be trained on that company's sales and retrained every season.

## Files

| File | What it holds |
|---|---|
| `verificacion_metricas.py` | the program that recomputes the figures on this page |
| `lead_scoring.ipynb` | the full analysis, with its charts |
| `Leads.csv` | the data |
| `requirements.txt` | the libraries it needs |

## Related repositories

- [RFM-Customer-Analytics](https://github.com/jleonceo/RFM-Customer-Analytics): customer segmentation by recency,
  frequency and monetary value.
- [de-datos-en-bruto-a-decisiones](https://github.com/jleonceo/de-datos-en-bruto-a-decisiones): a raw sales file
  turned into business answers and a dashboard.
- [analisis-contable](https://github.com/jleonceo/analisis-contable): financial analysis of a company, from the
  ledger to the conclusions.

---

*Part of [Juan Luis León](https://github.com/jleonceo)'s portfolio · [juanluisleon.vercel.app](https://juanluisleon.vercel.app) · Licence [MIT](LICENSE)*
