import cx_Oracle
import pandas as pd
import json

def conectar_oracle(user, password, dsn):
    try:
        conn = cx_Oracle.connect(user, password, dsn)
        return conn
    except cx_Oracle.Error as error:
        print(f"Erro ao conectar ao banco de dados: {error}")
        return None

def executar_consulta(conn, query):
    try:
        df = pd.read_sql(query, con=conn)
        
        # Converte colunas de int64 e float64 para int e float padrão do Python
        df = df.applymap(lambda x: int(x) if isinstance(x, pd.Int64Dtype) else float(x) if isinstance(x, pd.Float64Dtype) else x)
        
        return df
    except cx_Oracle.Error as error:
        print(f"Erro ao executar a consulta: {error}")
        return None

def dataframe_para_json(df):
    # Agrupar os dados por Estab e IdCarrinho
    grouped = df.groupby(['ESTAB', 'IDCARRINHO'])

    # Criar uma lista de dicionários para cada grupo
    data = []
    for (estab, id_carrinho), group in grouped:
        # Converte para tipos compatíveis com JSON (int e float)
        produtos = group.to_dict(orient='records')
        data.append({
            "Estab": int(estab),
            "IdCarrinho": int(id_carrinho),
            "Produtos": produtos
        })

    # Converter a lista de dicionários para JSON
    json_data = json.dumps(data, indent=4)

    return json_data

def realiza_conn(idcarrinho):
    # Exemplo de uso:
    user = 'VIASOFTMCP'
    password = 'VIASOFTMCP'
    dsn = '192.168.90.224:1521/VIASOFT'  # Exemplo: localhost/orcl

    conn = conectar_oracle(user, password, dsn)

    if conn:
        query = """SELECT CI.ESTAB, CI.IDCARRINHO, CI.SEQITEM, CI.IDITEM, I.DESCRICAO,
                CI.QUANTIDADE, CI.VALORUNIT, CI.DESCITEM, CI.CUSTOAQUIS, CI.VALORC,
                CI.DESCMAX, CI.VALORMINIMO, 30 AS MARGEM FROM CARRINHOITEM CI 
                LEFT JOIN USANDODE US ON US.ESTAB = CI.ESTAB AND US.TABELA = 'ITEM'
                LEFT JOIN ITEM I ON I.ESTAB = US.USADE AND I.IDITEM = CI.IDITEM
                WHERE CI.ESTAB = 500 AND IDCARRINHO = """ + str(idcarrinho) 
        resultado = executar_consulta(conn, query)

        if resultado is not None:
            json_orcamento = dataframe_para_json(resultado)
            #print(json_orcamento)

            conn.close()
            return json_orcamento
        else:
            print("Consulta não retornou resultados.")
            
            conn.close()
            return ""

        
