from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import sqlite3 as sq
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sistema.db")

def conectar_banco():
    return sq.connect(DB_PATH)

Pasta_Mes = datetime.now().strftime("%Y-%m")
Pasta_Historico = os.path.join("historico", Pasta_Mes)
os.makedirs(Pasta_Historico, exist_ok=True)

caminho_pdf_gerado = None
Y = 0

#Funções Secundárias
def total_clientes():
    con = conectar_banco()
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchall()
    con.close()
    return total[0]

def total_servicos():
    con = conectar_banco()
    cursor = con.cursor()
    cursor.execute("SELECT COUNT(*) FROM servicos")
    total = cursor.fetchall()
    con.close()
    return total[0]

def buscar_dados_relatorio():
    con = conectar_banco()
    cursor = con.cursor()
    cursor.execute("""SELECT
            c.nome_cliente,
            c.telefone,
            c.email,
            s.tipo_servico,
            s.status
        FROM clientes c
        LEFT JOIN servicos s ON c.id_cliente = s.id_cliente
        ORDER BY c.nome_cliente""")
    dados = cursor.fetchall()
    con.close()

    clientes = {}
    for nome_cliente, telefone, email, tipo_servico, status in dados:
        if nome_cliente not in clientes:
            clientes[nome_cliente] = {
                "telefone": telefone,
                "email": email,
                "servicos": []
            }

        clientes[nome_cliente]["servicos"].append((tipo_servico, status))
    return clientes

def draw_CS(c, largura, altura):
    global Y
    y = 656
    dados = buscar_dados_relatorio()
    for nome_cliente, info in dados.items():
        if y < 100:
            c.line(0, 36, largura, 36)
            c.showPage()
            c.setFont("Helvetica", 10)
            y = altura - 50
        t = info['telefone']
        c.drawString(10, y, f"Cliente: {nome_cliente}")
        y -= 12
        c.drawString(10, y, f"Telefone: ({t[:2]}) {t[2:7]}-{t[7:]}")
        y -= 12
        c.drawString(10, y, f"Email: {info['email']}")
        y -= 12
        c.drawString(20, y, "Serviços:")
        y -= 12
        for servico, status in info['servicos']:
            if not servico is None:
                c.drawString(50, y, f"- {servico} | {status}")
                y -= 12
            else:
                c.drawString(50, y, "Sem serviço cadastrado")
                y -= 12
        c.line(40, y, largura - 40, y)
        y -= 12
    Y = y

#Função Principal
def config_pdf(c, largura, altura, nome_funcionario):
    global Y
    c.setFont("Helvetica-Bold", 20)
    c.drawString(210, 772, "LogiCore Solutions")
    c.drawString(265, 752, "Relatório")
    c.setFont("Helvetica", 12)
    c.drawString(10, 727, "Resumo Geral:")
    c.drawString(20, 715, f"- Total de clientes cadastrados: {total_clientes()[0]}")
    c.drawString(20, 703, f"- Total de serviços cadastrados: {total_servicos()[0]}")
    c.line(0, 691, largura, 691)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(210, 671, "Clientes e Serviços")
    c.setFont("Helvetica", 10)
    draw_CS(c, largura, altura)
    Y += 12
    c.line(0, Y, largura, Y)
    c.line(0, 36, largura, 36)
    c.drawString(10, 22, f"Relatório gerado por: {nome_funcionario}")
    data = datetime.now().strftime("%d/%m/%Y - %H:%M")
    c.drawString(10, 10, f"Data/Hora: {data}")

def gerar_pdf(nome_funcionario):
    global caminho_pdf_gerado
    nome_pdf = f"Relatório_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    caminho_pdf = os.path.join(Pasta_Historico, nome_pdf)
    caminho_pdf_gerado = caminho_pdf

    c = canvas.Canvas(caminho_pdf, pagesize=letter)
    largura, altura = letter
    config_pdf(c, largura, altura, nome_funcionario)
    c.showPage()
    c.save()