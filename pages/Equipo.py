

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# --- CONFIGURACIÓN VISUAL DE STREAMLIT (coherente con Home y SIC) ---
st.set_page_config(page_title="SIC - Equipo", page_icon="⚽", layout="wide")
st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E88E5;
            text-align: center;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #0D47A1;
        }
        .info-text {
            color: #424242;
        }
        .stApp {
            background-color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# --- FUNCIONES ---
# ...existing code...
def mostrar_tabla_resumen(df_resumen):
    def mmss_a_seg(mmss):
        minutos, segundos = map(int, mmss.split(':'))
        return minutos * 60 + segundos

    # Cambia aquí el nombre de la columna:
    col_promedio = 'Promedio Back in Game (mm:ss)'
    promedios = df_resumen[col_promedio].apply(mmss_a_seg)
    promedio_general = promedios.mean()


    def color_promedio(val):
        valor = mmss_a_seg(val)
        if valor < promedio_general * 0.98:
            return 'background-color: #ffcccc; color: #b71c1c; font-weight: bold;'  # rojo
        elif valor > promedio_general * 1.02:
            return 'background-color: #ccffcc; color: #1b5e20; font-weight: bold;'  # verde
        else:
            return 'background-color: #fff7cc; color: #ff6f00; font-weight: bold;'  # amarillo

    def nombre_grande(val):
        return 'font-size: 18px; font-weight: bold; color: #fafafa; background-color: #222222;'

    def barra_tiempo_activo(val):
        valores = df_resumen['Tiempo Activo (mm:ss)'].apply(mmss_a_seg)
        minimo = valores.min()
        maximo = valores.max()
        actual = mmss_a_seg(val)
        ancho = (actual - minimo) / (maximo - minimo) if maximo > minimo else 0
        color = "#09b5f9"
        return f"background: linear-gradient(90deg, {color} {ancho*100:.0f}%, #222222 {ancho*100:.0f}%);"

    styled_df = (
        df_resumen.style
        .applymap(nombre_grande, subset=['Atleta'])
        .applymap(color_promedio, subset=[col_promedio])
        .applymap(barra_tiempo_activo, subset=['Tiempo Activo (mm:ss)'])
        .set_properties(**{
            'border': '2px solid #1976d2',
            'background-color': '#111111',
            'color': '#fafafa'
        }, subset=pd.IndexSlice[:, :])
    )

    st.markdown(styled_df.to_html(), unsafe_allow_html=True)

def obtener_datos_sensor(activity_id, atleta_id):
    """
    Obtiene datos del sensor de un atleta en una actividad específica
    Prueba dos endpoints posibles y retorna el primero que funcione.
    """
    urls = [
        f"{BASE_URL}/activities/{activity_id}/athletes/{atleta_id}/sensor",
        f"{BASE_URL}/activities/{activity_id}/athletes/{atleta_id}/sensor-data"
    ]
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code in [404, 403]:
                continue
            elif response.status_code != 200:
                continue
            return response.json()
        except Exception:
            continue
    return None


# Definir BASE_URL y API_TOKEN correctamente
BASE_URL = 'https://connect-us.catapultsports.com/api/v6'  # Cambia esto si tu endpoint es diferente
API_TOKEN = os.getenv('CATAPULT_API_TOKEN') or 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEzMWY5NGIxOTg3ZGY4NzcxNTljOGQ2MTAzMTIzNDNjIn0.eyJhdWQiOiI0NjFiMTExMS02ZjdhLTRkYmItOWQyOS0yMzAzOWZlMjI4OGUiLCJqdGkiOiIyNzFlM2U1MjMzNDRiMjAxOTQ4MWViYmJkNjk2NTJkZDMwNmZiZThiMjU5NDkxZGI5ZGRhYjJiMWQ1Y2ViYmJjOWVlYzFiODFiYzNiNzdlNyIsImlhdCI6MTc1MzExNjQ1NS45MDQ2MjYsIm5iZiI6MTc1MzExNjQ1NS45MDQ2MjgsImV4cCI6NDkwNjcxNjQ1NS44OTQ1ODMsInN1YiI6ImJkODAyMzAxLTk1YzgtNDgxNy05ZTAxLWFjOTI5Y2ZlZGMwNiIsInNjb3BlcyI6WyJjb25uZWN0IiwiY2F0YXB1bHRyIiwic2Vuc29yLXJlYWQtb25seSJdLCJpc3MiOiJodHRwczovL2JhY2tlbmQtdXMub3BlbmZpZWxkLmNhdGFwdWx0c3BvcnRzLmNvbSIsImNvbS5jYXRhcHVsdHNwb3J0cyI6eyJvcGVuZmllbGQiOnsiY3VzdG9tZXJzIjpbeyJyZWxhdGlvbiI6ImF1dGgiLCJpZCI6MTM3N31dfX19.P-w_Y3suqBxKtJcMMlaJEZBI-2z8BLOOkRhwVu85W5EG9y2MCeLukR4zMmr4G7bvEbTchaNCPXgEE4FSbuz7xGEFZVsLTyeYb6drEClcgY3SvXPNCH4Y3iwk93ioTLX-9mv9vtdIQSYD4fRo7gdy_JPNuQ4_nn8x384ljoL2aTFFMCf6O7oMRObBZXaJPmT0joDmxr4RcrtGK0kXzyNmx_zK6wI1bY9ovO3jTsYJxlBBqL8lWHU3r3XXEIfT78enb00AiwrdeSlzlkSBie767DFZopCmsfM91EXrMOE3TD7TmTlr9LHyiD1ErAoLihL62preFVGKdAVTnOIJxS9OnoD81KK-zyJAFjI7Xf2suyEgJy5VNjoPPYbKSnYWXbGfM4msxfSXawKnae8sy7nF0JtGzrXtTraJw1VwIllW9Nz2j1644NGsJiexIFY66TAOUIU-UGNVGFMxulB0k_S8_HvFB4JE_EWHw34S5IeDwznwvfFQdBBpRdDG2OBW9LMztVDDuo84yBSvuHAdJGwMwLjxHWmOmXgEoOpjUDGL68n6Jb3xE01DO7DCvAanIkJEESq-IKAl1E2Ap4uo-dFCYJYxsW2pCTukMaumFYUoetZJh_7cWwAcwoZegLNCRkZ0x6CdsqL0MZznZgXlW3lysuruiUFTAtLO2hWyF2qLnv0'


headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

def obtener_atletas_por_actividad(activity_id):
    url = f"{BASE_URL}/activities/{activity_id}/athletes"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        atletas = response.json()
        # Si la respuesta es un dict con una clave de lista, ajústalo aquí
        if isinstance(atletas, dict):
            atletas = atletas.get('athletes', [])
        return pd.DataFrame(atletas)
    else:
        st.error(f"Error al obtener atletas: Código {response.status_code}")
        return pd.DataFrame()

def extraer_eventos_rugby_actividad(activity_id, atleta_id=None):
    """
    Extrae eventos de rugby para una actividad específica y opcionalmente para un atleta.
    Devuelve un DataFrame con los eventos encontrados.
    """
    import json
    tipos_eventos = {
        "rugby_union_contact_involvement": "Contact",
        "rugby_union_kick": "Kick",
        "rugby_union_lineout": "Line",
        "rugby_league_tackle": "Tackle"
    }
    tipos_eventos_str = ",".join(tipos_eventos.keys())
    try:
        # Obtener atletas de la actividad
        url_atletas = f"{BASE_URL}/activities/{activity_id}/athletes"
        resp_atletas = requests.get(url_atletas, headers=headers)
        resp_atletas.raise_for_status()
        atletas = resp_atletas.json()
        if isinstance(atletas, dict):
            atletas = atletas.get('athletes', [])
        if atleta_id:
            atletas = [ath for ath in atletas if ath['id'] == atleta_id]
            if not atletas:
                return pd.DataFrame()
        todos_registros = []
        for atleta in atletas:
            ath_id = atleta['id']
            ath_name = atleta.get('name', 'Nombre desconocido')
            url = f"{BASE_URL}/activities/{activity_id}/athletes/{ath_id}/events?event_types={tipos_eventos_str}"
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                continue
            eventos = response.json()
            if not eventos:
                continue
            for evento in eventos:
                data = evento.get('data', {})
                if isinstance(data, str):
                    try:
                        data = json.loads(data)
                    except:
                        continue
                info_basica = {
                    'activity_id': activity_id,
                    'athlete_id': evento.get('athlete_id'),
                    'athlete_name': f"{evento.get('athlete_first_name', '')} {evento.get('athlete_last_name', '')}".strip(),
                    'team_name': evento.get('team_name', ''),
                    'jersey': evento.get('jersey', ''),
                }
                for tipo_evento, etiqueta in tipos_eventos.items():
                    if tipo_evento in data:
                        eventos_especificos = data[tipo_evento]
                        if not isinstance(eventos_especificos, list):
                            eventos_especificos = [eventos_especificos]
                        for i, evento_especifico in enumerate(eventos_especificos):
                            registro = info_basica.copy()
                            registro['evento_num'] = i + 1
                            registro['start_time'] = evento_especifico.get('start_time')
                            registro['end_time'] = evento_especifico.get('end_time')
                            registro['tipo_evento'] = etiqueta
                            registro['confidence'] = evento_especifico.get('confidence')
                            registro['version'] = evento_especifico.get('version')
                            registro['duration'] = evento_especifico.get('duration')
                            registro['active_percentage'] = evento_especifico.get('active_percentage')
                            registro['post_event_load'] = evento_especifico.get('post_event_load')
                            registro['post_event_active'] = evento_especifico.get('post_event_active')
                            registro['post_event_back_in_game_time'] = evento_especifico.get('post_event_back_in_game_time')
                            if registro['duration'] is None and registro['start_time'] and registro['end_time']:
                                registro['duration'] = registro['end_time'] - registro['start_time']
                            todos_registros.append(registro)
        if todos_registros:
            df = pd.DataFrame(todos_registros)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al obtener eventos para atleta {atleta_id}: {e}")
        return pd.DataFrame()

def calcular_back_in_game_equipo(df):
    # Calcula el back in game para todo el equipo
    if df is None or df.empty:
        return pd.DataFrame()
    resumen = []
    for atleta_id in df['athlete_id'].unique():
        df_atleta = df[df['athlete_id'] == atleta_id].copy()
        df_atleta = df_atleta.sort_values('start_time').reset_index(drop=True)
        df_atleta['back_in_game'] = df_atleta['start_time'].shift(-1) - df_atleta['end_time']
        df_atleta = df_atleta.iloc[:-1]
        df_atleta = df_atleta[df_atleta['back_in_game'] >= 0]
        resumen.append(df_atleta)
    if resumen:
        return pd.concat(resumen, ignore_index=True)
    else:
        return pd.DataFrame()

def resumen_back_in_game_equipo(df):
    if df is None or df.empty:
        st.warning("No hay datos para calcular.")
        return None

    def seg_a_mmss(segundos):
        minutos = int(segundos // 60)
        segundos = int(segundos % 60)
        return f"{minutos:02d}:{segundos:02d}"

    resumen = []
    lista_promedios_seg = []
    for atleta_id in df['athlete_id'].unique():
        df_atleta = df[df['athlete_id'] == atleta_id].copy()
        nombre = df_atleta['athlete_name'].iloc[0] if 'athlete_name' in df_atleta.columns else str(atleta_id)
        df_atleta = df_atleta.sort_values('start_time').reset_index(drop=True)
        df_atleta['back_in_game'] = df_atleta['start_time'].shift(-1) - df_atleta['end_time']
        df_atleta = df_atleta.iloc[:-1]
        df_atleta = df_atleta[df_atleta['back_in_game'] >= 0]
        promedio_back = df_atleta['back_in_game'].mean() if not df_atleta.empty else 0
        tiempo_activo = df_atleta['duration'].sum() if 'duration' in df_atleta.columns else 0
        resumen.append({
            'Atleta': nombre,
            'Promedio Back in Game (mm:ss)': seg_a_mmss(promedio_back),
            'Tiempo Activo (mm:ss)': seg_a_mmss(tiempo_activo)
        })
        lista_promedios_seg.append(promedio_back)

    df_resumen = pd.DataFrame(resumen)
    promedio_equipo_seg = sum(lista_promedios_seg) / len(lista_promedios_seg) if lista_promedios_seg else 0
    st.info(f"Promedio general de Back in Game del equipo: {seg_a_mmss(promedio_equipo_seg)} (mm:ss)")
    return df_resumen



# Nueva función para obtener actividades disponibles
def obtener_actividades():
    url = f"{BASE_URL}/activities"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        actividades = response.json()
        # Si la respuesta es un dict con una clave de lista, ajústalo aquí
        if isinstance(actividades, dict):
            actividades = actividades.get('activities', [])
        return pd.DataFrame(actividades)
    else:
        st.error(f"Error al obtener actividades: Código {response.status_code}")
        return pd.DataFrame()

st.title("Análisis Back in Game - Equipo")

# Mostrar lista de actividades disponibles
df_actividades = obtener_actividades()
if not df_actividades.empty:
    # Mostrar tabla de actividades
    st.subheader("Selecciona una actividad disponible:")
    # Intentar mostrar nombre y fecha si existen
    if 'name' in df_actividades.columns and 'id' in df_actividades.columns:
        df_actividades['opcion'] = df_actividades.apply(lambda row: f"{row['name']} (ID: {row['id']})", axis=1)
        opciones = df_actividades['opcion'].tolist()
        seleccion = st.selectbox("Actividades", opciones)
        # Extraer el id de la actividad seleccionada
        idx = opciones.index(seleccion)
        activity_id = str(df_actividades.iloc[idx]['id'])
    else:
        # Si no hay nombre, mostrar solo IDs
        opciones = df_actividades['id'].astype(str).tolist()
        seleccion = st.selectbox("Actividades (solo ID disponible)", opciones)
        activity_id = seleccion

    # El resto del flujo igual que antes
    df_atletas = obtener_atletas_por_actividad(activity_id)
    if not df_atletas.empty:
        st.success(f"Se encontraron {len(df_atletas)} atletas en la actividad.")
        df_eventos_equipo = pd.DataFrame()
        sensores_equipo = {}
        for idx, atleta in df_atletas.iterrows():
            atleta_id = atleta['id']
            # Obtener eventos
            df_atleta_eventos = extraer_eventos_rugby_actividad(activity_id, atleta_id)
            if df_atleta_eventos is not None and not df_atleta_eventos.empty:
                df_eventos_equipo = pd.concat([df_eventos_equipo, df_atleta_eventos], ignore_index=True)
            # Obtener datos de sensor
            datos_sensor = obtener_datos_sensor(activity_id, atleta_id)
            sensores_equipo[atleta_id] = datos_sensor

        # Mostrar resumen de eventos
        if not df_eventos_equipo.empty:
            if 'confidence' in df_eventos_equipo.columns:
                df_eventos_equipo_filtrado = df_eventos_equipo[df_eventos_equipo['confidence'] > 0.7]
            else:
                df_eventos_equipo_filtrado = df_eventos_equipo
            df_resumen_equipo = resumen_back_in_game_equipo(df_eventos_equipo_filtrado)
            if df_resumen_equipo is not None:
                mostrar_tabla_resumen(df_resumen_equipo)
        else:
            st.warning("No se encontraron eventos para los atletas.")

        # Mostrar resumen de sensores (opcional, aquí solo muestra cuántos tienen datos)
        sensores_con_datos = [k for k, v in sensores_equipo.items() if v]
        st.info(f"Datos de sensor encontrados para {len(sensores_con_datos)} de {len(df_atletas)} atletas.")
        # Si quieres mostrar los datos de sensor, puedes descomentar la siguiente línea:
        # st.write(sensores_equipo)
    else:
        st.warning("No se encontraron atletas para la actividad.")
else:
    st.warning("No se encontraron actividades disponibles.")
