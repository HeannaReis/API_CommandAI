import os
import glob
from pathlib import Path
from config.config import Config
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ler_todos_arquivos_python_e_java() -> str:
    """Lê todo o conteúdo de todos os arquivos .py e .java a partir de src/"""
    src_dir = Config.BASE_DIR

    conteudo_total = ""

    if not src_dir.exists():
        logging.warning(f"Diretório 'src' não encontrado: {src_dir}")
        return ""

    # Busca arquivos .py e .java separadamente
    padrao_busca_py = os.path.join(src_dir, '**', '*.py')
    padrao_busca_java = os.path.join(src_dir, '**', '*.java')

    arquivos_py = glob.glob(padrao_busca_py, recursive=True)
    arquivos_java = glob.glob(padrao_busca_java, recursive=True)

    arquivos = arquivos_py + arquivos_java
    arquivos.sort() # Ordena a lista completa

    for arquivo in arquivos:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                rel_path = os.path.relpath(arquivo, src_dir)
                conteudo_total += f"\n\n# {rel_path}\n\n{f.read()}"
                logging.info(f"Arquivo lido com sucesso: {rel_path}")
        except Exception as e:
            logging.error(f"Erro ao ler o arquivo {arquivo}: {e}")
            continue

    return conteudo_total