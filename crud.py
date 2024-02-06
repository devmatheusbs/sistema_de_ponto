import sqlite3 as lite
import arrow

def adicionar_usuario(i):
    con = lite.connect('controle_de_ponto.db')
    cur = con.cursor()
    try:
        query = '''
        INSERT INTO usuarios (nome, email, telefone, sexo, data_nascimento, cpf) VALUES (?,?,?,?,?,?)
        '''
        cur.execute(query, i)
        con.commit()
    except lite.Error as e:
        print('Erro ao criar usuário', e)
    finally:
        cur.close()
        con.close()

def ver_usuarios():
    lista = []
    con = lite.connect('controle_de_ponto.db')
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM usuarios')
        linha = cur.fetchall()
        for i in linha:
            lista.append(i)
        return lista
    except lite.Error as e:
        print('Erro ao consultar usuários', e)
    finally:
        cur.close()
        con.close()

def atualizar_usuario(nome, email, telefone, sexo,data_nascimento, cpf, id):
    con = lite.connect('controle_de_ponto.db')
    cur = con.cursor()
    try:
        query = '''
        UPDATE usuarios SET nome=?, email=?, telefone=?, sexo=?, data_nascimento?, cpf=?, WHERE id=?
        '''
        cur.execute(query, nome, email, telefone, sexo,data_nascimento, cpf, id)
    except lite.Error as e:
        print('Erro ao atualizar usuário', e)
    finally:
        cur.close()
        con.close()

def deletar_usuario(cpf):
    con = lite.connect('controle_de_ponto.db')
    cur = con.cursor()
    try:
        query = 'DELETE FROM usuarios WHERE cpf=?'
        cur.execute(query,(cpf,))
    except lite.Error as e:
        print('Erro ao deletar usuário', e)
    finally:
        cur.close()
        con.close()

def ponto_entrada_manha(cpf_usuario):
    con = lite.connect('controle_de_ponto.db')
    cur = con.cursor()
    try:
        hora = hora_atual()
        data = "2024-02-06"
        cur.execute("SELECT COUNT(*) FROM ponto WHERE usuario_cpf = ? AND data=?" , (cpf_usuario,data))
        resultado = cur.fetchone()    
        if resultado[0] == 0:
            query = "INSERT OR IGNORE INTO ponto (usuario_cpf, data, ponto_entrada_manha) VALUES (?,?,?)"        
            cur.execute(query, (cpf_usuario, data, hora))
            con.commit()
            print('Entrada manhã: ponto inserido')
        else:
            print('Já existe um ponto para o mesmo CPF e data. Não é possível repetir.')        
    except lite.Error as e:
        print('Erro ao inserir ponto de entrada', e)
    finally:
        cur.close()
        con.close()

def ponto_saida_manha(cpf_usuario):
    con = lite.connect('controle_de_ponto.db')
    cur = con.cursor()
    data = "2024-02-06"
    try:
        cur.execute("SELECT * FROM ponto WHERE usuario_cpf = ? AND data=?", (cpf_usuario, data))
        resultado = cur.fetchone()
        hora = hora_atual()           
        if isinstance(resultado, tuple) and len(resultado) >= 7: 
            if resultado[4]== None and resultado[5]== None and resultado[6]== None and resultado[3] != None:
                query = "UPDATE ponto SET ponto_saida_manha = ? WHERE usuario_cpf=? AND data=?"        
                cur.execute(query,(hora, cpf_usuario, data))
                con.commit()
                print('Saída manhã: ponto inserido com sucesso')
            else:
                print('Já existe um ponto para o mesmo CPF e data, não é possível repetir. Ou ponto anterior não registrado')
        else:
            print('Ponto entrada do dia ainda não registrado')
    except lite.Error as e:
        print('Erro ao inserir ponto de saída', e)
    finally:
        cur.close()
        con.close()
        
