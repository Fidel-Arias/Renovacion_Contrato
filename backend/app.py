from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import aiosmtplib
from email.message import EmailMessage
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
import base64
import requests

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500'],
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*'],
)

# Modelos de datos
class CreateContractRequest(BaseModel):
    price: float


# Endpoint 1: Crear Contrato
@app.post("/contract/create")
async def create_contract(request: CreateContractRequest):
    price = str(request.price)
    print(price)
    try:
        # Leer la clave pública desde el backend
        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        # Cifrar el mensaje
        cifrado = public_key.encrypt(
            price.encode('utf8'),
            padding.PKCS1v15()
        )

        #Codificamos en base64
        cifrado_base64 = base64.b64encode(cifrado).decode('utf-8')

        payload = {
            "mensaje_cifrado": cifrado_base64,
        }
        print(payload)
        return {"message": "Contrato creado y correo enviado exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el contrato: {str(e)}")


class UpdateContractRequest(BaseModel):
    date_start: str
    date_end: str
# Endpoint 2: Actualizar Contrato
@app.post("/contract/protected/renew")
async def update_contract(
    request: CreateContractRequest,
    price: str,
):
    # Verificar autorización
    price = str(request.price)
    print(price)
    
    try:
        # Leer la clave pública desde el backend
        with open("public_key.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())

        # Cifrar el mensaje
        cifrado = public_key.encrypt(
            price.encode('utf8'),
            padding.PKCS1v15()
        )

        #Codificamos en base64
        cifrado_base64 = base64.b64encode(cifrado).decode('utf-8')
        print(cifrado_base64)

        url = "http://34.27.178.31/contract/create"

        response = requests.post('')
        data = {
            "name": "Andre",
            "surnames": "Huaroc Condori",
            "address": "Paucarpata",
            "role": "Developer",
            "birthdate": "2005-02-06",
            "email": "jasonrch2011@gmail.com",
            "price": cifrado_base64,
            "date_start": "2024-10-11",
            "date_end": "2024-10-12",
            "enterprise_name": "Tech Corp",
            "enterprise_ruc": "123456789",
            "enterprise_represent": "Jane Smith",
            "represent_dni": "98765432",
            "dni": "72657497"
        }
        json = data
        responde = requests.post(url, data=json)
        return {"message": "Contrato actualizado y correo enviado exitosamente."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el contrato: {str(e)}")

    

class DecryptRequest(BaseModel):
    cifrado: str
@app.post('/contract/desencrypt')
def decrypt(request: DecryptRequest):
    try:
        # Leer la clave privada desde el backend
        with open("private_key.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)
        
        # Decodificar el mensaje cifrado
        mensaje_cifrado = base64.b64decode(request.cifrado)

        # Descifrar el mensaje
        descifrado = private_key.decrypt(
            mensaje_cifrado,
            padding.PKCS1v15()
        )
        
        # # Decomprimir el mensaje
        # buf = io.BytesIO(descifrado)
        # with gzip.GzipFile(fileobj=buf, mode='r') as f:
        #     json_str = f.read().decode('utf-8')
        
        # Convertir el JSON a diccionario
        email_body = descifrado
        return email_body
    
    except Exception as e:
        return("Error al desencriptar el mensaje: ", str(e))