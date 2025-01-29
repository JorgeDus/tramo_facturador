import pandas as pd
import streamlit as st
import glob
import io

# Buscar todos los archivos Parquet divididos
file_paths = sorted(glob.glob("data/tramo_facturador_part_*.parquet"))

# Cargar y unir todos los fragmentos en un solo DataFrame
@st.cache_data
def load_data():
    try:
        data_parts = [pd.read_parquet(file) for file in file_paths]
        data = pd.concat(data_parts, ignore_index=True)
        return data
    except Exception as e:
        st.error(f"Error al cargar los archivos: {e}")
        return None

# Función para buscar información por RUT
def search_by_rut(data, rut_value):
    result = data[data['RUT'] == rut_value]
    if not result.empty:
        return result[['RUT', 'Razón social', 'Tramo según ventas', 'Facturador']]
    else:
        return None

# Función para búsqueda masiva desde un archivo Excel
def search_bulk_ruts(data, uploaded_file):
    try:
        input_df = pd.read_excel(uploaded_file, dtype={"RUT": str})  # Asegurar que RUT es string
        if "RUT" not in input_df.columns:
            st.error("El archivo debe contener una columna llamada 'RUT'.")
            return None

        merged_df = input_df.merge(data, on="RUT", how="left")  # Hacer el join con los datos
        return merged_df
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
        return None

# Interfaz en Streamlit
st.title("Buscador Tramo Según Ventas y Tipo de Facturador")

# Cargar datos al iniciar la app
data = load_data()

# Sección 1: Búsqueda individual por RUT
st.header("Consulta individual por RUT")
if data is not None:
    rut_value = st.text_input("Introduce el RUT:")
    if rut_value:
        result = search_by_rut(data, str(rut_value))  # Convertir a string
        if result is not None:
            st.write(result)
        else:
            st.warning("RUT no encontrado.")

# Sección 2: Consulta masiva mediante archivo Excel
st.header("Consulta masiva de RUTs")
uploaded_file = st.file_uploader("Sube un archivo Excel con la columna 'RUT'", type=["xls", "xlsx"])

if uploaded_file is not None and data is not None:
    st.write("Procesando archivo...")
    output_df = search_bulk_ruts(data, uploaded_file)

    if output_df is not None:
        st.write(output_df)  # Mostrar los resultados en la app

        # Convertir DataFrame a un archivo Excel para descarga
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            output_df.to_excel(writer, sheet_name="Resultados", index=False)
        output.seek(0)

        # Botón de descarga del archivo
        st.download_button(
            label="Descargar resultados en Excel",
            data=output,
            file_name="resultados_ruts.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
