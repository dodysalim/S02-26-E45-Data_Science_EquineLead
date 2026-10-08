import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import subprocess

import streamlit as st
from modules.ai_subsystem import render_ai_subsystem
from modules.audience_analytics import render_audience_analytics
from modules.conversion_analytics import render_conversion_analytics
from modules.executive_summary import render_executive_summary
from modules.horse_analytics import render_horse_analytics
from modules.retail_analytics import render_retail_analytics
from utils.data_loader import get_all_dashboard_data, get_data_directory, REQUIRED_DATA_FILES
from utils.style_utils import inject_premium_style


def pull_data():
    import json
    import tempfile

    local_data = str(get_data_directory())
    required = REQUIRED_DATA_FILES
    if all(os.path.isfile(os.path.join(local_data, name)) for name in required):
        return
    try:
        creds_dict = dict(st.secrets["gcp"])
    except (FileNotFoundError, KeyError, st.errors.StreamlitSecretNotFoundError):
        st.info("Configure las credenciales GCP en Streamlit Secrets o descargue los datos DVC en data/clean o app/data/clean para abrir el dashboard.")
        st.stop()

    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(creds_dict, tmp)
    tmp.flush()
    tmp.close()

    try:
        result = subprocess.run(
            [sys.executable, "-m", "dvc", "pull", "--remote", "gcsremote"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            capture_output=True, text=True, timeout=300,
            env={**os.environ, "GOOGLE_APPLICATION_CREDENTIALS": tmp.name},
        )
        if result.returncode != 0:
            st.error("No se pudieron descargar los datos. Revisa la configuración DVC/GCP.")
            st.stop()
        local_data = str(get_data_directory())
        if not all(os.path.isfile(os.path.join(local_data, name)) for name in required):
            st.error("La descarga no contiene todos los archivos esperados en data/clean o app/data/clean.")
            st.stop()
        st.toast("Datos descargados", icon="✅")
    except (OSError, subprocess.TimeoutExpired):
        st.error("La descarga no terminó. Instala DVC con soporte GCS y revisa el acceso al almacén.")
        st.stop()
    finally:
        os.unlink(tmp.name)


if "data_pulled" not in st.session_state:
    pull_data()
    st.session_state["data_pulled"] = True

# ---------------------------------------------
# 1. GLOBAL CONFIGURATION & AESTHETICS
# ---------------------------------------------
st.set_page_config(
    page_title="EquineLead Analytics PRO",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded",
)

# Inject Premium Dark Theme
inject_premium_style()

# ---------------------------------------------
# 2. GLOBAL DATA SYNCHRONIZATION
# ---------------------------------------------
df_horses, df_products, df_users, df_u_sessions, df_p_sessions = (
    get_all_dashboard_data()
)

# ---------------------------------------------
# 3. SIDEBAR NAVIGATION
# ---------------------------------------------
st.sidebar.markdown(
    """<h2 style='text-align: center; color: #00B8D9;
    font-weight: 800;'>EQUINELEAD PRO</h2>""",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    """<p style='text-align: center; font-size: 0.9em;
      color: #64748B;'>Executive Analytics Engine</p>""",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "REPORT VIEWS",
    [
        "📊 1. Executive Summary",
        "🐎 2. Horse Inventory Metrics",
        "📦 3. Ecommerce & Products",
        "🌍 4. Global Audience",
        "⚡ 5. Conversion & Funnels",
        "🧠 6. AI Subsystem (Dagshub)",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Fuente: archivos Parquet cargados")
st.sidebar.caption("Sesiones: muestra de hasta 10.000 filas por tabla")
st.sidebar.caption("No Country · Equipo 45")

# ---------------------------------------------
# 4. ROUTING & RENDERING
# ---------------------------------------------
if page == "📊 1. Executive Summary":
    render_executive_summary(
        df_users, df_horses, df_products, df_u_sessions, df_p_sessions
    )

elif page == "🐎 2. Horse Inventory Metrics":
    render_horse_analytics(df_horses)

elif page == "📦 3. Ecommerce & Products":
    render_retail_analytics(df_products)

elif page == "🌍 4. Global Audience":
    render_audience_analytics(df_users)

elif page == "⚡ 5. Conversion & Funnels":
    render_conversion_analytics(df_u_sessions, df_p_sessions)

elif page == "🧠 6. AI Subsystem (Dagshub)":
    render_ai_subsystem()
