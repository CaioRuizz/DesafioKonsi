import json

from flask import Flask
from flask_restful import Api

from routes.numeros_beneficios import NumerosBeneficios

app = Flask(__name__)
api = Api(app)
 
api.add_resource(NumerosBeneficios, '/extratoclube/numeros_beneficios')

if __name__ == '__main__':
    app.run('0.0.0.0', '80')
