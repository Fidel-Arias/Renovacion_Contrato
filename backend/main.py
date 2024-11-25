from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes

# Generar clave privada
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# Serializar y guardar la clave privada
with open("private_key.pem", "wb") as private_file:
    private_file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Generar clave pública
public_key = private_key.public_key()

# Serializar y guardar la clave pública
with open("public_key.pem", "wb") as public_file:
    public_file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("Claves generadas: public_key.pem y private_key.pem")


# url = "http://192.168.0.152:8005/contract/protected/renew/126.4"  # Reemplaza con la URL de tu endpoint
# headers = {"Content-Type": "application/json"}
# response = requests.post(url, json=payload, headers=headers)

# if response.status_code == 200:
#     print("Mensaje enviado exitosamente:", response.json())
# else:
#     print("Error al enviar el mensaje:", response.status_code, response.text)
