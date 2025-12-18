"""
Multi-PDF Data Extraction Module

This module provides functions for extracting and processing data from PDF utility bills,
including data extraction, formatting, CSV export, and visualization generation.
"""

import pdfplumber
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from pandas.plotting import table

def buscar_contas(filepath):
    """
    Extract relevant data lines from a PDF utility bill.
    
    Args:
        filepath (str): Path to the PDF file to process
        
    Returns:
        tuple: Contains:
            - text_split (list): All text lines from the PDF
            - lines_contains_matricula (ndarray): Indices of lines containing matriculation numbers
            - lines_contains_cidade (ndarray): Indices of lines containing city information
            - lines_contains_consumo (ndarray): Indices of lines containing consumption data
    """
    pdf = pdfplumber.open(filepath)
    all_text = "".join(page.extract_text() for page in pdf.pages)
    pdf.close()

    text_split = all_text.split('\n')
    lines_contains_matricula = np.flatnonzero(np.core.defchararray.find(text_split, "MATRÍCULA") != -1)
    lines_contains_cidade = np.flatnonzero(np.core.defchararray.find(text_split, "Ligação") != -1)
    lines_contains_consumo = np.flatnonzero(np.core.defchararray.find(text_split, "Consumo Apurado no mês (m³) ") != -1)

    return text_split, lines_contains_matricula, lines_contains_cidade, lines_contains_consumo

def processar_dados(text_split, matricula_lines, cidade_lines, consumo_lines):
    """
    Process extracted data lines and organize into a structured DataFrame.
    
    Args:
        text_split (list): All text lines from the PDF
        matricula_lines (ndarray): Indices of lines containing matriculation numbers
        cidade_lines (ndarray): Indices of lines containing city information
        consumo_lines (ndarray): Indices of lines containing consumption data
        
    Returns:
        pandas.DataFrame: Structured data with columns: Matrícula, Valor, Cidade, Consumo
    """
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
    """
    Format and convert string numbers to float values.
    
    Removes currency symbols, handles different decimal separators,
    and converts to proper float format.
    
    Args:
        num (str or numeric): Number string to format
        
    Returns:
        float: Formatted number rounded to 3 decimal places
        None: If input is empty
        
    Raises:
        ValueError: If the string cannot be converted to a number
    """
    if not num:
        return None
    num = str(num).strip()
    alphas = set(('%$R°º()'))
    num = ''.join([c for c in num if c not in alphas])
    num_parts = re.split(r',|\.', num)
    try:
        if len(num_parts) > 1:
            return round(float(''.join(num_parts[:-1]) + '.' + num_parts[-1]), 3)
        else:
            return round(int(''.join(num_parts)), 3)
    except ValueError:
        raise ValueError(f"Unable to convert '{num}' to a number")

def salvar_como_csv(data, output_csv):
    """
    Save processed data to a CSV file.
    
    Args:
        data (pandas.DataFrame): Data to save
        output_csv (str): Output file path for the CSV
        
    Returns:
        str: Path to the saved CSV file
    """
    data['Valor'] = data['Valor'].apply(formata_numeros).astype(float)
    data.to_csv(output_csv, index=False)
    return output_csv


def gerar_tabela(data, output_png):
    """
    Generate a visual summary table from the data grouped by city.
    
    Creates a PNG image containing a formatted table showing
    total values grouped by city.
    
    Args:
        data (pandas.DataFrame): Data to visualize
        output_png (str): Output file path for the PNG image
    """
    data['Valor'] = data['Valor'].apply(formata_numeros).astype(float)
    grouped_data = data.groupby(['Cidade'])['Valor'].sum().reset_index()
    grouped_data['Valor'] = grouped_data['Valor'].apply(lambda x: f"{x:.3f}")
    fig, ax = plt.subplots(figsize=(10, 4)) # set size frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
    tabla = table(ax, grouped_data, loc='center', colWidths=[0.1]*len(grouped_data.columns))  # where df is your data frame
    tabla.auto_set_font_size(True) # Activate set fontsize manually
    tabla.set_fontsize(12) # if ++fontsize is necessary ++colWidths
    tabla.scale(2.2, 2.2) # change size table
    plt.savefig(output_png)
    plt.close()