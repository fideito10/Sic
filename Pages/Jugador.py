
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

import streamlit as st
from datetime import datetime

# --- CONFIGURACIÓN VISUAL DE STREAMLIT (coherente con Home y equipo) ---
st.set_page_config(page_title="SIC - Análisis Deportivo", page_icon="🏉", layout="wide")

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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Estilo personalizado
st.markdown("""
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
</style>
""", unsafe_allow_html=True)

# Título de la aplicación
st.markdown("<h1 class='main-header'>BIG Report - Análisis de Retorno a la Actividad</h1>", unsafe_allow_html=True)

# Intenta usar una variable de entorno si está disponible
try:
    env_token = os.getenv('CATAPULT_API_TOKEN')
    if env_token:
        api_token = env_token
    else:
        # Token de respaldo (se puede cambiar por uno real)
        api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEzMWY5NGIxOTg3ZGY4NzcxNTljOGQ2MTAzMTIzNDNjIn0.eyJhdWQiOiI0NjFiMTExMS02ZjdhLTRkYmItOWQyOS0yMzAzOWZlMjI4OGUiLCJqdGkiOiIyNzFlM2U1MjMzNDRiMjAxOTQ4MWViYmJkNjk2NTJkZDMwNmZiZThiMjU5NDkxZGI5ZGRhYjJiMWQ1Y2ViYmJjOWVlYzFiODFiYzNiNzdlNyIsImlhdCI6MTc1MzExNjQ1NS45MDQ2MjYsIm5iZiI6MTc1MzExNjQ1NS45MDQ2MjgsImV4cCI6NDkwNjcxNjQ1NS44OTQ1ODMsInN1YiI6ImJkODAyMzAxLTk1YzgtNDgxNy05ZTAxLWFjOTI5Y2ZlZGMwNiIsInNjb3BlcyI6WyJjb25uZWN0IiwiY2F0YXB1bHRyIiwic2Vuc29yLXJlYWQtb25seSJdLCJpc3MiOiJodHRwczovL2JhY2tlbmQtdXMub3BlbmZpZWxkLmNhdGFwdWx0c3BvcnRzLmNvbSIsImNvbS5jYXRhcHVsdHNwb3J0cyI6eyJvcGVuZmllbGQiOnsiY3VzdG9tZXJzIjpbeyJyZWxhdGlvbiI6ImF1dGgiLCJpZCI6MTM3N31dfX19.P-w_Y3suqBxKtJcMMlaJEZBI-2z8BLOOkRhwVu85W5EG9y2MCeLukR4zMmr4G7bvEbTchaNCPXgEE4FSbuz7xGEFZVsLTyeYb6drEClcgY3SvXPNCH4Y3iwk93ioTLX-9mv9vtdIQSYD4fRo7gdy_JPNuQ4_nn8x384ljoL2aTFFMCf6O7oMRObBZXaJPmT0joDmxr4RcrtGK0kXzyNmx_zK6wI1bY9ovO3jTsYJxlBBqL8lWHU3r3XXEIfT78enb00AiwrdeSlzlkSBie767DFZopCmsfM91EXrMOE3TD7TmTlr9LHyiD1ErAoLihL62preFVGKdAVTnOIJxS9OnoD81KK-zyJAFjI7Xf2suyEgJy5VNjoPPYbKSnYWXbGfM4msxfSXawKnae8sy7nF0JtGzrXtTraJw1VwIllW9Nz2j1644NGsJiexIFY66TAOUIU-UGNVGFMxulB0k_S8_HvFB4JE_EWHw34S5IeDwznwvfFQdBBpRdDG2OBW9LMztVDDuo84yBSvuHAdJGwMwLjxHWmOmXgEoOpjUDGL68n6Jb3xE01DO7DCvAanIkJEESq-IKAl1E2Ap4uo-dFCYJYxsW2pCTukMaumFYUoetZJh_7cWwAcwoZegLNCRkZ0x6CdsqL0MZznZgXlW3lysuruiUFTAtLO2hWyF2qLnv0'
