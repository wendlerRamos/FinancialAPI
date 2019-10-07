# FinancialAPI
API para consulta de pontos da ibovespa e de empresas na bolsa de valores utilizando dados da Alpha Vantage

Este projeto pode ser acessado através do link:
http://financial-points-api.herokuapp.com/


#Configurando o projeto 

Este projeto foi desenvolvido utilizando o microframework Flask

Para rodar o CRUD deste sistema, é necessário possuir um banco de dados Postgres

Instale as seguintes bibliotecas

pip install Flask
pip install requests
pip install flask_sqlalchemy
pip install flask_script    
pip install flask_migrate  
pip install psycopg2-binary 


No diretório do projeto com o prompt, insira os seguintes comandos
export APP_SETTINGS=config.DevelopmentConfig
export DATABASE_URL=postgresql://localhost/financialAPI

Configure as variáveis de ambiente no .env

Rode as migrations das tabelas do projeto para gerar as tabelas no banco de dados

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

(Caso o sistema não realize a migration, remova a pasta migrations e tente novamente)

Para rodar o projeto:
python manage.py runserver

#Endpoints da API

#Consultas Ibovespa

Consultar pontos da Ibovespa
Url: http://financial-points-api.herokuapp.com/ibovespa/points
Método: GET

Consultar pontos através do código financeiro
Url: http://financial-points-api.herokuapp.com/points/<financial_code>
Método: GET
Ex: http://financial-points-api.herokuapp.com/points/ITUB

#CRUD Usuário

Inserir usuário através de um formulário
Url: http://financial-points-api.herokuapp.com/user/add
Método: POST
Parâmetros: name, company, document, username, password

Editar usuário através de um formulário
Url: http://financial-points-api.herokuapp.com/user/update
Método: PUT
Parâmetros: id, name, company, document, username, password

Remover usuário através de um formulário
Url: http://financial-points-api.herokuapp.com/user/delete
Método: DELETE
Parâmetros: id

Mostrar os dados do usuário
Url: http://financial-points-api.herokuapp.com/user/get/<id_usuario>
Método: GET
Ex: http://financial-points-api.herokuapp.com/user/get/1

Mostrar todos os usuários cadastrados
Url: http://financial-points-api.herokuapp.com/users/all
Método: GET

#CRUD de empresa

Inserir empresa através de um formulário
Url: http://financial-points-api.herokuapp.com/company/add
Método: POST
Parâmetros: name, financialCode

Editar empresa através de um formulário
Url: http://financial-points-api.herokuapp.com/company/update
Método: PUT
Parâmetros: id, name, financialCode

Remover empresa através de um formulário
Url: http://financial-points-api.herokuapp.com/company/delete
Método: DELETE
Parâmetros: id

Mostrar os dados da empresa
Url: http://financial-points-api.herokuapp.com/company/get/<id_company>
Método: GET
Ex: http://financial-points-api.herokuapp.com/company/get/1

Mostrar todas as empresas cadastradas
Url: http://financial-points-api.herokuapp.com/companies/all
Método: GET

#CRUD de pontos da empresa

Atualiza ou adiciona pontos a uma empresa cadastrada
Url: http://financial-points-api.herokuapp.com/company/value/set
Método: POST
Parâmetros: id_company

Remover valor de empresa cadastrado
Url: http://financial-points-api.herokuapp.com/company/value/delete
Método: DELETE
Parâmetros: id

Mostrar os pontos da empresa
Url: http://financial-points-api.herokuapp.com/company/value/get/<id_company_>
Método: GET
Ex: http://financial-points-api.herokuapp.com/company/value/get/<id_company_>

Mostrar todos os pontos de empresas cadastrados
Url: http://financial-points-api.herokuapp.com/companies/values/all
Método: GET



