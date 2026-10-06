import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. Configurazione
st.set_page_config(page_title="Monitoraggio Rinnovabili", layout="wide", initial_sidebar_state="expanded")
st.title("🗺️ Mappa Italia: Corsa alle Rinnovabili e Decreto Aree Idonee")
st.markdown("Questa mappa interattiva mostra in tempo reale chi è in ritardo e chi è in anticipo rispetto agli obiettivi vincolanti fissati per ciascuna regione.")

# 2. GeoJSON Originale di OpenPolis
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
    return requests.get(url).json()

geojson_data = load_geojson()

# 3. Funzione di Normalizzazione e Caricamento Dati
def normalize_region(name):
    if not isinstance(name, str): return name
    n = name.upper()
    if 'FRIULI' in n: return 'Friuli-Venezia Giulia'
    if 'TRENTINO' in n: return 'Trentino-Alto Adige/Südtirol'
    if 'AOSTA' in n: return "Valle d'Aosta/Vallée d'Aoste"
    if 'EMILIA' in n: return 'Emilia-Romagna'
    mapping = {
        "ABRUZZO": "Abruzzo", "BASILICATA": "Basilicata", "CALABRIA": "Calabria",
        "CAMPANIA": "Campania", "LAZIO": "Lazio", "LIGURIA": "Liguria",
        "LOMBARDIA": "Lombardia", "MARCHE": "Marche", "MOLISE": "Molise",
        "PIEMONTE": "Piemonte", "PUGLIA": "Puglia", "SARDEGNA": "Sardegna",
        "SICILIA": "Sicilia", "TOSCANA": "Toscana", "UMBRIA": "Umbria", "VENETO": "Veneto"
    }
    return mapping.get(n, n)

@st.cache_data
def load_excel_data():
    try:
        # Legge il nuovo file Terna
        df = pd.read_excel("prova terna.xlsx", sheet_name='Foglio1')
        df = df.dropna(subset=['data', 'REGIONE'])
        df['regione'] = df['REGIONE'].apply(normalize_region)
        return df
    except Exception as e:
        return None

df_raw = load_excel_data()

# Dati Politici di base
data_politica = {
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
    ]
}
df_politica = pd.DataFrame(data_politica)

def categorizza_schieramento(coalizione):
    if not isinstance(coalizione, str): return "Autonomisti"
    if "Centrodestra" in coalizione: return "Centrodestra"
    if "Centrosinistra" in coalizione: return "Centrosinistra"
    return "Autonomisti"

# 4. Elaborazione Dati se il file è presente
if df_raw is not None:
    # Unione dati grezzi con informazioni politiche
    df_merged = pd.merge(df_raw, df_politica, on='regione', how='left')
    df_merged["macro_area_politica"] = df_merged["coalizione"].apply(categorizza_schieramento)

    # 4A. Estrazione Dati Attuali (Ultimo mese disponibile)
    latest_date = df_merged['data'].max()
    df_latest = df_merged[df_merged['data'] == latest_date].copy()
    
    df_latest = df_latest.rename(columns={
        "delta installato gen 2021 - mese riferimento (MW)": "installato_mw",
        "target aree idonee gen 2021 - mese riferimento (MW)": "target_mw",
        "delta (MW)": "delta_mw"
    })
    
    # Calcolo percentuale
    df_latest["delta_perc"] = ((df_latest["delta_mw"] / df_latest["target_mw"]) * 100).round(1)

    # 4B. Estrazione Dati Storici Aggregati (per il grafico)
    df_storico = df_merged.groupby(['data', 'macro_area_politica'])['delta (MW)'].sum().reset_index()
    df_storico_pivot = df_storico.pivot(index='data', columns='macro_area_politica', values='delta (MW)').reset_index()