except:
    # Si no se puede acceder a la variable de entorno, se usa el token hard-coded
    api_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjEzMWY5NGIxOTg3ZGY4NzcxNTljOGQ2MTAzMTIzNDNjIn0.eyJhdWQiOiI0NjFiMTExMS02ZjdhLTRkYmItOWQyOS0yMzAzOWZlMjI4OGUiLCJqdGkiOiIyNzFlM2U1MjMzNDRiMjAxOTQ4MWViYmJkNjk2NTJkZDMwNmZiZThiMjU5NDkxZGI5ZGRhYjJiMWQ1Y2ViYmJjOWVlYzFiODFiYzNiNzdlNyIsImlhdCI6MTc1MzExNjQ1NS45MDQ2MjYsIm5iZiI6MTc1MzExNjQ1NS45MDQ2MjgsImV4cCI6NDkwNjcxNjQ1NS44OTQ1ODMsInN1YiI6ImJkODAyMzAxLTk1YzgtNDgxNy05ZTAxLWFjOTI5Y2ZlZGMwNiIsInNjb3BlcyI6WyJjb25uZWN0IiwiY2F0YXB1bHRyIiwic2Vuc29yLXJlYWQtb25seSJdLCJpc3MiOiJodHRwczovL2JhY2tlbmQtdXMub3BlbmZpZWxkLmNhdGFwdWx0c3BvcnRzLmNvbSIsImNvbS5jYXRhcHVsdHNwb3J0cyI6eyJvcGVuZmllbGQiOnsiY3VzdG9tZXJzIjpbeyJyZWxhdGlvbiI6ImF1dGgiLCJpZCI6MTM3N31dfX19.P-w_Y3suqBxKtJcMMlaJEZBI-2z8BLOOkRhwVu85W5EG9y2MCeLukR4zMmr4G7bvEbTchaNCPXgEE4FSbuz7xGEFZVsLTyeYb6drEClcgY3SvXPNCH4Y3iwk93ioTLX-9mv9vtdIQSYD4fRo7gdy_JPNuQ4_nn8x384ljoL2aTFFMCf6O7oMRObBZXaJPmT0joDmxr4RcrtGK0kXzyNmx_zK6wI1bY9ovO3jTsYJxlBBqL8lWHU3r3XXEIfT78enb00AiwrdeSlzlkSBie767DFZopCmsfM91EXrMOE3TD7TmTlr9LHyiD1ErAoLihL62preFVGKdAVTnOIJxS9OnoD81KK-zyJAFjI7Xf2suyEgJy5VNjoPPYbKSnYWXbGfM4msxfSXawKnae8sy7nF0JtGzrXtTraJw1VwIllW9Nz2j1644NGsJiexIFY66TAOUIU-UGNVGFMxulB0k_S8_HvFB4JE_EWHw34S5IeDwznwvfFQdBBpRdDG2OBW9LMztVDDuo84yBSvuHAdJGwMwLjxHWmOmXgEoOpjUDGL68n6Jb3xE01DO7DCvAanIkJEESq-IKAl1E2Ap4uo-dFCYJYxsW2pCTukMaumFYUoetZJh_7cWwAcwoZegLNCRkZ0x6CdsqL0MZznZgXlW3lysuruiUFTAtLO2hWyF2qLnv0'



