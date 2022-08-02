import os
import unittest

import sys

sys.path.append('./src')

from crawler import Crawler
import exceptions


class CrawlerTest(unittest.TestCase):

    def test_authenticate(self):
        crawler = Crawler()
        crawler.authenticate(os.environ.get('KONSI_USERNAME'), os.environ.get('KONSI_PASSWORD'))
        self.assertNotEqual(crawler.token, None)


    def test_get_data(self):
        crawler = Crawler()
        crawler.authenticate(os.environ.get('KONSI_USERNAME'), os.environ.get('KONSI_PASSWORD'))
        self.assertNotEqual(crawler.get_numeros_beneficios(os.environ.get('KONSI_CPF')).get('beneficios'), None)

    
    def test_login_with_wrong_credentials(self):
        crawler = Crawler()
        try:
            crawler.authenticate('wrong', 'credentials')
        except exceptions.LoginIncorretoException:
            return
        raise Exception('login funcionou com credenciais incorretas')


    def test_get_data_without_login(self):
        crawler = Crawler()
        try:
            crawler.get_numeros_beneficios(os.environ.get('KONSI_CPF'))
        except exceptions.LoginExpiradoException:
            return
        raise Exception('get_data funcionou sem login ')

    def test_get_data_with_invalid_cpf(self):
        crawler = Crawler()
        crawler.authenticate(os.environ.get('KONSI_USERNAME'), os.environ.get('KONSI_PASSWORD'))
        try:
            crawler.get_numeros_beneficios('1111111111')
        except exceptions.CpfNaoEncontradoException:
            return
        raise Exception('get_data funcionou com um cpf invalido')
        

if __name__ == '__main__':
    unittest.main()