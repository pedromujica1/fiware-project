## Criando seu primeiro servidor MQTT Eclipse Mosquitto no Docker

# 1. Estrutura e permissões dos diretórios
mkdir -p config data log
sudo touch ./config/pwfile
sudo chown -R 1883:1883 ./config ./data ./log
sudo chmod 0700 ./config/pwfile

# 2. Arquivo compose.yml
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

# 3. Arquivo config/mosquitto.conf
cat << 'EOF' > ./config/mosquitto.conf
listener 1883
listener 9001
protocol websockets

persistence true
persistence_file mosquitto.db
persistence_location /mosquitto/data/

allow_anonymous false
password_file /mosquitto/config/pwfile
EOF

# 4. Gerar credenciais (user / senha)
docker run --rm -v $(pwd)/config:/mosquitto/config eclipse-mosquitto:latest mosquitto_passwd -b /mosquitto/config/pwfile user senha

# 5. Iniciar o serviço
docker compose up -d

# Extra comando para derrubar Postgres

docker compose down -v
docker compose up -d postgres-db