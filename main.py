from tkinter import *
from tkinter import ttk
import sqlite3 as sq
from datetime import date
import re

root = Tk()

#Variáveis Clientes
id_visual_Cli = StringVar()
nome_cliente_visual_Cli = StringVar()
telefone_visual_Cli = StringVar()
email_visual_Cli = StringVar()
data_contato_visual_Cli = StringVar()
data_cadastro_visual_Cli = StringVar()
id_edit_Cli = -1
nome_cliente_edit_Cli = ""
telefone_edit_Cli = ""
email_edit_Cli = ""

#Variáveis Serviços
id_servico_visual_Ser = StringVar()
id_visual_Ser = StringVar()
descricao_visual_Ser = StringVar()
tipo_servico_visual_Ser = StringVar()
status_visual_Ser = StringVar()
data_criacao_visual_Ser = StringVar()
nome_cliente_Ser = StringVar()
nome_cliente_Ser_T = False
id_servico_edit_Ser = -1
id_edit_Ser = id_edit_Cli
descricao_edit_Ser = ""
tipo_servico_edit_Ser = ""
status_edit_Ser = ""
data_criacao_edit_Ser = ""
value_status_servico_unic_bbt_edit = StringVar()

#Variáveis de Error Clientes
error_data_contato_Cli = StringVar()
error_telefone_Cli = StringVar()
error_nome_cliente_Cli = StringVar()
error_email_Cli = StringVar()
error_telefone_edit_Cli = StringVar()
error_nome_cliente_edit_Cli = StringVar()
error_email_edit_Cli = StringVar()

#Variáveis de Error Serviços
error_id_Ser = StringVar()
error_tipo_servico_Ser = StringVar()
error_descricao_Ser = StringVar()
error_tipo_servico_edit_Ser = StringVar()
error_descricao_edit_Ser = StringVar()

