# Fiware project

Integração dos dados da estação metereológica Envcity com o ambiente Fiware

## Teconlogias usadas
- IotAgentLoraWAN (Intermédio para obetr dados dos dispositivos da estação Envcity)
- Orion Context Broker (Receber dados dos dispositos)
- MongoDB (Armazenar/atualizardados dados das entidades do Orion)
- Draco (Sistema para gerenciamento do DataFlow/ Usado para persistir os dados)

Pré-requisitos: 
 - Docker Compose version v2.20.3 ou acima
 - Docker version 24.0.7, build 24.0.7-0ubuntu ou acima


## Execução

- Baixe o projeto localmente
```console
git clone https://github.com/pedromujica1/fiware-envcity.git
```
- Inicie os containers
```
cd fiware-envcity
docker-compose -f docker/docker-compose.yml up -d
```
- Verifique se os container estão em execução pelo seguinte comando
```
docker ps
```

#### 1️⃣ Requisição para verificar estado do Cygnus:

```console
curl -X GET \
  'http://localhost:9090/nifi-api/system-diagnostics'
```