# Clase CatapultSelector para interactuar con la API
class CatapultSelector:
    
    def __init__(self, api_token):
        self.api_token = api_token.strip()  # Eliminar espacios innecesarios
        self.base_url = "https://connect-us.catapultsports.com/api/v6"
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # Verificar que el token no esté vacío
        if not self.api_token:
            st.error("⚠️ El token API está vacío. Por favor proporcione un token válido.")
            
            
    def obtener_equipos(self):
        """Obtiene la lista de equipos disponibles sin imprimir en pantalla"""
        try:
            url = f"{self.base_url}/teams"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 404:
                return []
            elif response.status_code == 403:
                return []
            elif response.status_code != 200:
                return []
            equipos = response.json()
            return equipos
        except Exception:
            return []       
     
    
    def obtener_actividades_por_equipo(self, equipo_id, dias_atras=90, use_cache=True):
        """
        Obtiene las actividades de un equipo específico utilizando varios métodos alternativos
        """
        cache_key = f"actividades_{equipo_id}_{dias_atras}"
        if use_cache and cache_key in st.session_state:
            return st.session_state[cache_key]

        try:
            # Método 1: Intentar obtener actividades directamente (endpoint actual)
            url = f"{self.base_url}/teams/{equipo_id}/activities"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                actividades = response.json()
                return actividades

            # Método 2: Obtener actividades usando parámetro de equipo
            url = f"{self.base_url}/activities?team={equipo_id}"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                actividades = response.json()
                return actividades

            # Método 3: Obtener todas las actividades y filtrar por equipo
            from datetime import datetime, timedelta
            end_date = datetime.now()
            start_date = end_date - timedelta(days=dias_atras)
            start_timestamp = int(start_date.timestamp())
            end_timestamp = int(end_date.timestamp())
            params = {
                'startTime': start_timestamp,
                'endTime': end_timestamp
            }
            url = f"{self.base_url}/activities"
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                all_activities = response.json()
                team_activities = [act for act in all_activities if act.get('team_id') == equipo_id]
                return team_activities

            # Método 4: Usar el endpoint de estadísticas
            url = f"{self.base_url}/stats"
            stats_data = {
                "parameters": ["total_duration"],
                "filters": [
                    {"name": "team_id", "comparison": "=", "values": [equipo_id]},
                    {"name": "date", "comparison": ">=", "values": [start_date.strftime("%Y-%m-%d")]},
                    {"name": "date", "comparison": "<=", "values": [end_date.strftime("%Y-%m-%d")]}
                ],
                "group_by": ["activity"]
            }
            response = requests.post(url, headers=self.headers, json=stats_data)
            if response.status_code == 200:
                activities_stats = response.json()
                activities = []
                for stat in activities_stats:
                    activities.append({
                        'id': stat.get('activity_id'),
                        'name': stat.get('activity_name'),
                        'start_time': datetime.strptime(stat.get('date', ''), "%Y-%m-%d").timestamp() if stat.get('date') else None,
                        'team_id': equipo_id,
                        'duration': stat.get('total_duration', 0)
                    })
                if activities:
                    activities_sorted = sorted(
                        activities, 
                        key=lambda x: x.get('start_time', 0), 
                        reverse=True
                    )
                    return activities_sorted
                return activities

            return []
        except Exception:
            return []
        
    
    def obtener_atletas(self, equipo_id):
        """Obtiene la lista de atletas de un equipo sin imprimir en pantalla"""
        try:
            url = f"{self.base_url}/teams/{equipo_id}/athletes"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception:
            return []
    
    def obtener_atletas_por_actividad(self, actividad_id):
        """Obtiene los atletas que participaron en una actividad específica sin imprimir en pantalla"""
        try:
            url = f"{self.base_url}/activities/{actividad_id}/athletes"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception:
            return []
        
    def get_athlete_sensor_data(self, activity_id, athlete_id):
        """
        Obtiene datos del sensor de un atleta en una actividad específica
        """
        urls = [
            f"{self.base_url}/activities/{activity_id}/athletes/{athlete_id}/sensor",
            f"{self.base_url}/activities/{activity_id}/athletes/{athlete_id}/sensor-data"
        ]
        for url in urls:
            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code == 404:
                    continue
                elif response.status_code == 403:
                    continue
                elif response.status_code != 200:
                    continue
                return response.json()
            except Exception:
                continue
        return None

    
    def obtener_datos_sensor(self, activity_id, athlete_id):
        """
        Obtiene datos del sensor de un atleta en una actividad específica sin imprimir en pantalla
        """
        try:
            url = f"{self.base_url}/activities/{activity_id}/athletes/{athlete_id}/sensor-data"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 404:
                return None
            elif response.status_code == 403:
                return None
            elif response.status_code != 200:
                return None
            return response.json()
        except Exception:
            return None

    def extraer_eventos_rugby_actividad(self, activity_id, athlete_id=None):
        """
        Extrae eventos de rugby para una actividad específica y opcionalmente para un atleta.
        Devuelve un DataFrame con los eventos encontrados.
        """
        import json

        # Definir los tipos de eventos a extraer con sus etiquetas
        tipos_eventos = {
            "rugby_union_contact_involvement": "Contact",
            "rugby_union_kick": "Kick",
            "rugby_union_lineout": "Line",
            "rugby_league_tackle": "Tackle"
        }
        tipos_eventos_str = ",".join(tipos_eventos.keys())

        try:
            # Verificar si la actividad existe
            activities_url = f"{self.base_url}/activities"
            activities_response = requests.get(activities_url, headers=self.headers)
            activities_response.raise_for_status()
            activities = activities_response.json()
            activity_found = False
            activity_name = "Actividad desconocida"
            for act in activities:
                if act['id'] == activity_id:
                    activity_name = act.get('name', 'Actividad desconocida')
                    activity_found = True
                    break
            if not activity_found:
                return None

            # Obtener atletas de la actividad
            athletes_url = f"{self.base_url}/activities/{activity_id}/athletes"
            athletes_response = requests.get(athletes_url, headers=self.headers)
            athletes_response.raise_for_status()
            athletes = athletes_response.json()
            if not athletes:
                return None

            # Filtrar atleta si se especifica
            if athlete_id:
                athletes = [ath for ath in athletes if ath['id'] == athlete_id]
                if not athletes:
                    return None

            todos_registros = []
            for athlete in athletes:
                ath_id = athlete['id']
                ath_name = athlete.get('name', 'Nombre desconocido')
                url = f"{self.base_url}/activities/{activity_id}/athletes/{ath_id}/events?event_types={tipos_eventos_str}"
                response = requests.get(url, headers=self.headers)
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
                        'activity_name': activity_name,
                        'athlete_id': evento.get('athlete_id'),
                        'athlete_name': f"{evento.get('athlete_first_name', '')} {evento.get('athlete_last_name', '')}".strip(),
                        'team_name': evento.get('team_name', ''),
                        'jersey': evento.get('jersey', ''),
                        'fecha_extraccion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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
                                try:
                                    if registro['start_time']:
                                        registro['start_time_dt'] = datetime.fromtimestamp(
                                            registro['start_time']).strftime('%Y-%m-%d %H:%M:%S')
                                    if registro['end_time']:
                                        registro['end_time_dt'] = datetime.fromtimestamp(
                                            registro['end_time']).strftime('%Y-%m-%d %H:%M:%S')
                                except Exception:
                                    registro['start_time_dt'] = None
                                    registro['end_time_dt'] = None
                                todos_registros.append(registro)
            if todos_registros:
                df = pd.DataFrame(todos_registros)
                columnas_principales = [
                    'activity_id', 'activity_name', 'athlete_id', 'athlete_name', 'team_name', 'jersey',
                    'tipo_evento', 'start_time', 'start_time_dt', 'end_time', 'end_time_dt', 'duration', 'confidence'
                ]
                columnas_existentes = [col for col in columnas_principales if col in df.columns]
                otras_columnas = [col for col in df.columns if col not in columnas_principales]
                df = df[columnas_existentes + otras_columnas]
                return df
            else:
                return pd.DataFrame()
        except requests.exceptions.RequestException:
            return None
        except Exception:
            return
        
    def convert_catapult_to_dataframe(self, json_data):

        # Verificar si el formato es el de 'sensor-data'
        if 'samples' in json_data:
            # Formato 'sensor-data'
            df = pd.DataFrame(json_data['samples'])
            
            # Convertir timestamp a datetime si existe
            if 'ts' in df.columns:
                df['datetime'] = pd.to_datetime(df['ts'], unit='s')
                
            # Añadir información del atleta y actividad si está disponible
            if 'athlete_id' in json_data:
                df['athlete_id'] = json_data['athlete_id']
            if 'activity_id' in json_data:
                df['activity_id'] = json_data['activity_id']
                
            return df
        else:
            # Formato anterior ('sensor')
            all_data = []
            
            # Iterar sobre cada atleta en la respuesta
            for athlete_data in json_data:
                # Extraer información del atleta
                athlete_info = {
                    'athlete_id': athlete_data.get('athlete_id'),
                    'device_id': athlete_data.get('device_id'),
                    'stream_type': athlete_data.get('stream_type'),
                    'player_id': athlete_data.get('player_id'),
                    'athlete_first_name': athlete_data.get('athlete_first_name'),
                    'athlete_last_name': athlete_data.get('athlete_last_name'),
                    'jersey': athlete_data.get('jersey'),
                    'team_id': athlete_data.get('team_id'),
                    'team_name': athlete_data.get('team_name')
                }
                
                # Expandir los datos de sensores
                sensor_data = athlete_data.get('data', [])
                
                for record in sensor_data:
                    # Combinar información del atleta con cada registro de sensor
                    row = {**athlete_info, **record}
                    all_data.append(row)
            
            # Crear DataFrame
            df = pd.DataFrame(all_data)
            
            # Convertir timestamp a datetime si existe
            if 'ts' in df.columns:
                df['datetime'] = pd.to_datetime(df['ts'], unit='s')
            
            return df

    def obtener_datos_fusionados(self, activity_id, athlete_id):
        """
        Fusiona los eventos de rugby con los datos del sensor por timestamps.
        Devuelve un DataFrame con la información combinada.
        """
        # Obtener datos del sensor
        datos_sensor = self.get_athlete_sensor_data(activity_id, athlete_id)
        if not datos_sensor:
            st.warning("No se pudieron obtener datos del sensor para fusionar.")
            return None
        df_sensor = self.convert_catapult_to_dataframe(datos_sensor)
        if df_sensor.empty:
            st.warning("No hay datos del sensor para fusionar.")
            return None

        # Obtener eventos de rugby
        df_eventos = self.extraer_eventos_rugby_actividad(activity_id, athlete_id)
        if df_eventos is None or df_eventos.empty:
            st.warning("No se encontraron eventos de rugby para fusionar.")
            return None

        # Fusionar por rango de tiempo (cada evento con los datos del sensor en su rango)
        # Aquí se asume que 'start_time' y 'end_time' están en segundos (timestamp)
        eventos_fusionados = []
        for _, evento in df_eventos.iterrows():
            mask = (df_sensor['ts'] >= evento['start_time']) & (df_sensor['ts'] <= evento['end_time'])
            df_rango = df_sensor[mask].copy()
            for col in df_eventos.columns:
                df_rango[col] = evento[col]
            eventos_fusionados.append(df_rango)
        if eventos_fusionados:
            df_fusion = pd.concat(eventos_fusionados, ignore_index=True)
            return df_fusion
        else:
            st.warning("No se encontraron datos del sensor dentro de los rangos de eventos.")
            return pd.DataFrame()

    def calcular_back_in_game_multi(self, df):
            """
            Calcula el 'back in game' para cada atleta en el DataFrame y muestra los resultados en Streamlit.
            - Filtra eventos con confidence > 0.7
            - Convierte los tiempos a minutos
            - Devuelve las coordenadas y métricas relevantes
            """
            resultados = []
            resumen_metricas = []
            for atleta_id in df['athlete_id'].unique():
                df_atleta = df[df['athlete_id'] == atleta_id].copy()

                # Filtrar por confidence > 0.7 si existe la columna
                if 'confidence' in df_atleta.columns:
                    df_atleta = df_atleta[df_atleta['confidence'] > 0.7]

                df_atleta = df_atleta.sort_values('start_time').reset_index(drop=True)
                df_atleta['back_in_game'] = df_atleta['start_time'].shift(-1) - df_atleta['end_time']
                df_atleta = df_atleta.iloc[:-1]
                df_atleta = df_atleta[df_atleta['back_in_game'] >= 0]

                # Convertir tiempos a minutos
                df_atleta['duration_min'] = df_atleta['duration'] / 60 if 'duration' in df_atleta.columns else None
                df_atleta['back_in_game_min'] = df_atleta['back_in_game'] / 60

                resumen_metricas.append({
                    'Atleta': f"#{df_atleta['jersey'].iloc[0] if 'jersey' in df_atleta.columns and not df_atleta.empty else atleta_id}",
                    'Total eventos BIG': len(df_atleta),
                    'Tiempo medio entre eventos (min)': round(df_atleta['back_in_game_min'].mean(), 2),
                    'Duración media por evento (min)': round(df_atleta['duration_min'].mean(), 2) if 'duration_min' in df_atleta.columns else None,
                    'Carga total de actividad (min)': round(df_atleta['duration_min'].sum(), 2) if 'duration_min' in df_atleta.columns else None
                })

                cols_base = ['tipo_evento', 'end_time', 'start_time', 'duration_min', 'back_in_game_min', 'confidence']
                coords = ['start_x', 'start_y', 'end_x', 'end_y']
                cols = cols_base + [c for c in coords if c in df_atleta.columns]
                resultados.append(df_atleta)

            if resultados:
                st.session_state['resumen_metricas'] = resumen_metricas
                return pd.concat(resultados, ignore_index=True)
            else:
                st.session_state['resumen_metricas'] = []
                return



