import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Label
import os
from my_script import buscar_contas, processar_dados, salvar_como_csv

def selecionar_arquivos():
    filepaths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if filepaths:
        processar_arquivos(filepaths)

def processar_arquivos(filepaths):
    for filepath in filepaths:
        try:
            # Executar o pipeline para cada arquivo
            text_split, matricula_lines, cidade_lines, consumo_lines = buscar_contas(filepath)
            data = processar_dados(text_split, matricula_lines, cidade_lines, consumo_lines)
            
            # Gerar nome do arquivo de saída
            output_csv = gerar_nome_csv(filepath)
            salvar_como_csv(data, output_csv)
            
            messagebox.showinfo("Sucesso", f"Arquivo processado:\n{output_csv}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro com {os.path.basename(filepath)}:\n{e}")

def gerar_nome_csv(filepath):
    # Extrai o nome do arquivo original e muda para .csv
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_folder = os.path.dirname(filepath)  # Salva no mesmo diretório do PDF
    return os.path.join(output_folder, f"{base_name}.csv")

# Criar a janela principal
root = tk.Tk()
root.title("Processador de Contas UFRB - Multi Arquivos")

# Elementos da interface
instruction_label = Label(root, text="Selecione um ou mais arquivos PDF para processar:")
instruction_label.pack(pady=10)

select_btn = Button(root, text="Selecionar Arquivos PDF", command=selecionar_arquivos)
select_btn.pack(pady=10)

exit_btn = Button(root, text="Sair", command=root.quit)
exit_btn.pack(pady=10)

# Rodar a interface
root.mainloop()