else:
    # Fallback vuoto per evitare crash dell'interfaccia se manca il file
    df_latest = df_politica.copy()
    df_latest["delta_mw"] = 0
    df_latest["delta_perc"] = 0
    df_latest["installato_mw"] = 0
    df_latest["target_mw"] = 0
    df_latest["macro_area_politica"] = df_latest["coalizione"].apply(categorizza_schieramento)
    df_storico_pivot = None

# 5. Interfaccia Sidebar
st.sidebar.header("⚙️ Opzioni Visualizzazione")
tipo_visualizzazione = st.sidebar.radio(
    "Mostra i dati sulla mappa come:",
    options=["Valore Assoluto (MW)", "Percentuale sul Target (%)"]
)

# 6. Mappa Leggera (px.choropleth base)
colonna_colore = "delta_mw" if tipo_visualizzazione == "Valore Assoluto (MW)" else "delta_perc"
etichetta_colore = "Scostamento (MW)" if tipo_visualizzazione == "Valore Assoluto (MW)" else "Scostamento (%)"

fig = px.choropleth(
    df_latest,
    geojson=geojson_data,
    locations="regione",
    featureidkey="properties.reg_name",
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

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550)

# 7. Layout a colonne
col_map, col_details = st.columns([1.3, 1])

with col_map:
    map_selection = st.plotly_chart(fig, use_container_width=True, on_select="rerun", selection_mode="points")

# 8. Pannello Dettagli o Grafico Storico
with col_details:
    selected_region = None
    if map_selection and "selection" in map_selection and map_selection["selection"]["points"]:
        selected_region = map_selection["selection"]["points"][0].get("location")
        
    if selected_region:
        # Mostra i dettagli della regione selezionata
        row = df_latest[df_latest["regione"] == selected_region].iloc[0]
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
        # Mostra il grafico storico se nessuna regione è cliccata
        st.markdown("### 📈 Spread: Centrodestra vs Centrosinistra")
        st.write("Andamento aggregato nel tempo dello scostamento in MW (Clicca su una regione per i dettagli singoli).")
        
        if df_storico_pivot is not None:
            # Creiamo il grafico a linee dinamicamente dai dati aggregati
            fig_line = px.line(
                df_storico_pivot, 
                x='data', 
                y=['Centrodestra', 'Centrosinistra'],
                color_discrete_map={
                    "Centrodestra": "#1f77b4", # Blu
                    "Centrosinistra": "#d62728" # Rosso
                },
                labels={"value": "Scostamento (MW)", "variable": "", "data": "Data Rilevazione"}
            )
            
            fig_line.add_hline(y=0, line_dash="dash", line_color="black")
            fig_line.update_layout(
                margin={"r": 0, "t": 10, "l": 0, "b": 0}, 
                height=350,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("⚠️ File 'prova terna (1).xlsx' non trovato. Assicurati che il file sia nella stessa cartella.")

# 9. Metriche Finali
st.markdown("---")
st.subheader("⚖️️ Bilancio dell'Avanzamento Globale")
st.write("Aggregazione dello scostamento complessivo (in MW) in base al colore politico della Giunta.")

bilancio = df_latest.groupby("macro_area_politica")["delta_mw"].sum()

col1, col2, col3 = st.columns(3)
val_cdx = bilancio.get('Centrodestra', 0)
val_csx = bilancio.get('Centrosinistra', 0)
val_aut = bilancio.get('Autonomisti', 0)

col1.metric("🔵 Centrodestra", f"{val_cdx} MW", delta="In anticipo" if val_cdx >= 0 else "In ritardo", delta_color="normal" if val_cdx >= 0 else "inverse")
col2.metric("🔴 Centrosinistra", f"{val_csx} MW", delta="In anticipo" if val_csx >= 0 else "In ritardo", delta_color="normal" if val_csx >= 0 else "inverse")
col3.metric("⚪ Autonomisti", f"{val_aut} MW", delta="In anticipo" if val_aut >= 0 else "In ritardo", delta_color="normal" if val_aut >= 0 else "inverse")
