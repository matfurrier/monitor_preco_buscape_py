from bs4 import BeautifulSoup as bs


class Parser:

    def separar_dados(pagina):
        lista = {}
        indice = 0
        if pagina is not None:
            pagina_parse = bs(pagina.content, 'lxml')
            print('quantidade de produtos encontrados: {}'.format(len(pagina_parse.select('div[class*=card--]'))))
            if len(pagina_parse.select('div[class*=card--]')) > 0:
                for produto in pagina_parse.select('div[class*=card--]'):
                    if not 'Produto indisponível' in produto.text:
                        try:
                            lista['produto{}'.format(indice)] = {
                                'produto': produto.select('[class=cardBody] > a')[0].attrs['title'].strip(),
                                'valor': produto.select('[class=customValue] > span')[0].text.replace('R$',
                                                                                                      '').strip(),
                                'link': 'https://www.buscape.com.br/' +
                                        produto.select('[class=cardBody] > a')[0].attrs['href'].strip()}
                        except Exception as err:
                            print('erro: {} no indice: {}'.format(err, 'produto{}'.format(indice)))
                        indice += 1
        return lista
