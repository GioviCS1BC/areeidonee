import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. Configurazione
st.set_page_config(page_title="Monitoraggio Rinnovabili", layout="wide", initial_sidebar_state="expanded")
st.title("🗺️ Mappa Italia: Corsa alle Rinnovabili e Decreto Aree Idonee")

# 2. GeoJSON Originale (Quello che funzionava)
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
    return requests.get(url).json()

geojson_data = load_geojson()

# 3. Dati Attuali
data = {
    "regione": [
        "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", 
        "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", 
        "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", 
        "Trentino-Alto Adige/Südtirol", "Umbria", "Valle d'Aosta/Vallée d'Aoste", "Veneto"
    ],
    "presidente": [
        "Marco Marsilio", "Vito Bardi", "Roberto Occhiuto", "Vincenzo De Luca", "Michele De Pascale",
        "Massimiliano Fedriga", "Francesco Rocca", "Marco Bucci", "Attilio Fontana", "Francesco Acquaroli",
        "Francesco Roberti", "Alberto Cirio", "Michele Emiliano", "Alessandra Todde", "Renato Schifani", "Eugenio Giani",
        "Arno Kompatscher / Maurizio Fugatti", "Stefania Proietti", "Renzo Testolin", "Luca Zaia"
    ],
    "coalizione": [
        "Centrodestra", "Centrodestra", "Centrodestra", "Centrosinistra", "Centrosinistra",
        "Centrodestra", "Centrodestra", "Centrodestra", "Centrodestra", "Centrodestra",
        "Centrodestra", "Centrodestra", "Centrosinistra", "Centrosinistra", "Centrodestra", "Centrosinistra",
        "Autonomisti / Centrodestra", "Centrosinistra", "Autonomisti", "Centrodestra"
    ],
    "delta_mw": [
        -124, -182, -447, 91, 65, 314, 1428, -102, 697, -125, 
        -181, 422, -267, -599, -3, -302, 95, -193, -23, 377
    ],
    "installato_mw": [
        638, 697, 613, 1640, 2297, 1003, 3055, 238, 3923, 701, 
        156, 2262, 2610, 1336, 3393, 965, 543, 341, 40, 2612
    ],
    "target_mw": [
        763, 879, 1061, 1548, 2232, 689, 1628, 340, 3226, 825, 
        337, 1840, 2876, 1935, 3396, 1267, 449, 534, 63, 2236
    ]
}

df = pd.DataFrame(data)
df["delta_perc"] = ((df["delta_mw"] / df["target_mw"]) * 100).round(1)

def categorizza_schieramento(coalizione):
    if "Centrodestra" in coalizione: return "Centrodestra"
    if "Centrosinistra" in coalizione: return "Centrosinistra"
    return "Autonomisti"

df["macro_area_politica"] = df["coalizione"].apply(categorizza_schieramento)

# 4. Elaborazione Dati Storici (Sicura)
@st.cache_data
def load_historical_data():
    try:
        df_hist = pd.read_excel('prova terna.xlsx')
        df_hist = df_hist.rename(columns={'REGIONE': 'regione', 'delta (MW)': 'delta_mw', 'data': 'data_rilevazione'})
        df_hist = df_hist.dropna(subset=['regione', 'delta_mw'])
        df_hist['regione'] = df_hist['regione'].astype(str).str.upper().strip()
        
        mappa_nomi = {
            "EMILIA ROMAGNA": "Emilia-Romagna",
            "FRIULI VENEZIA GIULIA": "Friuli-Venezia Giulia",
            "TRENTINO ALTO ADIGE": "Trentino-Alto Adige/Südtirol",
            "VALLE D'AOSTA": "Valle d'Aosta/Vallée d'Aoste"
        }
        df_hist['regione'] = df_hist['regione'].apply(lambda x: mappa_nomi.get(x, x.title()))
        
        # Mappatura politica
        mappa_politica = dict(zip(df['regione'], df['macro_area_politica']))
        df_hist['macro_area_politica'] = df_hist['regione'].map(mappa_politica)
        
        return df_hist
    except Exception:
        return None

