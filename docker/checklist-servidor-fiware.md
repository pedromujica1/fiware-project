# Checklist do pcServidor: escalabilidade vertical FIWARE

Servidor: `ccsc-lscdesktop6` (Ryzen 7 5700G, 31 GiB, Ubuntu 24.04). Cliente (JMeter): outra máquina, ligada por cabo direto numa sub-rede própria (IPs fixos, ver **C**).
Faça **A** e **B** com internet. Se o servidor tiver uma única porta de rede, o cabo (**C**) vem por último.

---

## A. Preparar o servidor (uma vez)

- [ ] **Parar o ShareLaTeX** (não será mais usado; não apague os volumes ainda)
```bash
docker stop nginx sharelatex mongo redis
docker update --restart=no nginx sharelatex mongo redis
docker ps    # não deve sobrar nada rodando
```

- [ ] **Instalar ferramentas**
```bash
sudo apt update && sudo apt install -y iperf3 openssh-server ethtool netcat-openbsd curl
```

- [ ] **Evitar suspensão e atualizações automáticas durante os testes**
```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
sudo systemctl stop unattended-upgrades
```

- [ ] **Desligar SMT e fixar o governor** (voltam ao normal ao reiniciar; refaça após reboot)
```bash
echo off | sudo tee /sys/devices/system/cpu/smt/control
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
nproc                                                          # deve mostrar 8
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor | sort | uniq -c
```

- [ ] **Copiar o projeto** do PC antigo e **substituir** `docker-compose.yaml` e `.env` pelos novos
```bash
mkdir -p ~/fiware && scp -r fiware-user@IP_DO_PC_ANTIGO:~/Desktop/fiware/fiware-project/docker/. ~/fiware/
# copie para ~/fiware os docker-compose.yaml e .env novos (sobrescrevendo)
cd ~/fiware
ls -a                    # config cygnus data log postgres prometheus docker-compose.yaml .env
grep -E "listener|allow_anonymous" config/mosquitto.conf    # precisa ter: listener 1883 e allow_anonymous true
chmod -R a+rwX data log
```

---

## B. Subir a pilha e provisionar

- [ ] **Conferir portas livres e subir**
```bash
cd ~/fiware
ss -tlnp | grep -E ':(27017|1026|4041|5432|5055|5080|1883|9002|8080|9090)\b'    # deve ficar vazio
docker compose pull
docker compose up -d
docker compose ps
```

- [ ] **Provisionar** (a pilha nova começa vazia): rode os mesmos scripts/`curl` do artigo para criar o service group e os dispositivos no IoT Agent e a subscription Orion → Cygnus. Conferir:
```bash
curl -s localhost:1026/v2/subscriptions | head -c 400
curl -s localhost:4041/iot/devices -H 'fiware-service: openiot' -H 'fiware-servicepath: /' | head -c 400   # ajuste service/servicepath se forem outros
```

- [ ] **Registrar o ambiente** (para replicar)
```bash
mkdir -p ~/fiware/resultados
{ uname -r; lscpu | grep -E "Model name|^CPU\(s\)|Thread|MHz"; free -h; docker --version; docker compose version; } > resultados/ambiente.txt
docker compose images > resultados/versoes.txt
```

- [ ] **Criar as funções de apoio** (usadas em D)
```bash
cat > ~/fiware/helpers.sh <<'EOF'
cpu_stat() {   # throttling de CPU por container (cgroup v2)
  for c in fiware-orion-1 fiware-iotagent-lora-1 fiware-mongodb-1 fiware-cygnus db-postgres mosquitto; do
    id=$(docker inspect -f '{{.Id}}' $c)
    echo "$c $(grep -E 'nr_periods|nr_throttled|throttled_usec' /sys/fs/cgroup/system.slice/docker-$id.scope/cpu.stat | tr '\n' ' ')"
  done
}
rows() {       # linhas inseridas pelo Cygnus (contador acumulado: use a diferença entre antes e depois)
  docker exec db-postgres psql -U postgres -d postgres -tAc "SELECT coalesce(sum(n_tup_ins),0) FROM pg_stat_user_tables WHERE schemaname='openiot'"
}
EOF
source ~/fiware/helpers.sh
```

---

## C. Rede isolada: IP fixo em cada PC (cabo direto)

Ideia: o cabo liga os dois PCs direto, e cada um recebe um **IP fixo numa sub-rede só deles**, sem gateway nem DNS. Assim o tráfego do teste passa só pelo cabo, sem concorrer com a rede do lab. Se o servidor tiver uma única porta de rede, faça este bloco por último.

| PC | IP | Máscara |
|---|---|---|
| pcServidor | `10.99.99.1` | `/24` (255.255.255.0) |
| pcCliente (JMeter) | `10.99.99.2` | `/24` (255.255.255.0) |

