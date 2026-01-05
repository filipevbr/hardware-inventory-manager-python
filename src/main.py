import datetime
import json
import csv
from tabulate import tabulate
from colorama import init, Fore, Style

# Inicializa o colorama e reseta a cor apos o print
init(autoreset=True)

# Categorias fixas para padronização
VALID_CATEGORIES = {
    "1": "Hardware (Peças)",
    "2": "Periféricos",
    "3": "Cabos & Adaptadores",
    }

# Funcao que salva os dados do estoque
def save_data(inventory):
    with open("inventory.json", "w", encoding="utf-8") as data:
        json.dump(inventory, data, indent=4)

# Funcao que carrega os dados do estoque
def load_data():
    try:
        with open("inventory.json", "r", encoding="utf-8") as data:
            return json.load(data)
    except json.JSONDecodeError:
        print(Fore.RED + 'ERRO: Não foi possível ler o arquivo.')
        return []
    except FileNotFoundError:
        return []
    
# Funcao que exibe o menu principal
def show_menu():
    print("\n" + Fore.CYAN + Style.BRIGHT + "=== HARDWARE MANAGER SYSTEM ===")
    print("1 - Adicionar Itens")
    print("2 - Ver Estoque")
    print("3 - Atualizar Itens")
    print("4 - Remover Item")
    print("5 - Buscar Item")
    print("6 - Exportar Relatório (CSV)")
    print("7 - Dashboard Financeiro")
    print("8 - Sair")

# Funcao que trata os valores recebidos pelo usuario
def get_valid_float(prompt):
    while True:
        data = input(prompt).strip()  # Pede o dado usando a pergunta que veio no parametro "prompt"
        data = data.replace(",", ".")

        try:
            value = float(data)
            if value < 0:
                print(Fore.RED + "O valor não pode ser negativo.")
                continue  # Volta para o inicio do loop
            return value
        
        except ValueError:
            print(Fore.RED + "\nERRO: Digite apenas números válidos.")

# Funcao que verifica se a peca cadastrada existe
def select_item(inventory):
    if not inventory:
        print(Fore.YELLOW + "Estoque vazio.")
        return None
    
    print(Fore.CYAN + "\n=== Selecione um Item ===")
    table_data = []
    for index, item in enumerate(inventory, start=1):
        table_data.append([index, item['name'], f"R$ {item['sale']:.2f}"])

    headers = ["ID", "Nome", "Venda"]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

    print(" 0 - Cancelar\n")  # Opcao de saida para o usuario
    
    try:
        option = int(input("Opção: "))
        if option == 0:
            return None

        real_index = option - 1

        if 0 <= real_index < len(inventory):
            return real_index
        else:
            print(Fore.RED + "Opção inválida.")
            return None
        
    except ValueError:
        print(Fore.RED + "Por favor, digite apenas números inteiros.")
        return None
        
# Funcao para notificar a necessidade de aprovacao da gerencia
def manager_approval():
    print(Fore.YELLOW + Style.BRIGHT + "ATENÇÃO: Valor alto! Necessária a aprovação da gerencia.")

# Funcao para procurar pecas
def search_component(inventory):
    print("\n=== BUSCAR ITEM ===")
    if not inventory:
        print(Fore.YELLOW + "Estoque vazio.")
        return
    
    term = input("Digite o nome do item (ou parte dele): ").strip().upper()
    found_items = [item for item in inventory if term in item['name']]

    if found_items:
        print(f"\nForam encontrados {len(found_items)} itens:")
        headers = ["Nome", "Venda"]
        table_data = [[item['name'], f"R$ {item['sale']:.2f}"] for item in found_items]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    else:
        print(Fore.YELLOW + "Nenhum item foi encontrado.")

    input("\nPressione Enter para voltar ao menu...")

# Funcao para exportar o CSV
def export_report(inventory):
    print("\n=== EXPORTAR RELATÓRIO (CSV) ===")
    if not inventory:
        print(Fore.YELLOW + "Estoque vazio. Nada para exportar.")
        return
    
    filename = "relatorio_estoque.csv"

    try:
        # 'w' = write.
        # newline='' = evita pular linha extra no Windows.
        # encoding='utf-8' = pra não bugar acento.
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['name', 'cost', 'sale', 'registration_date']  # Define as colunas da tabela.
            writer = csv.DictWriter(file, fieldnames=fieldnames)  # Escreve a tabela.
            writer.writeheader()  # Escreve o cabecalho da tabela.
            writer.writerows(inventory)  # Escreve todas as linhas da lista de uma unica vez.
        
        print(Fore.GREEN + f"Sucesso! O arquivo '{filename}' foi gerado na pasta.")
    
    except Exception as e:
        print(Fore.RED + f"Erro ao exportar: {e}")
    
    input("\nPressione Enter para voltar ao menu...")

