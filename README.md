<h1 align="center">
  <img src="https://www.fiware.org/custom/brand-guide/img/logo/fiware/secondary/png/logo-fiware-secondary.png" width="200" style="margin-right: 60px;"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/LoRaWAN_Logo.svg/2560px-LoRaWAN_Logo.svg.png" alt="LoRaWAN Logo" width="300"/>
  <!--<img src="https://www.thethingsindustries.com/docs/img/TTS-logo.svg" alt="The Things Stack Logo" width="300" style="margin-left: 60px; margin-top: 69px; vertical-align: top;"/> -->
</h1>

## Integração entre dispostivos LoraWAN e Plataforma aberta Fiware

<!-- Descrição -->

Este tutorial mostra como integrar sua solução IoT que utiliza o protocolo LoRaWAN com os componentes da plataforma FIWARE, voltada para Cidades Inteligentes. A solução proposta inclui a conexão com a plataforma de The Things Network (TTN) para recebimento dos dados e a execução dos serviços em contêineres, permitindo sua implantação em ambientes de nuvem. Como exemplo, utilizamos uma estação de monitoramento da qualidade do ar equipada com sensores de baixo custo e demonstramos como o Fiware pode ser aplicado para armazenar, processar e visualizar os dados coletados por essa estação.

-   Acess in English: [ReadmeEN.md](README.ja.md)

## Capítulos

<details>
<summary><strong>Tópicos</strong></summary>

