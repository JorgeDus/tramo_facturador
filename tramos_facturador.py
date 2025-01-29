import pandas as pd
import streamlit as st

# Ruta del archivo con los datos ya generados
FILE_PATH = "tramo_facturador_2024.csv"

# Función para cargar los datos desde el archivo CSV
def load_data():
    try:
        data = pd.read_csv(FILE_PATH)
        return data
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return None

# Función para buscar información por RUT
def search_by_rut(data, rut_value):
    result = data[data['RUT'] == rut_value]
    if not result.empty:
        return result[['RUT', 'Razón social', 'Tramo según ventas', 'Facturador']]
    else:
        return "Rut no encontrado. Asegúrate de que el formato sea el correcto."

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
