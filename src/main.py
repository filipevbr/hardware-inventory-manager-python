import datetime
import json
import csv
from tabulate import tabulate
from colorama import init, Fore, Style

# Inicializa o colorama e reseta a cor apos o print
init(autoreset=True)

# Taxa para o calculo do preco final
fixed_profit = 0.3

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
    print("7 - Sair")

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

        # Coleta de dados
        name = input("Digite o nome do componente: ").strip().upper()
        cost = get_valid_float(f"Digite o custo da compra de {name}: ")
        
        # Calculo
        final_value = cost * (1 + fixed_profit)

        # Pacote com os dados da peça
        item = {
            "name": name,
            "cost": cost,
            "sale": final_value,
            "registration_date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        }

        # Adiciona o item a lista global
        inventory.append(item)
        save_data(inventory)
        
        # Feedback visual
        print(Fore.GREEN + f"\n{name} cadastrado! Venda: R${final_value:.2f}")

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

        current_data = [[f"R$ {item['cost']:.2f}", f"R$ {item['sale']:.2f}"]]
        print(tabulate(current_data, headers=["Custo Atual", "Venda Atual"], tablefmt="fancy_grid"))

        print("1 - Alterar Nome")
        print("2 - Alterar Custo")
        print("3 - Voltar/Salvar")

        option = input("Opção: ")

        if option == "1":
            new_name = input("Novo nome: ").strip().upper()
            if new_name: # Só altera se digitar algo
                item['name'] = new_name
                save_data(inventory)
                print(Fore.GREEN + "Nome do item atualizado!")

        elif option == "2":
            new_cost = get_valid_float(f"(Atual: {item['cost']:.2f}) Novo custo: ")
            item['cost'] = new_cost  # Atualiza o custo
            item['sale'] = new_cost * (1 + fixed_profit)  # Atualiza o preco da venda
            save_data(inventory)
            print(Fore.GREEN + f"Custo e Venda atualizados! Nova venda: R${item['sale']:.2f}")
            if new_cost >= 500.00:
                manager_approval()
        
        elif option == "3":
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
        row = [index, item['name'], f"R$ {item['cost']:.2f}", f"R$ {item['sale']:.2f}", item['registration_date']]
        table_data.append(row)

    headers = ["ID", "Produto", "Custo", "Venda", "Data"]

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
                print(Fore.CYAN + "Saindo do sistema...")
                break
            case _:
                print(Fore.RED + "Opção inválida.\n")

if __name__ == "__main__":
    main()
