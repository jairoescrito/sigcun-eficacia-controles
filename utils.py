#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 17:41:40 2026

@author: jairoescrito
"""

import pandas as pd
import unicodedata
import re


def limpiar_texto(texto):
    if pd.isna(texto):
        return ""
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                    if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def limpiar_saltos(df):
    for col in df.select_dtypes(include='object').columns:
        df[col] = (df[col].astype(str)
                   .str.replace('\n', ' ')
                   .str.replace('\r', ' ')
                   .str.replace('"', ''))
    return df


def exportar_csv(df, ruta):
    limpiar_saltos(df).to_csv(
        ruta,
        index=False,
        encoding='utf-8-sig',
        sep='|'
    )


def calcular_residual(grupo, prob_inh, imp_inh):
    prob = prob_inh
    imp = imp_inh

    for _, row in grupo.iterrows():
        if row['tipo_control'] in ['Preventivo', 'Detectivo']:
            prob = prob * (1 - row['peso'])
        elif row['tipo_control'] == 'Correctivo':
            imp = imp * (1 - row['peso'])

    return round(prob, 4), round(imp, 4)


def etiqueta_prob(p):
    if p <= 0.2:
        return 'Muy Baja'
    elif p <= 0.4:
        return 'Baja'
    elif p <= 0.6:
        return 'Media'
    elif p <= 0.8:
        return 'Alta'
    else:
        return 'Muy Alta'


def etiqueta_imp(i):
    if i <= 0.2:
        return 'Leve'
    elif i <= 0.4:
        return 'Menor'
    elif i <= 0.6:
        return 'Moderado'
    elif i <= 0.8:
        return 'Mayor'
    else:
        return 'Catastrófico'


def zona_riesgo(prob, imp):
    p = etiqueta_prob(prob)
    i = etiqueta_imp(imp)
    bajo = [('Muy Baja', 'Leve'), ('Muy Baja', 'Menor'), ('Baja', 'Leve')]
    moderado = [('Muy baja', 'Moderado'), ('Baja', 'Menor'), ('Baja', 'Moderado'),
                ('Media', 'Leve'), ('Media', 'Menor'), ('Media', 'Moderado'),
                ('Alta', 'Leve'), ('Alta', 'Menor')]
    extremo = [('Muy Baja', 'Catastrófico'), ('Baja', 'Catastrófico'), ('Media', 'Catastrófico'),
               ('Alta', 'Catastrófico'), ('Muy Alta', 'Catastrófico')]
    if (p, i) in bajo:
        return 'Bajo'
    elif (p, i) in moderado:
        return 'Moderado'
    elif (p, i) in extremo:
        return 'Extremo'
    else:
        return 'Alto'
