import growattServer
import os
import datetime
import json
import vault_cli
import psycopg
import sys
import time
from dateutil import relativedelta
from dotenv import load_dotenv
from log import Log
from utils import Utils

# --- Padroniza mensagens de erro ---
def mensagem_error(mensagem, error):
    print(mensagem)
    log.error.error(mensagem)
    log.error.exception(error)
    sys.exit()

# --- Carrega as variávei do arquivo .env ---
load_dotenv()

# --- Inicia objetos ---
log = Log()
utils = Utils()

# --- Data do último processamento ---
with open('data_ultimo_processamento.txt', 'r') as arquivo:
    ultimo_processamento = arquivo.read()

# --- Primeiro dia do mês da data do último processamento ---
ultimo_processamento = datetime.datetime.strptime(ultimo_processamento, '%d/%m/%Y').date().replace(day=1)

# --- Conecta ao Vault e recupera os dados necessários para o processamento ---
try:
    vault = vault_cli.get_client(url=os.environ.get('VAULT_URL'), token=os.environ.get('VAULT_TOKEN'))
    loginGrowatt = vault.get_secret('secret/growatt', 'login')
    senhaGrowatt = vault.get_secret('secret/growatt', 'senha')
    energiaDBBase = vault.get_secret('secret/energia-service', 'energiaDBBase')
    energiaDBHost = vault.get_secret('secret/energia-service', 'energiaDBHost')
    energiaDBPass = vault.get_secret('secret/energia-service', 'energiaDBPass')
    energiaDBUser = vault.get_secret('secret/energia-service', 'energiaDBUser')
    log.info.info('Conexão com Vault realizada com sucesso')
except Exception as e:
    mensagem = 'Erro ao usar o Vault'
    mensagem_error(mensagem, e)

# --- Conecta ao banco de dados ---
try:
    conn = psycopg.connect(host=energiaDBHost, dbname=energiaDBBase, user=energiaDBUser, password=energiaDBPass)
    cur = conn.cursor()
    log.info.info('Conexão com PostgreSQL realizada com sucesso')
except Exception as e:
    mensagem = 'Erro ao usar PostgreSQL'
    mensagem_error(mensagem, e)

# --- Conecta a API da Growatt com retry ---
i = 0
for i in range(5):
    try:
        log.info.info('Tentativa de conexão com API Growatt: %s' % str(i+1))
        api = growattServer.GrowattApi(False, 'my-user-id' + utils.gerador_alfanumerico())
        login_response = api.login(loginGrowatt, senhaGrowatt)
        log.info.info('Conexão com Growatt realizada com sucesso')
    except Exception as e:
        error = e
        time.sleep(5)
        continue
    else:
        break
else:
    mensagem = 'Erro ao usar a API da Growatt'
    mensagem_error(mensagem, error)

i = 0
while i <= utils.diferenca_meses(ultimo_processamento):

    # --- Mês a ser processado ---
    data = ultimo_processamento + relativedelta.relativedelta(months=i)

    # --- Pega os dados da API referente ao mês processado ---
    retorno = api.plant_detail(805995, growattServer.Timespan.month, data)
    log.info.info('Pegou dados do mês %s com sucesso' % data)

    # --- Ordena os dados retornados por dia ---
    dias_ordenados = json.dumps(retorno['data'], sort_keys=True)

    # --- Processa cada dia do mês ---
    for dia, valor in json.loads(dias_ordenados).items():
        data_geracao = datetime.date(data.year, data.month, int(dia))
        cur.execute("SELECT * FROM geracao WHERE data = '%s'" % data_geracao)
        existe = len(cur.fetchall())
        
        if existe == 1:
            cur.execute("UPDATE geracao SET gerado = %s, atualizado = CURRENT_TIMESTAMP WHERE data = '%s'" % (valor, data_geracao))
        else:
            cur.execute("INSERT INTO geracao (data, gerado) VALUES ('%s', %s)" % (data_geracao, valor))
        
        log.info.info('Processou o dia %s com sucesso' % data_geracao)
        conn.commit()

    i += 1

# --- Atualiza data do último processamento ---
with open('data_ultimo_processamento.txt', 'w') as arquivo:
    arquivo.write(datetime.date.today().strftime('%d/%m/%Y'))