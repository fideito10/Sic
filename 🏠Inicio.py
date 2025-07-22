import streamlit as st



# --- CONFIGURACIÓN VISUAL DE STREAMLIT (coherente con Pages) ---


st.set_page_config(page_title="Club SIC - Portal Deportivo", page_icon="📊", layout="centered")
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

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<h1 class='main-header'>Bienvenido al Club SIC</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>Portal Deportivo</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        <span style='color:#00bcd4; font-size:22px; font-weight:bold;'>Área de Análisis de Rendimiento Deportivo</span>
        """,
        unsafe_allow_html=True
    )
    st.markdown("""
    ¡Bienvenido al portal del Club SIC!  
    Aquí podrás encontrar información sobre:

    - **Back in Game:** Un espacio dedicado a la vuelta al juego, donde te explicamos de manera sencilla cómo los jugadores vuelven al juego luego de un contacto.  
    """)
with col2:
    st.image("Pages/assets/Sic.jpeg", width=180, caption="Club SIC")

st.markdown("<h2 class='sub-header'>Estadísticas</h2>", unsafe_allow_html=True)
st.info("⚽ SIC - Estadísticas de rendimiento")

st.markdown("<h2 class='sub-header'>Contacto</h2>", unsafe_allow_html=True)
st.write("📧 calvoj550@gmail.com.")
st.write("📱 +54 1221-357-1957")

st.markdown("Síguenos en [Instagram](https://instagram.com) y [Facebook](https://facebook.com)")

# Puedes agregar más secciones o funcionalidades según lo que necesites.