import pdfplumber
import pandas as pd
import numpy as np
import re

def buscar_contas(filepath):
    pdf = pdfplumber.open(filepath)
    all_text = "".join(page.extract_text() for page in pdf.pages)
    pdf.close()

    text_split = all_text.split('\n')
    lines_contains_matricula = np.flatnonzero(np.core.defchararray.find(text_split, "MATRÍCULA") != -1)
    lines_contains_cidade = np.flatnonzero(np.core.defchararray.find(text_split, "Ligação") != -1)
    lines_contains_consumo = np.flatnonzero(np.core.defchararray.find(text_split, "Consumo Apurado no mês (m³) ") != -1)

    return text_split, lines_contains_matricula, lines_contains_cidade, lines_contains_consumo

def processar_dados(text_split, matricula_lines, cidade_lines, consumo_lines):
    dados = []

    for i in range(1, len(matricula_lines), 2):
        index = matricula_lines[i]
        l = text_split[index + 1]
        matricula = l.split(" ")[0]
        valor = l.split(" ")[4]
        dados.append([matricula, valor])

    for line, d in zip(cidade_lines, dados):
        l = text_split[line]
        cidade = l.split(" - ")[0].split("Ligação ")[1]
        d.append(cidade)

    for line, d in zip(consumo_lines, dados):
        l = text_split[line]
        consumo = l.split("Consumo Apurado no mês (m³) ")[1]
        d.append(consumo)

    return pd.DataFrame(dados, columns=['Matrícula', 'Valor', 'Cidade', 'Consumo'])

def formata_numeros(num):
    if not num:
        return None
    num = str(num).strip()
    alphas = set(('%$R°º()'))
    num = ''.join([c for c in num if c not in alphas])
    num_parts = re.split(',|\.', num)
    try:
        if len(num_parts) > 1:
            return float(''.join(num_parts[:-1]) + '.' + num_parts[-1])
        else:
            return int(''.join(num_parts))
    except ValueError:
        raise ValueError(f"Unable to convert '{num}' to a number")

def salvar_como_csv(data, output_csv):
    data['Valor'] = data['Valor'].apply(formata_numeros).astype(float)
    data.to_csv(output_csv, index=False)
    return output_csv
