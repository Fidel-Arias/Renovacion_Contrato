import google.generativeai as genai
from fastapi.responses import FileResponse
import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from fpdf import FPDF
from fastapi.middleware.cors import CORSMiddleware
import base64
import requests
import jwt
import secrets


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
SECRET_KEY = os.getenv('SECRET_KEY')

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
    secret_key = secrets.token_hex(32)
    print(secret_key)
    # Dato a firmar
    price = contrato.salario

    # Crear la firma HS256
    token = jwt.encode(price, SECRET_KEY, algorithm='HS256')

    # Enviar el dato y la firma a la API en Rust
    url = "http://localhost:8000/renew/123.45"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "date_start": "2023-01-01",
        "date_end": "2023-12-31"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

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
