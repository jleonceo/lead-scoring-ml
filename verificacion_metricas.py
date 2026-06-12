# -*- coding: utf-8 -*-
"""
Verificación de métricas — Lead Scoring
Replica la preparación y los modelos del notebook (mismos hiperparámetros,
mismo split: test 20%, random_state=42, estratificado) y reporta las métricas
sobre el conjunto de test. Las cifras del README salen de ejecutar este script.

Incluye además el experimento de robustez: AUC sin las variables generadas
durante el proceso comercial (ult_actividad, score_actividad, score_perfil),
para medir cuánto dependen las métricas de información del propio funnel.

Uso: python verificacion_metricas.py
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, f1_score
import xgboost as xgb

VARS_PROCESO = ['ult_actividad', 'score_actividad', 'score_perfil']


def prepara(df, excluir_proceso=False):
    d = df.copy()
    for c in ['ambito', 'ocupacion', 'fuente', 'ult_actividad']:
        d[c] = d[c].fillna('Desconocido')
    for c in ['visitas_total', 'paginas_vistas_visita', 'score_actividad', 'score_perfil']:
        d[c] = d[c].fillna(d[c].median())
    binarias = ['no_enviar_email', 'no_llamar', 'descarga_lm',
                'conociste_google', 'conociste_revista', 'conociste_periodico',
                'conociste_youtube', 'conociste_facebook', 'conociste_referencias']
    for c in binarias:
        d[c] = (d[c] == 'Yes').astype(int)
    cat = ['origen', 'fuente', 'ult_actividad', 'ambito', 'ocupacion']
    if excluir_proceso:
        d = d.drop(columns=VARS_PROCESO)
        cat = [c for c in cat if c not in VARS_PROCESO]
    return pd.get_dummies(d, columns=cat).drop(columns=['id'])


def split(d):
    X = d.drop(columns=['compra'])
    y = d['compra']
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def evalua(nombre, modelo, X_te, y_te, scaler=None):
    X_in = scaler.transform(X_te) if scaler else X_te
    auc = roc_auc_score(y_te, modelo.predict_proba(X_in)[:, 1])
    f1 = f1_score(y_te, modelo.predict(X_in))
    print(f"{nombre:<22} AUC-ROC: {auc:.4f}   F1: {f1:.4f}")
    return auc


if __name__ == '__main__':
    df = pd.read_csv('Leads.csv', sep=';')

    print("— Métricas sobre test (todas las variables) —")
    X_tr, X_te, y_tr, y_te = split(prepara(df))

    sc = StandardScaler()
    lr = LogisticRegression(max_iter=1000, random_state=42).fit(sc.fit_transform(X_tr), y_tr)
    evalua('Regresión Logística', lr, X_te, y_te, scaler=sc)

    rf = RandomForestClassifier(n_estimators=200, max_depth=10,
                                random_state=42, n_jobs=-1).fit(X_tr, y_tr)
    evalua('Random Forest', rf, X_te, y_te)

    xgb_m = xgb.XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05,
                              subsample=0.8, colsample_bytree=0.8,
                              eval_metric='logloss', random_state=42,
                              n_jobs=-1).fit(X_tr, y_tr)
    auc_full = evalua('XGBoost', xgb_m, X_te, y_te)

    print("\n— Robustez: sin variables del proceso comercial —")
    X_tr2, X_te2, y_tr2, y_te2 = split(prepara(df, excluir_proceso=True))
    xgb_2 = xgb.XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.05,
                              subsample=0.8, colsample_bytree=0.8,
                              eval_metric='logloss', random_state=42,
                              n_jobs=-1).fit(X_tr2, y_tr2)
    auc_sin = evalua('XGBoost (sin funnel)', xgb_2, X_te2, y_te2)
    print(f"\nAporte de las variables del funnel al AUC: {auc_full - auc_sin:+.4f}")
