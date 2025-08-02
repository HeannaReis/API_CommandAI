# src/utils/dataframe_utils.py
import pandas as pd

# Define a ordem preferencial das colunas para exibição de dados de usuário
PREFERRED_USER_COLUMNS_ORDER = [
    'SAPPlant',
    'EmailAddress',
    'Name',
    'UniqueName',
    'Supervisor.UniqueName', # Nome da coluna ajustado para o padrão usado nos DataFrames
    'ApprovalLimit',
    'LastLoginDate',
    'cus_TimeUpdatedForExport',
    'cus_TimeCreatedForExport'
]

def reorder_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reordena as colunas de um DataFrame, colocando as colunas preferenciais no início,
    seguidas pelas demais colunas na sua ordem original.
    As colunas preferenciais que não existirem no DataFrame serão ignoradas.

    Args:
        df (pd.DataFrame): O DataFrame a ser reordenado.

    Returns:
        pd.DataFrame: O DataFrame com as colunas reordenadas.
    """
    # Identifica as colunas preferenciais que realmente existem no DataFrame
    existing_preferred_cols = [col for col in PREFERRED_USER_COLUMNS_ORDER if col in df.columns]

    # Identifica as demais colunas, mantendo a ordem original entre elas
    other_cols = [col for col in df.columns if col not in existing_preferred_cols]

    # Concatena as listas para formar a nova ordem
    new_column_order = existing_preferred_cols + other_cols

    return df[new_column_order]