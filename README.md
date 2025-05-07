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

- [📌 Contextualização](#-contextualização)
- [🏗️ Arquitetura do Projeto](#️-arquitetura-do-projeto)
  - [🧠 Gerenciadores de Contexto (2)](#-gerenciadores-de-contexto-2)
  - [🤖 Agente IoT teste](#-agente-iot-teste)
  - [🗃️ Bancos de Dados (2)](#️-bancos-de-dados-2)
  - [📈 Plataforma de Visualização](#-plataforma-de-visualização)
  - [Ferramenta de visualização de dados que se conecta ao banco **PostgreSQL** para exibir gráficos, painéis e indicadores com base nas informações coletadas pela estação de monitoramento da qualidade do ar.](#ferramenta-de-visualização-de-dados-que-se-conecta-ao-banco-postgresql-para-exibir-gráficos-painéis-e-indicadores-com-base-nas-informações-coletadas-pela-estação-de-monitoramento-da-qualidade-do-ar)
  - [🗺️ Diagrama da Arquitetura](#️-diagrama-da-arquitetura)
- [Pré-requisitos](#pré-requisitos)
  - [🐳 Docker e Docker Compose](#-docker-e-docker-compose)
    - [🔧 Instalação do Docker](#-instalação-do-docker)
    - [📦 Docker Compose](#-docker-compose)
    - [✅ Verificação de versões](#-verificação-de-versões)
  - [💻 Requisito para Windows: WSL 2](#-requisito-para-windows-wsl-2)
  - [🌐 Conta e Dispositivo Registrado na TTN ou ChirpStack](#-conta-e-dispositivo-registrado-na-ttn-ou-chirpstack)
- [🧱 Iniciando o Projeto](#-iniciando-o-projeto)
- [Requisitos para a conexão entre o IoT Agent e Orion Context Broker - The Things Stack](#requisitos-para-a-conexão-entre-o-iot-agent-e-orion-context-broker---the-things-stack)
  - [📌 Localizando as Informações da Aplicação e do Dispositivo](#-localizando-as-informações-da-aplicação-e-do-dispositivo)
  - [🔗 Configuração do MQTT](#-configuração-do-mqtt)
  - [📤 Registro do Dispositivo no IoT Agent](#-registro-do-dispositivo-no-iot-agent)
- [Configurando a persistência de dados - Cygnus/PostgresSQL](#configurando-a-persistência-de-dados---cygnuspostgressql)
  - [PostgreSQL - Configuração do Cygnus](#postgresql---configuração-do-cygnus)
    - [Inscrição em Mudanças de Contexto](#inscrição-em-mudanças-de-contexto)
      - [5️⃣ Requisição:](#5️⃣-requisição)
  - [PostgreSQL - Leitura de Dados do Banco](#postgresql---leitura-de-dados-do-banco)
- [Grafana - Visualização de dados persistidos](#grafana---visualização-de-dados-persistidos)
- [Grafana - Visualização de dados persistidos](#grafana---visualização-de-dados-persistidos-1)
  - [Acessando o Grafana via Docker](#acessando-o-grafana-via-docker)
  - [Adicionando uma Fonte de Dados PostgreSQL](#adicionando-uma-fonte-de-dados-postgresql)
    - [Connection](#connection)
    - [Authentication](#authentication)
  - [Criando um Dashboard com Consulta SQL](#criando-um-dashboard-com-consulta-sql)
  - [Considerações Finais](#considerações-finais)
- [Próximos passos](#próximos-passos)
  - [License](#license)


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

# Requisitos para a conexão entre o IoT Agent e Orion Context Broker - The Things Stack

Para inscrever seu dispositivo da TTN e conectá-lo ao **Orion Context Broker (OrionCB)** via IoT Agent LoRaWAN, você precisará das seguintes informações:

- `device_id`: Identificador único do dispositivo
- `app_eui`: Identificador da aplicação no padrão EUI
- `dev_eui`: Identificador único do dispositivo atribuído pela TTN
- `application_id`: No formato `nome-da-aplicacao@ttn`
- `application_key`: Chave de autenticação (API Key)

> Essas informações são essenciais para o provisionamento correto do dispositivo no IoT Agent.

## 📌 Localizando as Informações da Aplicação e do Dispositivo

Acesse o menu lateral em **Applications → (sua aplicação) → End devices**, e selecione o dispositivo cadastrado. Em seguida, na tela de visão geral do dispositivo, você encontrará:

- `End device ID` (equivale ao `device_id`)
- `AppEUI` (Application EUI)
- `DevEUI` (Device EUI)

Veja na imagem abaixo onde encontrar esses dados:

![Informações do dispositivo e EUI](/docs/img/ttn-data1.png)

---

## 🔗 Configuração do MQTT

Para conectar o IoT Agent à plataforma TTN vamos utilizar o protocolo [MQTT](https://mqtt.org/), frequentemente utilizado para transporte de dados entre dispositivos IoT:

1. No menu lateral, acesse:  
   **Applications → (sua aplicação) → MQTT**

2. Copie as seguintes informações:
   - `Public address` (exemplo: `au1.cloud.thethings.network:1883`) – este é o **host**
   - `Username` (exemplo: `envcity@ttn`)
   - `Password` – **API Key** que pode ser gerada no próprio painel

Veja a tela de onde extrair essas informações:

![Credenciais MQTT da TTN](/docs/img/ttn-data2.png)

> ✅ Agora que você possui os dados da aplicação e do dispositivo, você está pronto para registrá-los no IoT Agent LoRaWAN e integrá-los ao Orion Context Broker.
---

## 📤 Registro do Dispositivo no IoT Agent

Com as informações coletadas da TTN (como `device_id`, `app_eui`, `dev_eui`, `application_id`, `application_key`, `host`, `username` e `password`), você pode registrar seu dispositivo no IoT Agent por meio de uma requisição HTTP `POST` como a seguir:

```bash
#!/bin/sh

curl --location --request POST 'http://localhost:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /airQuality' \
--header 'Content-Type: application/json' \
--data-raw '{
  "devices": [
    {
      "device_id": "tbeam-v1",
      "entity_name": "PaxCounter",
      "entity_type": "LoraDevice",
      "attributes": [
        { "object_id": "field1", "name": "Field1", "type": "Number" },
        { "object_id": "field2", "name": "Field2", "type": "Number" },
        { "object_id": "field3", "name": "Field3", "type": "Number" }
      ],
      "internal_attributes": {
        "lorawan": {
          "application_server": {
            "host": "<ENDEREÇO_MQTT>",           // Ex: au1.cloud.thethings.network:1883
            "username": "<USUÁRIO_MQTT>",        // Ex: nome-aplicacao@ttn
            "password": "<API_KEY_MQTT>",
            "provider": "TTN"
          },
          "app_eui": "<APP_EUI>",
          "dev_eui": "<DEV_EUI>",
          "application_id": "<APPLICATION_ID>",   // Ex: nome-aplicacao@ttn
          "application_key": "<APPLICATION_KEY>",
          "data_model": "application_server"
        }
      }
    }
  ]
}'
```
---

# Configurando a persistência de dados - Cygnus/PostgresSQL

O Orion CB armazena apenas metadados no MongoDB. Para persistir os grandes volumes de dados dos sensores, usamos o conector Cygnus para enviar esses dados ao PostgreSQL (banco relacional).

Configuração básica:

  - Enviar request de assinatura ao Orion CB para notificar o Cygnus sobre mudanças nas entidades

  - O Cygnus então armazenará os dados nas tabelas do PostgreSQL


## PostgreSQL - Configuração do Cygnus

### Inscrição em Mudanças de Contexto

Para notificar o Cygnus sobre mudanças no contexto:

Enviar requisição POST para /v2/subscription no Orion CB

Parâmetros-chave:

  - fiware-service e fiware-servicepath filtram por dispositivo IoT. **Atenção**: O caminho definido deve ser o mesmo configurado na requisição anterior.

  - idPattern: ".*" monitora todas entidades

  - URL aponta para CYGNUS_POSTGRESQL_SERVICE_PORT

  - throttling controla frequência de amostragem

#### 5️⃣ Requisição:

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
Para verificar a inscrição, realize a seguinte requisição:

```bash
curl -X GET \
  'http://localhost:1026/v2/subscriptions/' \
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /airQuality'
```

## PostgreSQL - Leitura de Dados do Banco

Para ler os dados do PostgreSQL via linha de comando, é necessário ter acesso ao cliente `postgres`. Para isso, execute uma instância interativa da imagem `postgresql-client`, fornecendo a string de conexão como mostrado abaixo para obter um prompt:

```bash
docker exec -it db-postgres psql -U postgres -d postgres
```
Para exibir os seguintes Banco de Dados, exiba o seguinte comando
```console
\list
```
Resultado:

```console
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
(3 rows)
```

Para exibir a lista de schemas disponíveis, utilize:
Consulta:
```console
\dn
```

Resultado:
```console
  List of schemas
  Name   |  Owner
---------+----------
 openiot | postgres
 public  | postgres
(2 rows)
```

Como resultado da subscrição do Cygnus ao Orion Context Broker, foi criado um novo schema chamado openiot. O nome do schema corresponde ao cabeçalho fiware-service — portanto, openiot armazena o histórico do contexto dos dispositivos IoT.
Leitura de Contexto Histórico no PostgreSQL

Após rodar o container docker dentro da rede, é possível consultar as informações do banco de dados em execução.
Consulta:
```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'openiot'
ORDER BY table_schema, table_name;
```

Resultado:
```console
 table_schema |    table_name
--------------+-------------------
 openiot      | door_001_door
 openiot      | lamp_001_lamp
 openiot      | motion_001_motion
(3 rows)
```

O campo table_schema corresponde ao cabeçalho fiware-service fornecido com os dados de contexto.

Para consultar os dados de uma tabela, execute:
Consulta:
```sql
SELECT * FROM openiot.motion_001_motion LIMIT 10;
```
Resultado (exemplo):
```console
  recvtimets   |         recvtime         | fiwareservicepath |  entityid  | entitytype |  attrname   |   attrtype   |        attrvalue         |                                    attrmd
---------------+--------------------------+-------------------+------------+------------+-------------+--------------+--------------------------+------------------------------------------------------------------------------
 1528803005491 | 2018-06-12T11:30:05.491Z | /                 | Motion:001 | Motion     | TimeInstant | ISO8601      | 2018-06-12T11:30:05.423Z | []
 1528803005491 | 2018-06-12T11:30:05.491Z | /                 | Motion:001 | Motion     | count       | Integer      | 7                        | [{"name":"TimeInstant","type":"ISO8601","value":"2018-06-12T11:30:05.423Z"}]
...
```

A sintaxe padrão do PostgreSQL pode ser usada para filtrar os campos e valores desejados. Por exemplo, para consultar a taxa de contagem do sensor de movimento com id = Motion:001_Motion, use:
Consulta:

```sql
SELECT recvtime, attrvalue FROM openiot.motion_001_motion WHERE attrname = 'count' LIMIT 10;
```

Resultado:
```console
         recvtime         | attrvalue
--------------------------+-----------
 2018-06-12T11:30:05.491Z | 7
 2018-06-12T11:30:35.501Z | 10
 2018-06-12T11:30:41.563Z | 12
 ...
```

Para sair do cliente Postgres e retornar ao terminal, use:
```sql
\q
```


# Grafana - Visualização de dados persistidos

> [!NOTE]
> 
> Passar o nome de usuário e senha em variáveis de ambiente de texto simples como esta é um risco de segurança. Embora isso seja
> uma prática aceitável em um tutorial, para um ambiente de produção, você pode evitar esse risco aplicando
> [Docker Secrets](https://blog.docker.com/2017/02/docker-secrets-management/)

Claro! Aqui está um **tutorial em Markdown puro** (sem renderização) que explica como acessar o Grafana no Docker via `localhost:3003`, adicionar uma *data source* PostgreSQL, inserir as credenciais e criar um painel com um exemplo de consulta:


# Grafana - Visualização de dados persistidos

> [!IMPORTANTE]
> Passar o nome de usuário e senha em variáveis de ambiente de texto simples como esta é um risco de segurança. Embora isso seja
> uma prática aceitável em um tutorial, para um ambiente de produção, você pode evitar esse risco aplicando
> [Docker Secrets](https://blog.docker.com/2017/02/docker-secrets-management/)

---

## Acessando o Grafana via Docker

Se estiver executando o Grafana via Docker, o contêiner geralmente é configurado com a porta 3003 mapeada localmente. Acesse pelo navegador:

```
http://localhost:3003
```

As credenciais padrão são geralmente:

- **Username:** `admin`
- **Password:** `admin` (você pode ser solicitado a alterar no primeiro login)

---

## Adicionando uma Fonte de Dados PostgreSQL

1. No menu lateral esquerdo do Grafana, clique em **"Configuration" (ícone de engrenagem) > Data Sources**.
2. Clique em **"Add data source"**.
3. Escolha **PostgreSQL**.
4. Preencha os campos conforme abaixo:

### Connection

- **Host URL:** `postgres-db:5432`
- **Database name:** `postgres`

### Authentication

- **Username:** `postgres`
- **Password:** (senha configurada no seu `docker-compose.yml`)
- **TLS/SSL Mode:** `disable`

5. Clique em **Save & Test** para verificar se a conexão está funcionando.

---

## Criando um Dashboard com Consulta SQL

1. No menu lateral, clique em **"Create" > "Dashboard"**.
2. Clique em **"Add new panel"**.
3. No editor de consultas, selecione a fonte de dados PostgreSQL criada.
4. No modo SQL, insira a seguinte consulta:

```sql
SELECT
    recvtime::timestamp AS "time",
    NULLIF(attrvalue, 'null')::float AS "SO2"
FROM
    openiot.airquality_env2_loradevice
WHERE
    attrname = 'Best_SO2'
ORDER BY
    "time" ASC;
```

5. Clique em **Run query** para visualizar os dados.
6. Configure o tipo de gráfico desejado (ex: linha, barras).
7. Clique em **Apply** para salvar o painel no dashboard.

---

## Considerações Finais

- Certifique-se de que o container do Grafana esteja na mesma **rede Docker** que o container do PostgreSQL (`fiware_default`, por exemplo).
- Em caso de erros, verifique os logs dos containers com:

```bash
docker logs <nome-do-container>
```

- Para múltiplos sensores ou atributos, modifique o filtro `attrname` ou crie múltiplos painéis.

# Próximos passos

Want to learn how to add more complexity to your application by adding advanced features? You can find out by reading
the other [tutorials in this series](https://fiware-tutorials.rtfd.io)

---

## License

[MIT](LICENSE) © 2018-2025 FIWARE Foundation e.V.
