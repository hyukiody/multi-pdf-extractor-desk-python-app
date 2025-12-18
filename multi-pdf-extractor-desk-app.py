"""
Multi-PDF Extractor Desktop Application

A tkinter-based GUI application for processing multiple PDF utility bills,
extracting data, and generating CSV files and visual summaries.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Label
import os
from my_script import buscar_contas, processar_dados, salvar_como_csv, gerar_tabela

def selecionar_arquivos():
    """
    Open file dialog to select multiple PDF files for processing.
    
    Updates the GUI with selected file paths and enables the confirm button.
    """
    filepaths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if filepaths:
        selected_files_label.config(text="\n".join(filepaths))
        confirm_btn.config(state=tk.NORMAL)
        global selected_filepaths
        selected_filepaths = filepaths

def confirmar_processamento():
    """
    Trigger the processing of selected PDF files.
    """
    processar_arquivos(selected_filepaths)

def processar_arquivos(filepaths):
    """
    Process each selected PDF file through the extraction pipeline.
    
    For each file, extracts data, creates output folder, generates CSV and visualization.
    Shows success or error messages for each file processed.
    
    Args:
        filepaths (tuple): Paths to PDF files to process
    """
    for filepath in filepaths:
        try:
            # Execute the pipeline for each file
            text_split, matricula_lines, cidade_lines, consumo_lines = buscar_contas(filepath)
            data = processar_dados(text_split, matricula_lines, cidade_lines, consumo_lines)

            # Generate output file name
            output_folder = gerar_nome_csv(filepath)
            salvar_como_csv(data, os.path.join(output_folder, "output.csv"))
            gerar_tabela(data, os.path.join(output_folder, "tabela.png"))

            messagebox.showinfo("Success", f"File processed:\n{output_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred with {os.path.basename(filepath)}:\n{e}")

def gerar_nome_csv(filepath):
    """
    Generate output folder path based on the input PDF filename.
    
    Creates a folder with the same name as the PDF file (without extension)
    in the same directory as the input file.
    
    Args:
        filepath (str): Path to the input PDF file
        
    Returns:
        str: Path to the output folder
    """
    # Extract original filename and create a new folder
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_folder = os.path.join(os.path.dirname(filepath), base_name)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

# Create main window
root = tk.Tk()
root.title("Multi-PDF Bill Processor")

# Interface elements
instruction_label = Label(root, text="Select one or more PDF files to process:")
instruction_label.pack(pady=10)

select_btn = Button(root, text="Select PDF Files", command=selecionar_arquivos)
select_btn.pack(pady=10)

selected_files_label = Label(root, text="", wraplength=400)
selected_files_label.pack(pady=10)

confirm_btn = Button(root, text="Confirm Processing", command=confirmar_processamento, state=tk.DISABLED)
confirm_btn.pack(pady=10)

exit_btn = Button(root, text="Exit", command=root.quit)
exit_btn.pack(pady=10)

# Run the interface
root.mainloop()