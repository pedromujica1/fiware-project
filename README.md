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
- [🧱 Iniciando o Projeto - Configuração TTN](#-iniciando-o-projeto---configuração-ttn)
  - [Requisitos para a conexão entre o IoT Agent e Orion Context Broker - The Things Stack](#requisitos-para-a-conexão-entre-o-iot-agent-e-orion-context-broker---the-things-stack)
    - [🔧 Configuraando informações](#-configuraando-informações)
    - [⚠️ Segurança](#️-segurança)
  - [📌 Localizando informações da Aplicação e do Dispositivo](#-localizando-informações-da-aplicação-e-do-dispositivo)
  - [🔗 Configuração do MQTT](#-configuração-do-mqtt)
  - [📤 Registro do Dispositivo no IoT Agent](#-registro-do-dispositivo-no-iot-agent)
  - [🚀 Execução](#-execução)
- [📦 Configurando a persistência de dados - Cygnus/PostgresSQL](#-configurando-a-persistência-de-dados---cygnuspostgressql)
  - [🛠️ Etapas da Persistência](#️-etapas-da-persistência)
    - [📩 1. Criar a Inscrição (Subscription)](#-1-criar-a-inscrição-subscription)
    - [🔑 *Parâmetros-chave*:](#-parâmetros-chave)
      - [🧪 Exemplo de requisição:](#-exemplo-de-requisição)
    - [🚀 🧰 Execução via Script bash](#--execução-via-script-bash)
    - [🔍 Verificar inscrições ativas](#-verificar-inscrições-ativas)
  - [PostgreSQL: Leitura de Dados](#postgresql-leitura-de-dados)
    - [🧑‍💻 Acessar o banco via terminal](#-acessar-o-banco-via-terminal)
    - [📋 Ver banco de dados disponíveis](#-ver-banco-de-dados-disponíveis)
    - [📚 Listar tabelas no schema `openiot`](#-listar-tabelas-no-schema-openiot)
    - [🔎 Consultar dados da tabela](#-consultar-dados-da-tabela)
    - [🔎 Filtrar por atributo específico](#-filtrar-por-atributo-específico)
- [📊 Grafana - Visualização de dados persistidos](#-grafana---visualização-de-dados-persistidos)
  - [🌐 Acesso ao Grafana](#-acesso-ao-grafana)
  - [Adicionando uma Fonte de Dados PostgreSQL](#adicionando-uma-fonte-de-dados-postgresql)
    - [📥 Preencha os campos:](#-preencha-os-campos)
  - [Criando um Dashboard com Consulta SQL](#criando-um-dashboard-com-consulta-sql)
    - [Atenção!](#atenção)
  - [🧠 Considerações Finais](#-considerações-finais)
    - [📚 Referências Recomendadas](#-referências-recomendadas)
  - [🤝 Comunidade e Colaboração](#-comunidade-e-colaboração)


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

# 🧱 Iniciando o Projeto - Configuração TTN

Clone o repositório e gere as imagens necessárias localmente:

```bash
git clone https://github.com/pedromujica1/GUIA_MONITORAMENTO_DADOS_FIWARE-LORAWAN.git
cd GUIA_MONITORAMENTO_DADOS_FIWARE-LORAWAN
```

Inicie os Contêineres:
```bash
docker-compose -f docker/docker-compose.yml up
```
Abre outra janela no terminal e verifique se os containêrs estão inicializados:
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

## Requisitos para a conexão entre o IoT Agent e Orion Context Broker - The Things Stack

Para inscrever seu dispositivo da TTN e conectá-lo ao **Orion Context Broker (OrionCB)** via IoT Agent LoRaWAN, você precisará das seguintes informações:

- `device_id`: Identificador único do dispositivo
- `app_eui`: Identificador da aplicação no padrão EUI
- `dev_eui`: Identificador único do dispositivo atribuído pela TTN
- `application_id`: No formato `nome-da-aplicacao@ttn`
- `application_key`: Chave de autenticação (API Key)

Para facilitar o tutorial apresenta o arquivo .env_template para execução da requisição e facilidade

### 🔧 Configuraando informações

1. Copie o modelo de configuração:
   ```bash
   cp env_template .env
   ```

2. Edite o arquivo `.env` com suas credenciais:
   ```bash
   nano .env  # ou use seu editor de texto/código favorito
   ```

### ⚠️ Segurança

- Nunca compartilhe seu arquivo `.env`
- Adicione `.env` ao seu `.gitignore` 
 ```bash
   echo ".env" >> .gitignore
  ```



## 📌 Localizando informações da Aplicação e do Dispositivo

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
   - `application_id`: ID pode ser encontrado abaixo do nome `Envcity - Monitormaneto de Qualidade do Ar` , no formato `nome-da-aplicacao@ttn` como exemplo: `envcity-aqm@ttn` 

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
            "device_id": "'"$DEVICE_ID"'",
            "entity_name": "'"$ENTITY_NAME"'",
            "entity_type": "'"$ENTITY_TYPE"'",
            "attributes": [
                { "object_id": "best_co", "name": "Best_CO", "type": "Float"},
                { "object_id": "best_no2", "name": "Best_NO2", "type": "Float"},
                { "object_id": "best_ox", "name": "Best_OX", "type": "Float"},
                { "object_id": "best_so2", "name": "Best_SO2", "type": "Float"},
                { "object_id": "co_1", "name": "CO_1", "type": "Float"},
                { "object_id": "co_2", "name": "CO_2", "type": "Float"},
                { "object_id": "co_3", "name": "CO_3", "type": "Float"},
                { "object_id": "co_4", "name": "CO_4", "type": "Float"},
                { "object_id": "co_ae", "name": "CO_AE", "type": "Float"},
                { "object_id": "co_we", "name": "CO_WE", "type": "Float"},
                { "object_id": "no2_1", "name": "NO2_1", "type": "Float"},
                { "object_id": "no2_2", "name": "NO2_2", "type": "Float"},
                { "object_id": "no2_3", "name": "NO2_3", "type": "Float"},
                { "object_id": "no2_4", "name": "NO2_4", "type": "Float"},
                { "object_id": "no2_ae", "name": "NO2_AE", "type": "Float"},
                { "object_id": "no2_we", "name": "NO2_WE", "type": "Float"},
                { "object_id": "ox_1", "name": "OX_1", "type": "Float"},
                { "object_id": "ox_2", "name": "OX_2", "type": "Float"},
                { "object_id": "ox_3", "name": "OX_3", "type": "Float"},
                { "object_id": "ox_4", "name": "OX_4", "type": "Float"},
                { "object_id": "ox_ae", "name": "OX_AE", "type": "Float"},
                { "object_id": "ox_we", "name": "OX_WE", "type": "Float"},
                { "object_id": "so2_1", "name": "SO2_1", "type": "Float"},
                { "object_id": "so2_2", "name": "SO2_2", "type": "Float"},
                { "object_id": "so2_3", "name": "SO2_3", "type": "Float"},
                { "object_id": "so2_4", "name": "SO2_4", "type": "Float"},
                { "object_id": "so2_ae", "name": "SO2_AE", "type": "Float"},
                { "object_id": "so2_we", "name": "SO2_WE", "type": "Float"},
                { "object_id": "Temperatura", "name": "Temperatura", "type": "Float"},
                { "object_id": "Umidade", "name": "Umidade", "type": "Float"},
                { "object_id": "data", "name": "DATA", "type": "Text"},
                { "object_id": "hora", "name": "HORA", "type": "Text"}
            ],
            "internal_attributes": {
                "lorawan": {
                    "application_server": {
                        "host": "'"$APP_SERVER_HOST"'",
                        "username": "'"$APP_SERVER_USERNAME"'",
                        "password": "'"$APP_SERVER_PASSWORD"'",
                        "provider": "TTN"
                    },
                    "app_eui": "'"$APP_EUI"'",
                    "dev_eui": "'"$DEV_EUI"'",
                    "application_id": "'"$APPLICATION_ID"'",
                    "application_key": "'"$APPLICATION_KEY"'",
                    "data_model": "'"$DATA_MODEL"'"
                }
            }
        }
    ]
}'
```
> ❗❗ No exemplo acima são utilizados os atibutos da estação de monitoramento de Qualidade do ar registrada como Envcity, contudo o usuário deve adaptar os atributos ao seu dispositivo IoT registrado na TTN.
## 🚀 Execução

Após preencher os dados no arquivo `.env`. Para registrar o dispositivo, execute o script acima ou o seguinte comando:
```bash
bash ./scripts/registerLoraDevice.sh
```
- Caso não execute tente entrar no diretório executar o seguinte comando
```bash
chmod +x registerLoraDevice.sh
#Depois execute
./registerLoraDevice.sh
```
---

# 📦 Configurando a persistência de dados - Cygnus/PostgresSQL

O **Orion Context Broker** armazena apenas metadados no MongoDB. Para persistir os grandes volumes de dados dos sensores, usamos o conector *[Cygnus](https://fiware-cygnus.readthedocs.io/en/latest/)* para enviar esses dados ao *[PostgreSQL](https://www.postgresql.org/docs/ )* (banco relacional).

## 🛠️ Etapas da Persistência

  -  🔔 Criar uma inscrição (subscription) no Orion CB para notificar o Cygnus sobre alterações nas entidades IoT.

  -  🗃️ O Cygnus armazena os dados recebidos no PostgreSQL, organizados por schema e tabelas.


### 📩 1. Criar a Inscrição (Subscription)

Enviamos uma requisição POST para o Orion CB, no endpoint /v2/subscriptions, para notificar o Cygnus.

### 🔑 *Parâmetros-chave*:

  - `fiware-service` e `fiware-servicepath`: definem o serviço/caminho dos dados. **Atenção**: O caminho definido deve ser o mesmo configurado na requisição anterior.

  - `idPattern: ".*"` monitora todas entidades

  - `URL` aponta para CYGNUS_POSTGRESQL_SERVICE_PORT

  - `throttling` controla frequência de amostragem

#### 🧪 Exemplo de requisição:

```console
curl -iX POST \
  'http://localhost:1026/v2/subscriptions' \
  -H 'Content-Type: application/json' \
  -H 'fiware-service: openiot' \
  -H 'fiware-servicepath: /<seu_caminho_fiware>' \
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
### 🚀 🧰 Execução via Script bash

Para excutar o script acima, execute o seguinte comando:
```bash
bash ./scripts/CygnusSubscription.sh
```
---
### 🔍 Verificar inscrições ativas

```bash
bash ./scripts/SubscriptionVerification.sh
```

## PostgreSQL: Leitura de Dados

### 🧑‍💻 Acessar o banco via terminal

```bash
docker exec -it db-postgres psql -U postgres -d postgres
```
### 📋 Ver banco de dados disponíveis
```console
\list
```
🔎 Espera-se algo como:
```console
                                                    List of databases
   Name    |  Owner   | Encoding | Locale Provider |  Collate   |   Ctype    | Locale | ICU Rules |   Access privileges   
-----------+----------+----------+-----------------+------------+------------+--------+-----------+-----------------------
 postgres  | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           | 
 template0 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           | =c/postgres          +
           |          |          |                 |            |            |        |           | postgres=CTc/postgres
 template1 | postgres | UTF8     | libc            | en_US.utf8 | en_US.utf8 |        |           | =c/postgres          +
           |          |          |                 |            |            |        |           | postgres=CTc/postgres
(3 rows)
```
🧭 Listar schemas
```console
\dn
```
Resultado:
```console
       List of schemas
  Name   |       Owner       
---------+-------------------
 openiot | postgres
 public  | pg_database_owner
(2 rows)
```
### 📚 Listar tabelas no schema `openiot`
```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'openiot'
ORDER BY table_schema, table_name;
```
Exemplo:
```console
 table_schema |            table_name            
--------------+----------------------------------
 openiot      | airquality_sensorcvel_loradevice
(1 row)
```
### 🔎 Consultar dados da tabela
```sql
SELECT * FROM openiot.airquality_sensorcvel_loradevice LIMIT 10;
```
Resultado (exemplo):
```console
  recvtimets   |        recvtime         | fiwareservicepath |  entityid  | entitytype |  attrname   | attrtype | attrvalue | attrmd 
---------------+-------------------------+-------------------+------------+------------+-------------+----------+-----------+--------
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | CO_2        | Float    | null      | []
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | CO_1        | Float    | null      | []
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | CO_AE       | Float    | null      | []
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | SO2_WE      | Float    | null      | []
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | Temperatura | Float    | null      | []
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | Umidade     | Float    | null      | []
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | CO_WE       | Float    | null      | []
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | HORA        | Text     | null      | []
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | NO2_AE      | Float    | null      | []
 1747092312862 | 2025-05-12 23:25:12.862 | /airQuality       | SensorCvel | LoraDevice | OX_WE       | Float    | null      | []
```

### 🔎 Filtrar por atributo específico
Consulta:

```sql
SELECT recvtime, attrvalue FROM openiot.airquality_sensorcvel_loradevice WHERE attrname = 'count' LIMIT 10;
```
Resultado:
```console
 recvtime | attrvalue 
----------+-----------
(0 rows)
```

Para sair do cliente Postgres e retornar ao terminal, use:
```sql
\q
```

# 📊 Grafana - Visualização de dados persistidos

> [!NOTE]
> 
> Passar o nome de usuário e senha em variáveis de ambiente de texto simples como esta é um risco de segurança. Embora isso seja
> uma prática aceitável em um tutorial, para um ambiente de produção, você pode evitar esse risco aplicando
> [Docker Secrets](https://blog.docker.com/2017/02/docker-secrets-management/)
---

## 🌐 Acesso ao Grafana

Como a a aplicação executa o [Grafana](https://grafana.com/) via Docker, o contêiner é configurado com a porta 3003 mapeada localmente. Acesse pelo navegador:

```
http://localhost:3003
```

As credenciais padrão são geralmente:

- **Username:** `admin`
- **Password:** `admin` (você pode ser solicitado a alterar no primeiro login)

---

## Adicionando uma Fonte de Dados PostgreSQL

1. No menu lateral esquerdo do Grafana, Vá em ⚙️ **"Configuration"**  > **Data Sources**.
2. Clique em **"Add data source"**.
3. Escolha **PostgreSQL**.
4. Preencha os campos conforme abaixo:

### 📥 Preencha os campos:

- **Host URL:** `postgres-db:5432`
- **Database name:** `postgres`
- **Username:** `postgres`
- **Password:** (senha configurada no seu `docker-compose.yml` que é password)
- **TLS/SSL Mode:** `disable`

1. 🔁 Clique em Save & Test

---

## Criando um Dashboard com Consulta SQL

1. No menu lateral, clique em ➕ **"Create" > "Dashboard"**.
2. Clique em **"Add new panel"**.
3. No editor de consultas, selecione a fonte de dados PostgreSQL criada.
4. No modo SQL, insira a seguinte consulta:

```sql
SELECT
    recvtime::timestamp AS "time",
    NULLIF(attrvalue, 'null')::float AS "SO2"
FROM
    openiot.airquality_sensorcvel_loradevice
WHERE
    attrname = 'Best_SO2'
ORDER BY
    "time" ASC;
```

5. Clique em **Run query** para visualizar os dados.
6. Configure o tipo de gráfico desejado (ex: linha, barras).
7. Clique em **Apply** para salvar o painel no dashboard.
8. Seus dados de seu dispostivo IoT devem aparecer no novo Grafana Dashboard!

### Atenção!
- Certifique-se de que o container do Grafana esteja na mesma **rede Docker** que o container do PostgreSQL (`fiware_default`, por exemplo).
- Em caso de erros, verifique os logs dos containers com:
```bash
docker logs <nome-do-container>
```
---

## 🧠 Considerações Finais

Este tutorial apresentou uma configuração completa para **persistência de dados de sensores IoT com FIWARE**, utilizando:

- 🔗 *Orion Context Broker* para gerenciamento de contexto
- 📤 *Cygnus* como conector de dados
- 🐘 *PostgreSQL* como banco de dados relacional
- 📊 *Grafana* para visualização de dados históricos

Mas isso é só o começo! O ecossistema FIWARE é **flexível, open-source e extensível**, permitindo integração com várias outras tecnologias e bancos de dados, como:

- **MySQL**
- **MongoDB**
- **CKAN**
- **HDFS**
- **Amazon S3**
- **ElasticSearch**
- ... e muito mais!

### 📚 Referências Recomendadas

Explore configurações alternativas, exemplos avançados e ferramentas complementares nos links abaixo:

- 🔎 [FIWARE - Persisting Context Data with Apache Flume (Postman Collection)](https://www.postman.com/fiware/fiware-foundation-ev-s-public-workspace/collection/8yxw6rx/fiware-persisting-context-data-apache-flume)
- 🧪 [FIWARE Public Workspace no Postman (com várias coleções de testes)](https://www.postman.com/fiware/fiware-foundation-ev-s-public-workspace/overview)
- 📖 [FIWARE Tutorials (ReadTheDocs)](https://fiware-tutorials.readthedocs.io/en/latest/)

Essas fontes são excelentes para:

- 📦 Testar componentes FIWARE via API com o Postman
- 🧰 Aprender como usar diferentes bancos de dados com Cygnus e outros conectores
- 🚀 Explorar o universo Open Source FIWARE e suas aplicações em Cidades Inteligentes, Indústria 4.0, Energia, Saúde e mais

---

## 🤝 Comunidade e Colaboração

Se você tiver dúvidas, sugestões ou encontrar erros:

- 💬 Abra uma *issue* nos repositórios oficiais do [FIWARE no GitHub](https://github.com/FIWARE)
- 🔧 Contribua com *pull requests*, melhorando a documentação, corrigindo bugs ou adicionando novos tutoriais
- 🤝 Participe da comunidade FIWARE: Slack, Stack Overflow e fóruns abertos

FIWARE é um projeto **aberto e colaborativo** — todos são bem-vindos para contribuir!

---

🚀 **Bons testes e boas medições com seus sensores IoT!** 🌍🌱

