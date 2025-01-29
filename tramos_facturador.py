import pandas as pd
import streamlit as st
import glob

# Buscar todos los archivos Parquet divididos
file_paths = sorted(glob.glob("data/tramo_facturador_part_*.parquet"))

# Cargar y unir todos los fragmentos en un solo DataFrame
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
        return "RUT no encontrado. Asegúrate de que el formato sea el correcto."

# Interfaz en Streamlit
st.title("Buscador Tramo según Ventas y Tipo de Facturador")

# Cargar datos al iniciar la app
data = load_data()

# Si los datos se cargaron correctamente, permitir la búsqueda
if data is not None:
    rut_value = st.text_input("Introduce el RUT:")
    if rut_value:
        try:
            rut_value = str(rut_value)  # Asegurar que el RUT se maneja como string
            result = search_by_rut(data, rut_value)
            st.write(result)
        except ValueError:
            st.error("Formato inválido")

