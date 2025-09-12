import csv

# Vetores para armazenar os dados em memória
culturas = []
areas = []
insumos = []
quantidades = []

# =============================
# Funcoes auxiliares
# =============================

def calcular_area(cultura):
    """Calcula a área do talhão com base na cultura."""
    if cultura.lower() == "milho":
        try:
            base = float(input("Digite a largura do talhão (metros): "))
            comprimento = float(input("Digite o comprimento do talhão (metros): "))
            return base * comprimento
        except ValueError:
            print("Erro: Valor inválido para as dimensões.")
            return 0
    elif cultura.lower() == "soja":
        try:
            raio = float(input("Digite o raio do pivô de soja (metros): "))
            return 3.14159 * (raio ** 2) # Usando um valor mais preciso para PI
        except ValueError:
            print("Erro: Valor inválido para o raio.")
            return 0
    else:
        print("Cultura não cadastrada.")
        return 0

def calcular_insumo():
    """Calcula a quantidade total de insumo necessário."""
    try:
        produto = input("Digite o nome do insumo: ")
        dose = float(input("Digite a quantidade aplicada por metro (mL ou kg/m): "))
        ruas = int(input("Digite o número de ruas: "))
        comprimento = float(input("Digite o comprimento de cada rua (metros): "))

        # A conversão para Litros/Kg é feita aqui
        total = (ruas * comprimento * dose) / 1000
        
        print(f"Será necessário {total:.2f} Litros/Kg de {produto}.")
        return produto, total
    except ValueError:
        print("Erro: Valor inválido inserido para o cálculo de insumo.")
        return None, 0

def salvar_csv():
    """Salva os dados da memória em um arquivo CSV com codificação UTF-8-SIG."""
    if not culturas:
        print("Nenhum dado para salvar. Cadastre uma cultura primeiro.")
        return

    # A principal correção está aqui: encoding='utf-8-sig'
    # O '-sig' adiciona um 'Byte Order Mark' (BOM) que ajuda o R e o Excel
    # a reconhecerem a codificação UTF-8 automaticamente.
    with open('dados_culturas.csv', mode='w', newline='', encoding='utf-8-sig') as arquivo:
        escritor = csv.writer(arquivo)
        # Cabeçalhos sem acentos para facilitar a leitura no R
        escritor.writerow(["Cultura", "Area_m2", "Insumo", "Quantidade"])
        for i in range(len(culturas)):
            escritor.writerow([culturas[i], areas[i], insumos[i], quantidades[i]])
    print("Dados salvos em 'dados_culturas.csv' com sucesso!")

# =============================
# Menu principal
# =============================

def menu():
    """Exibe o menu principal e gerencia as operações do programa."""
    while True:
        print("\n===== FARMTECH SOLUTIONS =====")
        print("1 - Entrada de dados de cultura")
        print("2 - Listar dados cadastrados")
        print("3 - Atualizar um dado")
        print("4 - Deletar um dado")
        print("5 - Salvar dados em CSV")
        print("0 - Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            cultura = input("Digite a cultura (Milho/Soja): ")
            area = calcular_area(cultura)
            
            if area > 0:
                insumo, qtd = calcular_insumo()
                if insumo is not None:
                    culturas.append(cultura)
                    areas.append(area)
                    insumos.append(insumo)
                    quantidades.append(qtd)
                    print("Dados cadastrados com sucesso!")
        
        elif opcao == "2":
            print("\n--- Dados Cadastrados ---")
            if not culturas:
                print("Nenhum dado cadastrado.")
            else:
                for i in range(len(culturas)):
                    print(f"[{i}] Cultura: {culturas[i]}, Area: {areas[i]:.2f} m², "
                          f"Insumo: {insumos[i]}, Quantidade: {quantidades[i]:.2f} L/Kg")
        
        elif opcao == "3":
            try:
                indice = int(input("Digite o índice que deseja atualizar: "))
                if 0 <= indice < len(culturas):
                    print(f"Atualizando dados da cultura {culturas[indice]}")
                    cultura = input("Nova cultura (Milho/Soja): ")
                    area = calcular_area(cultura)
                    if area > 0:
                        insumo, qtd = calcular_insumo()
                        if insumo is not None:
                            culturas[indice] = cultura
                            areas[indice] = area
                            insumos[indice] = insumo
                            quantidades[indice] = qtd
                            print("Dados atualizados com sucesso!")
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Erro: Índice deve ser um número.")

        elif opcao == "4":
            try:
                indice = int(input("Digite o índice que deseja deletar: "))
                if 0 <= indice < len(culturas):
                    culturas.pop(indice)
                    areas.pop(indice)
                    insumos.pop(indice)
                    quantidades.pop(indice)
                    print("Dado deletado com sucesso!")
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Erro: Índice deve ser um número.")

        elif opcao == "5":
            salvar_csv()
        
        elif opcao == "0":
            print("Saindo do programa...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

# =============================
# Executar programa
# =============================
if __name__ == "__main__":
    menu()