# Funcao para adicionar pecas
def add_component(inventory):
    while True: 
        print("\n=== CADASTRAR ITEM ===")
        
        # Coleta de categoria
        print("Selecione a Categoria:")
        for key, value in VALID_CATEGORIES.items():
            print(f"{key} - {value}")

        cat_opt = input("Opção: ").strip()
        # Se digitar algo inválido, assume "Geral"
        category = VALID_CATEGORIES.get(cat_opt, "Geral")

        # Coleta de dados
        name = input("Digite o nome do componente: ").strip().upper()
        cost = get_valid_float(f"Digite o custo da compra de {name}: ")
        
        # Coleta da margem de Lucro variavel
        margin_percent = get_valid_float(f"Margem de Lucro desejada para este item (%): ")
        margin_decimal = margin_percent / 100

        # Calculo
        final_value = cost * (1 + margin_decimal)

        # Pacote com os dados do item
        item = {
            "name": name,
            "category": category,
            "cost": cost,
            "margin": margin_decimal,
            "sale": final_value,
            "registration_date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            }

        # Adiciona o item a lista global
        inventory.append(item)
        save_data(inventory)
        
        # Feedback visual
        print(Fore.GREEN + f"\n{name} ({category}) cadastrado! Venda: R${final_value:.2f}")

        if final_value >= 500.00:
            manager_approval()

        # Menu de decisao
        print("\nO que deseja fazer?")
        print("1 - Cadastrar outro")
        print("2 - Voltar ao menu principal")

        option = input("Opção: ")
        if option == "2":
            break  # Quebra o loop e finaliza a funcao

# Funcao para atualizar pecas
def update_component(inventory):
    print("\n" + Fore.CYAN + "\n=== ATUALIZAR ITEM ===")
    real_index = select_item(inventory)

    if real_index is None:
        return
    
    item = inventory[real_index]

    while True:
        print("\n" + Fore.CYAN + f"\nEditando: {item['name']}")

        # Recupera dados atuais (com proteção para itens antigos que não tinham margem salva)
        # Se não tiver margem salva, assume 30% (0.3) padrão
        current_cat = item.get('category', '---')
        current_margin = item.get('margin', 0.3) * 100
        
        # Mostra os dados atuais para o usuário
        current_data = [[current_cat, f"R$ {item['cost']:.2f}", f"{current_margin:.0f}%", f"R$ {item['sale']:.2f}"]]
        print(tabulate(current_data, headers=["Categoria", "Custo", "Margem", "Venda"], tablefmt="fancy_grid"))

        # Menu de decisao
        print("1 - Alterar Nome")
        print("2 - Alterar Custo")
        print("3 - Alterar Categoria")
        print("4 - Alterar Margem de Lucro")
        print("5 - Voltar/Salvar")

        option = input("Opção: ")

        if option == "1":
            new_name = input("Novo nome: ").strip().upper()
            if new_name: # Só altera se digitar algo
                item['name'] = new_name
                save_data(inventory)
                print(Fore.GREEN + "Nome do item atualizado!")

        elif option == "2":
            new_cost = get_valid_float(f"(Atual: {item['cost']:.2f}) Novo custo: ")
            
            current_margin_decimal = item.get('margin', 0.3)  # Recupera a margem atual do item

            item['cost'] = new_cost  # Atualiza o custo
            item['sale'] = new_cost * (1 + current_margin_decimal)  # Atualiza o preco da venda
            
            save_data(inventory)
            print(Fore.GREEN + f"Custo e Venda atualizados! Nova venda: R${item['sale']:.2f}")
            print(f"(Margem atual de {current_margin_decimal*100:.0f}%)")
            
            if new_cost >= 500.00:
                manager_approval()
        
        elif option == "3":
            print("\nSelecione a Nova Categoria:")
            for key, value in VALID_CATEGORIES.items():
                print(f"{key} - {value}")
            
            cat_opt = input("Opção: ").strip()
            # Se digitar algo inválido, assume "Geral"
            item['category'] = VALID_CATEGORIES.get(cat_opt, "Geral")
            
            save_data(inventory)
            print(Fore.GREEN + "Categoria atualizada!")

        elif option == "4":
            new_margin_percent = get_valid_float(f"(Atual: {current_margin:.0f}%) Nova Margem (%): ")
            new_margin_decimal = new_margin_percent / 100
            
            # Atualiza a margem e o preço final
            item['margin'] = new_margin_decimal
            item['sale'] = item['cost'] * (1 + new_margin_decimal)
            
            save_data(inventory)
            print(Fore.GREEN + f"Margem atualizada! Novo preço de venda: R$ {item['sale']:.2f}")

        elif option == "5":
            break

        else:
            print(Fore.RED + "Opção inválida.")

# Funcao para listar pecas no estoque
def list_inventory(inventory):
    print("\n" + Fore.CYAN + "=== ESTOQUE ATUAL ===")
    if not inventory:
        print(Fore.YELLOW + "Estoque vazio.")
        input("\nPressione Enter para voltar ao menu...")
        return
    
    table_data = []
    for index, item in enumerate(inventory, start=1):  # Percorre a lista de estoque enumerando o indice
        # Protecao para itens antigos (sem categoria)
        cat = item.get('category', '---')
        # Formata a margem para porcentagem (Ex: 0.5 vira "50%")
        margin_display = f"{item.get('margin', 0.3) * 100:.0f}%"
        
        row = [index, item['name'], cat, f"R$ {item['cost']:.2f}", margin_display, f"R$ {item['sale']:.2f}", item['registration_date']]
        table_data.append(row)

    headers = ["ID", "Produto", "Categoria", "Custo", "Margem", "Venda", "Data"]

    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))  # Imprime a tabela formatada

    input("\nPressione Enter para voltar ao menu...")