def normalizar_datos_atleta(df):
    """
    Normaliza los datos del atleta para preparar la visualización en la cancha de rugby.
    Adapta para eventos con columnas start_x, start_y, end_x, end_y.
    Solo usa valores válidos (>0) para calcular min/max.
    """
    df_norm = df.copy()
    # Si tienes coordenadas start_x/start_y y end_x/end_y
    if 'start_x' in df_norm.columns and 'start_y' in df_norm.columns and \
       'end_x' in df_norm.columns and 'end_y' in df_norm.columns:
        # Filtrar solo valores válidos (>0)
        x_valid = pd.concat([df_norm.loc[df_norm['start_x'] > 0, 'start_x'],
                             df_norm.loc[df_norm['end_x'] > 0, 'end_x']])
        y_valid = pd.concat([df_norm.loc[df_norm['start_y'] > 0, 'start_y'],
                             df_norm.loc[df_norm['end_y'] > 0, 'end_y']])
        x_min = x_valid.min() if not x_valid.empty else 0
        x_max = x_valid.max() if not x_valid.empty else 100
        y_min = y_valid.min() if not y_valid.empty else 0
        y_max = y_valid.max() if not y_valid.empty else 70
        # Normalizar solo los valores válidos
        if x_max != x_min:
            df_norm.loc[df_norm['start_x'] > 0, 'x_cancha'] = (df_norm.loc[df_norm['start_x'] > 0, 'start_x'] - x_min) / (x_max - x_min) * 100
        else:
            df_norm['x_cancha'] = 50
        if y_max != y_min:
            df_norm.loc[df_norm['start_y'] > 0, 'y_cancha'] = (df_norm.loc[df_norm['start_y'] > 0, 'start_y'] - y_min) / (y_max - y_min) * 70
        else:
            df_norm['y_cancha'] = 35
        # Si hay valores no válidos, ponlos en el centro
        df_norm['x_cancha'] = df_norm['x_cancha'].fillna(50)
        df_norm['y_cancha'] = df_norm['y_cancha'].fillna(35)
    # ...el resto igual...
    elif 'x' in df_norm.columns and 'y' in df_norm.columns:
        x_valid = df_norm.loc[df_norm['x'] > 0, 'x']
        y_valid = df_norm.loc[df_norm['y'] > 0, 'y']
        x_min = x_valid.min() if not x_valid.empty else 0
        x_max = x_valid.max() if not x_valid.empty else 100
        y_min = y_valid.min() if not y_valid.empty else 0
        y_max = y_valid.max() if not y_valid.empty else 70
        if x_max != x_min:
            df_norm.loc[df_norm['x'] > 0, 'x_cancha'] = (df_norm.loc[df_norm['x'] > 0, 'x'] - x_min) / (x_max - x_min) * 100
        else:
            df_norm['x_cancha'] = 50
        if y_max != y_min:
            df_norm.loc[df_norm['y'] > 0, 'y_cancha'] = (df_norm.loc[df_norm['y'] > 0, 'y'] - y_min) / (y_max - y_min) * 70
        else:
            df_norm['y_cancha'] = 35
        df_norm['x_cancha'] = df_norm['x_cancha'].fillna(50)
        df_norm['y_cancha'] = df_norm['y_cancha'].fillna(35)
    elif 'lat' in df_norm.columns and 'long' in df_norm.columns:
        lat_centro = df_norm['lat'].mean()
        long_centro = df_norm['long'].mean()
        factor_lat = 111320
        factor_long = 111320 * np.cos(np.radians(lat_centro))
        df_norm['x_temp'] = (df_norm['long'] - long_centro) * factor_long
        df_norm['y_temp'] = (df_norm['lat'] - lat_centro) * factor_lat
        x_valid = df_norm.loc[df_norm['x_temp'] != 0, 'x_temp']
        y_valid = df_norm.loc[df_norm['y_temp'] != 0, 'y_temp']
        x_temp_min = x_valid.min() if not x_valid.empty else 0
        x_temp_max = x_valid.max() if not x_valid.empty else 100
        y_temp_min = y_valid.min() if not y_valid.empty else 0
        y_temp_max = y_valid.max() if not y_valid.empty else 70
        if x_temp_max != x_temp_min:
            df_norm.loc[df_norm['x_temp'] != 0, 'x_cancha'] = (df_norm.loc[df_norm['x_temp'] != 0, 'x_temp'] - x_temp_min) / (x_temp_max - x_temp_min) * 100
        else:
            df_norm['x_cancha'] = 50
        if y_temp_max != y_temp_min:
            df_norm.loc[df_norm['y_temp'] != 0, 'y_cancha'] = (df_norm.loc[df_norm['y_temp'] != 0, 'y_temp'] - y_temp_min) / (y_temp_max - y_temp_min) * 70
        else:
            df_norm['y_cancha'] = 35
        df_norm['x_cancha'] = df_norm['x_cancha'].fillna(50)
        df_norm['y_cancha'] = df_norm['y_cancha'].fillna(35)
    else:
        st.warning("No se encontraron columnas de coordenadas válidas para normalizar.")
    return df_norm

