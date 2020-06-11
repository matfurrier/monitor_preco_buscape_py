import requests


class Crawler:

    def __init__(self, item_pesquisa, ordenar_consulta):
        self.url = 'https://www.buscape.com.br/search'
        self.item_pesquisa = item_pesquisa
        self.ordenar_consulta = ordenar_consulta

    def obter_pagina(self):
        payload = {'no-shortcut': 1,
                   'page': 1,
                   'sortBy': self.ordenar_consulta,
                   'q': self.item_pesquisa}

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/83.0.4103.61 Safari/537.36'}
        try:
            solicitacao = requests.request("GET", self.url, headers=headers, params=payload)
            if solicitacao.status_code != 200 or 'card--' not in solicitacao.content.decode('utf-8'):
                solicitacao = None
            return solicitacao
        except Exception as err:
            print(err)
            return None