-   [Contextualização](#introducao-fiware)
-   [Arquitetura](#arquitetura)
-   [Prerequisitos](#prerequisitos)
    -   [Docker and Docker Compose](#docker-and-docker-compose)
    -   [WSL](#wsl)
    -   [Conta e dispostivo registrado na TTN](#ttn-conta)
-   [Iniciando](#start-up)
-   [OrionCB/MongoDB - Gerenciamento de dados de contexto](#orion-mongoDB)
-   [Iot Agent LoraWAN - Intermediário entre IoT e Context Broker](#iotAgent-lorawan)
-   [Requisitos para Conexão entre Iot Agent e Orion CB - Versão The Things Stack](#requisitos-dispotivo-ttn)   
-   [PostgreSQL - Pesistindo Contexto para o Banco de dados](#postgresql---persistindo-contexto-banco-dados)
    -   [PostgreSQL - Configuração do Banco de dados](#postgresql---config-banco-dados)
    -   [PostgreSQL - COnfiguração do Cygnus](#postgresql---configuracao-cygnus)
    -   [PostgreSQL - Iniciando](#postgresql---iniciando)
        -   [Verificando status Cygnus](#checking-the-cygnus-service-health-1)
        -   [Incrição para mudanças de contexto](#context-mudancas-1)
    -   [PostgreSQL - Lendo dados do Banco](#postgresql-lend-bancoDados)
        -   [Banco de Dados disponíveis do PostgreSQL server](#show-available-databases-on-the-postgresql-server)
        -   [Contexto Histórico do PostgreSQL server](#read-historical-context-from-the-postgresql-server)
-   [Grafana - Visualização de dados persistidos](#visualizacao-grafana) 


</details>

# Contextualização

O ecossistema FIWARE (Cirillo et al., 2019), desenvolvido pela Comissão Europeia, tem com principal objetivo utilizar dados para otimizar a eficiência e a gestão de serviços em diversas áreas. A plataforma possui padrões de coleta, armazenamento e publicação de dados, tendo como exemplo os “Dados de contexto” que representam o estado atual de entidades como sensores, aplicações de tempo real e outros.

# Arquitetura do projeto

Dentre o vasto catálogo das ferramentas do Fiware, a classificação ocorre de acordo com 5 principais categorias: ferramentas de Deployment, gerenciamento de contexto, processamento, análise e monitoramento de Contexto, Interface para IoT e Robótica. Para o seguinte projeto utilizamos: 
- 2 Gerenciadores de Dados de Contexto
- 1 Agente Iot
- 2 Bancos de Dados
- 1 Plataforma de Visualização de dados

Os seguintes componentes são:

-   Dois **FIWARE Context Managers**:
    -   FIWARE [Orion Context Broker](https://fiware-orion.readthedocs.io/en/latest/) que recebe requisições usando a interface de API [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2)
    -   FIWARE [Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/) que se inscreve nas alterações e persiste os dados para um Banco de Dados (**MySQL** , **PostgreSQL** or **MongoDB**)
-   Necessariamente 2  **Banco de Dados**:
    -   O Banco de Dados NoSQL [MongoDB](https://www.mongodb.com/):
        -   Utilizado pelo **Orion Context Broker** para armazenar dados de entidades, inscrições
            e registros
        -   Usado pelo **IoT Agent** para armazenar informações dos dispostivos como chaves, registros e outros
    -   O Banco de dados [PostgreSQL](https://www.postgresql.org/):
        -   Usado para armazenar os dados de contexto persistidos como um Data Sink..
    
-   Visualização de dados:
    - Grafana: ferramenta de visualização de gráficos, painéis e indicadores baseados nos dados coletados pela estação de monitoramento.

# Prerequisitos

## Docker e Docker Compose

To keep things simple all components will be run using [Docker](https://www.docker.com). **Docker** is a container
technology which allows to different components isolated into their respective environments.

-   To install Docker on Windows follow the instructions [here](https://docs.docker.com/docker-for-windows/)
-   To install Docker on Mac follow the instructions [here](https://docs.docker.com/docker-for-mac/)
-   To install Docker on Linux follow the instructions [here](https://docs.docker.com/install/)

**Docker Compose** is a tool for defining and running multi-container Docker applications. A series of
[YAML files](https://github.com/FIWARE/tutorials.Historic-Context-Flume/tree/master/docker-compose) are used configure
the required services for the application. This means all container services can be brought up in a single command.
Docker Compose is installed by default as part of Docker for Windows and Docker for Mac, however Linux users will need
to follow the instructions found [here](https://docs.docker.com/compose/install/)

You can check your current **Docker** and **Docker Compose** versions using the following commands:

```console
docker-compose -v
docker version
```

Please ensure that you are using Docker version 24.0.x or higher and Docker Compose 2.24.x or higher and upgrade if
necessary.

## WSL



# Iniciando

Before you start you should ensure that you have obtained or built the necessary Docker images locally. Please clone the
repository and create the necessary images by running the commands as shown:

```console
git clone https://github.com/FIWARE/tutorials.Historic-Context-Flume.git
cd tutorials.Historic-Context-Flume
git checkout NGSI-v2

./services create
```

Thereafter, all services can be initialized from the command-line by running the
[services](https://github.com/FIWARE/tutorials.Historic-Context-Flume/blob/NGSI-v2/services) Bash script provided within
the repository:

```console
./services <command>
```

Where `<command>` will vary depending upon the databases we wish to activate. This command will also import seed data
from the previous tutorials and provision the dummy IoT sensors on startup.

> [!NOTE]
>
> If you want to clean up and start over again you can do so with the following command:
>
> ```console
> ./services stop
> ```
# OrionCB/MongoDB - Gerenciamento de dados de contexto

# Iot Agente LoraWAN - Intermediário entre Iot e Context Broker

# Requisitos para a conexão entre o Iot Agente e OrionCB - The Things Stack

# PostgreSQL - Persisting Context Data into a Database

To persist historic context data into an alternative database such as **PostgreSQL**, we will need an additional
container which hosts the PostgreSQL server - the default Docker image for this data can be used. The PostgreSQL
instance is listening on the standard `5432` port and the overall architecture can be seen below:

![](https://fiware.github.io/tutorials.Historic-Context-Flume/img/cygnus-postgres.png)

We now have a system with two databases, since the MongoDB container is still required to hold data related to the Orion
Context Broker and the IoT Agent.

## PostgreSQL - Database Server Configuration

```yaml
postgres-db:
    image: postgres:latest
    hostname: postgres-db
    container_name: db-postgres
    expose:
        - '5432'
    ports:
        - '5432:5432'
    networks:
        - default
    environment:
        - 'POSTGRES_PASSWORD=password'
        - 'POSTGRES_USER=postgres'
        - 'POSTGRES_DB=postgres'
```

The `postgres-db` container is listening on a single port:

-   Port `5432` is the default port for a PostgreSQL server. It has been exposed so you can also run the `pgAdmin4` tool
    to display database data if you wish

The `postgres-db` container is driven by environment variables as shown:

| Key               | Value.     | Description                               |
| ----------------- | ---------- | ----------------------------------------- |
| POSTGRES_PASSWORD | `password` | Password for the PostgreSQL database user |
| POSTGRES_USER     | `postgres` | Username for the PostgreSQL database user |
| POSTGRES_DB       | `postgres` | The name of the PostgreSQL database       |

> [!NOTE]
>
> Passing the Username and Password in plain text environment variables like this is a security risk. Whereas this is
> acceptable practice in a tutorial, for a production environment, you can avoid this risk by applying
> [Docker Secrets](https://blog.docker.com/2017/02/docker-secrets-management/)

## PostgreSQL - Cygnus Configuration

```yaml
cygnus:
    image: quay.io/fiware/cygnus-ngsi:latest
    hostname: cygnus
    container_name: fiware-cygnus
    networks:
        - default
    depends_on:
        - postgres-db
    expose:
        - '5080'
    ports:
        - '5055:5055'
        - '5080:5080'
    environment:
        - 'CYGNUS_POSTGRESQL_HOST=postgres-db'
        - 'CYGNUS_POSTGRESQL_PORT=5432'
        - 'CYGNUS_POSTGRESQL_USER=postgres'
        - 'CYGNUS_POSTGRESQL_PASS=password'
        - 'CYGNUS_POSTGRESQL_ENABLE_CACHE=true'
        - 'CYGNUS_POSTGRESQL_SERVICE_PORT=5055'
        - 'CYGNUS_LOG_LEVEL=DEBUG'
        - 'CYGNUS_API_PORT=5080'
        - 'CYGNUS_SERVICE_PORT=5055'
```

The `cygnus` container is listening on two ports:

-   The Subscription Port for Cygnus - `5055` is where the service will be listening for notifications from the Orion
    context broker
-   The Management Port for Cygnus - `5080` is exposed purely for tutorial access - so that cUrl or Postman can make
    provisioning commands without being part of the same network.

The `cygnus` container is driven by environment variables as shown:

| Key                            | Value         | Description                                                                    |
| ------------------------------ | ------------- | ------------------------------------------------------------------------------ |
| CYGNUS_POSTGRESQL_HOST         | `postgres-db` | Hostname of the PostgreSQL server used to persist historical context data      |
| CYGNUS_POSTGRESQL_PORT         | `5432`        | Port that the PostgreSQL server uses to listen to commands                     |
| CYGNUS_POSTGRESQL_USER         | `postgres`    | Username for the PostgreSQL database user                                      |
| CYGNUS_POSTGRESQL_PASS         | `password`    | Password for the PostgreSQL database user                                      |
| CYGNUS_LOG_LEVEL               | `DEBUG`       | The logging level for Cygnus                                                   |
| CYGNUS_SERVICE_PORT            | `5050`        | Notification Port that Cygnus listens when subscribing to context data changes |
| CYGNUS_API_PORT                | `5080`        | Port that Cygnus listens on for operational reasons                            |
| CYGNUS_POSTGRESQL_ENABLE_CACHE | `true`        | Switch to enable caching within the PostgreSQL configuration                   |

> [!NOTE]
>
> Passing the Username and Password in plain text environment variables like this is a security risk. Whereas this is
> acceptable practice in a tutorial, for a production environment, `CYGNUS_POSTGRESQL_USER` and `CYGNUS_POSTGRESQL_PASS`
> should be injected using [Docker Secrets](https://blog.docker.com/2017/02/docker-secrets-management/)

## PostgreSQL - Start up

To start the system with a **PostgreSQL** database run the following command:

```console
./services postgres
```

### Checking the Cygnus Service Health

Once Cygnus is running, you can check the status by making an HTTP request to the exposed `CYGNUS_API_PORT` port. If the
response is blank, this is usually because Cygnus is not running or is listening on another port.

#### 4️⃣ Request:

```console
curl -X GET \
  'http://localhost:5080/v1/version'
```

#### Response:

The response will look similar to the following:

```json
{
    "success": "true",
    "version": "1.18.0_SNAPSHOT.etc"
}
```

> **Troubleshooting:** What if the response is blank ?
>
> -   To check that a docker container is running try
>
> ```bash
> docker ps
> ```
>
> You should see several containers running. If `cygnus` is not running, you can restart the containers as necessary.

### Subscribing to Context Changes

Once a dynamic context system is up and running, we need to inform **Cygnus** of changes in context.

This is done by making a POST request to the `/v2/subscription` endpoint of the Orion Context Broker.

-   The `fiware-service` and `fiware-servicepath` headers are used to filter the subscription to only listen to
    measurements from the attached IoT Sensors, since they had been provisioned using these settings
-   The `idPattern` in the request body ensures that Cygnus will be informed of all context data changes.
-   The notification `url` must match the configured `CYGNUS_POSTGRESQL_SERVICE_PORT`
-   The `throttling` value defines the rate that changes are sampled.

#### 5️⃣ Request:

```console
curl -iX POST \
  'http://localhost:1026/v2/subscriptions' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /' \
  -d '{
  "description": "Notify Cygnus Postgres of all context changes",
  "subject": {
    "entities": [
      {
        "idPattern": ".*"
      }
    ]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5055/notify"
    }
  },
  "throttling": 5
}'
```

As you can see, the database used to persist context data has no impact on the details of the subscription. It is the
same for each database. The response will be **201 - Created**

## PostgreSQL - Reading Data from a database

To read PostgreSQL data from the command-line, we will need access to the `postgres` client, to do this, run an
interactive instance of the `postgresql-client` image supplying the connection string as shown to obtain a command-line
prompt:

```console
docker run -it --rm  --network fiware_default jbergknoff/postgresql-client \
   postgresql://postgres:password@postgres-db:5432/postgres
```

### Show Available Databases on the PostgreSQL server

To show the list of available databases, run the statement as shown:

#### Query:

```
\list
```

#### Result:

```
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)
```

The result includes two template databases `template0` and `template1` as well as the `postgres` database setup when the
docker container was started.

To show the list of available schemas, run the statement as shown:

#### Query:

```
\dn
```

#### Result:

```
  List of schemas
  Name   |  Owner
---------+----------
 openiot | postgres
 public  | postgres
(2 rows)
```

As a result of the subscription of Cygnus to Orion Context Broker, a new schema has been created called `openiot`. The
name of the schema matches the `fiware-service` header - therefore `openiot` holds the historic context of the IoT
devices.

### Read Historical Context from the PostgreSQL server

Once running a docker container within the network, it is possible to obtain information about the running database.

#### Query:

```sql
SELECT table_schema,table_name
FROM information_schema.tables
WHERE table_schema ='openiot'
ORDER BY table_schema,table_name;
```

#### Result:

```
 table_schema |    table_name
--------------+-------------------
 openiot      | door_001_door
 openiot      | lamp_001_lamp
 openiot      | motion_001_motion
(3 rows)
```

The `table_schema` matches the `fiware-service` header supplied with the context data:

To read the data within a table, run a select statement as shown:

#### Query:

```sql
SELECT * FROM openiot.motion_001_motion limit 10;
```

#### Result:

```
  recvtimets   |         recvtime         | fiwareservicepath |  entityid  | entitytype |  attrname   |   attrtype   |        attrvalue         |                                    attrmd
---------------+--------------------------+-------------------+------------+------------+-------------+--------------+--------------------------+------------------------------------------------------------------------------
 1528803005491 | 2018-06-12T11:30:05.491Z | /                 | Motion:001 | Motion     | TimeInstant | ISO8601      | 2018-06-12T11:30:05.423Z | []
 1528803005491 | 2018-06-12T11:30:05.491Z | /                 | Motion:001 | Motion     | count       | Integer      | 7                        | [{"name":"TimeInstant","type":"ISO8601","value":"2018-06-12T11:30:05.423Z"}]
 1528803005491 | 2018-06-12T11:30:05.491Z | /                 | Motion:001 | Motion     | refStore    | Relationship | Store:001                | [{"name":"TimeInstant","type":"ISO8601","value":"2018-06-12T11:30:05.423Z"}]
 1528803035501 | 2018-06-12T11:30:35.501Z | /                 | Motion:001 | Motion     | TimeInstant | ISO8601      | 2018-06-12T11:30:35.480Z | []
 1528803035501 | 2018-06-12T11:30:35.501Z | /                 | Motion:001 | Motion     | count       | Integer      | 10                       | [{"name":"TimeInstant","type":"ISO8601","value":"2018-06-12T11:30:35.480Z"}]
 1528803035501 | 2018-06-12T11:30:35.501Z | /                 | Motion:001 | Motion     | refStore    | Relationship | Store:001                | [{"name":"TimeInstant","type":"ISO8601","value":"2018-06-12T11:30:35.480Z"}]
 1528803041563 | 2018-06-12T11:30:41.563Z | /                 | Motion:001 | Motion     | TimeInstant | ISO8601      | 2018-06-12T11:30:41.520Z | []
 1528803041563 | 2018-06-12T11:30:41.563Z | /                 | Motion:001 | Motion     | count       | Integer      | 12                       | [{"name":"TimeInstant","type":"ISO8601","value":"2018-06-12T11:30:41.520Z"}]
 1528803041563 | 2018-06-12T11:30:41.563Z | /                 | Motion:001 | Motion     | refStore    | Relationship | Store:001                | [{"name":"TimeInstant","type":"ISO8601","value":"2018-06-12T11:30:41.520Z"}]
 1528803047545 | 2018-06-12T11:30:47.545Z | /
```

The usual **PostgreSQL** query syntax can be used to filter appropriate fields and values. For example to read the rate
at which the **Motion Sensor** with the `id=Motion:001_Motion` is accumulating, you would make a query as follows:

#### Query:

```sql
SELECT recvtime, attrvalue FROM openiot.motion_001_motion WHERE attrname ='count'  limit 10;
```

#### Result:

```
         recvtime         | attrvalue
--------------------------+-----------
 2018-06-12T11:30:05.491Z | 7
 2018-06-12T11:30:35.501Z | 10
 2018-06-12T11:30:41.563Z | 12
 2018-06-12T11:30:47.545Z | 13
 2018-06-12T11:31:02.617Z | 15
 2018-06-12T11:31:32.718Z | 20
 2018-06-12T11:31:38.733Z | 22
 2018-06-12T11:31:50.780Z | 24
 2018-06-12T11:31:56.825Z | 25
 2018-06-12T11:31:59.790Z | 26
(10 rows)
```

To leave the Postgres client and leave interactive mode, run the following:

```console
\q
```

You will then return to the command-line.

# Grafana - Visualização de dados persistidos

# Considerações


# Próximos passos

Want to learn how to add more complexity to your application by adding advanced features? You can find out by reading
the other [tutorials in this series](https://fiware-tutorials.rtfd.io)

---

## License

[MIT](LICENSE) © 2018-2025 FIWARE Foundation e.V.
