import httpx
import asyncio
import json

# ===============================
# Configurações do Context Broker
# ===============================

ORION_BASE_URL = "http://localhost:1026"
ORION_ENTITIES_URL = f"{ORION_BASE_URL}/v2/entities/"
ORION_VERSION_URL = f"{ORION_BASE_URL}/version"

FIWARE_SERVICE = "openiot"
FIWARE_SERVICEPATH = "/airQuality"

ORION_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "fiware-service": FIWARE_SERVICE,
    "fiware-servicepath": FIWARE_SERVICEPATH
}

# ===========================
# Função para requisições GET
# ===========================

async def async_request(url: str, headers: dict):
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return res.json()
        except httpx.HTTPStatusError as e:
            print(f"[HTTPStatusError] Status {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"[RequestError] Erro de conexão com Orion: {e}")
        except Exception as e:
            print(f"[Exception] Erro inesperado: {e}")

# ===================
# Funções de Teste
# ===================

async def verificar_orion():
    print("🔍 Verificando versão do Orion Context Broker...")
    version = await async_request(ORION_VERSION_URL, ORION_HEADERS)
    if version:
        print("✅ Orion está online:")
        print(json.dumps(version, indent=2))

async def listar_entidades():
    print("\n📦 Listando entidades registradas...")
    entidades = await async_request(ORION_ENTITIES_URL, ORION_HEADERS)
    if entidades:
        print("✅ Entidades encontradas:")
        print(json.dumps(entidades, indent=2))

# ===================
# Execução principal
# ===================

async def main():
    await verificar_orion()
    await listar_entidades()

if __name__ == "__main__":
    asyncio.run(main())
