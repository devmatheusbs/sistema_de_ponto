#CRUD DE CONTROLE DE HORAS
#INPUT - ENTRADA - HORAS
#INPUT - SAIDA - HORAS
import util
import crud
import creatdb
from time import sleep

#creatdb.criardb()
#usuario = ("matheus", "matheus@gmail.com", "6299889850", "masculino", "1994-12-08", "75106248191")
#crud.adicionar_usuario(usuario)
cpf = "75106248191"
crud.ponto_entrada_manha(cpf)
sleep(3)
crud.ponto_saida_manha(cpf)
sleep(3)
crud.ponto_entrada_tarde(cpf)
sleep(3)
crud.ponto_saida_tarde(cpf)
sleep(3)
crud.ver_ponto(cpf)
