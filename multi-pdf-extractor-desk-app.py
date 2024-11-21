import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Button, Label
import os
from my_script import buscar_contas, processar_dados, salvar_como_csv, gerar_tabela

def selecionar_arquivos():
    filepaths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    if filepaths:
        selected_files_label.config(text="\n".join(filepaths))
        confirm_btn.config(state=tk.NORMAL)
        global selected_filepaths
        selected_filepaths = filepaths

def confirmar_processamento():
    processar_arquivos(selected_filepaths)

def processar_arquivos(filepaths):
    for filepath in filepaths:
        try:
            # Executar o pipeline para cada arquivo
            text_split, matricula_lines, cidade_lines, consumo_lines = buscar_contas(filepath)
            data = processar_dados(text_split, matricula_lines, cidade_lines, consumo_lines)

            # Gerar nome do arquivo de saída
            output_folder = gerar_nome_csv(filepath)
            salvar_como_csv(data, os.path.join(output_folder, "output.csv"))
            gerar_tabela(data, os.path.join(output_folder, "tabela.png"))

            messagebox.showinfo("Sucesso", f"Arquivo processado:\n{output_folder}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro com {os.path.basename(filepath)}:\n{e}")

def gerar_nome_csv(filepath):
    # Extrai o nome do arquivo original e cria uma nova pasta
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_folder = os.path.join(os.path.dirname(filepath), base_name)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

# Criar a janela principal
root = tk.Tk()
root.title("Processador de Contas UFRB - Multi Arquivos")

# Elementos da interface
instruction_label = Label(root, text="Selecione um ou mais arquivos PDF para processar:")
instruction_label.pack(pady=10)

select_btn = Button(root, text="Selecionar Arquivos PDF", command=selecionar_arquivos)
select_btn.pack(pady=10)

selected_files_label = Label(root, text="", wraplength=400)
selected_files_label.pack(pady=10)

confirm_btn = Button(root, text="Confirmar Processamento", command=confirmar_processamento, state=tk.DISABLED)
confirm_btn.pack(pady=10)

exit_btn = Button(root, text="Sair", command=root.quit)
exit_btn.pack(pady=10)

# Rodar a interface
root.mainloop()