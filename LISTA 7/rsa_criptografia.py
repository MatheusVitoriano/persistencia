from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.primitives.hashes import SHA256
import hashlib
from pathlib import Path

#Código base começa aqui

# Gerar chaves assimétricas
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()


# Função para criptografar com chave pública
def encrypt_asymmetric(file_path, public_key):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    encrypted_data = public_key.encrypt(
        file_data,
        OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
    )
    encrypted_file = f"{file_path}.enc"
    with open(encrypted_file, 'wb') as f:
        f.write(encrypted_data)
    print(f"Arquivo criptografado: {encrypted_file}")
    return encrypted_file


# Função para decriptar com chave privada
def decrypt_asymmetric(file_path, private_key):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = private_key.decrypt(
        encrypted_data,
        OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
    )
    decrypted_file = file_path.replace('.enc', '.dec')
    with open(decrypted_file, 'wb') as f:
        f.write(decrypted_data)
    print(f"Arquivo decriptado: {decrypted_file}")
    return decrypted_file


# Função para calcular hash SHA-256
def calculate_sha256(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    sha256_hash = hashlib.sha256(file_data).hexdigest()
    print(f"SHA-256 do arquivo {file_path}: {sha256_hash}")
    return sha256_hash

#Código base termina aqui

# Função principal para o processo completo
def process_file(file_path):
    # Etapa 1: Criptografar o arquivo
    encrypted_file = encrypt_asymmetric(file_path, public_key)

    # Etapa 2: Decriptar o arquivo
    decrypted_file = decrypt_asymmetric(encrypted_file, private_key)

    # Etapa 3: Verificar a integridade
    original_hash = calculate_sha256(file_path)
    decrypted_hash = calculate_sha256(decrypted_file)

    
    if original_hash == decrypted_hash:
        print("Os arquivos são idênticos! Integridade verificada com sucesso.")
    else:
        print("Os arquivos são diferentes! Integridade comprometida.")


# Exemplo de uso
if __name__ == "__main__":
    # Caminho para o arquivo de teste
    file_path = "arquivo_teste.txt"
    
    # Criar arquivo de teste
    with open(file_path, 'w') as f:
        f.write("Este é um teste de criptografia assimétrica e verificação de integridade.")
    
    # Executar o processo completo
    process_file(file_path)
