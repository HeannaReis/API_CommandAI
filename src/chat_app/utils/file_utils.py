# src/utils/file_utils.py
import pandas as pd
import logging
import os
import streamlit as st

def carregar_csv_com_filtro(caminho_arquivo, filtro_coluna=None, filtro_valor=None, header_row=1):
    """Carrega um arquivo CSV, detecta a codificação e aplica um filtro."""
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            # Verificar se o arquivo começa com um BOM UTF-8
            if f.read(3) == '\ufeff':
                f.seek(3)  # Ignorar o BOM
            else:
                f.seek(0)  # Voltar ao início se não houver BOM

            # Usar pandas para ler o CSV
            df = pd.read_csv(f, header=header_row, low_memory=False)

        # Aplicar o filtro se a coluna e o valor forem fornecidos
        if filtro_coluna and filtro_valor:
            df_filtrado = df[df[filtro_coluna].str.contains(filtro_valor, na=False)]
        elif filtro_valor:
            # Se só o valor do filtro for fornecido, verifica em qualquer coluna
            df_filtrado = df[df.apply(lambda row: row.astype(str).str.contains(filtro_valor, na=False).any(), axis=1)]
        else:
            df_filtrado = df

        logging.info(f"Arquivo {caminho_arquivo} carregado e filtrado com sucesso.")
        return df_filtrado
    except FileNotFoundError:
        st.error(f"Arquivo {caminho_arquivo} não encontrado.")
        logging.error(f"Arquivo {caminho_arquivo} não encontrado.")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar ou filtrar o arquivo {caminho_arquivo}: {e}")
        logging.error(f"Erro ao carregar ou filtrar o arquivo {caminho_arquivo}: {e}")
        return None