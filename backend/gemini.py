import google.generativeai as genai
from fastapi.responses import FileResponse
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from fpdf import FPDF
from fastapi.middleware.cors import CORSMiddleware
from requests.exceptions import RequestException
import requests
import jwt
import secrets
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500'],
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*'],
)
load_dotenv()
genai.configure(api_key=os.getenv('API_KEY'))
# SECRET_KEY = os.getenv('SECRET_KEY')

class ContratoData(BaseModel):
    empresa: str
    ruc: str
    representante: str
    dni_representante: str
    nombre_trabajador: str
    dni_trabajador: str
    domicilio: str
    objeto_social: str
    puesto: str
    inicio_contrato: str
    fin_contrato: str
    f_inicio: str
    f_fin: str
    h_inicio: str
    h_fin: str
    salario: float

@app.post('/generar-contrato')
async def generar_contrato(contrato: ContratoData):

    # # Generar una clave privada (esto debería hacerse una vez y almacenarse de forma segura)
    # private_key = Ed25519PrivateKey.generate()

    # # Serializar la clave privada para almacenarla
    # private_bytes = private_key.private_bytes(
    #     encoding=serialization.Encoding.Raw,
    #     format=serialization.PrivateFormat.Raw,
    #     encryption_algorithm=serialization.NoEncryption()
    # )
    # # Guardar la clave privada en un archivo (esto debería hacerse una vez)
    # with open("private_key.bin", "wb") as f:
    #     f.write(private_bytes)
    try:
        # Cargar la clave privada desde el archivo
        with open("private_key.bin", "rb") as f:
            private_bytes = f.read()
            print('Private key: ', private_bytes)
            private_key = Ed25519PrivateKey.from_private_bytes(private_bytes)
            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3Mjk4ODgxMDcsInN0YXJ0IjoiMjAyNC0xMC0yNCIsImZpbmlzaCI6IjIwMjUtMDMtMjQiLCJpZCI6eyIkb2lkIjoiNjcxYWFkZWE4ZGNjYjBmNDhkZTFkZGIwIn19.cTurbVgTsKJud98NNrn9yUDpVyH-P1pCodwH9pCVik0'

            # Dato a firmar
            price = "123.45"
            message = price.encode()

            print('MENSAJE:', message)

            # Firmar el dato
            signature = private_key.sign(message)

            print('FIRMA: ', signature)

            # Convertir la firma a base64 para enviarla
            signature_base64 = base64.b64encode(signature).decode()

            print('BASE64: ', signature_base64)

            # Enviar el dato y la firma a la API en Rust
            url = "http://192.168.234.176:8005/contract/protected/renew/126.4"
            headers = {
                "X-Signature": signature_base64,
                "Authorization": f"Bearer {token}"
            }
            data = {
                "date_start": "2023-01-01",
                "date_end": "2023-12-31"
            }
            response = requests.post(url, json=data, headers=headers)
            print(response.json())

    except Exception as e:
        print("Error: ", e)


    # try: 
    # # Crear la firma HS256
    #     token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3Mjk4ODgxMDcsInN0YXJ0IjoiMjAyNC0xMC0yNCIsImZpbmlzaCI6IjIwMjUtMDMtMjQiLCJpZCI6eyIkb2lkIjoiNjcxYWFkZWE4ZGNjYjBmNDhkZTFkZGIwIn19.cTurbVgTsKJud98NNrn9yUDpVyH-P1pCodwH9pCVik0'

    #     # Enviar el dato y la firma a la API en Rust
    #     url = "http://172.20.10.11:8005/contract/protected/renew/126.4"
    #     headers = {
    #         "Authorization": f"Bearer {token}"
    #     }
    #     data = {
    #         "date_start": "2023-01-01",
    #         "date_end": "2023-12-31"
    #     }
    #     response = requests.post(url, json=data, headers=headers)
    #     response.raise_for_status()
    # except RequestException as e:
    #     if e.response is not None:
    #         print("Error: ", e.response.text)
    #     else:
    #         print("Request failed: ", e)

    # model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    # model_pdf = Path('C:/Users/arias/Documentos/Sexto_Semestre/Comp_en_Red_III/Teoria/PROYECTO_REDES/backend/CONTRATO_DE_TRABAJO.pdf')
    # sample_pdf = genai.upload_file(model_pdf)
    # prompt = f'''Generame un texto para un contrato de trabajo en formato PDF, utiliza el ejemplo del documento y reemplaza los placeholders del documento CONTRATO_DE_TRABAJO con los siguientes valores: 
    # empresa: {contrato.empresa}\n
    # ruc: {contrato.ruc}\n
    # representante: {contrato.representante}\n
    # dni_representante: {contrato.dni_representante}\n
    # nombre_trabajador: {contrato.nombre_trabajador}\n
    # dni_trabajador: {contrato.dni_trabajador}\n
    # domicilio: {contrato.domicilio}\n
    # objeto_social: {contrato.objeto_social}\n
    # puesto: {contrato.puesto}\n
    # inicio_contrato: {contrato.inicio_contrato}\n
    # fin_contrato: {contrato.fin_contrato}\n
    # f_inicio: {contrato.f_inicio}\n
    # f_fin: {contrato.f_fin}\n
    # h_inicio: {contrato.h_inicio}\n
    # h_fin: {contrato.h_fin}\n
    # salario: {contrato.salario} '''
    # response = model.generate_content([prompt, sample_pdf])

    # #Crear PDF
    # pdf = FPDF()
    # pdf.add_page()
    # pdf.set_font('Arial', 'B', 16)
    # pdf.cell(0, 10, 'Contrato de Trabajo', 0, 1, 'C')
    # pdf.set_font('Arial', '', 12)
    # pdf.multi_cell(0, 10, response.text.replace("“", '"').replace("”", '"').replace("**", "").replace('## CONTRATO DE TRABAJO', ''))
    # pdf_output = "contrato_generado.pdf"
    # pdf.output(pdf_output)
    # return FileResponse(pdf_output, media_type='application/pdf', filename='Contrato_de_Trabajo.pdf')
