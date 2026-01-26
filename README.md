# LogiCore Solutions

Sistema de gerenciamento de **Clientes e Serviços**, com geração automática de **relatórios em PDF** e envio por **email**, desenvolvido em Python para fins educacionais.

---

## 📌 Sobre o projeto

O **LogiCore Solutions** é um sistema desktop desenvolvido em Python com o objetivo de simular um sistema real de gestão empresarial, permitindo:

- Cadastro, edição e exclusão de clientes
- Cadastro, edição e exclusão de serviços
- Validação e formatação automática de dados
- Geração de relatórios profissionais em PDF
- Envio automático de relatórios por email
- Histórico organizado de relatórios gerados

Este projeto foi desenvolvido com foco em **aprendizado prático**, organização de código e boas práticas.

---

## ⚙️ Funcionalidades

### 👥 Clientes
- Cadastro de clientes
- Edição e exclusão
- Validação de:
  - Nome
  - Telefone (com formatação automática)
  - Email (com verificação de padrão)

### 🛠️ Serviços
- Cadastro de serviços vinculados a clientes
- Status do serviço
- Edição e exclusão
- Confirmação antes da exclusão

### 📄 Relatórios
- Geração automática de relatório em PDF
- Relatório contém:
  - Data e hora de geração
  - Nome do funcionário responsável
  - Total de clientes cadastrados
  - Total de serviços cadastrados
  - Lista de clientes com seus respectivos serviços
- Histórico de relatórios organizado por data

### ✉️ Envio por Email
- Envio automático do relatório por email
- Sistema solicita:
  - Email do remetente
  - Email do destinatário
  - App Password do email
- As informações são salvas no banco de dados e reutilizadas
- Código sensível de email não é versionado no GitHub

---

## 🛠️ Tecnologias utilizadas

- **Python 3**
- **Tkinter** – Interface gráfica
- **SQLite3** – Banco de dados
- **ReportLab** – Geração de PDFs
- **smtplib / email.message** – Envio de emails
- **Git & GitHub** – Controle de versão

---

## ▶️ Como executar o projeto

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/Sistema-Clientes-Servicos.git
```

2. Acesse a pasta do projeto:
cd Sistema-Clientes-Servicos

3. Execute o sistema:
python main.py

**Certifique-se de ter o Python 3 instalado.**

## 📄 Relatórios
- Os relatórios são gerados em formato PDF
- São armazenados automaticamente na pasta historico
- Cada relatório possui nome único baseado em data e hora

## 🔐 Segurança e Email
- Informações sensíveis (email e App Password) não estão versionadas no GitHub
- O sistema solicita os dados apenas uma vez e salva no banco de dados local

## ⚠️ Observações importantes
- **Este projeto utiliza nomes fictícios**
- **Desenvolvido exclusivamente para fins educacionais**
- **Não é recomendado para uso em produção sem ajustes de segurança**

## 📈 Status do projeto
✅ Projeto finalizado – Versão 1.0

Tempo total de desenvolvimento: 46 horas

## 👨‍💻 Autor
*Desenvolvido por Samuel Alves*

*Projeto criado para estudo, prática e portfólio em Python.*