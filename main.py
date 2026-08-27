import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. Configurazione
st.set_page_config(page_title="Monitoraggio Rinnovabili", layout="wide", initial_sidebar_state="expanded")
st.title("Corsa all'energia pulita")
st.markdown("Questa mappa interattiva mostra in tempo reale chi è in ritardo e chi è in anticipo rispetto agli obiettivi vincolanti fissati per ciascuna regione per questo mese.")

# 2. GeoJSON Originale di OpenPolis
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

# 4. Interfaccia Sidebar
st.sidebar.header("⚙️ Opzioni Visualizzazione")
tipo_visualizzazione = st.sidebar.radio(
    "Mostra i dati sulla mappa come:",
    options=["Valore Assoluto (MW)", "Percentuale sul Target (%)"]
)

# 5. Mappa Leggera (px.choropleth base)
colonna_colore = "delta_mw" if tipo_visualizzazione == "Valore Assoluto (MW)" else "delta_perc"
etichetta_colore = "Scostamento (MW)" if tipo_visualizzazione == "Valore Assoluto (MW)" else "Scostamento (%)"

fig = px.choropleth(
    df,
    geojson=geojson_data,
    locations="regione",
    featureidkey="properties.reg_name", # Chiave corretta OpenPolis
    color=colonna_colore,
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
    scope="europe",
    hover_name="regione",
    hover_data={"presidente": True, "delta_mw": True, "delta_perc": True, "regione": False},
    labels={
        "delta_mw": "Scostamento (MW)",
        "delta_perc": "Scostamento (%)",
        "presidente": "Governatore"
    }
)

# Ritaglia via l'Europa per concentrarsi solo sull'Italia
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550)

# Layout a colonne
col_map, col_details = st.columns([1.3, 1])

with col_map:
    map_selection = st.plotly_chart(fig, use_container_width=True, on_select="rerun", selection_mode="points")

# 6. Pannello Dettagli Dinamico
with col_details:
    selected_region = None
    if map_selection and "selection" in map_selection and map_selection["selection"]["points"]:
        selected_region = map_selection["selection"]["points"][0].get("location")
        
    if selected_region:
        row = df[df["regione"] == selected_region].iloc[0]
        st.markdown(f"### **Dettaglio: {row['regione']}**")
        st.write(f"👤 **Presidente:** {row['presidente']} (*{row['coalizione']}*)")
        st.write("---")
        
        delta_val = row['delta_mw']
        if delta_val >= 0:
            st.success(f"**Avanzamento**\n\n✅ **In anticipo:** `+{delta_val} MW` (+{row['delta_perc']}% sul target)")
        else:
            st.error(f"**Avanzamento**\n\n⚠️ **In ritardo:** `{delta_val} MW` ({row['delta_perc']}% sul target)")
        
        st.write(f"📊 **Target progressivo:** {row['target_mw']} MW")
        st.write(f"📈 **Installato netto:** {row['installato_mw']} MW")
            
    else:
        st.markdown("### 👈 Come leggere i dati")
        st.write("Clicca su una regione sulla mappa per vederne i numeri esatti.")
        st.info("🟢 **Verde:** in anticipo sul target.")
        st.warning("🔴 **Rosso:** in ritardo sul target.")

# 7. Metriche Finali
st.markdown("---")
st.subheader("⚖️ Bilancio dell'Avanzamento")
st.write("Aggregazione dello scostamento complessivo (in MW) in base al colore politico della Giunta.")
bilancio = df.groupby("macro_area_politica")["delta_mw"].sum()

col1, col2, col3 = st.columns(3)
val_cdx = bilancio.get('Centrodestra', 0)
val_csx = bilancio.get('Centrosinistra', 0)
val_aut = bilancio.get('Autonomisti', 0)

col1.metric("🔵 Centrodestra", f"{val_cdx} MW", delta="In anticipo" if val_cdx >= 0 else "In ritardo", delta_color="normal" if val_cdx >= 0 else "inverse")
col2.metric("🔴 Centrosinistra", f"{val_csx} MW", delta="In anticipo" if val_csx >= 0 else "In ritardo", delta_color="normal" if val_csx >= 0 else "inverse")
col3.metric("⚪ Autonomisti", f"{val_aut} MW", delta="In anticipo" if val_aut >= 0 else "In ritardo", delta_color="normal" if val_aut >= 0 else "inverse")