class Funcoes():
    #Bancos de Dados
    def conectar_bd(self):
        self.con = sq.connect("sistema.db")
        self.con.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.con.cursor()
    def desconectar_bd(self):
        self.con.close()
    def montar_Tabelas(self):
        self.conectar_bd()
        #Criar tabela clientes
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
                            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome_cliente TEXT NOT NULL,
                            telefone TEXT NOT NULL CHECK
                                (length(telefone) = 11),
                            email TEXT NOT NULL CHECK
                                (email LIKE '%@%.%'),
                            data_cadastro TEXT NOT NULL,
                            data_contato TEXT CHECK
                                (data_contato IS NULL
                                OR length(data_contato) = 8)
                            );""")
        #Criar tabela serviço
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS servicos (
                            id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
                            id_cliente INTEGER NOT NULL,
                            tipo_servico TEXT NOT NULL,
                            descricao TEXT NOT NULL,
                            status TEXT NOT NULL,
                            data_criacao TEXT NOT NULL,
                            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
                            );""")
        self.con.commit()
        self.desconectar_bd()
    #Funções de mudança de tela
    def entrar_tela2(self):
        self.frame_1.place_forget()
        self.frame_2.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.preencher_lista_Cli()
    def sair_tela2(self):
        self.frame_2.place_forget()
        self.frame_1.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.pesquisar_C.delete(0, END)
    def entrar_tela3(self):
        self.frame_2.place_forget()
        self.frame_3.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.pesquisar_C.delete(0, END)
    def sair_tela3(self):
        self.frame_3.place_forget()
        self.frame_2.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.entry_nome_cliente_C.delete(0, END)
        self.entry_telefone_C.delete(0, END)
        self.entry_email_C.delete(0, END)
        self.entry_data_contato_C.delete(0, END)
        error_data_contato_Cli.set(value="")
        error_telefone_Cli.set(value="")
        error_nome_cliente_Cli.set(value="")
        error_email_Cli.set(value="")
    def sair_tela4(self):
        self.frame_4.place_forget()
        self.frame_2.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
    def entrar_tela5(self):
        self.frame_4.place_forget()
        self.frame_5.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.entry_telefone_edit_C.insert(END, telefone_edit_Cli)
        self.entry_nome_cliente_edit_C.insert(END, nome_cliente_edit_Cli)
        self.entry_email_edit_C.insert(END, email_edit_Cli)
    def sair_tela5(self):
        self.frame_5.place_forget()
        self.frame_4.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.entry_telefone_edit_C.delete(0, END)
        self.entry_nome_cliente_edit_C.delete(0, END)
        self.entry_email_edit_C.delete(0, END)
        error_telefone_edit_Cli.set(value="")
        error_nome_cliente_edit_Cli.set(value="")
        error_email_edit_Cli.set(value="")
    def entrar_tela6(self):
        self.frame_1.place_forget()
        self.frame_6.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.preencher_lista_Ser()
    def sair_tela6(self):
        self.frame_6.place_forget()
        self.frame_1.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.pesquisar_S.delete(0, END)
    def entrar_tela7(self):
        self.frame_6.place_forget()
        self.frame_7.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.pesquisar_S.delete(0, END)
    def sair_tela7(self):
        self.frame_7.place_forget()
        self.frame_6.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.limpar_entry_S()
    def sair_tela8(self):
        self.frame_8.place_forget()
        self.frame_6.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
    def entrar_tela9(self):
        global value_status_servico_unic_bbt_edit
        self.frame_8.place_forget()
        self.frame_9.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        value_status_servico_unic_bbt_edit.set(value=status_edit_Ser)
        self.entry_tipo_servico_edit_S.insert(END, tipo_servico_edit_Ser)
        self.entry_descricao_edit_S.insert(END, descricao_edit_Ser)
    def sair_tela9(self):
        self.frame_9.place_forget()
        self.frame_8.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.entry_tipo_servico_edit_S.delete(0, END)
        self.entry_descricao_edit_S.delete(0, END)
    #Função do botão de multipla escolha da pesquisa
    def bbt_pesquisa_mudou(self):
        self.bbt_pesquisa_selecionado = self.value_unic_bbt.get()
        if self.bbt_pesquisa_selecionado== "ID":
            self.bbt_pesquisa_selecionado = "id_cliente"
        elif self.bbt_pesquisa_selecionado== "Nome":
            self.bbt_pesquisa_selecionado = "nome_cliente"
        elif self.bbt_pesquisa_selecionado== "Telefone":
            self.bbt_pesquisa_selecionado = "telefone"
        elif self.bbt_pesquisa_selecionado== "Email":
            self.bbt_pesquisa_selecionado = "email"
        elif self.bbt_pesquisa_selecionado== "Data do Cadastro":
            self.bbt_pesquisa_selecionado = "data_cadastro"
        return self.bbt_pesquisa_selecionado
    #Funções de preencher a tabela
    def preencher_lista_Cli(self):
        self.listaCli.delete(*self.listaCli.get_children())
        textopesqentry = self.pesquisar_C.get().strip()
        colunaCli = self.bbt_pesquisa_mudou()
        self.conectar_bd()
        if textopesqentry== "":
            self.cursor.execute("""SELECT id_cliente, nome_cliente, telefone, email, data_cadastro FROM clientes
                                        ORDER BY nome_cliente ASC; """)
        else:
            if colunaCli == "id_cliente":
                if not textopesqentry.isdigit():
                    self.desconectar_bd()
                    return
                self.cursor.execute("""SELECT id_cliente, nome_cliente, telefone, email, data_cadastro FROM clientes
                                    WHERE id_cliente = ?""", (textopesqentry,))
            else:
                self.cursor.execute(f"""SELECT id_cliente, nome_cliente, telefone, email, data_cadastro FROM clientes
                                    WHERE {colunaCli} LIKE ?
                                    ORDER BY nome_cliente ASC""", (f"%{textopesqentry}%",))
        for i in self.cursor.fetchall():
            i = list(i)
            i[2] = f"({i[2][:2]}) {i[2][2:7]}-{i[2][7:]}"
            self.listaCli.insert("", END, values=i)
        self.desconectar_bd()
    #Função da pesquisa dinamica na aba Clientes
    def pesquisar_dinamico_Cli(self, event=None):
        self.preencher_lista_Cli()
    #Função de limpar os Entrys do editar clientes
    def limpar_entry_C(self):
        self.entry_nome_cliente_C.delete(0, END)
        self.entry_telefone_C.delete(0, END)
        self.entry_email_C.delete(0, END)
        self.entry_data_contato_C.delete(0, END)
    #Função de Cadastrar um cliente
    def add_cliente_C(self):
        self.padronizar_email_Cli()
        self.verif_error_entrys_cadastro_Cli()
        self.nome_cliente_Cli = self.entry_nome_cliente_C.get()
        self.telefone_Cli = self.entry_telefone_C.get()
        self.telefone_limpo_Cli = ''.join(filter(str.isdigit, self.telefone_Cli))
        self.email_Cli = self.entry_email_C.get()
        self.data_contato_Cli = self.entry_data_contato_C.get()
        if self.data_contato_Cli== "":
            self.data_contato_limpo_Cli = None
        else:
            self.data_contato_limpo_Cli = ''.join(filter(str.isdigit, self.data_contato_Cli))
        self.data_cadastro_Cli = date.today()
        self.conectar_bd()
        if self.nome_cliente_Cli!="":
            if error_email_Cli.get()== "" and error_data_contato_Cli.get()== "":
                self.cursor.execute("""INSERT INTO clientes (nome_cliente, telefone, email, data_cadastro, data_contato)
                                VALUES (?,?,?,?,?); """, (self.nome_cliente_Cli, self.telefone_limpo_Cli, self.email_Cli, self.data_cadastro_Cli, self.data_contato_limpo_Cli))
                self.limpar_entry_C()
                self.cliente_cadastrado_confirm()
        self.con.commit()
        self.desconectar_bd()
        self.preencher_lista_Cli()
    #Função de Duplo Click
    def DuploClickOnCli(self):
        global nome_cliente_edit_Cli, telefone_edit_Cli, email_edit_Cli, id_edit_Cli
        self.frame_2.place_forget()
        self.frame_4.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.listaCli.selection()
        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5 = self.listaCli.item(n, "values")
            id_visual_Cli.set(col1)
            nome_cliente_visual_Cli.set(col2)
            telefone_visual_Cli.set(col3)
            email_visual_Cli.set(col4)
            data_cadastro_visual_Cli.set(col5)
            id_edit_Cli = col1
            nome_cliente_edit_Cli = col2
            telefone_edit_Cli = col3
            email_edit_Cli = col4
        self.conectar_bd()
        self.cursor.execute("""SELECT data_contato FROM clientes
                                WHERE id_cliente = ?; """, (id_edit_Cli,))
        data_contato_cliente = self.cursor.fetchone()
        self.desconectar_bd()
        if data_contato_cliente[0] is None:
            data_contato_visual_Cli.set("Não informado")
        else:
            data_contato_n = data_contato_cliente[0]
            data_contato_formatada = f"{data_contato_n[:4]}-{data_contato_n[4:6]}-{data_contato_n[6:]}"
            data_contato_visual_Cli.set(data_contato_formatada)
    #Função que garante que foi clicado 2 vezes em um cliente
    def DuploClickItemOnCli(self, event):
        self.mouseCli = event.widget
        self.regiaoCli = self.mouseCli.identify("region", event.x, event.y)
        if self.regiaoCli != "cell":
            return
        self.itemCli = self.mouseCli.identify_row(event.y)
        if not self.itemCli:
            return
        self.DuploClickOnCli()
    #Função de Deletar cliente
    def deletar_Cli(self):
        global id_edit_Cli
        self.conectar_bd()
        self.cursor.execute("""DELETE FROM servicos WHERE id_cliente = ? """, (id_edit_Cli,))
        self.cursor.execute("""DELETE FROM clientes WHERE id_cliente = ? """, (id_edit_Cli,))
        self.con.commit()
        self.desconectar_bd()
        self.limpar_entry_C()
        self.preencher_lista_Cli()
        self.tela_confirmar_deletar.destroy()
        self.sair_tela4()
    #Função de confrimação para deletar cliente
    def confirmar_deletar_Cli(self):
        self.tela_confirmar_deletar = Toplevel(self.root)
        self.tela_confirmar_deletar.title("Confirmação")
        self.tela_confirmar_deletar.geometry("300x150")
        self.tela_confirmar_deletar.resizable(False, False)
        self.tela_confirmar_deletar.transient(self.root)
        self.tela_confirmar_deletar.grab_set()
        Label(self.tela_confirmar_deletar, text="Você realmente quer apagar esse cliente?").place(x=30,y=30)
        bt_apagar_sim = Button(self.tela_confirmar_deletar, text="Sim", bg="#1AFF00", command=self.deletar_Cli)
        bt_apagar_sim.place(x=70, y=80, width=60, height=30)

        bt_apagar_nao = Button(self.tela_confirmar_deletar, text="Não", bg="#FF0000", command=self.tela_confirmar_deletar.destroy)
        bt_apagar_nao.place(x=170, y=80, width=60, height=30)
        self.root.wait_window(self.tela_confirmar_deletar)
    #Função de Alterar informações do cliente
    def alterar_inf_Cli(self):
        self.padronizar_email_edit_Cli()
        self.verif_error_entrys_edit_Cli()
        global id_edit_Cli, telefone_edit_Cli, nome_cliente_edit_Cli, email_edit_Cli
        self.nome_cliente_Cli = self.entry_nome_cliente_edit_C.get()
        self.telefone_Cli = self.entry_telefone_edit_C.get()
        self.telefone_limpo_Cli = ''.join(filter(str.isdigit, self.telefone_Cli))
        self.email_Cli = self.entry_email_edit_C.get()
        self.conectar_bd()
        if error_email_edit_Cli.get()== "" and error_nome_cliente_edit_Cli.get()== "" and error_telefone_edit_Cli.get()== "":
            self.cursor.execute("""UPDATE clientes SET nome_cliente = ?, telefone = ?, email = ?
                                WHERE id_cliente = ?""", (self.nome_cliente_Cli, self.telefone_limpo_Cli, self.email_Cli, id_edit_Cli,))
            self.limpar_entry_C()
            self.sair_tela5()
            self.cliente_editado_confirm()
            telefone_edit_Cli = self.telefone_Cli
            nome_cliente_edit_Cli = self.nome_cliente_Cli
            email_edit_Cli = self.email_Cli
        self.con.commit()
        self.desconectar_bd()
        self.preencher_lista_Cli()
        nome_cliente_visual_Cli.set(self.nome_cliente_Cli)
        telefone_visual_Cli.set(self.telefone_Cli)
        email_visual_Cli.set(self.email_Cli)
    #Função para formatar Telefone no cadastro de clientes
    def formatar_telefone_Cli(self, event=None):
        formatacao_telefone = self.entry_telefone_C.get()
        self.num_telefone = re.sub(r"\D", "", formatacao_telefone)[:11]
        if len(self.num_telefone) <= 2:
            telefone_formatado = f"{self.num_telefone}"
        elif len(self.num_telefone) <= 7:
            telefone_formatado = f"({self.num_telefone[:2]}) {self.num_telefone[2:]}"
        else:
            telefone_formatado = f"({self.num_telefone[:2]}) {self.num_telefone[2:7]}-{self.num_telefone[7:]}"
        self.entry_telefone_C.delete(0, END)
        self.entry_telefone_C.insert(0, telefone_formatado)
    #Função para formatar Telefone no edit de clientes
    def formatar_telefone_edit_Cli(self, event=None):
        formatacao_telefone_edit = self.entry_telefone_edit_C.get()
        self.num_telefone_edit = re.sub(r"\D", "", formatacao_telefone_edit)[:11]
        if len(self.num_telefone_edit) <= 2:
            telefone_formatado = f"{self.num_telefone_edit}"
        elif len(self.num_telefone_edit) <= 7:
            telefone_formatado = f"({self.num_telefone_edit[:2]}) {self.num_telefone_edit[2:]}"
        else:
            telefone_formatado = f"({self.num_telefone_edit[:2]}) {self.num_telefone_edit[2:7]}-{self.num_telefone_edit[7:]}"
        self.entry_telefone_edit_C.delete(0, END)
        self.entry_telefone_edit_C.insert(0, telefone_formatado)
    #Função para formatar Data de Contato no cadastro de clientes
    def formatar_data_contato_Cli(self, event=None):
        formatacao_data_contato = self.entry_data_contato_C.get()
        self.num_data_contato = re.sub(r"\D", "", formatacao_data_contato)[:8]
        if len(self.num_data_contato) <= 4:
            data_contato_formatado = f"{self.num_data_contato}"
        elif len(self.num_data_contato) <= 6:
            data_contato_formatado = f"{self.num_data_contato[:4]}-{self.num_data_contato[4:]}"
        else:
            data_contato_formatado = f"{self.num_data_contato[:4]}-{self.num_data_contato[4:6]}-{self.num_data_contato[6:]}"
        self.entry_data_contato_C.delete(0, END)
        self.entry_data_contato_C.insert(0, data_contato_formatado)
    #Função que garante o formato correto do email no cadastro de clientes
    def padronizar_email_Cli(self):
        padronizacao_email = self.entry_email_C.get().strip()
        padrao_email = r'^[\w\.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$'
        if padronizacao_email== "":
            error_email_Cli.set(value="Este campo deve estar preenchido")
        elif not re.fullmatch(padrao_email, padronizacao_email):
            error_email_Cli.set(value="Email inválido! Digite no formato correto (Exemplo: teste@gmail.com)")
        else:
            error_email_Cli.set(value="")
    #Função que garante o formato correto do email no edit de clientes
    def padronizar_email_edit_Cli(self):
        padronizacao_edit_email = self.entry_email_edit_C.get().strip()
        padrao_email = r'^[\w\.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$'
        if padronizacao_edit_email== "":
            error_email_edit_Cli.set(value="Este campo deve estar preenchido")
        elif not re.fullmatch(padrao_email, padronizacao_edit_email):
            error_email_edit_Cli.set(value="Email inválido! Digite no formato correto (Exemplo: teste@gmail.com)")
        else:
            error_email_edit_Cli.set(value="")
    #Função para verificar se ocorreu algum erro nos Entrys do cadastro de clientes
    def verif_error_entrys_cadastro_Cli(self):
        if len(self.num_data_contato) > 0 and len(self.num_data_contato) < 8:
            error_data_contato_Cli.set(value="Este campo não está devidamente preenchido")
        else:
            error_data_contato_Cli.set(value="")
        
        formatacao_telefone = self.entry_telefone_C.get()
        self.num_telefone = re.sub(r"\D", "", formatacao_telefone)[:11]
        if self.entry_telefone_C.get()== "":
            error_telefone_Cli.set(value="Este campo deve estar preenchido")
        elif len(self.num_telefone) < 11:
            error_telefone_Cli.set(value="Este campo não está devidamente preenchido")
        else:
            error_telefone_Cli.set(value="")

        if self.entry_nome_cliente_C.get()== "":
            error_nome_cliente_Cli.set(value="Este campo deve estar preenchido")
        else:
            error_nome_cliente_Cli.set(value="")
    #Função para verificar se ocorreu algum erro nos Entrys do edit de clientes
    def verif_error_entrys_edit_Cli(self):
        formatacao_telefone_edit = self.entry_telefone_edit_C.get()
        self.num_telefone_edit = re.sub(r"\D", "", formatacao_telefone_edit)[:11]
        if self.entry_telefone_edit_C.get()== "":
            error_telefone_edit_Cli.set(value="Este campo deve estar preenchido")
        elif len(self.num_telefone_edit) < 11:
            error_telefone_edit_Cli.set(value="Este campo não está devidamente preenchido")
        else:
            error_telefone_edit_Cli.set(value="")

        if self.entry_nome_cliente_edit_C.get()== "":
            error_nome_cliente_edit_Cli.set(value="Este campo deve estar preenchido")
        else:
            error_nome_cliente_edit_Cli.set(value="")
    #Função para mostrar que o cliente foi cadastrado
    def cliente_cadastrado_confirm(self):
        if self.cliente_cadastrado_C is not None and self.cliente_cadastrado_C.winfo_exists():
            self.cliente_cadastrado_C.destroy()
        self.cliente_cadastrado_C = Label(self.frame_3, text="Cliente Cadastrado!", bg="#dfe3ee", fg="#2bff00", font=("arial", 12, "bold"))
        self.cliente_cadastrado_C.place(relx=0.35, rely=0.15, relwidth=0.3)
        self.root.after(4000, self.esconder_cliente_cadastrado)
    #Função para esconder que o cliente foi cadastrado
    def esconder_cliente_cadastrado(self):
        if self.cliente_cadastrado_C is not None and self.cliente_cadastrado_C.winfo_exists():
            self.cliente_cadastrado_C.destroy()
            self.cliente_cadastrado_C = None
    #Função para mostrar que o cliente foi editado
    def cliente_editado_confirm(self):
        if self.cliente_editado_C is not None and self.cliente_editado_C.winfo_exists():
            self.cliente_editado_C.destroy()
        self.cliente_editado_C = Label(self.frame_4, text="Informações Editadas!", bg="#dfe3ee", fg="#2bff00", font=("arial", 12, "bold"))
        self.cliente_editado_C.place(relx=0.35, rely=0.15, relwidth=0.3)
        self.root.after(4000, self.esconder_cliente_editado)
    #Função para esconder que o cliente foi editado
    def esconder_cliente_editado(self):
        if self.cliente_editado_C is not None and self.cliente_editado_C.winfo_exists():
            self.cliente_editado_C.destroy()
            self.cliente_editado_C = None
