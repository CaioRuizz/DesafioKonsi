import json
import re

import requests

import exceptions


class Crawler:
    def __init__(self):
        self.token = None


    def authenticate(self, login, senha):
        url = 'http://extratoblubeapp-env.eba-mvegshhd.sa-east-1.elasticbeanstalk.com/login'

        payload = json.dumps({
            'login': login,
            'senha': senha,
        })
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'Content-Type': 'application/json'
        }

        response = requests.request('POST', url, headers=headers, data=payload)

        token = response.headers.get('Authorization')

        if token is None:
            raise exceptions.LoginIncorretoException('Login ou senha invalidos')

        self.token = token

        return token


    def get_numeros_beneficios(self, cpf):
        
        url = f'http://extratoblubeapp-env.eba-mvegshhd.sa-east-1.elasticbeanstalk.com/offline/listagem/{cpf}'

        payload={}
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }

        response = requests.request('GET', url, headers=headers, data=payload)

        data = response.json()

        status = data.get('status')

        nome = data.get('nome')

        if status != 0:
            raise exceptions.LoginExpiradoException('e necessario fazer login antes de solicitar os dados')

        if nome is None:
            raise exceptions.CpfNaoEncontradoException('cpf não encontrado')

        beneficios = list(map(lambda x: x.get('nb'), data.get('beneficios')))

        return {
            'beneficios': beneficios
        }


