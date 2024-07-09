import mysql.connector
import csv

def addPokemon():
    connection = None
    try:
        print(f'Tentando conexão com o banco..')
        connexao = mysql.connector.connect(
        host='bd-pkm',
        user='root',
        password='123@123',
        database='padrao'
        )
        print(f'Conectado!')
    except Exception as erro:
        print(f'Erro de conexão: {erro}')

    cursor = connexao.cursor()
    print(f'lendo CSV')
    my_data = []
    with open('pokemonsimple.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            my_data.append(tuple(row))
    print(my_data)
    query = 'INSERT INTO padrao.POKEMON_INFO(id_pokedex, name_pokemon) VALUES (%s, %s)'
    cursor.executemany(query,my_data)

    connexao.commit()
    cursor.close()
    connexao.close()
    return {
        "status_code": 200,
        "body": "Inserção valida!"
    }


def consultPokemon(id_pokedex):
    connection = None
    try:
        print(f'Tentando conexão com o banco..')
        connexao = mysql.connector.connect(
        host='bd-pkm',
        user='root',
        password='123@123',
        database='padrao'
        )
        print(f'Conectado!')
    except Exception as erro:
        print(f'Erro de conexão: {erro}')
    
    cursor = connexao.cursor()
    
    query = f"SELECT * FROM POKEMON_INFO where id_pokedex = {id_pokedex}"
    cursor.execute(query)
    resultados = cursor.fetchall()

    print(type(resultados))
    print(resultados[0])

    connexao.commit()
    cursor.close()
    connexao.close()

    return resultados

def allPokemon():
    connection = None
    try:
        print(f'Tentando conexão com o banco..')
        connexao = mysql.connector.connect(
        host='bd-pkm',
        user='root',
        password='123@123',
        database='padrao'
        )
        print(f'Conectado!')
    except Exception as erro:
        print(f'Erro de conexão: {erro}')
    
    cursor = connexao.cursor()
    
    query = f"SELECT * FROM POKEMON_INFO"
    cursor.execute(query)
    resultados = cursor.fetchall()

    print(type(resultados))

    connexao.commit()
    cursor.close()
    connexao.close()

    return (query, resultados)

def cria_banco():
    connection = None
    try:
        print(f'Tentando conexão com o banco..')
        connexao = mysql.connector.connect(
        host='bd-pkm',
        user='root',
        password='123@123',
        database='padrao'
        )
        print(f'Conectado!')
    except Exception as erro:
        print(f'Erro de conexão: {erro}')
    
    cur = connexao.cursor()
    with open('bd-pkm-definition.sql', 'r') as sql_file:
        result_iterator = cur.execute(sql_file.read(), multi=True)
    for res in result_iterator:
        print("Running query: ", res)  # Will print out a short representation of the query
        print(f"Affected {res.rowcount} rows" )

    connexao.commit()
    cur.close()