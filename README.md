<h1 align="center">
  <img src="https://www.fiware.org/custom/brand-guide/img/logo/fiware/secondary/png/logo-fiware-secondary.png" width="200" style="margin-right: 60px;"/>
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/LoRaWAN_Logo.svg/2560px-LoRaWAN_Logo.svg.png" alt="LoRaWAN Logo" width="300"/>
  <!--<img src="https://www.thethingsindustries.com/docs/img/TTS-logo.svg" alt="The Things Stack Logo" width="300" style="margin-left: 60px; margin-top: 69px; vertical-align: top;"/> -->
</h1>

## Integração entre dispostivos LoraWAN e Plataforma aberta Fiware

<!-- Descrição -->

Este tutorial mostra como integrar sua solução IoT que utiliza o protocolo [LoRaWAN](https://lora-alliance.org/) com os componentes da plataforma FIWARE, voltada para Cidades Inteligentes. A solução proposta inclui a conexão com a plataforma [The Things Network (TTN)](https://www.thethingsindustries.com/stack/) para recebimento dos dados e a execução dos serviços Fiware em contêineres, permitindo sua implantação em ambientes de nuvem. Como exemplo, utilizamos uma estação de monitoramento da qualidade do ar equipada com sensores de baixo custo e demonstramos como o Fiware pode ser aplicado para armazenar, processar e visualizar os dados coletados por essa estação.

-   Acess in English: [ReadmeEN.md](EN-README.md)

## Capítulos

<details>
<summary><strong>Tópicos</strong></summary>

-   [Contextualização](#introducao-fiware)
-   [Arquitetura](#arquitetura)
-   [Pré-requisitos](#prerequisitos)
    -   [Docker and Docker Compose](#docker-and-docker-compose)
    -   [WSL](#wsl)
    -   [Conta e dispostivo registrado na TTN](#ttn-conta)
-   [Iniciando o projeto](#start-up)
-   [Requisitos para Conexão entre Iot Agent e Orion CB - Versão The Things Stack](#requisitos-dispotivo-ttn)   
-   [PostgreSQL - Pesistindo Contexto para o Banco de dados](#postgresql---persistindo-contexto-banco-dados)
    -   [PostgreSQL - COnfiguração do Cygnus](#postgresql---configuracao-cygnus)
    -   [PostgreSQL - Iniciando](#postgresql---iniciando)
        -   [Verificando status Cygnus](#checking-the-cygnus-service-health-1)
        -   [Incrição para mudanças de contexto](#context-mudancas-1)
    -   [PostgreSQL - Lendo dados do Banco](#postgresql-lend-bancoDados)
        -   [Banco de Dados disponíveis do PostgreSQL server](#show-available-databases-on-the-postgresql-server)
        -   [Contexto Histórico do PostgreSQL server](#read-historical-context-from-the-postgresql-server)
-   [Grafana - Visualização de dados persistidos](#visualizacao-grafana) 


</details>

# 📌 Contextualização

O ecossistema **FIWARE** (Cirillo et al., 2019), desenvolvido pela Comissão Europeia, tem como principal objetivo utilizar dados para otimizar a eficiência e a gestão de serviços em diversas áreas. A plataforma adota padrões abertos para coleta, armazenamento e publicação de dados, destacando-se o conceito de **dados de contexto**, que representam o estado atual de entidades como sensores, aplicações em tempo real e outros dispositivos.

<p align="center">
  <img src="https://camo.githubusercontent.com/20338462f869e22f514eb10d83325e840c9d68396b336be8e6680d8e453eacda/68747470733a2f2f6669776172652e6769746875622e696f2f636174616c6f6775652f696d672f636174616c6f6775652e706e67" alt="FIWARE Monitor" width="550">
</p>

---

# 🏗️ Arquitetura do Projeto

Dentro do vasto [**catálogo**](https://www.fiware.org/catalogue/) de ferramentas do FIWARE, os componentes são organizados em cinco categorias principais:

- ⚙️ Deployment  
- 🧠 Gerenciamento de Contexto  
- 🧮 Processamento  
- 📊 Análise e Monitoramento de Contexto  
- 🌐 Interface para IoT e Robótica

Para este projeto, foram utilizados os seguintes componentes:

---

## 🧠 Gerenciadores de Contexto (2)

- [**Orion Context Broker**](https://fiware-orion.readthedocs.io/en/latest/):  
  Responsável por receber e gerenciar dados de contexto por meio da API [NGSI-v2](https://fiware.github.io/specifications/OpenAPI/ngsiv2).

- [**Cygnus**](https://fiware-cygnus.readthedocs.io/en/latest/):  
  Atua como conector para persistência dos dados, inscrevendo-se nas alterações de contexto e armazenando os dados em um banco relacional ou NoSQL (MySQL, PostgreSQL ou MongoDB).

---

## 🤖 Agente IoT teste

- [**IoT Agent LoRaWAN**](https://fiware-lorawan.readthedocs.io/en/latest/):  
  Responsável por integrar dispositivos LoRaWAN ao ecossistema FIWARE. Ele atua como intermediário entre a plataforma **The Things Stack (TTS)** e o **Orion Context Broker**, convertendo os dados recebidos em formato compatível com NGSI para posterior processamento e armazenamento.

---

## 🗃️ Bancos de Dados (2)

- [**MongoDB**](https://www.mongodb.com/):  
  - Usado pelo **Orion Context Broker** para armazenar entidades, inscrições e registros.  
  - Também utilizado pelo **IoT Agent** para guardar informações de dispositivos, como chaves, identificadores e configurações.

- [**PostgreSQL**](https://www.postgresql.org/):  
  - Funciona como destino (**data sink**) para os dados persistidos pelo **Cygnus**.

---

## 📈 Plataforma de Visualização

- [**Grafana**](https://grafana.com/):  
  Ferramenta de visualização de dados que se conecta ao banco **PostgreSQL** para exibir gráficos, painéis e indicadores com base nas informações coletadas pela estação de monitoramento da qualidade do ar.
---

## 🗺️ Diagrama da Arquitetura

![Diagrama da Arquitetura](/docs/img/Diagrama_ic.png)

---

# Pré-requisitos

## 🐳 Docker e Docker Compose

Todos os componentes deste projeto serão executados com contâiners [Docker](https://www.docker.com), que permite isolar diferentes serviços em ambientes independentes.

### 🔧 Instalação do Docker

- **Windows**: [Instruções oficiais](https://docs.docker.com/docker-for-windows/)  
- **macOS**: [Instruções oficiais](https://docs.docker.com/docker-for-mac/)  
- **Linux**: [Instruções oficiais](https://docs.docker.com/install/)

### 📦 Docker Compose

[Docker Compose](https://docs.docker.com/compose/) permite definir e executar múltiplos contêineres com um único comando via arquivos `docker-compose.yml`.  
- ⚠️ Já vem instalado no Docker Desktop (Windows/macOS). No Linux, siga [estas instruções](https://docs.docker.com/compose/install/).

### ✅ Verificação de versões

Use os comandos abaixo para checar se as versões estão atualizadas:

```bash
docker version
docker compose version
```

Recomendado: Docker 24.0.x ou superior e Docker Compose 2.24.x ou superior.

## 💻 Requisito para Windows: WSL 2

Se estiver usando Windows, é necessário ativar o WSL 2 [(Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/install) para compatibilidade total com o Docker Desktop.
🔧 Como instalar o WSL 2

Abra o terminal do Windows PowerShell como administrador e execute o comando:
```cmd
wsl --install
```
Reinicie o computador, se solicitado e verifique a versão ativa com:
```cmd
wsl --list --verbose
```

---

## 🌐 Conta e Dispositivo Registrado na TTN ou ChirpStack

> **Atenção:** Este tutorial assume que sua solução IoT já está registrada em uma rede LoRaWAN compatível.

Recomenda-se utilizar a plataforma [**The Things Stack** (TTN)](https://www.thethingsindustries.com/stack/), onde sua **Application** e seu **End Device** devem estar devidamente cadastrados em sua conta pessoal.

Caso ainda não possua uma conta na TTN, este tutorial também é compatível com a plataforma [**ChirpStack**](https://www.chirpstack.io/), uma alternativa open source para redes LoRaWAN privadas.

Ambas as plataformas permitem o uso dos seguintes **modelos de codificação de payload**, suportados pelo IoT Agent LoRaWAN:

- **[CayenneLPP (Low Power Payload)](https://developers.mydevices.com/cayenne/docs/lora/#lora-cayenne-low-power-payload)** – Formato padrão para sensores com suporte a diversos tipos de dados (temperatura, umidade, GPS, etc.), fácil de usar e interpretar.
- **[CBOR (Concise Binary Object Representation)](https://cbor.io/)** – Formato binário mais compacto e flexível, ideal para dispositivos com restrições de largura de banda e energia.

---

# 🧱 Iniciando o Projeto

Clone o repositório e gere as imagens necessárias localmente:

```bash
git clone https://github.com/pedromujica1/GUIA_MONITORAMENTO_DADOS_FIWARE-LORAWAN.git
cd GUIA_MONITORAMENTO_DADOS_FIWARE-LORAWAN
```

Inicie os Contêineres:
```bash
docker-compose -f docker/docker-compose.yml up -d
```
Verifique se estão inicializados:
```bash
docker ps
```
O resultado do comando deve ser algo similar ao abaixo:
```
CONTAINER ID   IMAGE                       COMMAND                  CREATED       STATUS                   PORTS                                                                                                NAMES
80850d97c6d7   fiware/cygnus-ngsi:latest   "/cygnus-entrypoint.…"   3 weeks ago   Up 6 hours               0.0.0.0:5055->5055/tcp, [::]:5055->5055/tcp, 5050/tcp, 0.0.0.0:5080->5080/tcp, [::]:5080->5080/tcp   fiware-cygnus
6061d69a1445   ioeari/iotagent-lora        "bin/iotagent-lora d…"   3 weeks ago   Up 6 hours               0.0.0.0:4041->4041/tcp, [::]:4041->4041/tcp                                                          docker-iotagent-lora-1
e4c1d735ac1c   grafana/grafana             "/run.sh"                3 weeks ago   Up 6 hours               0.0.0.0:3003->3000/tcp, [::]:3003->3000/tcp                                                          docker-grafana-1
ba0055dcf278   fiware/orion:3.3.1          "/usr/bin/contextBro…"   3 weeks ago   Up 6 hours (unhealthy)   0.0.0.0:1026->1026/tcp, [::]:1026->1026/tcp                                                          docker-orion-1
5eed5bf34ca2   postgres:latest             "docker-entrypoint.s…"   3 weeks ago   Up 6 hours               0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp                                                          db-postgres
d0fc0101c533   mongo:4.4                   "docker-entrypoint.s…"   3 weeks ago   Up 6 hours               0.0.0.0:27017->27017/tcp, [::]:27017->27017/tcp                                                      docker-mongodb-1
```

Caso deseje verificar e modificar o arquivo principal. A configuração de cada Contâiner pode ser encontrada neste arquivo [aqui](https://github.com/pedromujica1/GUIA_MONITORAMENTO_DADOS_FIWARE-LORAWAN/docker/docker-compose.yml)

# Requisitos para a conexão entre o Iot Agente e OrionCB - The Things Stack

Para inscrever o seu dispostivo TTN e conectar com o Orion Context Broker são necessários os seguintes

- device_id
- app_eui:
- dev_eu
- "application_id" (nomeapplicação@ttn)
- "application_key": "E078A5F764CFA112E6BA26496CA19A5B",

![](/fiware-project/docs/img/app_data.png)

## Informações Aplicação e dispositivo


## Configuração MQTT

Caminho: Applications --> (nome_aplicação) --> MQTT
Será necessário o Host, Username e Password

![Diagrama da Arquitetura](/fiware-project/docs/img/mqtt_connection.png)



---


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
