import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
import pandas as pd
from datetime import datetime
import os
import configparser

class App(ttk.Window):
    
        
    def __init__(self, title="ttkbootstrap", themename="litera", iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, hdpi=True, scaling=None, transient=None, overrideredirect=False, alpha=1):
        super().__init__(title, themename, iconphoto, size, position, minsize, maxsize, resizable, hdpi, scaling, transient, overrideredirect, alpha)
        
        self.title('Integração TOTVS')
        self.geometry('600x400')
        
        self.create_widgets()
        
    def create_widgets(self):
        self.btn_carregar = ttk.Button(self, text='Carregar arquivo CSV', command=self.carregar_arquivo, bootstyle = 'primary')
        self.btn_carregar.pack(pady=10)
        
        #self.btn_separador = ttk.Menubutton(self, text='Selecione o separador')
        
        self.label_arquivo = ttk.Label(self, text='Nenhum arquivo selecionado', bootstyle='light')
        self.label_arquivo.pack(pady=5)
        
        self.btn_pasta = ttk.Button(self, text='Selecionar pasta de saída', command=self.selecionar_pasta, bootstyle='primary')
        self.btn_pasta.pack(pady=10)        
        
        self.label_pasta = ttk.Label(self, text='Nenhuma pasta selecionada', bootstyle='light')
        self.label_pasta.pack(pady=5)
        
        self.btn_processar = ttk.Button(self, text='Gerar arquivos', command=self.gerar_arquivos, bootstyle='success')
        self.btn_processar.pack(pady=20)
        
        
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
        
        with open (caminho_adiantamentos, 'w', encoding='utf-8') as f:
            
            for i in range(len(df)):
                adiantamento = df['ADIANTAMENTO'][i].strip()
                vendedor = df['VENDEDOR'][i].strip()
                
                if adiantamento in ['', '0', '0,00', '0.00'] or vendedor == vendedor_config:
                    continue
                                
                data = datetime.now().strftime('%d/%m/%Y')                
                valor_adt = df['ADIANTAMENTO'][i].replace('.', '').replace(',','.')
                valor_adt_formatado = f'{float(valor_adt):.2f}'.replace('.', ',')
                cod_historico = '1990'
                            
                linha = f'||{data}|{cnpj}|{conta_adt_deb}||{valor_adt_formatado}|D|{cod_historico}|{vendedor}|\n'
                linha += f'||{data}|{cnpj}|{conta_adt_cred}||{valor_adt_formatado}|C|{cod_historico}|{vendedor}|\n'
                
                f.write(linha)
                
        messagebox.showinfo('Sucesso', 'Arquivos gerados com sucesso!') 
                
if __name__ == "__main__":
    app = App()
    app.mainloop()
                