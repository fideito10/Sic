from supabase import create_client, Client
from SIC import CatapultSelector, api_token  # Asegúrate de tener tu clase y token
from datetime import datetime

# Configura tu conexión a Supabase
url = "https://awllmjfnkvfaevvcxymv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF3bGxtamZua3ZmYWV2dmN4eW12Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMwOTQ4NzUsImV4cCI6MjA2ODY3MDg3NX0.wJ3Hl3eGDf-dAUEJGeL3IVFQzr1IpTNS2DU3xuioBhE"
supabase: Client = create_client(url, key)

catapult = CatapultSelector(api_token)

def sync_catapult_to_supabase():
    equipos = catapult.obtener_equipos()
    for equipo in equipos:
        # Insertar equipo
        supabase.table("teams").upsert({
            "id": equipo["id"],
            "sport": equipo.get("sport"),
            "name": equipo.get("name"),
            "tags": equipo.get("tags", [])
        }).execute()
        print(f"Equipo insertado: {equipo['name']}")

        # Atletas del equipo
        atletas = catapult.obtener_atletas(equipo["id"])
        for atleta in atletas:
            supabase.table("athletes").upsert({
                "id": atleta["id"],
                "first_name": atleta.get("first_name"),
                "last_name": atleta.get("last_name"),
                "jersey": atleta.get("jersey"),
                "height": atleta.get("height"),
                "weight": atleta.get("weight"),
                "team_id": equipo["id"],
                "tags": atleta.get("tags", [])
            }).execute()
        print(f"Atletas insertados para equipo {equipo['name']}")

        # Actividades del equipo
        actividades = catapult.obtener_actividades_por_equipo(equipo["id"], dias_atras=365)
        for actividad in actividades:
            # Conversión de timestamps
            start_time = actividad.get("start_time")
            end_time = actividad.get("end_time")
            if start_time:
                start_time = datetime.fromtimestamp(start_time).isoformat()
            else:
                start_time = None
            if end_time:
                end_time = datetime.fromtimestamp(end_time).isoformat()
            else:
                end_time = None

            supabase.table("activities").upsert({
                "id": actividad["id"],
                "name": actividad.get("name"),
                "start_time": start_time,
                "end_time": end_time,
                "venue": actividad.get("venue"),
                "tags": actividad.get("tags", [])
            }).execute()
            print(f"Actividad insertada: {actividad.get('name')}")

            # Atletas participantes en la actividad
            atletas_actividad = catapult.obtener_atletas_por_actividad(actividad["id"])
            import uuid
            def atleta_existe(supabase, atleta_id):
                res = supabase.table("athletes").select("id").eq("id", atleta_id).execute()
                return bool(res.data)

            for atleta_act in atletas_actividad:
                # Verifica si el atleta existe en la tabla athletes
                if not atleta_existe(supabase, atleta_act["id"]):
                    supabase.table("athletes").upsert({
                        "id": atleta_act["id"],
                        "first_name": atleta_act.get("first_name", ""),
                        "last_name": atleta_act.get("last_name", ""),
                        "jersey": atleta_act.get("jersey", ""),
                        "height": atleta_act.get("height"),
                        "weight": atleta_act.get("weight"),
                        "team_id": equipo["id"],
                        "tags": atleta_act.get("tags", [])
                    }).execute()
                supabase.table("participating_athletes").upsert({
                    "id": str(uuid.uuid4()),  # Genera un UUID válido
                    "athlete_id": atleta_act["id"],
                    "period_id": None,  # Si tienes periodos, pon el id correcto
                    "tags": atleta_act.get("tags", [])
                }).execute()
            print(f"Participantes insertados para actividad {actividad.get('name')}")

if __name__ == "__main__":
    sync_catapult_to_supabase()
    print("¡Sincronización completa!")