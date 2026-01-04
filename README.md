# 🛠️ Hardware Inventory Manager

**Um software de console em Python para gerenciar estoque de peças de manutenção.**

---

## 🚧 STATUS DO PROJETO
**✅ Estável (v2.1)**

O projeto conta com o ciclo completo de CRUD (Create, Read, Update, Delete), sistema de busca avançada e geração de relatórios para planilhas.
> **Novidade v2.1:** Interface visual aprimorada com **tabelas formatadas** e **alertas coloridos** para melhor UX no terminal.

---

## ⚙️ Funcionalidades

### Core
* [X] **CRUD Completo:** Adicionar, Ler, Atualizar e Remover itens.
* [X] **Persistência Automática:** Salva dados em `inventory.json` instantaneamente.
* [X] **Lógica de Negócio:** Cálculo automático de preço de venda (Margem de 30%).
* [X] **Proteção de Dados:** Validação de inputs numéricos (blinda contra erros de digitação).

### Recursos Avançados
* [X] **Busca Inteligente:** Localiza peças por nome ou trecho.
* [X] **Exportação CSV:** Gera planilhas compatíveis com Excel/Google Sheets.
* [X] **Visual Pro:** Tabelas alinhadas (`tabulate`) e feedback colorido (`colorama`).
* [X] **Alerta Gerencial:** Notifica visualmente vendas de alto valor (> R$ 500).
---

## 💻 Como Usar

1.  Certifique-se de ter o **Python 3.10** (ou superior) instalado.

2.  Clone este repositório:
    ```bash
    git clone https://github.com/filipevbr/hardware-inventory-manager.git
    ```

3.  Navegue até o diretório do projeto:
    ```bash
    cd hardware-inventory-manager
    ```

4.  **Instale as dependências visuais:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute o sistema:**
    ```bash
    python src/main.py
    ```
---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **Biblioteca `json`** (Persistência de dados)
* **Biblioteca `csv`** (Geração de relatórios)
* **Biblioteca `datetime`** (Registro temporal)
* **Interface** `tabulate`, `colorama`

---

## 👨‍💻 Autor

* **Filipe Vaz**
      *(Estudante de Análise e Desenvolvimento de Sistemas - PUCPR)*

---

## 🤖 Declaração de Uso de IA

> Durante o desenvolvimento, o Gemini (Google) foi utilizado como "peer review" para revisão de lógica e brainstorming de arquitetura. Todo o código foi validado, testado e refinado pelo autor.