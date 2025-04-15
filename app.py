from flask import Flask, render_template
from dotenv import load_dotenv
from cursepy.errors import CurseBaseException
from datetime import datetime
import os
import cursepy
import json
import re

load_dotenv()

app = Flask(__name__)
app.debug = True

def remover_banner_bisecthosting(descricao_html):
    """Remove o banner da BisectHosting da string HTML de descrição."""
    print("DEBUG: HTML da descrição ANTES da remoção do banner:", descricao_html) # LOG ANTES
    banner_pattern = re.compile(
        r'<p>\s*<a\s+href="[^"]*bisecthosting\.com[^"]*"[^>]*>\s*<strong>\s*<img\s+src="[^"]*bisecthosting\.com/partners/custom-banners/[^"]*\.webp"[^>]*>\s*</strong>\s*</a>\s*</p>',
        re.IGNORECASE | re.DOTALL
    )
    descricao_sem_banner = banner_pattern.sub('', descricao_html)
    print("DEBUG: HTML da descrição DEPOIS da remoção do banner:", descricao_sem_banner) # LOG DEPOIS
    return descricao_sem_banner

def formatar_data(data_iso):
    """
    Converte uma string de data no formato ISO 8601 para um formato legível.

    Args:
    data_iso: Uma string de data e hora no formato 'AAAA-MM-DDTHH:MM:SS.fffZ'.

    Returns:
    Uma string da data e hora formatada no padrão 'AAAA-MM-DD HH:MM:SS'.
    Retorna None em caso de erro na conversão.
    """
    try:
        # Remove a parte 'date=' se estiver presente e remove o 'Z' indicando UTC
        data_string = data_iso.replace("date='", "").replace("'", "").replace('Z', '')
        # Converte a string para um objeto datetime
        data_objeto = datetime.fromisoformat(data_string)
        # Formata o objeto datetime para o formato desejado
        data_formatada = data_objeto.strftime('%d/%m/%Y %H:%M')
        return data_formatada
    except ValueError:
        print(f"Erro ao converter a data: {data_iso}")
    return None

# Exemplo de uso:
data_iso = '2025-03-31T22:56:51.353Z'
data_normal = formatar_data(data_iso)

if data_normal:
    print(f"A data no formato normal é: {data_normal}")

if data_normal:
    print(f"A data no formato normal é: {data_normal}")

@app.route('/')
async def index():
    modpack_id = os.getenv('MODPACK_ID')
    curse_api_key = os.getenv('CURSE_API_KEY')

    if not modpack_id:
        return "Erro: ID do modpack não encontrado no arquivo .env", 500
    if not curse_api_key:
        return "Erro: Chave da API da CurseForge não encontrada no arquivo .env", 500

    client = cursepy.CurseClient(curse_api_key=curse_api_key)
    downloads = 0
    descricao_final = "Descrição não disponível."
    try:
        print("Passo 1: Cliente CursePy inicializado.")
        modpack = client.addon(int(modpack_id))
        print(f"Passo 2: Modpack obtido: {modpack.name if hasattr(modpack, 'name') else 'Objeto Modpack'}.")
        print(f"Atributos do objeto modpack (dir): {dir(modpack)}")
        descricao_bytes = modpack.description.raw
        descricao_completa = descricao_bytes.decode('utf-8').strip() # Aplicando .strip() AQUI

        print("DEBUG: Descrição COMPLETA (bruta - JSON):", descricao_completa) # LOG BRUTO

        try:
            descricao_json = json.loads(descricao_completa)
            descricao_html = descricao_json.get('data', '') # Extraindo o HTML
            descricao_sem_banner = remover_banner_bisecthosting(descricao_html) # Removendo o banner do HTML
            descricao_final = descricao_sem_banner
            print(f"Descrição FINAL (sem banner): {descricao_final}") # DEBUG
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON da descrição.") # DEBUG
            descricao_final = descricao_completa # Se falhar, usa a versão original

        files_info = client.addon_files(int(modpack_id))
        print(f"Passo 3: Informações dos arquivos obtidas: {files_info}.")
        changelog_content = "Changelog não encontrado."
        latest_file = None
        if files_info and isinstance(files_info, tuple) and len(files_info) > 0:
            latest_file = max(files_info, key=lambda f: f.date)
            print(f"Passo 4: Arquivo mais recente encontrado: {latest_file.display_name if hasattr(latest_file, 'display_name') else 'Arquivo Mais Recente'}.")
            print("DEBUG: Chegou após encontrar o latest_file")
            changelog_object = latest_file.changelog
            print(f"Tipo de changelog_object: {type(changelog_object)}")
            print(f"Atributos de changelog_object (dir): {dir(changelog_object)}")
            if hasattr(changelog_object, 'raw'):
                changelog_bytes = changelog_object.raw
                changelog_string = changelog_bytes.decode('utf-8')
                print(f"Conteúdo do changelog (decodificado ANTES do JSON): {changelog_string}")
                try:
                    changelog_json = json.loads(changelog_string)
                    print(f"JSON decodificado com sucesso: {changelog_json}")
                    changelog_content = changelog_json.get('data', changelog_content)
                    print(f"Changelog extraído do JSON: {changelog_content}")
                except json.JSONDecodeError as e:
                    print(f"Erro ao decodificar JSON do changelog: {e}")
                    print(f"String que falhou na decodificação: {changelog_string}")

        version = latest_file.display_name
        date = latest_file.date

        data_iso = date
        data_normal = formatar_data(data_iso)

        downloads = modpack.download_count
        print(f"TIPO de changelog_content ANTES do template: {type(changelog_content)}")
        print(f"VALOR de changelog_content ANTES do template: {changelog_content}")

        return render_template('index.html', changelog=changelog_content, downloads=downloads, description=descricao_final, version=version, date=data_normal)
    except CurseBaseException as e:
        print(f"Erro CurseForgeAPIError: {e}")
        return f"Erro ao acessar a API da CurseForge: {e}", 500
    except Exception as e:
        print(f"Erro Genérico: {e}")
        return f"Ocorreu um erro inesperado: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)