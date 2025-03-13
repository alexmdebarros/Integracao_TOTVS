import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
import pandas as pd
from datetime import datetime
import os
import configparser
import webbrowser

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        
        self.title('Integração TOTVS')
        self.resizable(False, False)
        self.geometry('600x400')
        
        self.create_widgets()
        
    def create_widgets(self):
        self.label_title = ttk.Label(self, text='Integração de Comissões com TOTVS', font='arial, 20')
        self.label_buttons = ttk.Label(self)
        self.btn_carregar = ttk.Button(self, text='Carregar arquivo CSV 🗂️', command=self.carregar_arquivo, bootstyle = 'primary')
        self.label_title.pack(pady=40)
        self.btn_carregar.pack(pady=10)       
                     
        self.label_arquivo = ttk.Label(self, text='Nenhum arquivo selecionado', bootstyle='light')
        self.label_arquivo.pack(pady=5)
        
        self.btn_pasta = ttk.Button(self, text='Selecionar pasta de saída 📁', command=self.selecionar_pasta, bootstyle='primary')
        self.btn_pasta.pack(pady=15)        
        
        self.label_pasta = ttk.Label(self, text='Nenhuma pasta selecionada', bootstyle='light')
        self.label_pasta.pack(pady=5)
        
        self.btn_processar = ttk.Button(self, text='Gerar arquivos ✅', command=self.gerar_arquivos, bootstyle='success')
        self.btn_processar.pack(pady=30)
        
        def abrir_link(event):
            webbrowser.open('https://github.com/alexmdebarros')
        
        def efeito_digitacao(texto, label, indice=0):            
            label.config(text=texto[:indice + 1])
            if indice < len(texto) - 1:
                label.after(120, efeito_digitacao, texto, label, indice + 1)
            
        self.label_creator = ttk.Label(self, text='', font=('Courier New', 8), cursor='hand2')
        self.after(800, efeito_digitacao, 'By - Alex', self.label_creator)
        self.label_creator.bind('<Button-2>', abrir_link)
        self.label_creator.place(relx=0.0, rely=1.0, anchor='sw', x=10, y=-10)
        
        
    def carregar_arquivo(self):
        arquivo = filedialog.askopenfilename(title='Selecione o arquivo CSV', filetypes=[('Arquivos CSV', '*.csv')])
        
        if arquivo:
            self.caminho_arquivo = arquivo
            self.label_arquivo.config(text=os.path.basename(arquivo))
            
    
    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title='Selecione a pastas de saída')
        
        if pasta:
            self.pasta_saida = pasta
            self.label_pasta.config(text=pasta)
            
            
    def gerar_arquivos(self):
        
        config = configparser.ConfigParser()
        config.read('config.txt')
        
        cnpj = config['config']['cnpj']
        conta_comissao_deb = config['config']['conta_deb_comissoes']
        conta_comissao_cred = config['config']['conta_cred_comissoes']
        conta_adt_deb = config['config']['conta_adt_deb']
        conta_adt_cred = config['config']['conta_adt_cred']
        vendedor_config = config['config']['vendedor']
        cod_historico_adt = config['config']['cod_hist_adt']
        
        if not hasattr(self, 'caminho_arquivo') or not hasattr(self, 'pasta_saida'):
            messagebox.showwarning('Aviso', 'Selecione um arquivo e uma pasta antes de continuar.')
            return
        
        df = pd.read_csv(self.caminho_arquivo, sep=';', encoding='latin1')
        
        caminho_comissoes = os.path.join(self.pasta_saida, 'comissoes.txt')
        caminho_adiantamentos = os.path.join(self.pasta_saida, 'adiantamento.txt')
        
        with open (caminho_comissoes, 'w', encoding='utf-8') as f:
            for i in range(len(df)):
                data = datetime.now().strftime('%d/%m/%Y')                
                valor = df['COMISSAO'][i].replace('.', '').replace(',','.')
                valor_formatado = f'{float(valor):.2f}'.replace('.', ',')
                cod_historico = df['COD_HIST'][i]
                
                linha = f'||{data}|{cnpj}|{conta_comissao_deb}||{valor_formatado}|D|{cod_historico}||\n'
                linha += f'||{data}|{cnpj}|{conta_comissao_cred}||{valor_formatado}|C|{cod_historico}||\n'
                
                f.write(linha)
            messagebox.showinfo('Sucesso', f'Arquivo {caminho_comissoes} gerado com sucesso!')
        
        with open (caminho_adiantamentos, 'w', encoding='utf-8') as f:
            
            for i in range(len(df)):
                adiantamento = df['ADIANTAMENTO'][i].strip()
                vendedor = df['VENDEDOR'][i].strip()
                
                if adiantamento in ['', '0', '0,00', '0.00'] or vendedor == vendedor_config:
                    continue
                                
                data = datetime.now().strftime('%d/%m/%Y')                
                valor_adt = df['ADIANTAMENTO'][i].replace('.', '').replace(',','.')
                valor_adt_formatado = f'{float(valor_adt):.2f}'.replace('.', ',')
                
                            
                linha = f'||{data}|{cnpj}|{conta_adt_deb}||{valor_adt_formatado}|D|{cod_historico_adt}|{vendedor}|\n'
                linha += f'||{data}|{cnpj}|{conta_adt_cred}||{valor_adt_formatado}|C|{cod_historico_adt}|{vendedor}|\n'
                
                f.write(linha)
                
            messagebox.showinfo('Sucesso', f'Arquivo {caminho_adiantamentos} gerado com sucesso!') 
                
if __name__ == "__main__":
    app = App()
    app.mainloop()
                