import os
import httpx
import base64
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()

BELVO_SECRET_ID = os.getenv("BELVO_SECRET_ID")
BELVO_SECRET_PASSWORD = os.getenv("BELVO_SECRET_PASSWORD")
# La URL base para la Mock API de Belvo
BELVO_API_URL = os.getenv("BELVO_API_URL")

# Link ID estático para las peticiones a la Mock API
MOCK_LINK_ID = "8848bd0c-9c7e-4f53-a732-ec896b11d4c4"

async def get_belvo_basic_auth_headers():
    if not BELVO_SECRET_ID or not BELVO_SECRET_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Belvo credentials (BELVO_SECRET_ID or BELVO_SECRET_PASSWORD) not set in environment variables."
        )
    
    credentials = f"{BELVO_SECRET_ID}:{BELVO_SECRET_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    
    return {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

# Esta función ya no es necesaria si todas las llamadas usan Basic Auth directamente
# async def get_belvo_access_token():
#     headers = await get_belvo_basic_auth_headers()
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.post(
#                 f"{BELVO_API_URL}/api/tokens/",
#                 headers=headers
#             )
#             response.raise_for_status()
#             return response.json().get("access")
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(
#                 status_code=e.response.status_code,
#                 detail=f"Error al obtener token de Belvo: {e.response.text}"
#             )
#         except httpx.RequestError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Error de red al conectar con Belvo: {e}"
#             )

async def get_belvo_institutions():
    headers = await get_belvo_basic_auth_headers()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BELVO_API_URL}/institutions/", # Ruta ajustada según tu baseURL
                headers=headers
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error al obtener instituciones de Belvo: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de red al conectar con Belvo: {e}"
            )

# La función get_belvo_link_creation_token ya no es necesaria si no se usa el widget
# async def get_belvo_link_creation_token():
#     access_token = await get_belvo_access_token()
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json",
#         "Accept": "application/json"
#     }
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.post(
#                 f"{BELVO_API_URL}/api/token-creation-requests/",
#                 headers=headers
#             )
#             response.raise_for_status()
#             return response.json().get("link_creation_token")
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(
#                 status_code=e.response.status_code,
#                 detail=f"Error al obtener token de creación de link de Belvo: {e.response.text}"
#             )
#         except httpx.RequestError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"Error de red al conectar con Belvo: {e}"
#             )

async def get_belvo_accounts():
    headers = await get_belvo_basic_auth_headers()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BELVO_API_URL}/accounts/?link={MOCK_LINK_ID}", # Ruta y link_id ajustados
                headers=headers
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error al obtener cuentas de Belvo para link {MOCK_LINK_ID}: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de red al conectar con Belvo: {e}"
            )

async def get_belvo_balances():
    headers = await get_belvo_basic_auth_headers()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BELVO_API_URL}/br/balances/?link={MOCK_LINK_ID}",
                headers=headers
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error al obtener balances de Belvo para link {MOCK_LINK_ID}: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de red al conectar con Belvo: {e}"
            )

async def get_belvo_transactions():
    headers = await get_belvo_basic_auth_headers()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BELVO_API_URL}/transactions/?link={MOCK_LINK_ID}",
                headers=headers
            )
            response.raise_for_status()
            return response.json().get("results", [])
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Error al obtener transacciones de Belvo para link {MOCK_LINK_ID}: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de red al conectar con Belvo: {e}"
            )