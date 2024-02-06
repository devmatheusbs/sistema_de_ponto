#SQL-DB
import sqlite3
def criardb():
    try:
        con = sqlite3.connect('controle_de_ponto.db')        
    except sqlite3.Error as e: 
        print(' O banco de dados não está acessível')

    #criar tabela usuario    
    try:
        with con:
            cur = con.cursor()
            cur.execute(""" CREATE TABLE IF NOT EXISTS usuarios(
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome VARCHAR(60) NOT NULL,
                email VARCHAR(80) NOT NULL UNIQUE,
                telefone VARCHAR(12),
                sexo VARCHAR(12),            
                data_nascimento DATE NOT NULL,
                cpf CHAR(11) NOT NULL UNIQUE
                )""")
        
    except sqlite3.Error as e:
        print('Erro ao criar a tabela de horas', e)
    #criar tabela registrodeponto
    try:
        with con:
            cur= con.cursor()
            cur.execute(""" CREATE TABLE IF NOT EXISTS ponto(
                id_ponto INTEGER PRIMARY KEY, 
                usuario_cpf CHAR(11),
                data DATE,
                ponto_entrada_manha TIME,
                ponto_saida_manha TIME,
                ponto_entrada_tarde TIME,
                ponto_saida_tarde TIME,
                FOREIGN KEY (usuario_cpf) REFERENCES usuario (cpf)
                )""")
         
    except sqlite3.Error as e:
        print('Erro ao criar a tabela ponto ', e)