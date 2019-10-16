# FinancialAPI
API para consulta de pontos da ibovespa e de empresas na bolsa de valores utilizando dados da Alpha Vantage

Este projeto pode ser acessado através do link:
http://financial-points-api.herokuapp.com/


# Configurando o projeto 

Este projeto foi desenvolvido utilizando o microframework Flask

Para rodar o CRUD deste sistema, é necessário possuir um banco de dados Postgres

Instale as seguintes bibliotecas

pip install Flask  </br>
pip install requests  </br>
pip install flask_sqlalchemy </br>
pip install flask_script     </br>
pip install flask_migrate   </br>
pip install psycopg2-binary  </br>


No diretório do projeto com o prompt, insira os seguintes comandos </br>

export APP_SETTINGS=config.DevelopmentConfig </br>
export DATABASE_URL=postgresql://localhost/financialAPI </br>

Configure as variáveis de ambiente no .env

Rode as migrations das tabelas do projeto para gerar as tabelas no banco de dados

python manage.py db init  </br>
python manage.py db migrate  </br>
python manage.py db upgrade </br>

(Caso o sistema não realize a migration, remova a pasta migrations e tente novamente)

Para rodar o projeto: </br>
python manage.py runserver  </br>

# Endpoints da API

# Consultas Ibovespa

Consultar pontos da Ibovespa
Url: http://financial-points-api.herokuapp.com/ibovespa/points
Método: GET

Consultar pontos através do código financeiro
Url: http://financial-points-api.herokuapp.com/points/<financial_code>
Método: GET
Ex: http://financial-points-api.herokuapp.com/points/ITUB

# CRUD Usuário

Inserir usuário através de um formulário </br>
Url: http://financial-points-api.herokuapp.com/user/add </br>
Método: POST </br>
Parâmetros: name, company, document, username, password </br>

Editar usuário através de um formulário </br>
Url: http://financial-points-api.herokuapp.com/user/update </br>
Método: PUT </br>
Parâmetros: id, name, company, document, username, password </br>

Remover usuário através de um formulário </br>
Url: http://financial-points-api.herokuapp.com/user/delete </br>
Método: DELETE </br>
Parâmetros: id </br>

Mostrar os dados do usuário </br>
Url: http://financial-points-api.herokuapp.com/user/get/<id_usuario> </br>
Método: GET </br>
Ex: http://financial-points-api.herokuapp.com/user/get/1 </br>

Mostrar todos os usuários cadastrados </br>
Url: http://financial-points-api.herokuapp.com/users/all </br>
Método: GET </br>

# CRUD de empresa

Inserir empresa através de um formulário </br>
Url: http://financial-points-api.herokuapp.com/company/add </br>
Método: POST </br>
Parâmetros: name, financialCode </br>

Editar empresa através de um formulário </br>
Url: http://financial-points-api.herokuapp.com/company/update </br>
Método: PUT </br>
Parâmetros: id, name, financialCode </br>

Remover empresa através de um formulário </br>
Url: http://financial-points-api.herokuapp.com/company/delete </br>
Método: DELETE </br>
Parâmetros: id </br>

Mostrar os dados da empresa </br>
Url: http://financial-points-api.herokuapp.com/company/get/<id_company> </br>
Método: GET </br>
Ex: http://financial-points-api.herokuapp.com/company/get/1 </br>

Mostrar todas as empresas cadastradas </br>
Url: http://financial-points-api.herokuapp.com/companies/all </br>
Método: GET </br>

# CRUD de pontos da empresa

Atualiza ou adiciona pontos a uma empresa cadastrada </br>
Url: http://financial-points-api.herokuapp.com/company/value/set </br>
Método: POST </br>
Parâmetros: id_company </br>

Remover valor de empresa cadastrado </br>
Url: http://financial-points-api.herokuapp.com/company/value/delete </br>
Método: DELETE </br>
Parâmetros: id </br>

Mostrar os pontos da empresa </br>
Url: http://financial-points-api.herokuapp.com/company/value/get/<id_company_> </br>
Método: GET </br>
Ex: http://financial-points-api.herokuapp.com/company/value/get/<id_company_> </br>

Mostrar todos os pontos de empresas cadastrados </br>
Url: http://financial-points-api.herokuapp.com/companies/values/all </br>
Método: GET </br>



