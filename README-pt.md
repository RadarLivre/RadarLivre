# RadarLivre

O sistema RadarLivre é uma solução que integra software-hardware baseada na tecnologia ADS-B para monitoramento do espaço aéreo. Os componentes principais são: 

* Receptor ADS-B
* Software para interpretação de dados coletados
* Servidor web que recebe e guarda os dados em um banco de dados
* Software para análise das informações coletadas e detecção de possíveis colisões entre aeronaves e acidentes geográficos
* Website que apresenta publicamente os dados

## Manual de Introdução

Este documento o ajudará a obter uma cópia do projeto (lado-do-servidor) para rodar na sua máquina local. Se você procura pelo lado-do-cliente para coleta de dados de um receptor ADS-B, [este é o repositório](https://github.com/RadarLivre/RadarLivreCollector). Você precisará de ambos para utilizar o sistema.

## Plataformas Suportadas

Este projeto foi prioritariamente desenvolvido e testado no **Ubuntu Server**, porém a instalação via Docker deve funcionar em qualquer outro sistema operacional.

As instruções a seguir são para **Ubuntu Server**. Se você usa um outro sistema operacional, cheque a documentação do seu gerenciador de pacotes e faça os devidos ajustes aos comandos.

## Configuração de Máquina Virtual (Oracle VirtualBox)

#### Redirecionamento de Portas

Se você planeja rodar o servidor dentro de uma Máquina Virtual (VM), você precisará configurar o **redirecionamento de portas** nas configurações da VM para acessar o server via sua máquina hospedeira.

**Exemplo para VirtualBox:**
1. Selecione sua VM **desligada** → Settings → Expert
2. Network → Adapter 1 (attached to NAT) → Port Forwarding
3. Adicione uma nova regra, onde: Protocol `TCP` ; Host Port `8001` ; Guest IP `10.0.2.15` ; Guest Port `8000`

**Importante:**
- **Host Port** (Porta Host): Escolha qualquer porta disponível na sua máquina hospedeira (exemplo sendo 8001)
- **Guest IP** (IP Convidado): **Necessariamente `10.0.2.15`** (IP fixo para modo NAT no VirtualBox)
- **Guest Port**(Porta Convidado): Sempre `8000` (onde Django roda)

**Nota**: Quando acessar o sistema pelo navegador da sua máquina hospedeira, use [http://localhost:8001](http://localhost:8001).

## Trabalhando com Múltiplos Terminais (Sem Interface Gráfica)

Durante desenvolvimento e testes, você frequentemente precisará de **múltiplas sessões de terminais** simultaneamente. Por exemplo:
- Um terminal rodando o servidor Django
- Outro para criação de superusuários ou adicionar coletores
- Terminais adicionais para testes de análise de performance

Como o Ubuntu Server não contém uma interface gráfica, você pode navegar entre **6 terminais independentes** usando `Alt + F1` até `Alt + F6`.

## Pré-requisitos

Se você está começando do zero e não possui nenhum dos pré-requisitos instalados ainda, siga estes passos antes de proceder com a instalação do servidor.

Primeiro, atualize os pacotes disponíveis nos repositórios do seu sistema:
```bash
sudo apt-get update
```
Depois, escolha um método de instalação e instale seus respectivos pacotes requeridos.

### Para Instalação Local
* Git
```bash
sudo apt-get install git -y
```
* Python 3.x
```bash
sudo apt-get install python3 python3-pip python3-venv -y
```
* PostgreSQL com extensão PostGIS
```bash
sudo apt-get install postgresql postgresql-contrib postgis -y
```

### Para Instalação Docker
* Git
```bash
sudo apt-get install git -y
```
* Docker e Docker Compose
```bash
sudo apt-get install docker.io docker-compose -y
```
* Python 3.x/pip (opcional, somente necessários para testes opcionais de [análise de performance](performance_analysis/README.md))
```bash
sudo apt-get install python3 python3-pip python3-venv -y
```

### Arquivos de Configuração

O sistema utiliza arquivos `.ini` para configuração. Tais arquivos precisam ser colocados no diretório raiz do projeto **após** a clonagem. As instruções de clonagem/instalação do servidor e o conteúdo para cada um dos arquivos estão listados mais adiante. 

Principais diferenças entre configurações locais e Docker:
- Host do banco de dados: `localhost` para local, `db` para Docker (nome do serviço)
- Porta do banco de dados: `5431` para local (porta mapeada), `5432` para Docker (porta interna)
- Modo debug: Normalmente `True` para desenvolvimento local, `False` para Docker

### Método 1: Instalação Local

1. Clone o repositório:
```bash
git clone https://github.com/RadarLivre/RadarLivre.git
# Após clonar, entre na pasta
cd RadarLivre
```

2. Crie o arquivo `development.ini` usando `nano`:
```bash
nano development.ini
# Isso abrirá o editor de arquivos nano
```

3. Copie e cole a estrutura abaixo:
```ini
[DATABASE]
ENGINE = django.contrib.gis.db.backends.postgis
NAME = radarlivre
HOST = localhost
USER = postgres
PASSWORD = postgres
PORT = 5431

[GENERAL]
DEBUG = True
LOG_FILE = ./api.log
DJANGO_LOG_LEVEL = ERROR
ALLOWED_HOSTS = localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS = http://localhost,http://127.0.0.1
```

4. Salve o arquivo:
```bash
# Pressione ^(Ctrl) + O, depois (Enter) e saia usando ^(Ctrl) + X
```

5. Dê permissão para rodar todos os scripts:
```bash
chmod +x *.sh
```

6. Rode o script de setup:
```bash
./setup.sh
```

7. Inicie o servidor:
```bash
./runserver.sh
```

8. Acesse o sistema em [http://localhost:8000](http://localhost:8000).

### Método 2: Instalação Docker

1. Clone o repositório:
```bash
git clone https://github.com/RadarLivre/RadarLivre.git
# Após clonar, entre na pasta
cd RadarLivre
```

2. Crie o arquivo `development-docker.ini` usando `nano`:
```bash
nano development-docker.ini
# Isso abrirá o editor de arquivos nano
```

3. Copie e cole a estrutura abaixo:
```ini
[DATABASE]
ENGINE = django.contrib.gis.db.backends.postgis
NAME = radarlivre
HOST = db
USER = postgres
PASSWORD = postgres
PORT = 5432

[GENERAL]
DEBUG = True
LOG_FILE = ./api.log
DJANGO_LOG_LEVEL = ERROR
ALLOWED_HOSTS = localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS = http://localhost,http://127.0.0.1
```

4. Salve o arquivo:
```bash
# Pressione ^(Ctrl) + O, depois (Enter) e saia usando ^(Ctrl) + X
```

5. Inicie os containers:
```bash
# Para a primeira vez rodando, use '--build'
sudo docker-compose up -d --build

# Para as próximas vezes, você pode remover o '--build'
```

6. Acesse o sistema em [http://localhost:8000](http://localhost:8000). Se você quiser parar os containers, rode `sudo docker-compose down`.

## Configuração do Sistema

### Criando um Superusuário

Para acessar o painel de administração, você precisará criar um superusuário.

**Nota**: O padrão para as credenciais, nas quais são usadas posteriormente em testes simulados para [análise de performance](performance_analysis/README.md), são:
- Usuário: "admin"
- Senha: "123456"

1. Para instalação local:
```bash
./create_superuser.sh
```

2. Para instalação Docker:
```bash
sudo docker exec -it radar_livre python manage.py createsuperuser
```

Após criar um superusuário, e **enquanto o servidor está rodando**, você poderá autenticar-se acessando o painel de admin do Django em [http://localhost:8000/admin](http://localhost:8000/admin).
Por lá, poderá gerenciar grupos, usuários, coletores, e outras configurações de sistema.


### Adicionando um Coletor

Para adicionar um novo coletor ao sistema:

1. Para instalação local:
```bash
./add_collector.sh <usuário> <latitude> <longitude>
```

2. Para instalação Docker:
```bash
docker exec -it radar_livre python manage.py createcollector <usuário> <latitude> <longitude>
```

Exemplo:
```bash
./add_collector.sh admin -3.7319 -38.5267
```

## Desenvolvimento

### Estilo e Qualidade de Código

Antes de commitar suas mudanças, garanta que seu cógido segue nossas diretrizes de estilo:

1. Ative o ambiente virtual:
```bash
. .venv/bin/activate
```

2. Formate seu código usando Black:
```bash
black --exclude migrations radarlivre_api
```

3. Rode Ruff para linting e checagem de qualidade de código:
```bash
ruff check --fix
```

4. Desative o ambiente virtual:
```bash
deactivate
```

### Mensagens de Commit

Siga a especificação Convencional de Commmits para as mensagens de commit:

```
<tipo>: <descrição>
```
Tipos:
- `fix`: Correções de bugs (e.g., `fix: fix button click issue`)
- `feat`: Novas features (e.g., `feat: add biometric login`)
- `chore`: Tarefas de manutenção (e.g., `chore: update dependencies`)
- `ci`: Mudanças das configurações do CI (e.g., `ci: update deploy workflow`)
- `docs`: Mudanças de documentação (e.g., `docs: update README instructions`)
- `style`: Mudanças no estilo do código (e.g., `style: improve code comments`)
- `refactor`: Refatoramento de código (e.g., `refactor: simplify user authentication flow`)
- `test`: Adicionar ou modificar testes (e.g., `test: add tests for login service`)

## Análise de Performance

Para informações sobre testes de carga e análise de performance, veja o [README da pasta performance_analysis](performance_analysis/README.md) (somente em inglês).

## Tecnologias Utilizadas

* [Python 3](https://www.python.org/)
* [PostgreSQL/PostGIS](https://postgis.net/)
* [Django](https://www.djangoproject.com/)
* [Docker](https://www.docker.com/)
* [Apache](https://httpd.apache.org/)

## Versionamento

Utilizamos [SemanticVersioning](http://semver.org/) para versionamento. Para as versões disponíveis, veja as [tags neste repositório](https://github.com/RadarLivre/RadarLivre/tags).

## Changelog

Para detalhes sobre desenvolvimento e diferenças entre versões, veja o [CHANGELOG.md](CHANGELOG.md).
