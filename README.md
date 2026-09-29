
# 🌊 WaveMatch — Backend

O **WaveMatch** é uma aplicação web desenvolvida para ajudar surfistas a encontrar condições de surf compatíveis com seu nível de experiência e suas preferências pessoais.

Este repositório contém o **backend da aplicação**, desenvolvido em Python com Flask.

## 🛠️ Tecnologias utilizadas

- **Python:** linguagem de programação.
- **Flask:** framework utilizado no desenvolvimento da API REST.
- **Flask-SQLAlchemy:** integração com o banco de dados.
- **PostgreSQL:** armazenamento e persistência dos dados.
- **Flask-JWT-Extended:** autenticação utilizando tokens JWT.
- **Flasgger (Swagger):** documentação interativa da API.
- **Open-Meteo API:** obtenção de dados meteorológicos e marítimos.
- **Docker:** conteinerização da aplicação.

## ✨ Funcionalidades

- Cadastro e autenticação de usuários.
- Autenticação utilizando JWT.
- Consulta, atualização e exclusão de usuários.
- Armazenamento do nível de surf e das preferências de altura das ondas.
- Consulta de condições meteorológicas e marítimas por meio de APIs externas.
- Geração de recomendações com base nas preferências dos usuários.
- Documentação interativa dos endpoints utilizando Swagger.

## 🏗️ Arquitetura

O WaveMatch utiliza uma arquitetura cliente-servidor, com frontend e backend organizados em repositórios independentes.

O backend é responsável por:

1. Receber e processar as requisições HTTP do frontend.
2. Gerenciar o cadastro e a autenticação dos usuários.
3. Armazenar e consultar informações no PostgreSQL.
4. Consumir dados externos da API Open-Meteo.
5. Processar as condições de surf e gerar recomendações personalizadas.
6. Retornar os resultados ao frontend por meio de uma API REST.

### Componentes principais

| Componente | Responsabilidade |
|---|---|
| Frontend | Interface e interação com o usuário |
| Backend Flask | API REST e regras de negócio |
| PostgreSQL | Persistência dos dados |
| Open-Meteo | Fornecimento de dados meteorológicos e marítimos |

## 📡 Principais endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/register` | Cadastrar um usuário |
| POST | `/login` | Autenticar um usuário |
| GET | `/users/<int:user_id>` | Consultar um usuário |
| PUT | `/users/<int:user_id>` | Atualizar as preferências de um usuário |
| DELETE | `/user/<int:user_id>` | Excluir um usuário |
| GET | `/user_main_dashboard` | Obter recomendações personalizadas |

**Observação:** endpoints protegidos exigem um token JWT válido.

A documentação interativa completa está disponível no Swagger.

## 🚀 Executando com Docker

### Pré-requisitos

- Docker Desktop instalado.
- PostgreSQL instalado, configurado e em execução.
- Banco de dados `wavematch` criado.

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO_BACKEND
cd NOME_DO_REPOSITORIO
```

Substitua os valores pelos dados do seu repositório.

### 2. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```dotenv
DATABASE_URL=postgresql+psycopg://USUARIO:SENHA@host.docker.internal:5432/wavematch
JWT_SECRET_KEY=SUA_CHAVE_SECRETA
```

Substitua os valores de exemplo pelas suas configurações.

**Importante:**

- Não publique o arquivo `.env` no GitHub.
- O endereço `host.docker.internal` permite que o container acesse o PostgreSQL instalado no computador.
- Se o banco estiver em outro ambiente, ajuste a variável `DATABASE_URL`.

### 3. Construa a imagem Docker

No terminal, dentro da pasta do backend:

```bash
docker build -t wavematch-backend .
```

### 4. Execute o container

```bash
docker run --name wavematch-api -p 5000:5000 --env-file .env wavematch-backend
```

A aplicação estará disponível em:

http://localhost:5000

### 5. Acesse o Swagger

Abra o navegador:

http://localhost:5000/apidocs/

O Swagger permite visualizar a documentação e testar os endpoints da API.

## 🔐 Autenticação

O WaveMatch utiliza autenticação baseada em **JSON Web Tokens (JWT)**.

Após realizar o login, o usuário recebe um token de acesso, utilizado para autenticar as requisições aos endpoints protegidos.

Exemplo de cabeçalho HTTP:

```http
Authorization: Bearer SEU_TOKEN_JWT
```

## 🌊 Recomendações de surf

O sistema utiliza as preferências cadastradas pelo usuário, incluindo:

- Nível de experiência no surf.
- Altura mínima de onda desejada.
- Altura máxima de onda desejada.

Quando as alturas não são informadas, a aplicação utiliza valores padrão definidos de acordo com o nível do surfista.

O backend consulta os dados externos e processa as condições disponíveis para gerar recomendações personalizadas.

## 📚 Contexto acadêmico

O WaveMatch foi desenvolvido como projeto acadêmico, com o objetivo de aplicar conhecimentos relacionados a:

- Desenvolvimento de APIs REST.
- Integração entre sistemas.
- Consumo de APIs externas.
- Persistência de dados.
- Autenticação de usuários.
- Conteinerização com Docker.

## 🏗️ Arquitetura do sistema

O diagrama abaixo apresenta a arquitetura do WaveMatch
e a comunicação entre seus componentes.

![Arquitetura do WaveMatch](arquitetura-wavematch.png)