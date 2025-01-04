"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""

import os
from glob import glob

import pandas as pd  # type: ignore


def load_data(input_file):
    """Loads csv file from path"""
    df = pd.read_csv(input_file, sep=";", index_col=0)

    return df


def _create_ouptput_directory(output_directory):
    if os.path.exists(output_directory):
        for file in glob(f"{output_directory}/*"):
            os.remove(file)
        os.rmdir(output_directory)
    os.makedirs(output_directory)


def _save_output(output_directory, filename, df):
    df.to_csv(f"{output_directory}/{filename}.csv", index=False, sep=";")


def int_transform_types(df):
    """Transforma a entero las columnas numéricas"""
    df = df.copy()

    df["monto_del_credito"] = df["monto_del_credito"].str.strip()
    df["monto_del_credito"] = df["monto_del_credito"].str.strip("$")
    df["monto_del_credito"] = df["monto_del_credito"].str.replace(".00", "")
    df["monto_del_credito"] = df["monto_del_credito"].str.replace(",", "")

    df["monto_del_credito"] = df["monto_del_credito"].astype(int)
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype(int)

    return df


def clean_fecha(df):
    """4. Verificación de rangos de fecha"""
    df = df.copy()

    # Dada la naturaleza del DF asumimos que el día va primero
    df["fecha_de_beneficio"] = pd.to_datetime(
        df["fecha_de_beneficio"], dayfirst=True, format="mixed"
    )

    return df


def clean_sexo(df):
    """Easy str transformations"""
    df = df.copy()

    df["sexo"] = df["sexo"].str.strip()
    df["sexo"] = df["sexo"].str.lower()

    return df


def clean_emprendimiento(df):
    """Easy str transformations"""
    df = df.copy()

    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.strip()
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower()

    return df


def clean_linea_credito(df):
    """Limpieza de línea de crédito"""
    df = df.copy()

    df["línea_credito"] = df["línea_credito"].str.strip()
    df["línea_credito"] = df["línea_credito"].str.lower()
    df["línea_credito"] = df["línea_credito"].str.replace(" ", "")

    df["línea_credito"] = df["línea_credito"].str.translate(
        str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    )

    return df


def clean_idea_negocio(df):
    """Limpieza idea negocio"""

    df = df.copy()

    df["idea_negocio"] = df["idea_negocio"].str.strip()
    df["idea_negocio"] = df["idea_negocio"].str.lower()
    df["idea_negocio"] = df["idea_negocio"].str.replace("á", "a")
    df["idea_negocio"] = df["idea_negocio"].str.replace("é", "e")
    df["idea_negocio"] = df["idea_negocio"].str.replace("í", "i")
    df["idea_negocio"] = df["idea_negocio"].str.replace("ó", "o")
    df["idea_negocio"] = df["idea_negocio"].str.replace("ú", "u")
    df["idea_negocio"] = df["idea_negocio"].str.replace(" ", "")

    df["idea_negocio"] = df["idea_negocio"].str.translate(
        str.maketrans("", "", "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
    )

    return df


def clean_barrio(df):
    """Limpieza idea negocio"""

    # 1. Limpieza básica del texto
    df = df.copy()

    df["barrio"] = df["barrio"].str.lower()
    df["barrio"] = df["barrio"].str.replace("_", " ")
    df["barrio"] = df["barrio"].str.replace("-", " ")

    return df


def verify_numeric_ranges(df):
    """2. Verificación de Rangos numéricos"""
    df = df.copy()

    # df = df[df["estrato"] >= 1]
    # df = df[(df["comuna_ciudadano"] <= 16) & (df["comuna_ciudadano"] >= 1)]

    return df


def no_dupe(df):
    """10. Registros duplicados"""
    df = df.copy()
    df.drop_duplicates(inplace=True)

    return df


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

    df = load_data("files/input/solicitudes_de_credito.csv")

    df = int_transform_types(df)

    # Clean easy String Columns
    df = clean_sexo(df)
    df = clean_emprendimiento(df)
    df = clean_linea_credito(df)

    df = clean_fecha(df)

    # Clean more complex String Columns

    df = clean_idea_negocio(df)
    df = clean_barrio(df)

    # Verify numeric ranges of Comunas & Estratos
    # df = verify_numeric_ranges(df)

    # Drop duplicates and missing
    df = df.dropna()
    df = no_dupe(df)

    _create_ouptput_directory("files/output")
    _save_output("files/output", "solicitudes_de_credito", df)

    return 1


pregunta_01()
