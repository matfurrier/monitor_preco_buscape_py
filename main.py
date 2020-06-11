from crawl.baixar_pagina import Crawler
from parse.extrair_info import Parser
from persist.bd_persist import Conexao
from notify.notificacao import Alerta
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime as dt
import json


def realiza_busca():
    inicio = dt.now().strftime('%Y-%m-%d %H:%M')
    print('iniciando busca \nhorario: {}'.format(dt.now().strftime('%d/%m/%Y %H:%M:%S')))
    with open('configuracao.json', 'rb') as arquivo:
        configuracao = json.load(arquivo)
        for item_configuracao in configuracao['itens']:
            crawler = Crawler(item_configuracao['nome'], item_configuracao['ordenar_consulta'])
            pagina = crawler.obter_pagina()
            if pagina is not None:
                lista = Parser.separar_dados(pagina)
                if len(lista) > 0:
                    bd = Conexao(r'./persist/bd_info_buscape.db')
                    for item in lista.items():
                        bd.inserir_bd(item[1]['produto'].lower(), float(item[1]['valor'].replace('.', '')), item[1]['link'], item_configuracao['nome'], float(item_configuracao['preco_alvo']))
        alerta = Alerta(configuracao['email']['usuario'], configuracao['email']['senha'], bd)
        alerta.valida_envio_notificacao(configuracao, inicio)
        bd.desconectar_bd()
        print('busca concluida \nhorario: {} \n'.format(dt.now().strftime('%d/%m/%Y %H:%M:%S')))

if __name__ == '__main__':
    print('iniciando atividade de monitoramento {} \n'.format(dt.now().strftime('%d/%m/%Y %H:%M:%S')))
    agendador = BlockingScheduler()
    agendador.add_job(realiza_busca, 'interval', hours=1)
    agendador.start()
