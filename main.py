import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Monitoraggio Rinnovabili", layout="wide")

st.title("🗺️ Avanzamento Rinnovabili: Mappa e Andamento Politico")
st.markdown("Mappa del ritardo/anticipo sul target PNIEC (dati più recenti) e confronto storico tra coalizioni.")

# 1. Caricamento GeoJSON
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
    return requests.get(url).json()

geojson_data = load_geojson()

# 2. Dati attuali (per la mappa)
data = {
    "regione": [
        "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", 
        "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", 
        "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", 
        "Trentino-Alto Adige/Südtirol", "Umbria", "Valle d'Aosta/Vallée d'Aoste", "Veneto"
    ],
    "presidente": [
        "Marsilio", "Bardi", "Occhiuto", "De Luca", "De Pascale",
        "Fedriga", "Rocca", "Bucci", "Fontana", "Acquaroli",
        "Roberti", "Cirio", "Emiliano", "Todde", "Schifani", "Giani",
        "Kompatscher/Fugatti", "Proietti", "Testolin", "Zaia"
    ],
    "coalizione": [
        "Centrodestra", "Centrodestra", "Centrodestra", "Centrosinistra", "Centrosinistra",
        "Centrodestra", "Centrodestra", "Centrodestra", "Centrodestra", "Centrodestra",
        "Centrodestra", "Centrodestra", "Centrosinistra", "Centrosinistra", "Centrodestra", "Centrosinistra",
        "Autonomisti", "Centrosinistra", "Autonomisti", "Centrodestra"
    ],
    "delta_mw": [-124, -182, -447, 91, 65, 314, 1428, -102, 697, -125, -181, 422, -267, -599, -3, -302, 95, -193, -23, 377]
}

df_attuale = pd.DataFrame(data)

def categorizza(c):
    if "Centrodestra" in c: return "Centrodestra"
    if "Centrosinistra" in c: return "Centrosinistra"
    return "Autonomisti"

df_attuale["macro_area_politica"] = df_attuale["coalizione"].apply(categorizza)

# 3. Mappa
fig_map = px.choropleth_mapbox(
    df_attuale,
    geojson=geojson_data,
    locations="regione",
    featureidkey="properties.reg_name",
    color="delta_mw",
    color_continuous_scale="RdYlGn",
    mapbox_style="carto-positron",
    zoom=4.8,
    center={"lat": 41.9, "lon": 12.5},
    opacity=0.8,
    hover_name="regione",
    hover_data={"delta_mw": True, "presidente": True, "coalizione": True, "regione": False},
    labels={"delta_mw": "Scostamento (MW)", "presidente": "Presidente"}
)
fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550)

st.plotly_chart(fig_map, use_container_width=True)

# 4. Elaborazione dati storici per il grafico
@st.cache_data
def prepara_dati_storici(df_riferimento):
    try:
        df_hist = pd.read_excel('prova terna.xlsx')
        df_hist = df_hist.rename(columns={'REGIONE': 'regione', 'delta (MW)': 'delta_mw', 'data': 'data_rilevazione'})
        df_hist = df_hist.dropna(subset=['regione', 'delta_mw'])
        df_hist['regione'] = df_hist['regione'].astype(str).str.upper()
        
        mappa_nomi = {
            "EMILIA ROMAGNA": "Emilia-Romagna",
            "FRIULI VENEZIA GIULIA": "Friuli-Venezia Giulia",
            "TRENTINO ALTO ADIGE": "Trentino-Alto Adige/Südtirol",
            "VALLE D'AOSTA": "Valle d'Aosta/Vallée d'Aoste"
        }
        df_hist['regione'] = df_hist['regione'].apply(lambda x: mappa_nomi.get(x, x.title()))
        
        # Unisce le info politiche
        mappa_politica = dict(zip(df_riferimento['regione'], df_riferimento['macro_area_politica']))
        df_hist['macro_area_politica'] = df_hist['regione'].map(mappa_politica)
        
        # Somma i MW per data e coalizione
        df_grouped = df_hist.groupby(['data_rilevazione', 'macro_area_politica'])['delta_mw'].sum().reset_index()
        # Tiene solo CDX e CSX
        return df_grouped[df_grouped['macro_area_politica'].isin(['Centrodestra', 'Centrosinistra'])]
    except Exception as e:
        return None

df_grafico = prepara_dati_storici(df_attuale)

# 5. Grafico Storico
st.markdown("---")
st.subheader("📈 Evoluzione dello Spread: Centrodestra vs Centrosinistra")

if df_grafico is not None and not df_grafico.empty:
    fig_line = px.line(
        df_grafico, 
        x='data_rilevazione', 
        y='delta_mw', 
        color='macro_area_politica',
        color_discrete_map={"Centrodestra": "#1f77b4", "Centrosinistra": "#d62728"}, # Blu per CDX, Rosso per CSX
        markers=True,
        labels={"data_rilevazione": "Data", "delta_mw": "Scostamento Totale (MW)", "macro_area_politica": "Coalizione"}
    )
    fig_line.add_hline(y=0, line_dash="dash", line_color="black")
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.warning("Impossibile caricare il grafico storico. Verifica che 'prova terna.xlsx' sia formattato correttamente.")
