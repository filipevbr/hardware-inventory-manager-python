# 🛠️ CLI Hardware Inventory Manager

**Um software de console em Python para gerenciar estoque de peças de manutenção.**

---

## 🚧 STATUS DO PROJETO
**✅ Estável (v2.0)**

O projeto conta com o ciclo completo de CRUD (Create, Read, Update, Delete), sistema de busca avançada e geração de relatórios para planilhas.
> **Destaque v2.0:** Agora com **Busca de Itens**, **Exportação para Excel (CSV)** e persistência automática de dados.

---

## ⚙️ Funcionalidades

### Funcionalidades Implementadas
* [X] **Menu Principal:** Interface de console limpa e navegável.
* [X] **Persistência de Dados:** Salva automaticamente em `inventory.json`.
* [X] **Input Validation:** Blinda o sistema contra erros de digitação (aceita `10,50` ou `10.50`).
* [X] **Comando `ADD`:** Cadastro de componentes com data/hora e cálculo de margem (30%).
* [X] **Alerta Gerencial:** Notifica quando o preço de venda ultrapassa R$ 500,00.
* [X] **Comando `LIST`:** Visualização tabular das peças.
* [X] **Comando `UPDATE`:** Edição de Nome e Custo (com recálculo automático do preço de venda).
* [X] **Comando `DELETE`:** Remoção segura de itens.
* [X] **Comando `SEARCH`:** Busca dinâmica de peças por nome ou trecho.
* [X] **Comando `EXPORT`:** Gera relatório em `.csv` compatível com Excel/Google Sheets.

---

## 💻 Como Usar

1.  Certifique-se de ter o **Python 3.10** (ou superior) instalado.
2.  Clone este repositório:
    ```bash
    git clone [https://github.com/filipevbr/hardware-inventory-manager-python.git](https://github.com/filipevbr/hardware-inventory-manager-python.git)
    ```
3.  Navegue até o diretório do projeto:
    ```bash
    cd hardware-inventory-manager-python
    ```
4.  Execute o script principal:
    ```bash
    python src/main.py
    ```
5.  **Para gerar relatórios:** Selecione a opção `6` no menu. O arquivo `relatorio_estoque.csv` será criado na raiz do projeto.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Biblioteca `json`** (Persistência de dados)
* **Biblioteca `csv`** (Geração de relatórios)
* **Biblioteca `datetime`** (Registro temporal)

---

## 👨‍💻 Autor

* **Filipe Vaz**
      *(Estudante de Análise e Desenvolvimento de Sistemas - PUCPR)*

---

## 🤖 Declaração de Uso de IA

> Durante a preparação deste projeto e documentação, o autor utilizou o Gemini (Google) como ferramenta de apoio para auxiliar na estruturação do código, revisão de lógica e formatação de texto. O autor revisou, testou e editou todo o conteúdo, assumindo total responsabilidade pelo código final.