#Funções do Serviço
    #Função do botão de multipla escolha da pesquisa de Serviços
    def bbt_pesquisa_2_mudou(self):
        self.bbt_pesquisa_2_selecionado = self.value_servico_unic_bbt.get()
        if self.bbt_pesquisa_2_selecionado== "ID de Serviço":
            self.bbt_pesquisa_2_selecionado = "id_servico"
        elif self.bbt_pesquisa_2_selecionado== "ID":
            self.bbt_pesquisa_2_selecionado = "id_cliente"
        elif self.bbt_pesquisa_2_selecionado== "Serviço":
            self.bbt_pesquisa_2_selecionado = "tipo_servico"
        elif self.bbt_pesquisa_2_selecionado== "Status":
            self.bbt_pesquisa_2_selecionado = "status"
        elif self.bbt_pesquisa_2_selecionado== "Data de Criação":
            self.bbt_pesquisa_2_selecionado = "data_criacao"
        return self.bbt_pesquisa_2_selecionado
    #Funções de preencher a tabela
    def preencher_lista_Ser(self):
        self.listaSer.delete(*self.listaSer.get_children())
        textopesqentry2 = self.pesquisar_S.get().strip()
        colunaSer = self.bbt_pesquisa_2_mudou()
        self.conectar_bd()
        if textopesqentry2== "":
            self.cursor.execute("""SELECT id_servico, id_cliente, tipo_servico, status, data_criacao FROM servicos
                                        ORDER BY id_servico ASC; """)
        else:
            if colunaSer == "id_servico":
                if not textopesqentry2.isdigit():
                    self.desconectar_bd()
                    return
                self.cursor.execute("""SELECT id_servico, id_cliente, tipo_servico, status, data_criacao FROM servicos
                                    WHERE id_servico = ?""", (textopesqentry2,))
            else:
                self.cursor.execute(f"""SELECT id_servico, id_cliente, tipo_servico, status, data_criacao FROM servicos
                                    WHERE {colunaSer} LIKE ?
                                    ORDER BY id_servico ASC""", (f"%{textopesqentry2}%",))
        for i in self.cursor.fetchall():
            self.listaSer.insert("", END, values=i)
        self.desconectar_bd()
    #Função da pesquisa dinamica na aba Serviços
    def pesquisar_dinamico_Ser(self, event=None):
        self.preencher_lista_Ser()
    #Função de limpar os Entrys do editar clientes
    def limpar_entry_S(self):
        self.entry_id_S.delete(0, END)
        self.entry_descricao_S.delete(0, END)
        self.entry_tipo_servico_S.delete(0, END)
        self.lb2_nome_cliente_S.place_forget()
        self.id_passado_S = ""
    #Função de Cadastrar um cliente
    def add_servico_S(self):
        self.verif_error_entrys_cadastro_Ser()
        self.id_Ser = self.entry_id_S.get()
        self.descricao_Ser = self.entry_descricao_S.get()
        self.tipo_servico_Ser = self.entry_tipo_servico_S.get()
        self.status_Ser = self.value_status_servico_unic_bbt.get()
        self.data_criacao_Ser = date.today()
        self.conectar_bd()
        if error_id_Ser.get()== "" and error_tipo_servico_Ser.get()== "" and error_descricao_Ser.get()== "":
            self.cursor.execute("""INSERT INTO servicos (id_cliente, tipo_servico, descricao, status, data_criacao)
                                VALUES (?,?,?,?,?); """, (self.id_Ser, self.tipo_servico_Ser, self.descricao_Ser, self.status_Ser, self.data_criacao_Ser))
            self.limpar_entry_S()
            self.servico_cadastrado_confirm()
        self.con.commit()
        self.desconectar_bd()
        self.preencher_lista_Ser()
    #Função de Duplo Click
    def DuploClickOnSer(self):
        global id_servico_edit_Ser, id_edit_Ser, tipo_servico_edit_Ser, descricao_edit_Ser, status_edit_Ser, data_criacao_edit_Ser
        self.frame_6.place_forget()
        self.frame_8.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        self.listaSer.selection()
        for n in self.listaSer.selection():
            col1, col2, col3, col4, col5 = self.listaSer.item(n, "values")
            id_servico_visual_Ser.set(col1)
            id_visual_Ser.set(col2)
            tipo_servico_visual_Ser.set(col3)
            status_visual_Ser.set(col4)
            data_criacao_visual_Ser.set(col5)
            id_servico_edit_Ser = col1
            tipo_servico_edit_Ser = col3
            status_edit_Ser = col4
            data_criacao_edit_Ser = col5
        self.conectar_bd()
        self.cursor.execute("""SELECT descricao FROM servicos
                                WHERE id_servico = ?; """, (id_servico_edit_Ser,))
        descricao_servico = self.cursor.fetchone()
        self.desconectar_bd()
        descricao_edit_Ser = descricao_servico[0]
        descricao_visual_Ser.set(descricao_servico[0])
    #Função que garante que foi clicado 2 vezes em um serviço
    def DuploClickItemOnSer(self, event):
        self.mouseSer = event.widget
        self.regiaoSer = self.mouseSer.identify("region", event.x, event.y)
        if self.regiaoSer != "cell":
            return
        self.itemSer = self.mouseSer.identify_row(event.y)
        if not self.itemSer:
            return
        self.DuploClickOnSer()
    #Função para verificar se o ID do cliente existe
    def id_cliente_existe(self, event):
        global nome_cliente_Ser_T
        cliente_existe = False
        self.conectar_bd()
        self.cursor.execute("""SELECT id_cliente FROM clientes
                                        ORDER BY id_cliente ASC; """)
        for i in self.cursor.fetchall():
            if str(i[0]) == self.entry_id_S.get():
                cliente_existe = True
                break
        self.desconectar_bd()
        if not cliente_existe:
            if self.entry_id_S.get():
                if self.id_passado_S is not None:
                    self.entry_id_S.delete(len(self.id_passado_S), END)
                else:
                    self.entry_id_S.delete(0, END)
        self.conectar_bd()
        self.cursor.execute(f"""SELECT nome_cliente FROM clientes
                                        WHERE id_cliente = ?; """, (self.entry_id_S.get(),))
        nome_cliente_Ser_confirmar = self.cursor.fetchone()
        if self.entry_id_S.get():
            nome_cliente_Ser.set(value=nome_cliente_Ser_confirmar[0])
        self.desconectar_bd()
        if self.entry_id_S.get():
            self.lb2_nome_cliente_S.place(relx=0.3, rely=0.305, relwidth=0.65, relheight=0.05)
        else:
            self.lb2_nome_cliente_S.place_forget()
        self.id_passado_S = self.entry_id_S.get()
    #Função de Deletar cliente
    def deletar_Ser(self):
        global id_servico_edit_Ser
        self.conectar_bd()
        self.cursor.execute("""DELETE FROM servicos WHERE id_servico = ? """, (id_servico_edit_Ser,))
        self.con.commit()
        self.desconectar_bd()
        self.limpar_entry_S()
        self.preencher_lista_Ser()
        self.tela_2_confirmar_deletar.destroy()
        self.sair_tela8()
    #Função de confrimação para deletar cliente
    def confirmar_deletar_Ser(self):
        self.tela_2_confirmar_deletar = Toplevel(self.root)
        self.tela_2_confirmar_deletar.title("Confirmação")
        self.tela_2_confirmar_deletar.geometry("300x150")
        self.tela_2_confirmar_deletar.resizable(False, False)
        self.tela_2_confirmar_deletar.transient(self.root)
        self.tela_2_confirmar_deletar.grab_set()
        Label(self.tela_2_confirmar_deletar, text="Você realmente quer apagar esse serviço?").place(x=30,y=30)
        bt_apagar_2_sim = Button(self.tela_2_confirmar_deletar, text="Sim", bg="#1AFF00", command=self.deletar_Ser)
        bt_apagar_2_sim.place(x=70, y=80, width=60, height=30)

        bt_apagar_2_nao = Button(self.tela_2_confirmar_deletar, text="Não", bg="#FF0000", command=self.tela_2_confirmar_deletar.destroy)
        bt_apagar_2_nao.place(x=170, y=80, width=60, height=30)
        self.root.wait_window(self.tela_2_confirmar_deletar)
    #Função de Alterar informações do cliente
    def alterar_inf_Ser(self):
        global id_servico_edit_Ser, status_edit_Ser, tipo_servico_edit_Ser, descricao_edit_Ser
        self.verif_error_entrys_edit_Ser()
        self.status_Ser = self.bbt_status_servico_edit.get()
        self.tipo_servico_Ser = self.entry_tipo_servico_edit_S.get()
        self.descricao_Ser = self.entry_descricao_edit_S.get()
        self.conectar_bd()
        if error_tipo_servico_edit_Ser.get()== "" and error_descricao_edit_Ser.get()== "":
            self.cursor.execute("""UPDATE servicos SET status = ?, tipo_servico = ?, descricao = ?
                            WHERE id_servico = ?""", (self.status_Ser, self.tipo_servico_Ser, self.descricao_Ser, id_servico_edit_Ser,))
            self.sair_tela9()
            self.limpar_entry_S()
            self.servico_editado_confirm()
            status_edit_Ser = self.status_Ser
            tipo_servico_edit_Ser = self.tipo_servico_Ser
            descricao_edit_Ser = self.descricao_Ser
        self.con.commit()
        self.desconectar_bd()
        self.preencher_lista_Ser()
        status_visual_Ser.set(self.status_Ser)
        tipo_servico_visual_Ser.set(self.tipo_servico_Ser)
        descricao_visual_Ser.set(self.descricao_Ser)
    #Função para verificar se ocorreu algum erro nos Entrys do cadastro de serviços
    def verif_error_entrys_cadastro_Ser(self):
        if self.entry_id_S.get()== "":
            error_id_Ser.set(value="ID não informado")
        else:
            error_id_Ser.set(value="")

        if self.entry_tipo_servico_S.get()== "":
            error_tipo_servico_Ser.set(value="Este campo deve estar preenchido")
        else:
            error_tipo_servico_Ser.set(value="")

        if self.entry_descricao_S.get()== "":
            error_descricao_Ser.set(value="Este campo deve estar preenchido")
        else:
            error_descricao_Ser.set(value="")
    #Função para verificar se ocorreu algum erro nos Entrys do edit de serviços
    def verif_error_entrys_edit_Ser(self):
        if self.entry_tipo_servico_edit_S.get()== "":
            error_tipo_servico_edit_Ser.set(value="Este campo deve estar preenchido")
        else:
            error_tipo_servico_edit_Ser.set(value="")

        if self.entry_descricao_edit_S.get()== "":
            error_descricao_edit_Ser.set(value="Este campo deve estar preenchido")
        else:
            error_descricao_edit_Ser.set(value="")
    #Função para mostrar que o serviço foi cadastrado
    def servico_cadastrado_confirm(self):
        if self.servico_cadastrado_S is not None and self.servico_cadastrado_S.winfo_exists():
            self.servico_cadastrado_S.destroy()
        self.servico_cadastrado_S = Label(self.frame_7, text="Serviço Cadastrado!", bg="#dfe3ee", fg="#2bff00", font=("arial", 12, "bold"))
        self.servico_cadastrado_S.place(relx=0.35, rely=0.15, relwidth=0.3)
        self.root.after(4000, self.esconder_servico_cadastrado)
    #Função para esconder que o serviço foi cadastrado
    def esconder_servico_cadastrado(self):
        if self.servico_cadastrado_S is not None and self.servico_cadastrado_S.winfo_exists():
            self.servico_cadastrado_S.destroy()
            self.servico_cadastrado_S = None
    #Função para mostrar que o serviço foi editado
    def servico_editado_confirm(self):
        if self.servico_editado_S is not None and self.servico_editado_S.winfo_exists():
            self.servico_editado_S.destroy()
        self.servico_editado_S = Label(self.frame_8, text="Informações Editadas!", bg="#dfe3ee", fg="#2bff00", font=("arial", 12, "bold"))
        self.servico_editado_S.place(relx=0.35, rely=0.15, relwidth=0.3)
        self.root.after(4000, self.esconder_servico_editado)
    #Função para esconder que o serviço foi editado
    def esconder_servico_editado(self):
        if self.servico_editado_S is not None and self.servico_editado_S.winfo_exists():
            self.servico_editado_S.destroy()
            self.servico_editado_S = None

