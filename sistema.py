import uuid
import json
from datetime import datetime

def gera_id() -> str:
    """Gera um ID único."""
    return str(uuid.uuid4())

def registra_data():
    """Captura a data atual e retorna os campos no formato desejado."""
    data_atual = datetime.now()
    return {
        "dia": data_atual.day, 
        "mes": data_atual.month, 
        "ano": data_atual.year
    }

def cria_registro(tipo: str, valor: float, montante: float, taxa: float):
    """Cria um novo registro. Um registro representa uma entrada do usuário sob uma atividade financeira."""
    id = gera_id()
    data_atual = registra_data()
    return {
        "id": id,
        "dia": data_atual["dia"],
        "mes": data_atual["mes"],
        "ano": data_atual["ano"],
        "tipo": tipo,
        "valor": valor,
        "montante": montante,
        "taxa": taxa
    }

def recupera_todos_registros():
    """Abre arquivo de registros e retorna as entradas em formato JSON."""
    try:
        with open("registros.json", "r") as arquivo_registros:
            return json.load(arquivo_registros)["registros"]
    except FileNotFoundError:
        print("Arquivo de registros não encontrado.")
        return []

def consulta_registros(id: str = None, mes = None, tipo: str = None, valor: float = None) -> list:
    """Consulta os registros armazenados por id, mes, tipo ou valor."""
    registros = recupera_todos_registros()
    lista_registros = list()
    
    for registro in registros:
        if id and registro['id'] == id:
            lista_registros.append(registro)
        elif mes and registro['mes'] == int(mes):
            lista_registros.append(registro)
        elif tipo and registro['tipo'] == tipo:
            lista_registros.append(registro)
        elif valor is not None and registro['valor'] == float(valor):
            lista_registros.append(registro)
    
    return lista_registros


def atualiza_registro(id: str, valor: float = None, tipo: str = None, taxa: float = None):
    """Atualiza um campo de um registro. O campo de data deverá ser preenchido com a data da atualização."""
    nova_data = registra_data()
    registro_alvo = consulta_registros(id=id)
    if not registro_alvo:
        print("Registro não encontrado.")
        return

    registro_alvo = registro_alvo[0]
    
    if valor is not None:
        registro_alvo["valor"] = valor
    if tipo is not None:
        if tipo == "investimento":
            if registro_alvo["valor"] < 0:
                registro_alvo["valor"] *= -1
            registro_alvo["montante"] += calculo_montante(registro_alvo, nova_data, taxa)
        if tipo == "despesa" and registro_alvo["tipo"] != "despesa":
            registro_alvo["valor"] *= -1
        registro_alvo["tipo"] = tipo
    registro_alvo["dia"] = nova_data["dia"]
    registro_alvo["mes"] = nova_data["mes"]
    registro_alvo["ano"] = nova_data["ano"]
    deleta_registro(id)
    grava_registro(registro_alvo)

def grava_registro(registro):
    """Grava um registro no arquivo de registros."""
    dados = recupera_todos_registros()
    dados.append(registro)
    
    with open("registros.json", "w") as arquivo_registros:
        json.dump({"registros": dados}, arquivo_registros, indent=4)

def calculo_montante(registro_alvo, nova_data, taxa):
    """Calcula o valor do montante a partir da fórmula: M = C * (1 + i)^t."""
    taxa /= 100
    meses = (nova_data["ano"] - registro_alvo["ano"]) * 12 + (nova_data["mes"] - registro_alvo["mes"])
    return registro_alvo["valor"] * (1 + taxa) ** meses

def deleta_registro(id: str) -> bool:
    """Deleta um registro a partir de seu ID."""
    todos_registros = recupera_todos_registros()
    lista_registros = [registro for registro in todos_registros if registro["id"] != id]
    if len(todos_registros) - len(lista_registros) == 1:
        sobrescreve_registros_arquivo(lista_registros=lista_registros)
        return True
    return False

def sobrescreve_registros_arquivo(lista_registros: list):
    """A partir de uma lista de registros, sobrescreve o arquivo de registros."""
    with open("registros.json", "w") as arquivo_registros:
        json.dump({"registros": lista_registros}, arquivo_registros, indent=4)

def exportar_relatorio(formato: str = "json"):
    """Exporta um relatório em CSV ou JSON."""
    registros = recupera_todos_registros()
    
    if formato == "csv":
        with open("relatorio.csv", "w") as arquivo_csv:
            arquivo_csv.write("ID,Dia,Mes,Ano,Tipo,Valor,Montante\n")
            for registro in registros:
                if registro['tipo'] == 'investimento':
                    nova_data = registra_data()
                    registro['montante'] = calculo_montante(registro, nova_data, registro['taxa'])
                linha = f"{registro['id']},{registro['dia']},{registro['mes']},{registro['ano']},{registro['tipo']},{registro['valor']},{registro['montante']}\n"
                arquivo_csv.write(linha)
    elif formato == "json":
        temp_registros = registros
        for registro in temp_registros:
            if registro['tipo'] == 'investimento':
                nova_data = registra_data()
                registro['montante'] = calculo_montante(registro, nova_data, registro['taxa'])
                tamanho_registros = len(registros)
                contador = 0
                while (contador < tamanho_registros):
                    if registros[contador]['id'] == registro['id']:
                        registros[contador] = registro
                    contador += 1
        with open("relatorio.json", "w") as arquivo_json:
            json.dump({"registros": registros}, arquivo_json, indent=4)
    else:
        print("Formato de exportação não suportado.")


def agrupa_por_tipo():
    """Agrupa os registros por tipo e mostra o total de valores para cada tipo."""
    registros = recupera_todos_registros()
    total_por_tipo = {}

    for registro in registros:
        tipo = registro["tipo"]
        valor = registro["valor"]
        if tipo not in total_por_tipo:
            total_por_tipo[tipo] = 0
        total_por_tipo[tipo] += valor

    for tipo, total in total_por_tipo.items():
        print(f"Tipo: {tipo}, Total: {total}")