def dibujar_cancha_rugby_con_eventos(df_eventos):
    # --- Guardar eventos en Supabase ---
    try:
        from supabase import create_client, Client
        import uuid
        url = "https://awllmjfnkvfaevvcxymv.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3bGxtamZua3ZmYWV2dmN4eW12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMwOTQ4NzUsImV4cCI6MjA2ODY3MDg3NX0.wJ3Hl3eGDf-dAUEJGeL3IVFQzr1IpTNS2DU3xuioBhE"
        supabase: Client = create_client(url, key)
        for _, evento in df_eventos.iterrows():
            supabase.table("events").upsert({
                "id": str(uuid.uuid4()),
                "activity_id": evento.get("activity_id"),
                "athlete_id": evento.get("athlete_id"),
                "tipo_evento": evento.get("tipo_evento"),
                "start_time": evento.get("start_time"),
                "end_time": evento.get("end_time"),
                "duration": evento.get("duration"),
                "confidence": evento.get("confidence"),
                "x_cancha": evento.get("x_cancha"),
                "y_cancha": evento.get("y_cancha"),
            }).execute()
    except Exception as e:
        print(f"Error guardando eventos en Supabase: {e}")
    # Configuración inicial
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_aspect('equal')
    
    # Dimensiones estándar (en metros)
    ancho_total = 70
    largo_total = 100
    area_gol = 10
    linea_22 = 22

    # Límites y fondo
    ax.set_xlim(-area_gol - 10, largo_total + area_gol + 10)
    ax.set_ylim(-10, ancho_total + 10)
    ax.set_axis_off()
    fondo = patches.Rectangle((-area_gol - 10, -10), largo_total + 2*area_gol + 20, ancho_total + 20, facecolor='darkgreen', zorder=0)
    ax.add_patch(fondo)
    campo_principal = patches.Rectangle((0, 0), largo_total, ancho_total, linewidth=2, edgecolor='white', facecolor='green', zorder=1)
    ax.add_patch(campo_principal)
    area_gol_izq = patches.Rectangle((-area_gol, 0), area_gol, ancho_total, linewidth=2, edgecolor='white', facecolor='green', zorder=1)
    area_gol_der = patches.Rectangle((largo_total, 0), area_gol, ancho_total, linewidth=2, edgecolor='white', facecolor='green', zorder=1)
    ax.add_patch(area_gol_izq)
    ax.add_patch(area_gol_der)
    plt.plot([largo_total/2, largo_total/2], [0, ancho_total], 'white', linewidth=2)
    plt.plot([linea_22, linea_22], [0, ancho_total], 'white', linewidth=2)
    plt.plot([largo_total-linea_22, largo_total-linea_22], [0, ancho_total], 'white', linewidth=2)
    plt.plot([5, 5], [0, ancho_total], 'white', linewidth=1, linestyle='--')
    plt.plot([largo_total-5, largo_total-5], [0, ancho_total], 'white', linewidth=1, linestyle='--')
    for x in [5, linea_22, largo_total/2, largo_total-linea_22, largo_total-5]:
        plt.plot([x, x], [0, 5], 'white', linewidth=1)
        plt.plot([x, x], [ancho_total-5, ancho_total], 'white', linewidth=1)

    # Añadir texto descriptivo
    plt.text(largo_total/2, ancho_total+5, "Línea de touch (ancho: 70m)", ha='center', color='white')
    plt.text(-5, ancho_total/2, "Línea de meta", va='center', rotation=90, color='white')
    plt.text(largo_total+5, ancho_total/2, "Línea de meta", va='center', rotation=270, color='white')
    plt.text(linea_22, -5, "Línea de 22m", ha='center', color='white')
    plt.text(largo_total-linea_22, -5, "Línea de 22m", ha='center', color='white')
    plt.text(largo_total/2, -5, "Mitad de cancha", ha='center', color='white')
    plt.title('Cancha de Rugby con Eventos', fontsize=16, pad=20, color='white')
    
    # --- Graficar eventos ---
    colores = {
        'Contact': 'red',
        'Kick': 'yellow',
        'Line': 'blue',
        'Tackle': 'orange'
    }
    # Usar las coordenadas normalizadas
    for _, evento in df_eventos.iterrows():
        x = evento.get('x_cancha', None)
        y = evento.get('y_cancha', None)
        tipo = evento.get('tipo_evento', 'Evento')
        if x is not None and y is not None:
            ax.plot(x, y, 'o', color=colores.get(tipo, 'white'), markersize=12, label=tipo, alpha=0.7)
            ax.text(x, y+2, tipo, color=colores.get(tipo, 'white'), fontsize=9, ha='center')
    handles = [plt.Line2D([0], [0], marker='o', color='w', label=tipo, markerfacecolor=col, markersize=10)
               for tipo, col in colores.items()]
    ax.legend(handles=handles, loc='upper right')
    st.pyplot(fig)
 