def ponto_entrada_tarde(cpf_usuario):
    con = lite.connect('controle_de_ponto.db')
    cur = con.cursor()
    data = "2024-02-06"
    try:
        cur.execute("SELECT * FROM ponto WHERE usuario_cpf = ? AND data=?", (cpf_usuario, data))
        resultado = cur.fetchone()
        hora = hora_atual()
        if isinstance(resultado, tuple) and len(resultado) >= 7:       
            if resultado[5] == None and resultado[6] == None and resultado[3] != None and resultado[4] != None:
                query = "UPDATE ponto SET ponto_entrada_tarde = ? WHERE usuario_cpf=? AND data=?"        
                cur.execute(query,(hora, cpf_usuario, data))
                con.commit()
                print('Entrada Tarde: ponto inserido com sucesso')
            else:
                print('Já existe um ponto para o mesmo CPF e data. Não é possível repetir. Ou ponto anterior não registrado')
        else:
            print('Ponto de entrada do dia ainda não registrado')
    except lite.Error as e:
        print('Erro ao inserir ponto de entrada', e)
    finally:
        cur.close()
        con.close()
        
def ponto_saida_tarde(cpf_usuario):
    con = lite.connect('controle_de_ponto.db')
    cur = con.cursor()    
    data = "2024-02-06" 
    try:
        cur.execute("SELECT * FROM ponto WHERE usuario_cpf = ? AND data=?", (cpf_usuario, data))
        resultado = cur.fetchone()
        hora = hora_atual()
        if isinstance(resultado, tuple) and len(resultado) >= 7:           
            if resultado[6] is None and resultado[3] is not None and resultado[4] is not None and resultado[5] is not None:
                query = "UPDATE ponto SET ponto_saida_tarde= ? WHERE usuario_cpf=? AND data=?"        
                cur.execute(query,(hora, cpf_usuario, data))
                con.commit()
                print('Saída tarde: ponto inserido com sucesso')
            else:
                print('Já existe um ponto para o mesmo CPF e data. Não é possível repetir.')
        else:
            print('Ponto de entrada do dia ainda não registrado')
    except lite.Error as e:
        print('Erro ao inserir ponto de saída', e)
    finally:
        cur.close()
        con.close()

def ver_ponto(cpf):
    con = lite.connect('controle_de_ponto.db')
    cur = con.cursor()
    try:
        query = "SELECT * FROM ponto WHERE usuario_cpf = ?"        
        cur.execute(query, (cpf,))
        resultado = cur.fetchall()
        print(f'Pontos registrado no {cpf}: ')
        for linha in resultado:
            print(f'Data: {linha[2]}, Entrada manhã: {linha[3]}, Saída manhã: {linha[4]}, Entrada tarde: {linha[5]}, Saída tarde: {linha[6]}') 
    except lite.Error as e:
        print('Erro ao consultar usuários', e)
    finally:
        cur.close()
        con.close()
        
def deletar_ponto(cpf,data):
    conexao = lite.connect('controle_de_ponto.db')
    cursor = conexao.cursor()
    try:
        # Verificar se existe um registro para o mesmo CPF e data
        cursor.execute("SELECT COUNT(*) FROM ponto WHERE usuario_cpf = ? AND data = ?", (cpf, data))
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            # Se existe, deletar o ponto
            query_delete = "DELETE FROM ponto WHERE usuario_cpf = ? AND data = ?"
            cursor.execute(query_delete, (cpf, data))
            conexao.commit()
            print("Ponto deletado com sucesso!")

        else:
            print("Não existe ponto registrado para o mesmo CPF e data.")

    except lite.Error as e:
        print("Erro ao deletar ponto:", e)

    finally:
        cursor.close()
        conexao.close()

def data_atual():
    data_atual = arrow.now().format('YYYY-MM-DD')
    return data_atual    
def hora_atual():
    hora_atual = arrow.now().format('HH:mm:ss')
    return hora_atual