
# Desafio-Konsi
Desafio técnico para aplicação na vaga de desenvolvedor back-end na empresa Konsi

# Objetivo

O objetivo do desafio é desenvolver uma API que receberá o CPF do cliente e as credenciais de login do [portal extratoclube](http://extratoclube.com.br/) e retorne a matrícula do servidor no portal.

# Serviços

Será utilizada a arquitetura de microsserviços e os serviços serão os seguintes:

- extratoclube

O Crawler será o responsável por extrair os dados do portal, simulando as requisições que seriam feitas pelo navegador e extraindo as informações desejadas do html.

- nginx

O nginx será utilizado para servir o crawler de forma segura, veloz e escalável.


# Desenvolvimento do Crawler

será necessário criar solicitações HTTP para simular o navegador no portal, para criar essas solicitações, utilizarei o aplicativo [postman](https://www.postman.com/) e a extensão do Google Chrome [postman interceptor](https://chrome.google.com/webstore/detail/postman-interceptor/aicmkgpgakddgnaphhhpliifpcfhicfo)

Ao analisar as solicitações, identifiquei que seria necessário utilizar as seguintes rotas:


## Login - POST

### URL

http://extratoblubeapp-env.eba-mvegshhd.sa-east-1.elasticbeanstalk.com/login

### Uso

essa rota será utilizada para realizar a autenticação e obter o token de acesso

### Parâmetros

os seguintes parâmetros são passados pelo corpo da requisição em formato json:

- login

string com o nome de usuário

- senha

string com a senha

### Resposta

A resposta é um corpo vazio, mas utilizaremos um dos cabeçalhos de resposta, o Authorization, que contem o token de acesso.

Caso o token venha vazio, significa que o usuário e/ou a senha estão incorretos.

## Listagem - GET

### URL

http://extratoblubeapp-env.eba-mvegshhd.sa-east-1.elasticbeanstalk.com/offline/listagem/{CPF}

### Uso

essa rota será utilizada para listar os benefícios

### Parâmetros

os seguintes parâmetros são passados pela url:

- CPF

string ou inteiro com o cpf a ser consultado

os seguintes parâmetros deverão ser passados no cabeçalho:

- Authorization

string com o token de acesso

### Resposta

A resposta é um corpo no formato json contendo as informações sobre o CPF consultado, dessas informações utilizaremos as informações de benefícios e pegaremos apenas o campo "nb" (número do benefício) de cada benefício.

# Tornando o crawler acessível

Para tornar o Crawler acessível, será utilizado um servidor HTTP com flask para que o Crawler se torne acessível através de solicitação HTTP.

## Rotas

A única rota do Crawler será `/extratoclube/numeros_beneficios`, que retornará a lista com os números dos benefícios ou com a mensagem de erro.

### Parâmetros

Será necessário passar os seguintes parâmetros no corpo da requisição no formato json:

- login

string com o nome de usuário

- senha

string com a senha

- cpf

string ou inteiro com o cpf a ser consultado

### Resposta

Será retornado um corpo no formato json com uma das seguintes informações

- beneficios

lista com os números dos benefícios

- message

mensagem de erro caso ocorra algum erro

### Possíveis erros

- Login ou Senha incorretos

- CPF não encontrado

- Ausência de parâmetros

# Executando o projeto

Caso você não tenha o docker instalado em seu computador, instale-o seguindo este [passo-a-passo](https://docs.docker.com/engine/install/).

Com o docker instalado em seu computador basta executar o seguinte comando na raíz do projeto:

> docker compose up -d --build

Então a API ficará disponível na porta 80 e poderá ser acessado em: [`http://localhost/`](http://localhost/)

# Testando o código

A primeira coisa a se fazer é criar um arquivo shamado setup_env.sh na raíz do projeto no seguinte formato:

```
#!/bin/bash

export KONSI_USERNAME="SEU NOME DE USUARIO"
export KONSI_PASSWORD="SUA SENHA"
export KONSI_CPF="CPF VALIDO COM BENEFICIOS"
```

## Testes unitários

para executar os testes unitários, basta ir até a pasta crawler através do comando

> cd services/crawler

e então executando o script `test.sh`

> ./test.sh

## Teste integrado

para executar o teste integrado, o projeto deverá estar sendo executado, então basta executar o seguinte comando:

> ./integration_test.sh

# Escalabilidade

Para escalar um crawler, adicionando novas rotas e funcionalidades à ele, basta alterar a classe Crawler, adicionando os novos recursos à classe, criar uma nova classe na pasta routes para definir a os métodos da nova rota, importar a nova rota no server.py e adicionar o recurso.

Para escalar o sistema adicionando novos crawlers, é necessário criar mais uma pasta na pasta services com o código do novo crawler e do servidor para deixar o crawler acessível para o nginx, criar um Dockerfile para a aplicação, que provavelmente será igual ao Dockerfile do extratoclube, adicionar o serviço no `docker-compose.yml` e adicionar uma rota para ele no arquivo de configuração do nginx (`services/nginx/nginx.conf`) no seguinte formato:

```
location /novo_crawler {
    proxy_pass http://novo_crawler:80;
}
```

## Por que não deixar todos os crawlers no mesmo container?

Conforme são criados novos crawlers, o sistema passa a exigir mais hardware, exigindo aumentos de RAM e de processadores.

Dividindo os crawlers em containeres diferentes, é possível fazer uma escalabilidade horizontal, onde, em vez de aumentar o poder computacional de uma máquina, se aumenta a quantidade de máquinas, tornando a escalabilidade mais barata e eficiente.

Além disso, caso fosse um monolito ou se todos os crawlers estivessem em apenas um container, a falha de um dos crawlers poderia tornar todos os crawlers indisponíveis, o que não acontece no caso dos crawlers estarem em containeres diferentes.
