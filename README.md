# RadarLivre

The RadarLivre system is a mixed software-hardware solution based in the ADS-B technology for monitoring the airspace. The main components are: 

* ADS-B receptor
* Software for interpreting the collected data
* Web server that receives the data and store them in a database
* Software for analising the collected information and detecting possible collision between the airplanes and geographical accidents
* Website that presents the data publicly

## Getting Started

This paper will help you get a copy of the project(server-side) to run it in your local machine. If you are looking for the client-side for collecting the data of an ADS-B receptor, [this is the repository](https://github.com/RadarLivre/RadarLivreCollector). You need both to get the system running.

## Supported Platforms

This project has been primarily developed and tested on **Ubuntu Server**, but the Docker installation should work in any other operating system.

The instructions following are for **Ubuntu Server**. If you’re using a different operating system, check your package manager documentation and make the needed adjustments to the commands.

## Virtual Machine Configuration (Oracle VirtualBox)

#### Port Forwarding
If you plan on running the server inside a Virtual Machine, you'll need to configure **port forwarding** in your VM settings to access the server from your host machine.

**Example for VirtualBox:**
1. Select your **turned off** VM → Settings → Expert
2. Network → Adapter 1 (should be attached to NAT) → Port Forwarding
3. Add a new rule, where: Protocol `TCP` ; Host Port `8001` ; Guest IP `10.0.2.15` ; Guest Port `8000`

**Important:**
- **Host Port**: Choose any available port on your host machine (example being 8001)
- **Guest IP**: **Must be `10.0.2.15`** (fixed IP for NAT mode in VirtualBox)
- **Guest Port**: Always `8000` (where Django runs)

**Note**: When accessing the system from the browser on your host machine, use [http://localhost:8001](http://localhost:8001).

## Working with Multiple Terminals (No GUI)

During development and testing, you'll often need **multiple terminal sessions** simultaneously. For example:
- One terminal running the Django server
- Another for creating superusers or adding collectors  
- Additional terminals for running performance analysis tests

Since Ubuntu Server doesn't have a graphical interface, you can switch between **6 independent terminals** using `Alt + F1` through `Alt + F6`.

## Prerequisites

If you’re starting from scratch and don’t have any of the prerequisites installed yet, follow these steps before proceeding with the installation of the server.

First, update the available packages in your system’s repositories:
```bash
sudo apt-get update
```
Then, choose an installation method and install its required packages.

### For Local Installation
* Git
```bash
sudo apt-get install git -y
```
* Python 3.x
```bash
sudo apt-get install python3 python3-pip python3-venv -y
```
* PostgreSQL with PostGIS extension
```bash
sudo apt-get install postgresql postgresql-contrib postgis -y
```

### For Docker Installation
* Git
```bash
sudo apt-get install git -y
```
* Docker and Docker Compose
```bash
sudo apt-get install docker.io docker-compose -y
```
* Python 3.x/pip (optional, only required for [performance analysis](performance_analysis/README.md) tests)
```bash
sudo apt-get install python3 python3-pip python3-venv -y
```

### Configuration Files

The system uses `.ini` files for configuration. These files should be placed in the root directory of the project **after** you already cloned it. The instructions for cloning/setting up the server and the content for each of these files are listed further.

Key differences between local and Docker configurations:
- Database host: `localhost` for local, `db` for Docker (service name)
- Database port: `5431` for local (mapped port), `5432` for Docker (internal port)
- Debug mode: Usually `True` for local development, `False` for Docker

### Method 1: Local Installation

1. Clone the repository:
```bash
git clone https://github.com/RadarLivre/RadarLivre.git
# After cloning, enter the folder
cd RadarLivre
```

2. Create the `development.ini` file using `nano`:
```bash
nano development.ini
# This will open the nano file editor
```

3. Paste the following structure:
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

4. Save the file:
```bash
# Press ^(Ctrl) + O, then (Enter) and exit using ^(Ctrl) + X
```

5. Give permission to run all scripts:
```bash
chmod +x *.sh
```

6. Run the setup script:
```bash
./setup.sh
```

7. Start the server:
```bash
./runserver.sh
```

8. Access the system at [http://localhost:8000](http://localhost:8000).

### Method 2: Docker Installation

1. Clone the repository:
```bash
git clone https://github.com/RadarLivre/RadarLivre.git
# After cloning, enter the folder
cd RadarLivre
```

2. Create the `development-docker.ini` file using `nano`:
```bash
nano development-docker.ini
# This will open the nano file editor
```

3. Paste the following structure:
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

4. Save the file:
```bash
# Press ^(Ctrl) + O, then (Enter) and exit using ^(Ctrl) + X
```

5. Start the containers:
```bash
# For the first time running, use '--build'
sudo docker-compose up -d --build

# For the subsequent runs, you can remove '--build'
```

6. Access the system at [http://localhost:8000](http://localhost:8000). If you want to stop the containers, run `sudo docker-compose down`.

## System Configuration

### Creating Superuser

To access the admin panel, you need to create a superuser.

**Note**: The default credentials, which are later used in the simulated tests in [performance analysis](performance_analysis/README.md), are:
- Username: "admin"
- Password: "123456"

1. For local installation:
```bash
./create_superuser.sh
```

2. For Docker installation:
```bash
sudo docker exec -it radar_livre python manage.py createsuperuser
```

After creating a superuser, and **while the server is running**, you can log in by accessing the Django admin panel at [http://localhost:8000/admin](http://localhost:8000/admin).
From there, you can manage groups, users, collectors, and other system configurations.

### Adding a Collector

To add a new collector to the system:

1. For local installation:
```bash
./add_collector.sh <username> <latitude> <longitude>
```

2. For Docker installation:
```bash
docker exec -it radar_livre python manage.py createcollector <username> <latitude> <longitude>
```

Example:
```bash
./add_collector.sh admin -3.7319 -38.5267
```

## Development

### Code Style and Quality

Before committing your changes, ensure your code follows our style guidelines:

1. Activate the virtual environment:
```bash
. .venv/bin/activate
```

2. Format your code using Black:
```bash
black --exclude migrations radarlivre_api
```

3. Run Ruff for linting and code quality checks:
```bash
ruff check --fix
```

4. Deactivate the virtual environment:
```bash
deactivate
```

### Commit Messages

Follow the Conventional Commits specification for commit messages:

```
<type>: <description>
```
Types:
- `fix`: Bug fixes (e.g., `fix: fix button click issue`)
- `feat`: New features (e.g., `feat: add biometric login`)
- `chore`: Maintenance tasks (e.g., `chore: update dependencies`)
- `ci`: Changes to CI configuration (e.g., `ci: update deploy workflow`)
- `docs`: Documentation changes (e.g., `docs: update README instructions`)
- `style`: Code style changes (e.g., `style: improve code comments`)
- `refactor`: Code refactoring (e.g., `refactor: simplify user authentication flow`)
- `test`: Adding or modifying tests (e.g., `test: add tests for login service`)

## Performance Analysis

For information about load testing and performance analysis, see the [README in the performance_analysis folder](performance_analysis/README.md).

## Technologies Used

* [Python 3](https://www.python.org/)
* [PostgreSQL/PostGIS](https://postgis.net/)
* [Django](https://www.djangoproject.com/)
* [Docker](https://www.docker.com/)
* [Apache](https://httpd.apache.org/)

## Versioning

We use [SemanticVersioning](http://semver.org/) for versioning. For available versions, see the [tags in this repository](https://github.com/RadarLivre/RadarLivre/tags).

## Changelog

For details about development and differences between versions, see [CHANGELOG.md](CHANGELOG.md).

<!--
## Running the tests TODO

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```
-->

<!-- Won't be displayed

<div style="text-align:center">
  <img src="https://raw.githubusercontent.com/RadarLivre/RadarLivre/master/radarlivre_website/static/website/img/icon.ico" width="256">
</div>

# O Sistema Radar Livre

O sistema de monitoramento aéreo Radar Livre é uma solução mista de hadware e software baseada na tecnologia ADS-B. Seus principais componentes são: um aparelho receptor de mensagens ADS-B, um software capaz de interpretar os dados coletados, um servidor web que recebe os dados e armazena em um banco de dados, um software capaz de analisar as informações coletadas e detectar possíveis conflitos entre trajetórias de aeronaves e entre aeronaves e acidentes geográficos, além de um site que disponibiliza os dados publicamente.

# Coleta de mensagens ADS-B

O aparelho coletor de mensagens ADS-B é um componente simples, que pode ser instalado e configurado facilmente. É composto por uma antena pequena e um receptor que pode ser conectado a uma porta USB de qualquer computador. Para o tratamento das mensagens recebidas é necessário um software específico. As aplicações disponíveis atualmente para o reconhecimento das mensagens ADS-B são em sua maioria privadas e para o sistema operacional Windows, o que gera uma dependência da plataforma e um alto custo de instalação. O sistema Radar livre conta com seu próprio software de coleta, uma aplicação de código fonte aberto implementada sobre a plataforma linux pela equipe do projeto na UFC. A aplicação interpreta as mensagens e extrai informações como identificação, posicionamento, velocidade e altitude, armazenando-os em um banco de dados local. Posteriormente, os dados são enviados a um servidor web.

# Servidor web e site

Após serem coletados, os dados são enviados a um servidor web, que armazena-os em um banco de dados que pode ser acessado para análise das informações obtidas das aeronaves. Esses dados serão disponibilisados em um site de acesso livre e gratuito, onde aeronaves serão representadas graficamente, mostrando sua posição e outras informações. Essa interface web também foi implementada pela equipe do projeto na UFC em Quixadá e resultou num Trabalho de Conclusão de Curso (TCC).

# Componentes em produção

Encontram-se em desenvolvimento a versão do software coletor para Android e o Software de Análise de Colisão. O software coletor para Android permitirá o uso de plataformas mais leves e baratas para a implantação das estações coletoras e está sendo desenvolvido também na forma de um Trabalho de Conclusão de Curso. Já o Software de Análise de Colisão está sendo implementado pelo autor deste artigo como projeto de Iniciação Científica.

# Software de Análise de Colisão

Uma das principais falhas do sistema de monitoramento aéreo atual é o atraso na atualização do posicionamento das aeronaves que gera um grande intervalo entre a identificação da possível colisão e o alerta aos pilotos das aeronaves envolvidas. Além disso, o sistema não prevê possíveis colisões contra acidentes geográficos. A Tecnologia ADS-B diminui substancialmente o tempo de atualização do posicionamento dos aviões, tornando o sistema bem mais seguro e confiável.

Com o objetivo de otimizar a prevensão contra colisões, o sistema Radar Livre disponibilizará um software que utiliza os dados coletados em tempo real para análise e verificação de possíveis conflitos entre rotas de aeronaves e entre rotas de aeronaves e acidentes geográficos. A aplicação, que está em fase de desenvolvimento, funcionará na plataforma linux e terá código fonte aberto. Portanto, poderá ser utilizada livremente, especialmente por torres de controle para auxiliar no monitoramento aéreo.

# Conclusão

O projeto Radar Livre, com seus componentes simples e acessíveis, permitirá que o sistema de monitoramento aéreo brasileiro acompanhe as melhorias que estão acontecendo nos sistemas norte americanos com a adoção do método de monitoramento ADS-B. Apesar de ainda estar em fase de desenvolvimento, o sistema já disponibiliza as funcionalidades de coleta, armazenamento e apresentação em funciomaneto, e prevê uma versão do Software Coletor para a plataforma Android e um Software de Análise de Colisão. O site está disponível em <a href="http://www.radarlivre.com">www.radarlivre.com</a>. Os softwares já produzidos estão neste repositório e podem ser baixados e configurados facilmente em qualquer máquina com plataforma linux. Para a instalação, consulte nosso manual em <a href="https://docs.google.com/document/d/1ipKDKALwp97XyFSJrwYT17DriH22y-IMSrwTwS7odJA/edit?usp=sharing">Manual de Instalação</a>.

-->
