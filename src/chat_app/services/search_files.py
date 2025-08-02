import os
import glob
from pathlib import Path
from config.config import Config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ler_arquivos_por_extensao(extensions: list[str]) -> str: # <--- Nova função mais genérica
    """
    Lê todo o conteúdo de arquivos com as extensões fornecidas (ex: ['.py', '.java'])
    a partir do diretório base configurado.
    """
    src_dir = Config.BASE_DIR
    conteudo_total = ""

    if not src_dir.exists():
        logging.warning(f"Diretório 'src' não encontrado: {src_dir}")
        return ""

    # Itera sobre cada extensão fornecida
    for ext in extensions:
        # Garante que a extensão comece com um ponto, se ainda não tiver
        if not ext.startswith('.'):
            ext = '.' + ext

        padrao_busca = os.path.join(src_dir.as_posix(), '**', f'*{ext}') # <--- Padrão dinâmico
        arquivos = glob.glob(padrao_busca, recursive=True)

        for arquivo in sorted(arquivos):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    rel_path = os.path.relpath(arquivo, src_dir)
                    # Adiciona um cabeçalho para indicar o arquivo e seu caminho relativo
                    conteudo_total += f"\n\n# {rel_path}\n\n{f.read()}"
                    logging.info(f"Arquivo lido com sucesso: {rel_path}")
            except Exception as e:
                logging.error(f"Erro ao ler o arquivo {arquivo}: {e}")
                continue

    return conteudo_total