# Función principal
def main():
    # Inicializar el selector de Catapult
    catapult = CatapultSelector(api_token)
    
    # Contenedor para el flujo de selección
    st.markdown("<h2 class='sub-header'>Selección de Datos</h2>", unsafe_allow_html=True)
    
    # PASO 1: Seleccionar equipo
    st.sidebar.markdown("<h2 class='sub-header'>Selección de Jugador</h2>", unsafe_allow_html=True)

    # PASO 1: Seleccionar equipo
    st.sidebar.markdown("### 1. Seleccionar Equipo")
    if st.sidebar.button("Cargar Equipos"):
        equipos = catapult.obtener_equipos()
        st.session_state['equipos'] = equipos
        st.session_state['paso'] = 1
        if not equipos:
            st.warning("No se encontraron equipos asociados a tu cuenta o tu token no tiene permisos.")

    equipo_seleccionado = None
    if 'equipos' in st.session_state and st.session_state['equipos']:
        opciones_equipos = {f"{equipo['name']} (ID: {equipo['id']})": equipo['id'] 
                            for equipo in st.session_state['equipos']}
        equipo_opcion = st.sidebar.selectbox(
            "Seleccione un equipo:",
            options=list(opciones_equipos.keys()),
            key="selector_equipo"
        )
        if equipo_opcion:
            equipo_seleccionado = opciones_equipos[equipo_opcion]
            st.session_state['equipo_id'] = equipo_seleccionado
            st.session_state['paso'] = 2

    # PASO 2: Seleccionar actividad
    if 'paso' in st.session_state and st.session_state['paso'] >= 2:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 2. Seleccionar Actividad")
        dias_atras = st.sidebar.slider(
            "Mostrar actividades de los últimos días:", 
            min_value=7, 
            max_value=365, 
            value=90,
            step=7
        )
        if st.sidebar.button("Cargar Actividades"):
            actividades = catapult.obtener_actividades_por_equipo(st.session_state['equipo_id'], dias_atras=dias_atras)
            st.session_state['actividades'] = actividades

        actividad_seleccionada = None
        if 'actividades' in st.session_state and st.session_state['actividades']:
            opciones_actividades = {}
            for actividad in st.session_state['actividades']:
                fecha = ""
                if 'start_time' in actividad and actividad['start_time']:
                    try:
                        fecha_dt = datetime.fromtimestamp(actividad['start_time'])
                        fecha = fecha_dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        fecha = "Fecha desconocida"
                etiqueta = f"{actividad.get('name', 'Sin nombre')} - {fecha} (ID: {actividad['id']})"
                opciones_actividades[etiqueta] = actividad['id']
            actividad_opcion = st.sidebar.selectbox(
                "Seleccione una actividad:",
                options=list(opciones_actividades.keys()),
                key="selector_actividad"
            )
            if actividad_opcion:
                actividad_seleccionada = opciones_actividades[actividad_opcion]
                st.session_state['actividad_id'] = actividad_seleccionada
                st.session_state['paso'] = 3

    # PASO 3: Seleccionar atleta
    if 'paso' in st.session_state and st.session_state['paso'] >= 3:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 3. Seleccionar Atleta")
        if st.sidebar.button("Cargar Atletas de la Actividad"):
            atletas = catapult.obtener_atletas_por_actividad(st.session_state['actividad_id'])
            st.session_state['atletas'] = atletas

        if 'atletas' in st.session_state and st.session_state['atletas']:
            opciones_atletas = {}
            for atleta in st.session_state['atletas']:
                nombre_completo = f"{atleta.get('first_name', '')} {atleta.get('last_name', '')}"
                if not nombre_completo.strip():
                    nombre_completo = "Atleta sin nombre"
                jersey = atleta.get('jersey', 'N/A')
                etiqueta = f"{nombre_completo} - #{jersey} (ID: {atleta['id']})"
                opciones_atletas[etiqueta] = atleta['id']
            atleta_opcion = st.sidebar.selectbox(
                "Seleccione un atleta:",
                options=list(opciones_atletas.keys()),
                key="selector_atleta"
            )
            if atleta_opcion:
                atleta_seleccionado = opciones_atletas[atleta_opcion]
                st.session_state['atleta_id'] = atleta_seleccionado
                st.session_state['paso'] = 4
        # ...existing code...

    if 'paso' in st.session_state and st.session_state['paso'] >= 4:
            st.sidebar.markdown("---")
            st.sidebar.markdown("### 4. Back in Game")
            if st.sidebar.button("Back in Game"):
                # Obtener datos del atleta y actividad
                atleta_info = next(
                    (a for a in st.session_state.get('atletas', []) if a['id'] == st.session_state['atleta_id']),
                    None
                )
                nombre_atleta = f"{atleta_info.get('first_name', '')} {atleta_info.get('last_name', '')}" if atleta_info else "Atleta seleccionado"
                jersey = atleta_info.get('jersey', '') if atleta_info else ''

                actividad_info = next(
                    (a for a in st.session_state.get('actividades', []) if a['id'] == st.session_state['actividad_id']),
                    {}
                )
                rival = actividad_info.get('opponent', actividad_info.get('team_name', ''))
                tipo_sesion = actividad_info.get('type', actividad_info.get('name', 'Sesión'))
                fecha = ""
                if actividad_info.get('start_time'):
                    try:
                        fecha = datetime.fromtimestamp(actividad_info['start_time']).strftime("%d/%m/%Y")
                    except:
                        fecha = "Fecha desconocida"
                duracion = actividad_info.get('duration', None)
                if duracion is None and actividad_info.get('start_time') and actividad_info.get('end_time'):
                    duracion = round((actividad_info['end_time'] - actividad_info['start_time']) / 60, 1)
                elif duracion is not None:
                    duracion = round(duracion / 60, 1)
                else:
                    duracion = "N/D"

                # Título y resumen de actividad
                st.markdown(f"""
                <div style='border:2px solid #1E88E5; border-radius:12px; padding:18px; margin-bottom:18px; background:#F5F5F5;'>
                    <span style='font-size:2rem; font-weight:700;'>🧾 BACK IN GAME REPORT</span><br>
                    <span style='font-size:1.2rem;'><b>Jugador:</b> {nombre_atleta} <b>#{jersey}</b></span><br>
                    <span style='font-size:1.2rem;'><b>Actividad:</b> {tipo_sesion} vs. {rival}</span><br>
                    <span style='font-size:1.2rem;'><b>Fecha:</b> {fecha}</span><br>
                    <span style='font-size:1.2rem;'><b>Duración de actividad:</b> {duracion} minutos</span>
                </div>
                """, unsafe_allow_html=True)

                # Paso principal: obtener datos fusionados y calcular métricas
                df_fusion = catapult.obtener_datos_fusionados(
                    st.session_state['actividad_id'],
                    st.session_state['atleta_id']
                )
                if df_fusion is not None and not df_fusion.empty:
                    df_back = catapult.calcular_back_in_game_multi(df_fusion)
                    # ...existing code...
                    if 'resumen_metricas' in st.session_state and st.session_state['resumen_metricas']:
                        st.markdown("<div style='text-align:center; font-size:1.1rem; font-weight:600;'>Resumen de métricas</div>", unsafe_allow_html=True)
                        for metrica in st.session_state['resumen_metricas']:
                            st.markdown(f"""
                            <div style='border:2px solid #1E88E5; border-radius:12px; padding:18px; margin:12px 0; background:#E3F2FD; text-align:center;'>
                                <span style='font-size:2rem; font-weight:700;'>Atleta: {metrica['Atleta']}</span><br>
                                <span style='font-size:1.5rem;'><b>Total eventos BIG:</b> {metrica['Total eventos BIG']}</span><br>
                                <span style='font-size:1.5rem;'><b>Tiempo medio entre eventos (min):</b> {metrica['Tiempo medio entre eventos (min)']}</span><br>
                                <span style='font-size:1.5rem;'><b>Duración media por evento (min):</b> {metrica['Duración media por evento (min)']}</span><br>
                                <span style='font-size:1.5rem;'><b>Carga total de actividad (min):</b> {metrica['Carga total de actividad (min)']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                            
                    if df_back is not None and not df_back.empty:
                        st.markdown("<hr>", unsafe_allow_html=True)
                        st.markdown("<div style='text-align:center; font-size:1.3rem; font-weight:600;'>Cancha de Rugby con Eventos</div>", unsafe_allow_html=True)
                        df_normalizado = normalizar_datos_atleta(df_back)
                        dibujar_cancha_rugby_con_eventos(df_normalizado)
                        # Mostrar el DataFrame debajo de la cancha
                        cols_base = ['tipo_evento', 'end_time', 'start_time', 'duration_min', 'back_in_game_min', 'confidence']
                        coords = ['start_x', 'start_y', 'end_x', 'end_y']
                        cols = cols_base + [c for c in coords if c in df_back.columns]
                        st.markdown("<div style='text-align:center; font-size:1.1rem; font-weight:600;'>Detalle de eventos</div>", unsafe_allow_html=True)
                        st.dataframe(df_back[cols])

                    else:
                        st.warning("No se pudieron calcular eventos 'Back in Game' para este atleta.")
                else:
                    st.warning("No se pudieron obtener eventos fusionados para este atleta.")

                # Agregar contacto al final del sidebar
            st.sidebar.markdown("---")
            st.sidebar.markdown("""
            <div style='font-size:1.1rem; color:#0D47A1;'>
                <b>Contacto:</b><br>
                Juan Calvo<br>
                <a href='mailto:calvoj550@gmail.com'>calvoj550@gmail.com</a>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()