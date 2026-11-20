# Criando seu primeiro servidor MQTT Eclipse Mosquitto no Docker

## 1. Estrutura e permissões dos diretórios

Cria as pastas necessárias, o arquivo de senhas e ajusta o proprietário para o UID/GID `1883` (usuário interno padrão do contêiner Mosquitto):

```bash
mkdir -p config data log
sudo touch ./config/pwfile
sudo chown -R 1883:1883 ./config ./data ./log
sudo chmod 0700 ./config/pwfile
```

## 2. Arquivo `compose.yml`

Cria o arquivo de orquestração do Docker Compose com as portas MQTT (`1883`) e WebSockets (`9001`):

```bash
cat << 'EOF' > compose.yml
services:
  mosquitto:
    image: eclipse-mosquitto:latest
    container_name: mosquitto
    hostname: mqtt
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./config:/mosquitto/config
      - ./data:/mosquitto/data
      - ./log:/mosquitto/log
    stdin_open: true
    tty: true
EOF
```

## 3. Arquivo `config/mosquitto.conf`

Configura os *listeners*, persistência em disco e desabilita conexões anônimas:

```bash
sudo tee ./config/mosquitto.conf > /dev/null << 'EOF'
listener 1883

listener 9001
protocol websockets

persistence true
persistence_file mosquitto.db
persistence_location /mosquitto/data/

allow_anonymous false
password_file /mosquitto/config/pwfile
EOF
```

## 4. Gerar credenciais (`user` / `senha`)

Executa um contêiner temporário para gerar o hash da senha dentro de `pwfile`:

```bash
docker exec mosquitto mosquitto_passwd -b /mosquitto/config/pwfile user password
```



## 5. Verifica se usuario teve senha gerada

```bash
docker exec mosquitto cat /mosquitto/config/pwfile

#esse mata o processo
docker exec mosquitto kill -HUP 1
```

## 5. Iniciar o serviço

Sobe o servidor MQTT em segundo plano:

```bash
docker exec mosquitto mosquitto_pub -h localhost -p 1883 -u "user" -P "password" -t "teste/fiware" -m "ok"
```

---

## Extra: Comandos úteis para PostgreSQL

Derrubar os contêineres removendo volumes e subir apenas o serviço `postgres-db`:

```bash
docker compose down -v
docker compose up -d postgres-db
```