df_storico = load_historical_data()

# 5. Interfaccia Sidebar
st.sidebar.header("⚙️ Opzioni Visualizzazione")
tipo_visualizzazione = st.sidebar.radio(
    "Mostra i dati sulla mappa come:",
    options=["Valore Assoluto (MW)", "Percentuale sul Target (%)"]
)

# 6. Mappa Originale Funzionante
colonna_colore = "delta_mw" if tipo_visualizzazione == "Valore Assoluto (MW)" else "delta_perc"
etichetta_colore = "Scostamento (MW)" if tipo_visualizzazione == "Valore Assoluto (MW)" else "Scostamento (%)"

fig = px.choropleth_mapbox(
    df,
    geojson=geojson_data,
    locations="regione",
    featureidkey="properties.reg_name", # La chiave originale corretta
    color=colonna_colore,
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
    mapbox_style="carto-positron",
    zoom=4.8,
    center={"lat": 41.9, "lon": 12.5},
    opacity=0.8,
    hover_name="regione",
    hover_data={"presidente": True, "delta_mw": True, "delta_perc": True, "regione": False}
)

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550)

# Layout a colonne
col_map, col_details = st.columns([1.3, 1])

with col_map:
    map_selection = st.plotly_chart(fig, use_container_width=True, on_select="rerun", selection_mode="points")

# 7. Pannello Dettagli o Grafico Spread
with col_details:
    selected_region = None
    if map_selection and "selection" in map_selection and map_selection["selection"]["points"]:
        selected_region = map_selection["selection"]["points"][0].get("location")
        
    if selected_region:
        row = df[df["regione"] == selected_region].iloc[0]
        st.markdown(f"### **Dettaglio: {row['regione']}**")
        st.write(f"👤 **Presidente:** {row['presidente']} (*{row['coalizione']}*)")
        
        delta_val = row['delta_mw']
        if delta_val >= 0:
            st.success(f"✅ **In anticipo:** `+{delta_val} MW` (+{row['delta_perc']}% sul target)")
        else:
            st.error(f"⚠️ **In ritardo:** `{delta_val} MW` ({row['delta_perc']}% sul target)")
            
    else:
        st.markdown("### 📈 Spread Centrodestra vs Centrosinistra")
        st.write("Andamento aggregato nel tempo dello scostamento in MW (Clicca su una regione per i dettagli singoli).")
        
        if df_storico is not None:
            df_grouped = df_storico.groupby(['data_rilevazione', 'macro_area_politica'])['delta_mw'].sum().reset_index()
            df_spread = df_grouped[df_grouped['macro_area_politica'].isin(['Centrodestra', 'Centrosinistra'])]
            
            fig_line = px.line(
                df_spread, 
                x='data_rilevazione', 
                y='delta_mw', 
                color='macro_area_politica',
                color_discrete_map={"Centrodestra": "#1f77b4", "Centrosinistra": "#d62728"},
                markers=True
            )
            fig_line.add_hline(y=0, line_dash="dash", line_color="black")
            fig_line.update_layout(margin={"r": 0, "t": 10, "l": 0, "b": 0}, height=350)
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("Dati storici non caricati. Controlla il file 'prova terna.xlsx'.")

# 8. Metriche Finali
st.markdown("---")
st.subheader("⚖️ Bilancio dell'Avanzamento")
bilancio = df.groupby("macro_area_politica")["delta_mw"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("🔵 Centrodestra", f"{bilancio.get('Centrodestra', 0)} MW")
col2.metric("🔴 Centrosinistra", f"{bilancio.get('Centrosinistra', 0)} MW")
col3.metric("⚪ Autonomisti", f"{bilancio.get('Autonomisti', 0)} MW")
