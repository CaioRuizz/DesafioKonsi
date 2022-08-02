#!/bin/bash

. ./setup_env.sh

response=$(python3 -c "import json, os, requests;url = 'http://localhost/extratoclube/numeros_beneficios';payload = json.dumps({'login':os.environ.get('KONSI_USERNAME'),'password':os.environ.get('KONSI_PASSWORD'),'cpf':os.environ.get('KONSI_CPF')});headers = {'Content-Type': 'application/json'};response = requests.request('POST', url, headers=headers, data=payload);print(response.status_code)")

if [[ $response == "200" ]]; then
    echo "success"
    exit 0
else
    echo "fail wih code $response"
    exit 1
fi

