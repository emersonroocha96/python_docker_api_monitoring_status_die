
### Código Comentado para Monitoramento de Containers

# -*- coding: utf-8 -*-

"""
Script de Monitoramento de Eventos Docker

Este script se conecta à API do Docker para monitorar eventos em tempo real.
Ele filtra especificamente por eventos 'die' (quando um container para/morre)
e envia uma notificação formatada para um webhook do Discord.
"""

# --- 1. Importação de Dependências ---
# Importamos as bibliotecas (toolkits) que usaremos no script.
import docker        # A biblioteca oficial do Docker para Python. Usada para se conectar ao daemon e ouvir eventos.
import datetime      # Usada para converter o timestamp do evento (um número) em uma data e hora legíveis.
import requests      # Usada para realizar requisições HTTP, especificamente para enviar a notificação (POST) ao Discord.


# --- 2. Configuração Inicial ---

# Inicializa o cliente Docker.
# docker.from_env() é o método preferido. Ele localiza automaticamente como se
# conectar ao daemon do Docker (seja via socket no Linux/macOS ou 
# named pipe no Windows) usando variáveis de ambiente padrão.
# É mais robusto e portável do que fixar um IP/porta como 'tcp://127.0.0.1:2375'.
client = docker.from_env()

# Define a URL do webhook do Discord para onde as notificações serão enviadas.
# IMPORTANTE: Mantenha esta URL em segredo, pois qualquer um com ela pode enviar mensagens para o seu canal.
webhook_url = "https://discord.com/api/webhooks/1433598870704881725/Kx-3QZM9LF2umXYm4rnt8ZTcDtAyD764LeFZ2IRsfNO57mNcDknHJ8DTAkwHbLJddEj7"

# Imprime uma mensagem no console para indicar que o script foi iniciado
# e está na fase de monitoramento. É uma boa prática de logging.
print("Monitorando eventos 'DIE' do docker...")


# --- 3. Loop Principal de Monitoramento ---

# Inicia o loop principal de escuta. Isso cria um "stream" de eventos do Docker.
# O script ficará "preso" aqui, esperando novos eventos chegarem.
#
# - client.events(): Conecta ao stream de eventos do Docker daemon.
# - decode=True: Garante que os eventos (que vêm como bytes JSON) sejam
#   automaticamente decodificados para dicionários Python, facilitando o acesso.
# - filters={"event": "die"}: É o filtro crucial. Dizemos ao Docker para nos
#   enviar *apenas* eventos do tipo 'die', ignorando 'start', 'create', 'pull', etc.
for event in client.events(decode=True, filters={"event": "die"}):
    
    # --- 4. Tratamento de Eventos e Exceções ---
    
    # Inicia um bloco 'try...except'. Isso é uma prática de programação defensiva.
    # Se um evento chegar malformado ou uma chave esperada não existir
    # (ex: um container sem nome), o script não irá "quebrar" e parar.
    # Ele apenas registrará o erro e continuará monitorando o próximo evento.
    try:
        # --- 5. Extração e Formatação de Dados ---
        
        # O 'event' é um dicionário Python. Acessamos seus dados usando chaves.
        container_id = event["id"]
        
        # O nome do container fica aninhado dentro de "Actor" -> "Attributes"
        container_name = event["Actor"]["Attributes"]["name"]
        
        # O 'time' do evento vem no formato "Epoch" (ou Unix Timestamp),
        # que é o número de segundos desde 1º de janeiro de 1970.
        epoch_time = event["time"]
        
        # Convertemos o timestamp Epoch em um objeto datetime legível.
        # Em seguida, formatamos (strftime) para o padrão "Ano-Mês-Dia Hora:Minuto:Segundo".
        # (CORREÇÃO: O seu código original usava %Y-%M-%D, que está incorreto.
        # %M é Minuto e %D é o formato americano mm/dd/yy. O correto é %Y-%m-%d).
        date_time = datetime.datetime.fromtimestamp(epoch_time).strftime('%Y-%m-%d %H:%M:%S')

        # --- 6. Montagem do Payload para o Discord ---
        
        # Montamos o dicionário (payload) que será enviado ao Discord.
        # O Discord espera um JSON que tenha uma chave principal chamada "content".
        # Usamos f-strings (ou %s como no seu original) para formatar a mensagem
        # de forma dinâmica, inserindo as variáveis que coletamos.
        # `container_id[:12]` pega apenas os 12 primeiros caracteres do ID (a versão curta).
        payload = {
            "content": f"🚨 **Container Parou!**\nO container `{container_name}` ({container_id[:12]}) foi finalizado às {date_time}"
        }

        # Imprime no console local o que será enviado.
        print(f"Evento Detectado: {payload}")

        # --- 7. Envio da Notificação ---
        
        # Usa a biblioteca 'requests' para enviar a notificação.
        # - requests.post(): Realiza uma requisição HTTP do tipo POST.
        # - webhook_url: O destino da requisição.
        # - json=payload: (CORREÇÃO: Seu código original usava data=payload).
        #   Usar `json=payload` é o método correto e mais robusto.
        #   A biblioteca 'requests' automaticamente converte o dicionário Python
        #   em uma string JSON e, crucialmente, define o cabeçalho
        #   'Content-Type' como 'application/json', que é o que o Discord espera.
        response = requests.post(webhook_url, json=payload)

        # --- 8. Verificação de Erro no Envio ---
        
        # Verifica o código de status HTTP da resposta do Discord.
        # Códigos 2xx (como 200 ou 204) significam sucesso.
        # Códigos 4xx (como 404 - não encontrado) ou 5xx (erro de servidor)
        # indicam que a notificação falhou (ex: URL do webhook errada, rate limit).
        if response.status_code >= 400:
            print(f"Erro ao enviar dados para o Discord: {response.status_code} - {response.text}")

    # Este é o bloco 'except' do 'try' lá de cima.
    # Se qualquer linha dentro do 'try' falhar, o código pula para cá.
    # 'Exception as e' captura o erro na variável 'e' e o imprime no console.
    except Exception as e:
        print(f"Erro ao processar evento: {e}")
        # O loop 'for' continua, esperando o próximo evento.
