# My Markdown page




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