import os
import requests
from zipfile import ZipFile
from bs4 import BeautifulSoup

def fetch_pdf_links(url):
    headers = {
        'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        pdf_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.pdf')]
        full_links = [link if link.startswith('http') else f'https://www.gov.br{link}' for link in pdf_links]
        return full_links

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return []

def download_pdf(url, download_folder):
    try:
        filename = url.split('/')[-1]
        file_path = os.path.join(download_folder, filename)

        response = requests.get(url)
        response.raise_for_status()
        
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Download completo: {filename}")
        return file_path
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o PDF: {e}")
        return None

def compress_pdfs(pdf_files, zip_filename):
    try:
        with ZipFile(zip_filename, 'w') as zipf:
            for pdf_file in pdf_files:
                zipf.write(pdf_file, os.path.basename(pdf_file))
                os.remove(pdf_file)  # Remove o arquivo PDF após a compactação
        
        print(f"Arquivos compactados com sucesso em {zip_filename}")
    
    except Exception as e:
        print(f"Erro ao compactar os arquivos: {e}")

def main():
    url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
    download_folder = 'downloads'
    zip_filename = 'anexos.zip'

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    print("Obtendo links dos PDFs...")
    pdf_links = fetch_pdf_links(url)
    
    if not pdf_links:
        print("Nenhum link de PDF encontrado.")
        return
    
    downloaded_files = []
    for pdf_link in pdf_links:
        file_path = download_pdf(pdf_link, download_folder)
        if file_path:
            downloaded_files.append(file_path)
    
    if downloaded_files:
        print("Compactando os arquivos...")
        compress_pdfs(downloaded_files, zip_filename)
    else:
        print("Nenhum PDF foi baixado para compactar.")

if __name__ == '__main__':
    main()