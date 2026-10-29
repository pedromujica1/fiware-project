#!/bin/bash


{
echo "===== SISTEMA ====="
cat /etc/os-release | grep -E "PRETTY_NAME"
uname -r

echo -e "\n===== CPU ====="
lscpu | grep -E "Model name|^CPU\(s\)|Thread|Core|Socket|MHz|L3 cache|NUMA node\(s\)"
nproc
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null

echo -e "\n===== MEMORIA ====="
free -h
swapon --show

echo -e "\n===== DISCO ====="
lsblk -d -o NAME,SIZE,ROTA,TYPE,MODEL   # ROTA=0 => SSD/NVMe, 1 => HDD
df -h /var/lib/docker .

echo -e "\n===== DOCKER ====="
docker --version
docker compose version
docker info 2>/dev/null | grep -E "Server Version|Storage Driver|Cgroup Driver|Cgroup Version|CPUs|Total Memory|Swap"
stat -fc %T /sys/fs/cgroup/   # cgroup2fs => v2 | tmpfs => v1

echo -e "\n===== LIMITES ATUAIS DOS CONTAINERS ====="
docker ps --format '{{.Names}}' | xargs -I{} docker inspect {} \
  --format '{{.Name}} | NanoCpus={{.HostConfig.NanoCpus}} | Memory={{.HostConfig.Memory}} | CpusetCpus={{.HostConfig.CpusetCpus}}'

echo -e "\n===== CONSUMO ATUAL (ocioso) ====="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
} > specs_servidor.txt 2>&1

cat specs_servidor.txt
