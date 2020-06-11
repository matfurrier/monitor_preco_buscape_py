from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import smtplib

import pandas as pd


class Alerta:

    def __init__(self, usuario, senha, bd):
        self.usuario = usuario
        self.senha = senha
        self.bd = bd

    def enviar_alerta(self, assunto, corpo, para):
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        smtpserver.login(self.usuario, self.senha)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = assunto
        msg['From'] = self.usuario
        msg['To'] = ", ".join(para)
        msg.attach(MIMEText(corpo, 'html'))
        smtpserver.sendmail(self.usuario, para, msg.as_string())
        smtpserver.close()

    def valida_envio_notificacao(self, configuracao, inicio):
        fim = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        resultado = self.bd.consultar_bd('''select id, produto, valor, item_alvo, valor_alvo, link
                                FROM tb_dados_buscape
                                where valor_alvo >= valor
                                    and notificado = 0
                                    and data_consulta between '{}'
                                        and '{}' '''.format(inicio, fim))
        if len(resultado) > 0:
            tabela = pd.DataFrame(resultado, columns=['id', 'produto', 'valor', 'item_alvo', 'valor_alvo', 'link'])
            self.enviar_alerta('Notificacao produto encontrado',
                               'Segue a lista de produto(s) encontrados: <p>' + tabela.to_html(),
                               configuracao['notificacao'])

            self.bd.atualizar_bd('''update tb_dados_buscape 
                    set notificado = 1
                    where id in ({})'''.format(', '.join([str(x) for x in tabela['id']])))
            print('notificação enviada com sucesso')
        else:
            print('nenhum item atendeu ao requesito da busca')
        self.bd.desconectar_bd()
