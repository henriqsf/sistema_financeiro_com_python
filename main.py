from sistema import *

def main():
    while True:
        print("\n=== i-budget ===")
        print("1. Criar novo registro")
        print("2. Consultar registros")
        print("3. Atualizar registro")
        print("4. Deletar registro")
        print("5. Exportar relatório")
        print("6. Agrupar por tipo")
        print("0. Sair")

        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            montante = 0.0
            taxa = 0.0
            
            tipo = input("Informe o tipo (receita, despesa, investimento): ").lower()
            while tipo not in ["receita", "despesa", "investimento"]:
                print("Tipo inválido. Escolha entre receita, despesa ou investimento.")
                tipo = input("Informe o tipo (receita, despesa, investimento): ").lower()
                
            valor = float(input("Informe o valor: "))
            while valor <= 0:
                print("O valor deve ser positivo.")
                valor = float(input("Informe o valor: "))
                
            if tipo == "despesa":
                valor *= -1 
            if tipo == "investimento":
                taxa = float(input("Informe o valor da taxa em porcentos (a.m.): "))
                
            registro = cria_registro(tipo, valor, montante, taxa)
            grava_registro(registro)
            print("Registro criado com sucesso!")

        elif escolha == "2":
            opcao_consulta = input("Deseja consultar por id/mês/tipo/valor): ").lower()
            if opcao_consulta in ["id", "mês", "mes", "tipo", "valor"]:
                termo = input(f"Informe o {opcao_consulta}: ")
                if opcao_consulta == "mes" or opcao_consulta == "mês":
                    opcao_consulta = "mes"
                resultados = consulta_registros(**{opcao_consulta: termo})
                if resultados:
                    print("Registros encontrados:")
                    for resultado in resultados:
                        print(resultado)
                else:
                    print("Nenhum registro encontrado.")
            else:
                print("Opção de consulta inválida.")

        elif escolha == "3":
            id_registro = input("Informe o ID do registro a ser atualizado: ")
            tipo_atualizacao = input("Atualizar por (valor/tipo): ").lower()
            if tipo_atualizacao in ["valor", "tipo"]:
                novo_valor = float(input("Novo valor: ")) if tipo_atualizacao == "valor" else None
                while tipo_atualizacao == "valor" and novo_valor <= 0:
                    print("O valor deve ser positivo.")
                    novo_valor = float(input("Novo valor: "))
                    
                novo_tipo = input("Novo tipo (receita, despesa, investimento): ") if tipo_atualizacao == "tipo" else None
                while tipo_atualizacao == "tipo" and novo_tipo not in ["receita", "despesa", "investimento"]:
                    print("Tipo inválido. Escolha entre receita, despesa ou investimento.")
                    novo_tipo = input("Novo tipo (receita, despesa, investimento): ")
                    
                taxa = float(input("Informe a taxa de investimento: ")) if novo_tipo == "investimento" else None
                atualiza_registro(id_registro, valor=novo_valor, tipo=novo_tipo, taxa=taxa)
                print("Registro atualizado com sucesso!")
            else:
                print("Opção de atualização inválida.")

        elif escolha == "4":
            id_delecao = input("Informe o ID do registro a ser deletado: ")
            if deleta_registro(id_delecao):
                print(f"Registro com id {id_delecao} deletado com sucesso!")
            else:
                print(f"Não existe registro com o id {id_delecao} a ser deletado!")

        elif escolha == "5":
            formato_exportacao = input("Informe o formato de exportação (csv/json): ").lower()
            exportar_relatorio(formato_exportacao)
            print(f"Relatório exportado com sucesso para relatorio.{formato_exportacao}")

        elif escolha == "6":
            agrupa_por_tipo()

        elif escolha == "0":
            print("Saindo do sistema. Até mais!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
