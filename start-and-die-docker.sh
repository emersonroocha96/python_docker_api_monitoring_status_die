#!/bin/sh

# ==============================================================================
# == SCRIPT DE TESTE PARA O MONITORAMENTO DOCKER (events.py) ==
#
# ATENÇÃO: Este script NÃO deve ser executado sozinho.
# Ele serve apenas para GERAR ATIVIDADE no Docker e testar se o script
# 'events.py' está capturando os eventos corretamente.
#
# O QUE ELE FAZ:
# 1. Inicia 5 (cinco) contêineres "nginx" em modo background (-d).
# 2. Assim que os 5 são iniciados, ele imediatamente PARA todos os
#    contêineres que estão em execução.
#
# COMO USAR CORRETAMENTE:
# 1. Em um terminal, inicie o script de monitoramento primeiro:
#    $ python3 events.py
#
# 2. Em OUTRO terminal, execute este script para gerar os eventos:
#    $ ./start-and-die-docker.sh
#
# Se tudo funcionar, você deverá ver o 'events.py' (no primeiro terminal)
# reportar os eventos de "start" e "stop" que este script causou.
# ==============================================================================

# Inicia 5 contêineres nginx
echo "Iniciando 5 contêineres Nginx para teste..."
for i in `seq 5`; do
    docker run -d nginx
done

# Para todos os contêineres em execução
# (O `docker ps -q` lista apenas os IDs dos contêineres ativos)
echo "Parando todos os contêineres..."
docker stop `docker ps -q`

echo