#Variáveis de iniciação
    def variaveis_iniciais(self):
        self.id_passado_S = None
        self.num_telefone = ""
        self.num_telefone_edit = ""
        self.num_data_contato = ""
        self.cliente_cadastrado_C = None
        self.cliente_editado_C = None
        self.servico_cadastrado_S = None
        self.servico_editado_S = None

class Tela(Funcoes):
    def __init__(self):
        self.variaveis_iniciais()
        self.root = root
        self.criar_tela()
        self.frames_da_tela()
        self.botoes_tela_1()
        #tela clientes
        self.botoes_tela_2()
        self.entry_tela_2()
        self.tabela_clientes()
        self.montar_Tabelas()
        self.preencher_lista_Cli()
        #tela cadastrar clientes
        self.botoes_tela_3()
        self.preencher_lista_Cli()
        self.entry_tela_3()
        #tela visualizar cliente
        self.botoes_tela_4()
        self.label_tela_4()
        #tela de alteração
        self.botoes_tela_5()
        self.entry_tela_5()
        #tela de serviços
        self.botoes_tela_6()
        self.entry_tela_6()
        self.tabela_servico()
        self.preencher_lista_Ser()
        #tela cadastrar serviço
        self.botoes_tela_7()
        self.entry_tela_7()
        #tela visualizar serviço
        self.botoes_tela_8()
        self.label_tela_8()
        #tela de alteração
        self.botoes_tela_9()
        self.entry_tela_9()
        self.root.mainloop()
    def criar_tela(self):
        self.root.title("Gerenciador da Empresa")
        self.root.geometry("640x480")
        self.root.resizable(False, False)
        self.root.configure(background="#646464")
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root,bd=4,bg="#dfe3ee", highlightbackground="#2C2C2C", highlightthickness=3)
        self.frame_1.place(relx=0.02,rely=0.02,relwidth=0.96, relheight=0.96)
        #frames da tela clientes
        self.frame_2 = Frame(self.root,bd=4,bg="#dfe3ee", highlightbackground="#2C2C2C", highlightthickness=3)
        self.frame_3 = Frame(self.root,bd=4,bg="#dfe3ee", highlightbackground="#2C2C2C", highlightthickness=3)
        self.frame_4 = Frame(self.root,bd=4,bg="#dfe3ee", highlightbackground="#2C2C2C", highlightthickness=3)
        self.frame_5 = Frame(self.root,bd=4,bg="#dfe3ee", highlightbackground="#2C2C2C", highlightthickness=3)
        #frames da tela serviços
        self.frame_6 = Frame(self.root,bd=4,bg="#dfe3ee", highlightbackground="#2C2C2C", highlightthickness=3)
        self.frame_7 = Frame(self.root,bd=4,bg="#dfe3ee", highlightbackground="#2C2C2C", highlightthickness=3)
        self.frame_8 = Frame(self.root,bd=4,bg="#dfe3ee", highlightbackground="#2C2C2C", highlightthickness=3)
        self.frame_9 = Frame(self.root,bd=4,bg="#dfe3ee", highlightbackground="#2C2C2C", highlightthickness=3)
    #Tela Menu Principal
    def botoes_tela_1(self):
        #Botão cliente
        self.bt_cliente = Button(self.frame_1, text="Clientes", bd=3, bg="#ffffff", fg="black", font=("arial", 18, "bold"), command=self.entrar_tela2)
        self.bt_cliente.place(relx=0.05, rely=0.05, relwidth=0.2, relheight=0.15)
        #Botão serviços
        self.bt_servico = Button(self.frame_1, text="Serviços", bd=3, bg="#ffffff", fg="black", font=("arial", 18, "bold"), command=self.entrar_tela6)
        self.bt_servico.place(relx=0.3, rely=0.05, relwidth=0.2, relheight=0.15)
    
    #Tela Clientes
    def botoes_tela_2(self):
        #Botão voltar
        self.bt_voltar_C = Button(self.frame_2, text="<", bd=3, bg="#ff0000", fg="black", font=("arial", 18, "bold"), command=self.sair_tela2)
        self.bt_voltar_C.place(relx=0.05, rely=0.87, relwidth=0.08, relheight=0.08)
        #Botão de Cadastro
        self.bt_cadastrar_C = Button(self.frame_2, text="Cadastrar", bd=3, bg="#00ff2a", fg="black", font=("arial", 18, "bold"), command=self.entrar_tela3)
        self.bt_cadastrar_C.place(relx=0.75, rely=0.87, relwidth=0.2, relheight=0.08)
        #Botão de escolher o que vai pesquisar
        self.values_bbt = ["ID", "Nome", "Telefone", "Email", "Data do Cadastro"]
        self.value_unic_bbt = StringVar(value=self.values_bbt[0])
        self.bbt_escolher_pesquisa = ttk.Combobox(self.frame_2, textvariable=self.value_unic_bbt, values=self.values_bbt, font=("arial", 8, "bold"), state="readonly")
        self.bbt_escolher_pesquisa.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.06)
    def entry_tela_2(self):
        #Label informando o que o duplo click faz
        self.lb_aviso_DuploClick = Label(self.frame_2, text="Clique 2 vezes em um cliente para visualizar", bg="#dfe3ee", fg="#1b1d1f", font=("arial", 10, "bold"))
        self.lb_aviso_DuploClick.place(relx=0.18, rely=0.87, relwidth=0.52, relheight=0.08)
        #Barra de pesquisa
        self.pesquisar_C = Entry(self.frame_2)
        self.pesquisar_C.place(relx=0.16, rely=0.05, relwidth=0.79, relheight=0.06)
        self.pesquisar_C.bind("<KeyRelease>", self.pesquisar_dinamico_Cli)
    def tabela_clientes(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4", "col5"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="ID")
        self.listaCli.heading("#2", text="Nome")
        self.listaCli.heading("#3", text="Telefone")
        self.listaCli.heading("#4", text="Email")
        self.listaCli.heading("#5", text="Data do Cadastro")

        self.listaCli.column("#0", width=1, stretch=NO)
        self.listaCli.column("#1", width=30)
        self.listaCli.column("#2", width=150)
        self.listaCli.column("#3", width=80)
        self.listaCli.column("#4", width=150)
        self.listaCli.column("#5", width=90)

        self.listaCli.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.7)

        self.listaCli.bind("<Double-1>", self.DuploClickItemOnCli)
    #Tela Cadastro de Cliente
    def botoes_tela_3(self):
        #Botão voltar
        self.bt_voltar_C = Button(self.frame_3, text="<", bd=3, bg="#ff0000", fg="black", font=("arial", 18, "bold"), command=self.sair_tela3)
        self.bt_voltar_C.place(relx=0.05, rely=0.87, relwidth=0.08, relheight=0.08)
        #Botão Limpar
        self.bt_limpar_C = Button(self.frame_3, text="Limpar", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.limpar_entry_C)
        self.bt_limpar_C.place(relx=0.39, rely=0.87, relwidth=0.15, relheight=0.08)
        #Botão Novo
        self.bt_novo_C = Button(self.frame_3, text="Novo", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.add_cliente_C)
        self.bt_novo_C.place(relx=0.8, rely=0.87, relwidth=0.15, relheight=0.08)
    def entry_tela_3(self):
        #Entry da Data de Contato
        self.lb_data_contato_C = Label(self.frame_3, text="Data do Primeiro Contato", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_data_contato_C.place(relx=0.05, rely=0.255)

        self.entry_data_contato_C = Entry(self.frame_3)
        self.entry_data_contato_C.place(relx=0.05, rely=0.305, relwidth=0.425, relheight=0.05)
        self.entry_data_contato_C.bind("<KeyRelease>", self.formatar_data_contato_Cli)
        #Entry do Telefone
        self.lb_telefone_C = Label(self.frame_3, text="Telefone", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_telefone_C.place(relx=0.525, rely=0.255)

        self.entry_telefone_C = Entry(self.frame_3)
        self.entry_telefone_C.place(relx=0.525, rely=0.305, relwidth=0.425, relheight=0.05)
        self.entry_telefone_C.bind("<KeyRelease>", self.formatar_telefone_Cli)
        #Entry do Nome do cliente
        self.lb_nome_cliente_C = Label(self.frame_3, text="Nome do cliente", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_nome_cliente_C.place(relx=0.05, rely=0.385)

        self.entry_nome_cliente_C = Entry(self.frame_3)
        self.entry_nome_cliente_C.place(relx=0.05, rely=0.435, relwidth=0.9, relheight=0.05)
        #Entry do Email
        self.lb_email_C = Label(self.frame_3, text="Email", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_email_C.place(relx=0.05, rely=0.515)

        self.entry_email_C = Entry(self.frame_3)
        self.entry_email_C.place(relx=0.05, rely=0.565, relwidth=0.9, relheight=0.05)

        #Mensagens de Erro
        self.error_data_contato_C = Label(self.frame_3, textvariable=error_data_contato_Cli, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"), anchor="w")
        self.error_data_contato_C.place(relx=0.05, rely=0.355)
        
        self.error_telefone_C = Label(self.frame_3, textvariable=error_telefone_Cli, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"), anchor="w")
        self.error_telefone_C.place(relx=0.525, rely=0.355)
        
        self.error_nome_cliente_C = Label(self.frame_3, textvariable=error_nome_cliente_Cli, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"), anchor="w")
        self.error_nome_cliente_C.place(relx=0.05, rely=0.485)
        
        self.error_email_C = Label(self.frame_3, textvariable=error_email_Cli, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"), anchor="w")
        self.error_email_C.place(relx=0.05, rely=0.615)
    #Tela Visualização das Informações do cliente
    def botoes_tela_4(self):
        #Botão voltar
        self.bt_voltar_C = Button(self.frame_4, text="<", bd=3, bg="#ff0000", fg="black", font=("arial", 18, "bold"), command=self.sair_tela4)
        self.bt_voltar_C.place(relx=0.05, rely=0.87, relwidth=0.08, relheight=0.08)
        #Botão Alterar
        self.bt_alterar_C = Button(self.frame_4, text="Alterar", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.entrar_tela5)
        self.bt_alterar_C.place(relx=0.39, rely=0.87, relwidth=0.15, relheight=0.08)
        #Botão Apagar
        self.bt_apagar_C = Button(self.frame_4, text="Apagar", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.confirmar_deletar_Cli)
        self.bt_apagar_C.place(relx=0.8, rely=0.87, relwidth=0.15, relheight=0.08)
    def label_tela_4(self):
        #Label do ID
        self.lb_id_visual_C = Label(self.frame_4, text="ID", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_id_visual_C.place(relx=0.05, rely=0.255)

        self.lb2_id_visual_C = Label(self.frame_4, textvariable=id_visual_Cli, bg="#999999", fg="#1b1d1f", anchor="w")
        self.lb2_id_visual_C.place(relx=0.05, rely=0.305, relwidth=0.15, relheight=0.05)
        #Label da Data de Cadastro
        self.lb_data_cadastro_visual_C = Label(self.frame_4, text="Data de Cadastro", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_data_cadastro_visual_C.place(relx=0.25, rely=0.255)

        self.lb2_data_cadastro_visual_C = Label(self.frame_4, textvariable=data_cadastro_visual_Cli, bg="#999999", fg="#1b1d1f")
        self.lb2_data_cadastro_visual_C.place(relx=0.25, rely=0.305, relwidth=0.15, relheight=0.05)
        #Label da Data de Contato
        self.lb_data_contato_visual_C = Label(self.frame_4, text="Data do Primeiro contato", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_data_contato_visual_C.place(relx=0.45, rely=0.255)

        self.lb2_data_contato_visual_C = Label(self.frame_4, textvariable=data_contato_visual_Cli, bg="#999999", fg="#1b1d1f")
        self.lb2_data_contato_visual_C.place(relx=0.45, rely=0.305, relwidth=0.15, relheight=0.05)
        #Label do Telefone
        self.lb_telefone_visual_C = Label(self.frame_4, text="Telefone", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_telefone_visual_C.place(relx=0.72, rely=0.255)

        self.lb2_telefone_visual_C = Label(self.frame_4, textvariable=telefone_visual_Cli, bg="#999999", fg="#1b1d1f", anchor="w")
        self.lb2_telefone_visual_C.place(relx=0.72, rely=0.305, relwidth=0.23, relheight=0.05)
        #Label do Nome do cliente
        self.lb_nome_cliente_visual_C = Label(self.frame_4, text="Nome do cliente", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_nome_cliente_visual_C.place(relx=0.05, rely=0.385)

        self.lb2_nome_cliente_visual_C = Label(self.frame_4, textvariable=nome_cliente_visual_Cli, bg="#999999", fg="#1b1d1f", anchor="w")
        self.lb2_nome_cliente_visual_C.place(relx=0.05, rely=0.435, relwidth=0.9, relheight=0.05)
        #Label do Email
        self.lb_email_visual_C = Label(self.frame_4, text="Email", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_email_visual_C.place(relx=0.05, rely=0.515)

        self.lb2_email_visual_C = Label(self.frame_4, textvariable=email_visual_Cli, bg="#999999", fg="#1b1d1f", anchor="w")
        self.lb2_email_visual_C.place(relx=0.05, rely=0.565, relwidth=0.9, relheight=0.05)
    #Tela de Alteração
    def botoes_tela_5(self):
        #Botão voltar
        self.bt_voltar_C = Button(self.frame_5, text="<", bd=3, bg="#ff0000", fg="black", font=("arial", 18, "bold"), command=self.sair_tela5)
        self.bt_voltar_C.place(relx=0.05, rely=0.87, relwidth=0.08, relheight=0.08)
        #Botão salvar Alteração
        self.bt_salvar_alteracao_C = Button(self.frame_5, text="Salvar Alteração", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.alterar_inf_Cli)
        self.bt_salvar_alteracao_C.place(relx=0.65, rely=0.87, relwidth=0.3, relheight=0.08)
    def entry_tela_5(self):
        #Entry do Telefone
        self.lb_telefone_edit_C = Label(self.frame_5, text="Telefone", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_telefone_edit_C.place(relx=0.05, rely=0.255)

        self.entry_telefone_edit_C = Entry(self.frame_5)
        self.entry_telefone_edit_C.place(relx=0.05, rely=0.305, relwidth=0.9, relheight=0.05)
        self.entry_telefone_edit_C.bind("<KeyRelease>", self.formatar_telefone_edit_Cli)
        #Entry do Nome do cliente
        self.lb_nome_cliente_edit_C = Label(self.frame_5, text="Nome do cliente", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_nome_cliente_edit_C.place(relx=0.05, rely=0.385)

        self.entry_nome_cliente_edit_C = Entry(self.frame_5)
        self.entry_nome_cliente_edit_C.place(relx=0.05, rely=0.435, relwidth=0.9, relheight=0.05)
        #Entry do Email
        self.lb_email_edit_C = Label(self.frame_5, text="Email", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_email_edit_C.place(relx=0.05, rely=0.515)

        self.entry_email_edit_C = Entry(self.frame_5)
        self.entry_email_edit_C.place(relx=0.05, rely=0.565, relwidth=0.9, relheight=0.05)

        #Mensagens de Erro
        self.error_telefone_edit_C = Label(self.frame_5, textvariable=error_telefone_edit_Cli, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"))
        self.error_telefone_edit_C.place(relx=0.05, rely=0.355)
        
        self.error_nome_cliente_edit_C = Label(self.frame_5, textvariable=error_nome_cliente_edit_Cli, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"))
        self.error_nome_cliente_edit_C.place(relx=0.05, rely=0.485)
        
        self.error_email_edit_C = Label(self.frame_5, textvariable=error_email_edit_Cli, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"))
        self.error_email_edit_C.place(relx=0.05, rely=0.615)

    #Tela Serviços
    def botoes_tela_6(self):
        #Botão voltar
        self.bt_voltar_S = Button(self.frame_6, text="<", bd=3, bg="#ff0000", fg="black", font=("arial", 18, "bold"), command=self.sair_tela6)
        self.bt_voltar_S.place(relx=0.05, rely=0.87, relwidth=0.08, relheight=0.08)
        #Botão de cadastrar serviço
        self.bt_cadastrar_S = Button(self.frame_6, text="Cadastrar", bd=3, bg="#00ff2a", fg="black", font=("arial", 18, "bold"), command=self.entrar_tela7)
        self.bt_cadastrar_S.place(relx=0.75, rely=0.87, relwidth=0.2, relheight=0.08)
        #Botão de escolher o que vai pesquisar
        self.values_servico_bbt = ["ID de Serviço", "ID", "Serviço", "Status", "Data de Criação"]
        self.value_servico_unic_bbt = StringVar(value=self.values_servico_bbt[0])
        self.bbt_escolher_pesquisa_servico = ttk.Combobox(self.frame_6, textvariable=self.value_servico_unic_bbt, values=self.values_servico_bbt, font=("arial", 8, "bold"), state="readonly")
        self.bbt_escolher_pesquisa_servico.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.06)
    def entry_tela_6(self):
        #Label informando o que o duplo click faz
        self.lb_aviso_2_DuploClick = Label(self.frame_6, text="Clique 2 vezes em um serviço para visualizar", bg="#dfe3ee", fg="#1b1d1f", font=("arial", 10, "bold"))
        self.lb_aviso_2_DuploClick.place(relx=0.18, rely=0.87, relwidth=0.52, relheight=0.08)
        #Barra de pesquisa
        self.pesquisar_S = Entry(self.frame_6)
        self.pesquisar_S.place(relx=0.16, rely=0.05, relwidth=0.79, relheight=0.06)
        self.pesquisar_S.bind("<KeyRelease>", self.pesquisar_dinamico_Ser)
    def tabela_servico(self):
        self.listaSer = ttk.Treeview(self.frame_6, height=3, columns=("col1", "col2", "col3", "col4", "col5"))
        self.listaSer.heading("#0", text="")
        self.listaSer.heading("#1", text="ID do Serviço")
        self.listaSer.heading("#2", text="ID")
        self.listaSer.heading("#3", text="Serviço")
        self.listaSer.heading("#4", text="Status")
        self.listaSer.heading("#5", text="Data de Criação")

        self.listaSer.column("#0", width=1, stretch=NO)
        self.listaSer.column("#1", width=70)
        self.listaSer.column("#2", width=40)
        self.listaSer.column("#3", width=200)
        self.listaSer.column("#4", width=105)
        self.listaSer.column("#5", width=85)

        self.listaSer.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.7)

        self.listaSer.bind("<Double-1>", self.DuploClickItemOnSer)
    #Tela Cadastro de Serviço
    def botoes_tela_7(self):
        #Botão voltar
        self.bt_voltar_S = Button(self.frame_7, text="<", bd=3, bg="#ff0000", fg="black", font=("arial", 18, "bold"), command=self.sair_tela7)
        self.bt_voltar_S.place(relx=0.05, rely=0.87, relwidth=0.08, relheight=0.08)
        #Botão Limpar
        self.bt_limpar_S = Button(self.frame_7, text="Limpar", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.limpar_entry_S)
        self.bt_limpar_S.place(relx=0.39, rely=0.87, relwidth=0.15, relheight=0.08)
        #Botão Novo
        self.bt_novo_S = Button(self.frame_7, text="Novo", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.add_servico_S)
        self.bt_novo_S.place(relx=0.8, rely=0.87, relwidth=0.15, relheight=0.08)
    def entry_tela_7(self):
        #Label do Nome do cliente através do ID
        self.lb_nome_cliente_S = Label(self.frame_7, text="Nome do Cliente", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_nome_cliente_S.place(relx=0.3, rely=0.255)
        self.lb3_nome_cliente_S = Label(self.frame_7, bg="#ffffff")
        self.lb3_nome_cliente_S.place(relx=0.3, rely=0.305, relwidth=0.65, relheight=0.05)
        self.lb2_nome_cliente_S = Label(self.frame_7, textvariable=nome_cliente_Ser, bg="#FFFFFF", fg="#1b1d1f", anchor="w")
        #Entry do ID
        self.lb_id_S = Label(self.frame_7, text="ID", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_id_S.place(relx=0.05, rely=0.255)

        self.entry_id_S = Entry(self.frame_7)
        self.entry_id_S.place(relx=0.05, rely=0.305, relwidth=0.2, relheight=0.05)
        self.entry_id_S.bind("<KeyRelease>", self.id_cliente_existe)
        #Entry do Tipo de Serviço
        self.lb_tipo_servico_S = Label(self.frame_7, text="Tipo de Serviço", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_tipo_servico_S.place(relx=0.05, rely=0.385)

        self.entry_tipo_servico_S = Entry(self.frame_7)
        self.entry_tipo_servico_S.place(relx=0.05, rely=0.435, relwidth=0.625, relheight=0.05)
        #Combobox do Status
        self.lb_status_S = Label(self.frame_7, text="Status", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_status_S.place(relx=0.725, rely=0.385)

        self.values_status_servico_bbt = ["Pendente", "Em processo", "Aguardando cliente", "Concluído", "Cancelado"]
        self.value_status_servico_unic_bbt = StringVar(value=self.values_status_servico_bbt[0])
        self.bbt_status_servico = ttk.Combobox(self.frame_7, textvariable=self.value_status_servico_unic_bbt, values=self.values_status_servico_bbt, font=("arial", 8, "bold"), state="readonly")
        self.bbt_status_servico.place(relx=0.725, rely=0.435, relwidth=0.225, relheight=0.05)
        #Entry da Descrição
        self.lb_descricao_S = Label(self.frame_7, text="Descrição", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_descricao_S.place(relx=0.05, rely=0.515)

        self.entry_descricao_S = Entry(self.frame_7)
        self.entry_descricao_S.place(relx=0.05, rely=0.565, relwidth=0.9, relheight=0.05)

        #Mensagem de Erro
        self.error_id_S = Label(self.frame_7, textvariable=error_id_Ser, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"), anchor="w")
        self.error_id_S.place(relx=0.05, rely=0.355)
        
        self.error_tipo_servico_S = Label(self.frame_7, textvariable=error_tipo_servico_Ser, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"), anchor="w")
        self.error_tipo_servico_S.place(relx=0.05, rely=0.485)
        
        self.error_descricao_S = Label(self.frame_7, textvariable=error_descricao_Ser, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"), anchor="w")
        self.error_descricao_S.place(relx=0.05, rely=0.615)
    #Tela Visualização das Informações do serviço
    def botoes_tela_8(self):
        #Botão voltar
        self.bt_voltar_S = Button(self.frame_8, text="<", bd=3, bg="#ff0000", fg="black", font=("arial", 18, "bold"), command=self.sair_tela8)
        self.bt_voltar_S.place(relx=0.05, rely=0.87, relwidth=0.08, relheight=0.08)
        #Botão Alterar
        self.bt_alterar_S = Button(self.frame_8, text="Alterar", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.entrar_tela9)
        self.bt_alterar_S.place(relx=0.39, rely=0.87, relwidth=0.15, relheight=0.08)
        #Botão Apagar
        self.bt_apagar_S = Button(self.frame_8, text="Apagar", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.confirmar_deletar_Ser)
        self.bt_apagar_S.place(relx=0.8, rely=0.87, relwidth=0.15, relheight=0.08)
    def label_tela_8(self):
        #Label do ID de Serviço
        self.lb_id_servico_visual_S = Label(self.frame_8, text="ID de Serviço", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_id_servico_visual_S.place(relx=0.05, rely=0.255)

        self.lb2_id_servico_visual_S = Label(self.frame_8, textvariable=id_servico_visual_Ser, bg="#999999", fg="#1b1d1f", anchor="w")
        self.lb2_id_servico_visual_S.place(relx=0.05, rely=0.305, relwidth=0.15, relheight=0.05)
        #Label do ID do Cliente
        self.lb_id_visual_S = Label(self.frame_8, text="ID", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_id_visual_S.place(relx=0.25, rely=0.255)

        self.lb2_id_visual_S = Label(self.frame_8, textvariable=id_visual_Ser, bg="#999999", fg="#1b1d1f", anchor="w")
        self.lb2_id_visual_S.place(relx=0.25, rely=0.305, relwidth=0.15, relheight=0.05)
        #Label do Status
        self.lb_status_visual_S = Label(self.frame_8, text="Status", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_status_visual_S.place(relx=0.45, rely=0.255)

        self.lb2_status_visual_S = Label(self.frame_8, textvariable=status_visual_Ser, bg="#999999", fg="#1b1d1f", anchor="w")
        self.lb2_status_visual_S.place(relx=0.45, rely=0.305, relwidth=0.2, relheight=0.05)
        #Label da Data de Criação
        self.lb_data_criacao_visual_S = Label(self.frame_8, text="Data de Criação", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_data_criacao_visual_S.place(relx=0.7, rely=0.255)

        self.lb2_data_criacao_visual_S = Label(self.frame_8, textvariable=data_criacao_visual_Ser, bg="#999999", fg="#1b1d1f")
        self.lb2_data_criacao_visual_S.place(relx=0.7, rely=0.305, relwidth=0.25, relheight=0.05)
        #Label do Tipo de Serviço
        self.lb_tipo_servico_visual_S = Label(self.frame_8, text="Tipo de Serviço", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_tipo_servico_visual_S.place(relx=0.05, rely=0.385)

        self.lb2_tipo_servico_visual_S = Label(self.frame_8, textvariable=tipo_servico_visual_Ser, bg="#999999", fg="#1b1d1f", anchor="w")
        self.lb2_tipo_servico_visual_S.place(relx=0.05, rely=0.435, relwidth=0.9, relheight=0.05)
        #Label da Descrição
        self.lb_descricao_visual_S = Label(self.frame_8, text="Descrição", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_descricao_visual_S.place(relx=0.05, rely=0.515)

        self.lb2_descricao_visual_S = Label(self.frame_8, textvariable=descricao_visual_Ser, bg="#999999", fg="#1b1d1f", anchor="w")
        self.lb2_descricao_visual_S.place(relx=0.05, rely=0.565, relwidth=0.9, relheight=0.05)
    #Tela de Alteração de serviço
    def botoes_tela_9(self):
        #Botão voltar
        self.bt_voltar_S = Button(self.frame_9, text="<", bd=3, bg="#ff0000", fg="black", font=("arial", 18, "bold"), command=self.sair_tela9)
        self.bt_voltar_S.place(relx=0.05, rely=0.87, relwidth=0.08, relheight=0.08)
        #Botão salvar Alteração
        self.bt_salvar_alteracao_S = Button(self.frame_9, text="Salvar Alteração", bd=3, bg="#808080", fg="white", font=("arial", 15, "bold"), command=self.alterar_inf_Ser)
        self.bt_salvar_alteracao_S.place(relx=0.65, rely=0.87, relwidth=0.3, relheight=0.08)
    def entry_tela_9(self):
        #Entry do Status
        self.lb_status_edit_S = Label(self.frame_9, text="Status", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_status_edit_S.place(relx=0.05, rely=0.255)

        self.bbt_status_servico_edit = ttk.Combobox(self.frame_9, textvariable=value_status_servico_unic_bbt_edit, values=self.values_status_servico_bbt, font=("arial", 8, "bold"), state="readonly")
        self.bbt_status_servico_edit.place(relx=0.05, rely=0.305, relwidth=0.9, relheight=0.05)
        #Entry do Tipo de Serviço
        self.lb_tipo_servico_edit_S = Label(self.frame_9, text="Tipo de Serviço", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_tipo_servico_edit_S.place(relx=0.05, rely=0.385)

        self.entry_tipo_servico_edit_S = Entry(self.frame_9)
        self.entry_tipo_servico_edit_S.place(relx=0.05, rely=0.435, relwidth=0.9, relheight=0.05)
        #Entry da Descrição
        self.lb_descricao_edit_S = Label(self.frame_9, text="Descrição", bg="#dfe3ee", fg="#1b1d1f")
        self.lb_descricao_edit_S.place(relx=0.05, rely=0.515)

        self.entry_descricao_edit_S = Entry(self.frame_9)
        self.entry_descricao_edit_S.place(relx=0.05, rely=0.565, relwidth=0.9, relheight=0.05)

        #Mensagem de Erro
        self.error_tipo_servico_edit_S = Label(self.frame_9, textvariable=error_tipo_servico_edit_Ser, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"), anchor="w")
        self.error_tipo_servico_edit_S.place(relx=0.05, rely=0.485)
        
        self.error_descricao_edit_S = Label(self.frame_9, textvariable=error_descricao_edit_Ser, bg="#dfe3ee", fg="#ff0000", font=("arial", 8, "bold"), anchor="w")
        self.error_descricao_edit_S.place(relx=0.05, rely=0.615)

Tela()