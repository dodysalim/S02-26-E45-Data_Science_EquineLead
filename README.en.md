<p align="center"><img src="https://dodysalim.github.io/assets/project-covers/equinelead.webp" alt="EquineLead" width="100%"></p>

<h1 align="center">EquineLead</h1>

<p align="center"><b>Equestrian-market analytics: audience, inventory and business opportunities.</b></p>

<p align="center"><img src="https://img.shields.io/badge/No_Country_·_Team_45_·_February_2026-75E6CE?style=for-the-badge&labelColor=0b1222" alt="No Country · Team 45 · February 2026"></p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/Parquet-50ABF1?style=flat-square&logoColor=white" alt="Parquet"> <img src="https://img.shields.io/badge/XGBoost-1F6FEB?style=flat-square&logoColor=white" alt="XGBoost"> <img src="https://img.shields.io/badge/DVC-13ADC7?style=flat-square&logo=dvc&logoColor=white" alt="DVC"> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"> <img src="https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logoColor=black" alt="Power BI">
</p>

<p align="center"><a href="https://dodysalim.github.io/"><b>🌐 Portfolio</b></a> · <a href="https://nocountry.tech/showcase/simulacion-laboral-febrero-2026/equipo-45-data-science"><b>🏆 No Country Showcase</b></a> · <a href="README.md"><b>🇪🇸 Versión en español</b></a></p>

---

## 📌 At a glance

| | |
| --- | --- |
| **🎯 Problem** | Relate visits, engagement and inventory to conversion opportunities. |
| **🛠️ Solution** | Team ML pipelines and services, DVC-versioned data and efficient Parquet loading. |
| **📈 Deliverables** | 6-view dashboard (inventory, retail, audience, conversion, AI) and Power BI. |
| **👤 My role** | Data Analyst in a 4-person team. |

## 🏗️ Architecture

```mermaid
flowchart LR
    SRC[Sitios ecuestres] --> SCR[scraping] --> CLN[cleaning]
    SYN[synthetizing<br/>tracking de usuarios] --> DVC
    CLN --> DVC[(Parquet + DVC)]
    DVC --> EXP[experiments<br/>XGBoost leads] --> REG[registry<br/>MLflow / DagsHub]
    REG --> API[API FastAPI]
    DVC --> APP[Dashboard Streamlit<br/>6 vistas]
    REG --> APP
```

## 🚀 How to run

```bash
pip install -r app/requirements.txt
cp .env.example .env
python -m streamlit run app/app.py
```

## ⚖️ Scope

Requires the original Parquet files or DVC/GCP access; it never substitutes fake data.

## 👥 Team

Team: Alexander Rios · Daisy Quinteros · Iñaki Rosello · Dody Dueñas (Data Analyst). Collective authorship is preserved.

---

<p align="center">
<b>Dody Dueñas Remache</b> · Data Analyst / Data Scientist · Guayaquil, Ecuador (remote LATAM)<br>
<a href="https://dodysalim.github.io/">Portfolio</a> · <a href="https://github.com/dodysalim">GitHub</a> · <a href="https://www.linkedin.com/in/dody-duenas/">LinkedIn</a> · <a href="mailto:dodydurema67@gmail.com">dodydurema67@gmail.com</a>
</p>
