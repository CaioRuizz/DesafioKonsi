import json

from flask import request
from flask_restful import Resource

from crawler import Crawler
import exceptions

class NumerosBeneficios(Resource):
    def __init__(self):
        self.crawler = Crawler()

    def post(self):
        data = request.json
        if not all([
            'login' in data,
            'password' in data,
            'cpf' in data,
        ]):
            return {
                'message': 'está faltando login, passord ou cpf',
            }, 400

        response = {}

        try:
            self.crawler.authenticate(str(data.get('login')), str(data.get('password')))
            response = self.crawler.get_numeros_beneficios(str(data.get('cpf')))

        except exceptions.LoginIncorretoException:
            return {
                'message': 'usario e/ou senha incorreto(s)',
            }, 403

        except exceptions.CpfNaoEncontradoException:
            return {
                'message': 'CPF não encontrado',
            }, 404
        
        return response, 200