- [ ] **Confirmar que a faixa está livre** (em cada PC; a saída deve ficar vazia)
```bash
ip -4 route | grep 10.99.99
```

- [ ] **Ligar o cabo e achar a interface** (em cada PC)
```bash
ip -br link                                              # achar a interface (ex.: enp3s0)
sudo ethtool enp3s0 | grep -E "Speed|Link detected"      # esperado: 1000Mb/s e yes
```

- [ ] **No servidor** (IP `10.99.99.1`, sem gateway)
```bash
sudo nmcli connection add type ethernet ifname enp3s0 con-name teste-direto \
  ipv4.method manual ipv4.addresses 10.99.99.1/24 ipv4.never-default yes ipv6.method disabled
sudo nmcli connection up teste-direto
```

- [ ] **No cliente** (IP `10.99.99.2`, sem gateway)

Ubuntu (troque `enp3s0` pela interface do cliente):
```bash
sudo nmcli connection add type ethernet ifname enp3s0 con-name teste-direto \
  ipv4.method manual ipv4.addresses 10.99.99.2/24 ipv4.never-default yes ipv6.method disabled
sudo nmcli connection up teste-direto
```
Windows (PowerShell como administrador; deixe gateway e DNS em branco):
```powershell
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 10.99.99.2 -PrefixLength 24
```

- [ ] **Testar nos dois sentidos**
```bash
# no servidor
ping -c 4 10.99.99.2
iperf3 -s                                # no cliente: iperf3 -c 10.99.99.1  (esperado ~940 Mbits/s; anote o resultado)

# no cliente
ping -c 4 10.99.99.1
ip route get 10.99.99.1                  # deve mostrar a interface do cabo
nc -zv 10.99.99.1 1883                   # Mosquitto
curl http://10.99.99.1:1026/version      # Orion
ssh pedro@10.99.99.1                     # opcional: controlar o servidor pelo cabo
```
Se o cliente for Windows, o firewall dele bloqueia ping por padrão: faça o ping a partir do cliente e teste as portas.

- [ ] **JMeter no cliente** aponta para `10.99.99.1` (Mosquitto `1883`, Orion `1026`).

Desfazer (em cada PC): `sudo nmcli connection delete teste-direto`

---

## D. Para cada rodada (repetir por nível)

Níveis sugeridos: `0.25 / 0.5 / 1 / 2 / 4` CPUs, **um componente por vez** (valores finais a definir após o `docker stats` do pico).

- [ ] **1. Definir o nível e recriar** (exemplo: Orion com 0.5 CPU)
```bash
cd ~/fiware && source helpers.sh
sed -i 's/^ORION_CPUS=.*/ORION_CPUS=0.5/' .env
docker compose up -d --force-recreate
docker inspect $(docker compose ps -q) --format '{{.Name}} cpus={{.HostConfig.NanoCpus}} mem={{.HostConfig.Memory}}'    # 0.5 CPU = 500000000
```
Limpe os dados da rodada anterior como você fazia no artigo e reprovisione se necessário.

- [ ] **2. Antes do teste**
```bash
tag=orion0.5_rps1000          # identifica a rodada: componente+nível_taxa
cp .env resultados/$tag.env
cpu_stat > resultados/$tag.antes ; rows > resultados/$tag.rows_antes
```

- [ ] **3. Durante o teste** (rode o JMeter no cliente; aqui, em outro terminal; Ctrl+C ao terminar)
```bash
while true; do docker stats --no-stream --format '{{.Name}},{{.CPUPerc}},{{.MemUsage}}' | sed "s/^/$(date +%T),/"; sleep 5; done > resultados/$tag.stats.csv
```

- [ ] **4. Depois do teste**
```bash
sleep 40                                   # flush do Cygnus (batch_timeout = 30 s)
cpu_stat > resultados/$tag.depois ; rows > resultados/$tag.rows_depois
docker inspect $(docker compose ps -aq) --format '{{.Name}} OOM={{.State.OOMKilled}} restarts={{.RestartCount}} exit={{.State.ExitCode}}'
docker logs --since 10m fiware-cygnus 2>&1 | grep -iE "channel|exception" | tail -20
curl -s localhost:1026/statistics | python3 -m json.tool | head -60       # fila de notificações do Orion
```

Como ler:
- **throttling** = diferença de `nr_throttled` ÷ diferença de `nr_periods` entre `.antes` e `.depois` (perto de 0 = o limite de CPU não foi o gargalo)
- **escritas** = (`rows_depois` − `rows_antes`) ÷ 4
- qualquer `OOM=true`, `restarts` > 0 ou erro de canal no Cygnus invalida a rodada

---

## E. Ao terminar

```bash
docker compose down            # mantém os volumes; use -v para apagar os dados
sudo nmcli connection delete teste-direto
```
Guarde a pasta `~/fiware/resultados` (contém `ambiente.txt`, `versoes.txt`, `.env` e as medições de cada rodada).