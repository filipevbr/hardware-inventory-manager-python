# 🛠️ Hardware Inventory Manager

**Um software de console em Python para gerenciar estoque de peças de manutenção e acessórios.**

---

## 🚧 STATUS DO PROJETO
**✅ Versão 2.2**

O projeto conta com o ciclo completo de CRUD (Create, Read, Update, Delete), sistema de busca avançada e geração de relatórios para planilhas.
> **Novidade v2.2:** Dashboard Financeiro, Margens de Lucro Variáveis e Categorização.

---

## ⚙️ Funcionalidades

### Core & Gestão
* [X] **CRUD:** Adicionar, Ler, Atualizar e Remover itens.
* [X] **Persistência Automática:** Salva dados em `inventory.json` instantaneamente.
* [X] **Precificação Dinâmica:** Definição de **Margem de Lucro Variável** por produto (ex: 30% em Hardware, 100% em Cabos).
* [X] **Categorização:** Organização por tipos (Hardware, Periféricos, Acessórios).

### Business Intelligence (BI)
* [X] **Dashboard Financeiro:** Relatório executivo com KPIs (Capital Investido, Receita Potencial e Lucro Projetado).
* [X] **Alertas de Estoque:** Monitoramento visual de itens com baixo estoque (< 3 unidades).

### Recursos Visuais & Extras
* [X] **Busca Avançada:** Localiza peças por nome.
* [X] **Exportação CSV:** Gera planilhas para Excel/Google Sheets.
* [X] **Interface Pro:** Tabelas formatadas (`tabulate`) e feedback colorido (`colorama`).
* [X] **Proteção de Caixa:** Alerta para itens de alto valor (> R$ 500).

## 🔜 Roadmap (Funcionalidades Futuras)

Os próximos passos planejados são:

* [ ] **Stock Tracking (Volumetria):** Implementação de controle de quantidade (`qty`) para gerenciar múltiplas unidades do mesmo item (soma e baixa automática).
* [ ] **Containerização:** Criação de `Dockerfile` e `docker-compose` para isolar a aplicação e suas dependências.

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
    python main.py
    ```

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **JSON** (Persistência de dados)
* **CSV** (Geração de relatórios)
* **Tabulate & Colorama** (UX/UI no Terminal)
* **Biblioteca `datetime`** (Registro temporal)
* **Git/GitHub** (Versionamento)

---

## 👨‍💻 Autor

* **Filipe Vaz**
      *(Estudante de Análise e Desenvolvimento de Sistemas - PUCPR)*

---

## 🤖 Declaração de Uso de IA

> Durante o desenvolvimento, o Gemini (Google) foi utilizado como "peer review" para revisão de lógica e brainstorming de arquitetura. Todo o código foi validado, testado e refinado pelo autor.