# Funcao para remover pecas do estoque
def remove_component(inventory):
    print("\n" + Fore.CYAN + "\n=== REMOVER ITEM ===")
    real_index = select_item(inventory)

    if real_index is None:
        return
    
    item_name = inventory[real_index]['name']
    confirm = input(Fore.RED + f"Tem certeza que deseja remover '{item_name}'? (S/N): ").strip().upper()

    if confirm == 'S':
        inventory.pop(real_index)
        save_data(inventory)
        print(Fore.GREEN + f"Item '{item_name}' removido com sucesso!")
    
    else:
        print(Fore.YELLOW + "Operação cancelada.")
    
    input("\nPressione Enter para voltar ao menu...")

# Funcao que exibe o dashboard financeiro
def show_financial_dashboard(inventory):
    print("\n" + Fore.CYAN + "=== RESUMO FINANCEIRO ===")
    if not inventory:
        print(Fore.YELLOW + "Estoque vazio. Nada para calcular.")
        input("\nPressione Enter para voltar ao menu...")
        return

    # Calculos
    total_invested = sum(item['cost'] for item in inventory)
    total_revenue_potential = sum(item['sale'] for item in inventory)
    projected_profit = total_revenue_potential - total_invested
    total_items = len(inventory)

    # Tabela
    dashboard_data = [
        ["Total de Itens", f"{total_items}"], 
        ["Capital Investido", f"R$ {total_invested:,.2f}"], 
        ["Receita Potencial", f"R$ {total_revenue_potential:,.2f}"], 
        ["Lucro Projetado", f"R$ {projected_profit:,.2f}"]
        ]

    print(tabulate(dashboard_data, tablefmt="fancy_grid"))

    # Alerta de estoque
    names = [item['name'] for item in inventory]
    low_stock = list(set([name for name in names if names.count(name) < 3]))

    if low_stock:
        print(Fore.YELLOW + "\nALERTA DE ESTOQUE BAIXO (Menos de 3 un.):")
        for item in low_stock:
            print(f" - {item}")
    else:
        print(Fore.GREEN + "\nNíveis de estoque otimizados.")

    input("\nPressione Enter para voltar ao menu...")

# Funcao principal
def main():
    inventory = load_data()
    while True: 
        show_menu()
        option = input("Digite a opção desejada: ").strip()
        match option:
            case "1":
                add_component(inventory)
            case "2":
                list_inventory(inventory)
            case "3":
                update_component(inventory)
            case "4":
                remove_component(inventory)
            case "5":
                search_component(inventory)
            case "6":
                export_report(inventory)
            case "7":
                show_financial_dashboard(inventory)
            case "8":
                print(Fore.CYAN + "Saindo do sistema...")
                break
            case _:
                print(Fore.RED + "Opção inválida.\n")

if __name__ == "__main__":
    main()
