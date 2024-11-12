import zipfile
import os

def processar_arquivo(caminho_arquivo, arquivo_consolidado):
    # Inicializa contadores
    total_palavras = 0
    total_caracteres = 0
    linhas_validas = 0

    # Abre o arquivo para leitura
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        # Lê cada linha do arquivo
        for linha in file:
            # Remove espaços em branco e nova linha no início/final
            linha = linha.strip()

            # Ignora linhas em branco
            if not linha:
                continue

            # Conta as palavras e caracteres na linha atual
            palavras = linha.split()
            num_palavras = len(palavras)
            num_caracteres = len(linha)

            # Atualiza os contadores
            total_palavras += num_palavras
            total_caracteres += num_caracteres
            linhas_validas += 1

            # Imprime a linha atual (opcional, caso queira ver o conteúdo)
            # print(linha)
    
    # Escreve as estatísticas no arquivo consolidado
    with open(arquivo_consolidado, 'a', encoding='utf-8') as output_file:
        output_file.write(f"Resumo do arquivo: {caminho_arquivo}\n")
        output_file.write(f"Linhas válidas: {linhas_validas}\n")
        output_file.write(f"Total de palavras: {total_palavras}\n")
        output_file.write(f"Total de caracteres: {total_caracteres}\n")
        output_file.write("\n")  # Espaço extra entre os resumos

def compactar_arquivo(arquivo_consolidado):
    # Caminho para o arquivo ZIP
    caminho_zip = arquivo_consolidado.replace('.txt', '.zip')
    
    # Cria o arquivo ZIP
    with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(arquivo_consolidado, os.path.basename(arquivo_consolidado))
    
    print(f"Arquivo compactado com sucesso: {caminho_zip}")

# Caminho do arquivo consolidado
arquivo_consolidado = "C:\\Users\\mathe\\Documents\\PERSISTÊNCIA\\textos\\consolidado.txt"

# Certifique-se de limpar o arquivo consolidado antes de iniciar, caso seja necessário
with open(arquivo_consolidado, 'w', encoding='utf-8') as file:
    file.write("Resumo Consolidado dos Arquivos\n\n")

# Processa os arquivos
processar_arquivo("C:\\Users\\mathe\\Documents\\PERSISTÊNCIA\\textos\\arquivo1.txt", arquivo_consolidado)
processar_arquivo("C:\\Users\\mathe\\Documents\\PERSISTÊNCIA\\textos\\arquivo2.txt", arquivo_consolidado)
processar_arquivo("C:\\Users\\mathe\\Documents\\PERSISTÊNCIA\\textos\\arquivo3.txt", arquivo_consolidado)

# Compacta o arquivo consolidado em ZIP
compactar_arquivo(arquivo_consolidado)

print("Processamento concluído. Arquivo consolidado compactado em ZIP.")
