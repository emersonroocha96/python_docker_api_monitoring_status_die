Guide/Guia:
1 - Version English 
2 - Versão Português-BR

================================================
Docker Container Monitoring with Discord Alert
================================================

This project contains two main scripts:

1- events.py
   - This is the main monitoring script.
   - It uses Python to connect to the Docker API and listen
     for specific events (when a container 'dies').
   - When a container stops- it sends an alert to Discord.

2- start-and-die-docker.sh
   - This is a TEST script.
   - Its only purpose is to generate Docker activity to verify
     if the monitor (events.py) is working.
   - It starts 5 containers and then immediately stops them all.


HOW TO USE CORRECTLY
======================

You must run the scripts in TWO separate terminals.
The order is very important.

Step 1- In Terminal 1- Start the monitor (the .py script):
python3 events.py

(You will see the message "Monitorando eventos 'DIE' do docker...")


Step 2- In Terminal 2- Run the test script (the .sh script):
./start-and-die-docker.sh


Result:
When you run the .sh script- you will see Terminal 1 (with the .py script)
display alerts for the containers that stopped- and send them
to Discord.

_____________________________________________________________________________________

==================================================
Monitoramento de Containers Docker com Alerta Discord
==================================================

Este projeto contem dois scripts principais:

1- events.py
   - Este e o script de monitoramento principal.
   - Ele usa Python para se conectar a API do Docker e ficar
     escutando por eventos especificos (quando um container 'morre').
   - Quando um container para- ele envia um alerta para o Discord.

2- start-and-die-docker.sh
   - Este e um script de TESTE.
   - Ele serve apenas para gerar atividade no Docker e verificar
     se o monitoramento (events.py) esta funcionando.
   - Ele inicia 5 containers e depois para todos eles imediatamente.


COMO USAR CORRETAMENTE
========================

Voce deve rodar os scripts em DOIS TERMINAIS separados.
A ordem e muito importante.

Passo 1- No Terminal 1- Inicie o monitor (o script .py):
python3 events.py

(Voce vera a mensagem "Monitorando eventos 'DIE' do docker...")


Passo 2- No Terminal 2- Execute o script de teste (o script .sh):
./start-and-die-docker.sh


Resultado:
Ao rodar o script .sh- voce vera o Terminal 1 (com o script .py)
mostrar os alertas dos containers que pararam- enviando-os
para o Discord.
