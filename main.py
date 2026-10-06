```python
import pandas as pd
file_path = "prova terna (1).xlsx"
xls = pd.ExcelFile(file_path)
print("Sheet names:", xls.sheet_names)
for sheet in xls.sheet_names:
    print(f"\n--- Sheet: {sheet} ---")
    df = pd.read_excel(file_path, sheet_name=sheet)
    print(df.head())
    print(df.columns)


```

```text
Sheet names: ['Foglio1']

--- Sheet: Foglio1 ---
          REGIONE  delta installato gen 2021 - mese riferimento (MW)  target aree idonee gen 2021 - mese riferimento (MW)  delta (MW)  target aree idonee gen 21 - dic anno riferimento (MW)       data
0         ABRUZZO                                              650.0                                                780.0      -130.0                                                  850.0 2026-08-01
1      BASILICATA                                              729.0                                                898.0      -169.0                                                  973.0 2026-08-01
2        CALABRIA                                              627.0                                               1090.0      -463.0                                                 1206.0 2026-08-01
3        CAMPANIA                                             1653.0                                               1584.0        69.0                                                 1728.0 2026-08-01
4  EMILIA ROMAGNA                                             2333.0                                               2286.0        46.0                                                 2504.0 2026-08-01
Index(['REGIONE', 'delta installato gen 2021 - mese riferimento (MW)',
       'target aree idonee gen 2021 - mese riferimento (MW)', 'delta (MW)',
       'target aree idonee gen 21 - dic anno riferimento (MW)', 'data'],
      dtype='object')


```

```python
import pandas as pd
file_path = "prova terna (1).xlsx"
df = pd.read_excel(file_path, sheet_name='Foglio1')
print(df['REGIONE'].unique())


```

```text
['ABRUZZO' 'BASILICATA' 'CALABRIA' 'CAMPANIA' 'EMILIA ROMAGNA'
 'FRIULI VENEZIA GIULIA' 'LAZIO' 'LIGURIA' 'LOMBARDIA' 'MARCHE' 'MOLISE'
 'PIEMONTE' 'PUGLIA' 'SARDEGNA' 'SICILIA' 'TOSCANA' 'TRENTINO ALTO ADIGE'
 'UMBRIA' "VALLE D'AOSTA" 'VENETO' nan 'FRIULI']


```

```python
import pandas as pd
file_path = "prova terna (1).xlsx"
df = pd.read_excel(file_path, sheet_name='Foglio1')
print(df[['REGIONE', 'data']].to_string())


```

```text
                   REGIONE       data
0                  ABRUZZO 2026-08-01
1               BASILICATA 2026-08-01
2                 CALABRIA 2026-08-01
3                 CAMPANIA 2026-08-01
4           EMILIA ROMAGNA 2026-08-01
5    FRIULI VENEZIA GIULIA 2026-08-01
6                    LAZIO 2026-08-01
7                  LIGURIA 2026-08-01
8                LOMBARDIA 2026-08-01
9                   MARCHE 2026-08-01
10                  MOLISE 2026-08-01
11                PIEMONTE 2026-08-01
12                  PUGLIA 2026-08-01
13                SARDEGNA 2026-08-01
14                 SICILIA 2026-08-01
15                 TOSCANA 2026-08-01
16     TRENTINO ALTO ADIGE 2026-08-01
17                  UMBRIA 2026-08-01
18           VALLE D'AOSTA 2026-08-01
19                  VENETO 2026-08-01
20                     NaN        NaT
21                 ABRUZZO 2026-07-01
22              BASILICATA 2026-07-01
23                CALABRIA 2026-07-01
24                CAMPANIA 2026-07-01
25          EMILIA ROMAGNA 2026-07-01
26   FRIULI VENEZIA GIULIA 2026-07-01
27                   LAZIO 2026-07-01
28                 LIGURIA 2026-07-01
29               LOMBARDIA 2026-07-01
30                  MARCHE 2026-07-01
31                  MOLISE 2026-07-01
32                PIEMONTE 2026-07-01
33                  PUGLIA 2026-07-01
34                SARDEGNA 2026-07-01
35                 SICILIA 2026-07-01
36                 TOSCANA 2026-07-01
37     TRENTINO ALTO ADIGE 2026-07-01
38                  UMBRIA 2026-07-01
39           VALLE D'AOSTA 2026-07-01
40                  VENETO 2026-07-01
41                     NaN        NaT
42                 ABRUZZO 2026-05-01
43              BASILICATA 2026-05-01
44                CALABRIA 2026-05-01
45                CAMPANIA 2026-05-01
46          EMILIA ROMAGNA 2026-05-01
47   FRIULI VENEZIA GIULIA 2026-05-01
48                   LAZIO 2026-05-01
49                 LIGURIA 2026-05-01
50               LOMBARDIA 2026-05-01
51                  MARCHE 2026-05-01
52                  MOLISE 2026-05-01
53                PIEMONTE 2026-05-01
54                  PUGLIA 2026-05-01
55                SARDEGNA 2026-05-01
56                 SICILIA 2026-05-01
57                 TOSCANA 2026-05-01
58     TRENTINO ALTO ADIGE 2026-05-01
59                  UMBRIA 2026-05-01
60           VALLE D'AOSTA 2026-05-01
61                  VENETO 2026-05-01
62                 ABRUZZO 2026-04-01
63              BASILICATA 2026-04-01
64                CALABRIA 2026-04-01
65                CAMPANIA 2026-04-01
66          EMILIA ROMAGNA 2026-04-01
67   FRIULI VENEZIA GIULIA 2026-04-01
68                   LAZIO 2026-04-01
69                 LIGURIA 2026-04-01
70               LOMBARDIA 2026-04-01
71                  MARCHE 2026-04-01
72                  MOLISE 2026-04-01
73                PIEMONTE 2026-04-01
74                  PUGLIA 2026-04-01
75                SARDEGNA 2026-04-01
76                 SICILIA 2026-04-01
77                 TOSCANA 2026-04-01
78     TRENTINO ALTO ADIGE 2026-04-01
79                  UMBRIA 2026-04-01
80           VALLE D'AOSTA 2026-04-01
81                  VENETO 2026-04-01
82                 ABRUZZO 2026-03-01
83              BASILICATA 2026-03-01
84                CALABRIA 2026-03-01
85                CAMPANIA 2026-03-01
86          EMILIA ROMAGNA 2026-03-01
87                  FRIULI 2026-03-01
88                   LAZIO 2026-03-01
89                 LIGURIA 2026-03-01
90               LOMBARDIA 2026-03-01
91                  MARCHE 2026-03-01
92                  MOLISE 2026-03-01
93                PIEMONTE 2026-03-01
94                  PUGLIA 2026-03-01
95                SARDEGNA 2026-03-01
96                 SICILIA 2026-03-01
97                 TOSCANA 2026-03-01
98     TRENTINO ALTO ADIGE 2026-03-01
99                  UMBRIA 2026-03-01
100          VALLE D'AOSTA 2026-03-01
101                 VENETO 2026-03-01
102                ABRUZZO 2026-02-01
103             BASILICATA 2026-02-01
104               CALABRIA 2026-02-01
105               CAMPANIA 2026-02-01
106         EMILIA ROMAGNA 2026-02-01
107                 FRIULI 2026-02-01
108                  LAZIO 2026-02-01
109                LIGURIA 2026-02-01
110              LOMBARDIA 2026-02-01
111                 MARCHE 2026-02-01
112                 MOLISE 2026-02-01
113               PIEMONTE 2026-02-01
114                 PUGLIA 2026-02-01
115               SARDEGNA 2026-02-01
116                SICILIA 2026-02-01
117                TOSCANA 2026-02-01
118    TRENTINO ALTO ADIGE 2026-02-01
119                 UMBRIA 2026-02-01
120          VALLE D'AOSTA 2026-02-01
121                 VENETO 2026-02-01
122                    NaN        NaT
123                ABRUZZO 2025-12-01
124             BASILICATA 2025-12-01
125               CALABRIA 2025-12-01
126               CAMPANIA 2025-12-01
127         EMILIA ROMAGNA 2025-12-01
128  FRIULI VENEZIA GIULIA 2025-12-01
129                  LAZIO 2025-12-01
130                LIGURIA 2025-12-01
131              LOMBARDIA 2025-12-01
132                 MARCHE 2025-12-01
133                 MOLISE 2025-12-01
134               PIEMONTE 2025-12-01
135                 PUGLIA 2025-12-01
136               SARDEGNA 2025-12-01
137                SICILIA 2025-12-01
138                TOSCANA 2025-12-01
139    TRENTINO ALTO ADIGE 2025-12-01
140                 UMBRIA 2025-12-01
141          VALLE D'AOSTA 2025-12-01
142                 VENETO 2025-12-01
143                ABRUZZO 2025-11-01
144             BASILICATA 2025-11-01
145               CALABRIA 2025-11-01
146               CAMPANIA 2025-11-01
147         EMILIA ROMAGNA 2025-11-01
148  FRIULI VENEZIA GIULIA 2025-11-01
149                  LAZIO 2025-11-01
150                LIGURIA 2025-11-01
151              LOMBARDIA 2025-11-01
152                 MARCHE 2025-11-01
153                 MOLISE 2025-11-01
154               PIEMONTE 2025-11-01
155                 PUGLIA 2025-11-01
156               SARDEGNA 2025-11-01
157                SICILIA 2025-11-01
158                TOSCANA 2025-11-01
159    TRENTINO ALTO ADIGE 2025-11-01
160                 UMBRIA 2025-11-01
161          VALLE D'AOSTA 2025-11-01
162                 VENETO 2025-11-01
163                ABRUZZO 2025-10-01
164             BASILICATA 2025-10-01
165               CALABRIA 2025-10-01
166               CAMPANIA 2025-10-01
167         EMILIA ROMAGNA 2025-10-01
168  FRIULI VENEZIA GIULIA 2025-10-01
169                  LAZIO 2025-10-01
170                LIGURIA 2025-10-01
171              LOMBARDIA 2025-10-01
172                 MARCHE 2025-10-01
173                 MOLISE 2025-10-01
174               PIEMONTE 2025-10-01
175                 PUGLIA 2025-10-01
176               SARDEGNA 2025-10-01
177                SICILIA 2025-10-01
178                TOSCANA 2025-10-01
179    TRENTINO ALTO ADIGE 2025-10-01
180                 UMBRIA 2025-10-01
181          VALLE D'AOSTA 2025-10-01
182                 VENETO 2025-10-01
183                ABRUZZO 2025-09-01
184             BASILICATA 2025-09-01
185               CALABRIA 2025-09-01
186               CAMPANIA 2025-09-01
187         EMILIA ROMAGNA 2025-09-01
188  FRIULI VENEZIA GIULIA 2025-09-01
189                  LAZIO 2025-09-01
190                LIGURIA 2025-09-01
191              LOMBARDIA 2025-09-01
192                 MARCHE 2025-09-01
193                 MOLISE 2025-09-01
194               PIEMONTE 2025-09-01
195                 PUGLIA 2025-09-01
196               SARDEGNA 2025-09-01
197                SICILIA 2025-09-01
198                TOSCANA 2025-09-01
199    TRENTINO ALTO ADIGE 2025-09-01
200                 UMBRIA 2025-09-01
201          VALLE D'AOSTA 2025-09-01
202                 VENETO 2025-09-01
203                ABRUZZO 2025-08-01
204             BASILICATA 2025-08-01
205               CALABRIA 2025-08-01
206               CAMPANIA 2025-08-01
207         EMILIA ROMAGNA 2025-08-01
208  FRIULI VENEZIA GIULIA 2025-08-01
209                  LAZIO 2025-08-01
210                LIGURIA 2025-08-01
211              LOMBARDIA 2025-08-01
212                 MARCHE 2025-08-01
213                 MOLISE 2025-08-01
214               PIEMONTE 2025-08-01
215                 PUGLIA 2025-08-01
216               SARDEGNA 2025-08-01
217                SICILIA 2025-08-01
218                TOSCANA 2025-08-01
219    TRENTINO ALTO ADIGE 2025-08-01
220                 UMBRIA 2025-08-01
221          VALLE D'AOSTA 2025-08-01
222                 VENETO 2025-08-01


```

```python
import pandas as pd
file_path = "prova terna (1).xlsx"
df = pd.read_excel(file_path, sheet_name='Foglio1')
# Get the most recent date
latest_date = df['data'].max()
latest_df = df[df['data'] == latest_date].copy()
print("Latest date:", latest_date)
print(latest_df)


```

```text
Latest date: 2026-08-01 00:00:00
                  REGIONE  delta installato gen 2021 - mese riferimento (MW)  target aree idonee gen 2021 - mese riferimento (MW)  delta (MW)  target aree idonee gen 21 - dic anno riferimento (MW)       data
0                 ABRUZZO                                              650.0                                                780.0      -130.0                                                  850.0 2026-08-01
1              BASILICATA                                              729.0                                                898.0      -169.0                                                  973.0 2026-08-01
2                CALABRIA                                              627.0                                               1090.0      -463.0                                                 1206.0 2026-08-01
3                CAMPANIA                                             1653.0                                               1584.0        69.0                                                 1728.0 2026-08-01
4          EMILIA ROMAGNA                                             2333.0                                               2286.0        46.0                                                 2504.0 2026-08-01
5   FRIULI VENEZIA GIULIA                                             1028.0                                                706.0       322.0                                                  772.0 2026-08-01
6                   LAZIO                                             3078.0                                               1668.0      1410.0                                                 1829.0 2026-08-01
7                 LIGURIA                                              239.0                                                348.0      -109.0                                                  382.0 2026-08-01
8               LOMBARDIA                                             3958.0                                               3299.0       659.0                                                 3592.0 2026-08-01
9                  MARCHE                                              721.0                                                846.0      -125.0                                                  930.0 2026-08-01
10                 MOLISE                                              157.0                                                346.0      -189.0                                                  383.0 2026-08-01
11               PIEMONTE                                             2324.0                                               1882.0       442.0                                                 2053.0 2026-08-01
12                 PUGLIA                                             2651.0                                               2944.0      -293.0                                                 3213.0 2026-08-01
13               SARDEGNA                                             1340.0                                               1989.0      -649.0                                                 2207.0 2026-08-01
14                SICILIA                                             3411.0                                               3486.0       -75.0                                                 3847.0 2026-08-01
15                TOSCANA                                              995.0                                               1302.0      -308.0                                                 1444.0 2026-08-01
16    TRENTINO ALTO ADIGE                                              551.0                                                458.0        93.0                                                  497.0 2026-08-01
17                 UMBRIA                                              346.0                                                549.0      -203.0                                                  609.0 2026-08-01
18          VALLE D'AOSTA                                               41.0                                                 66.0       -24.0                                                   75.0 2026-08-01
19                 VENETO                                             2647.0                                               2285.0       362.0                                                 2483.0 2026-08-01


```

```python
import pandas as pd
file_path = "prova terna (1).xlsx"
df = pd.read_excel(file_path, sheet_name='Foglio1')
print(df.columns)
print(df['data'].nunique())
print(df.groupby('data')['delta (MW)'].sum())


```

```text
Index(['REGIONE', 'delta installato gen 2021 - mese riferimento (MW)',
       'target aree idonee gen 2021 - mese riferimento (MW)', 'delta (MW)',
       'target aree idonee gen 21 - dic anno riferimento (MW)', 'data'],
      dtype='object')
11
data
2025-08-01     848.0
2025-09-01     686.0
2025-10-01    1011.0
2025-11-01    1454.0
2025-12-01    1606.0
2026-02-01    1257.0
2026-03-01    1171.0
2026-04-01    1239.0
2026-05-01    1045.0
2026-07-01     941.0
2026-08-01     666.0
Name: delta (MW), dtype: float64


```

```python
df_clean = df.dropna(subset=['data', 'REGIONE']).copy()
print(df_clean[df_clean['REGIONE'] == 'FRIULI'])


```

```text
    REGIONE  delta installato gen 2021 - mese riferimento (MW)  target aree idonee gen 2021 - mese riferimento (MW)  delta (MW)  target aree idonee gen 21 - dic anno riferimento (MW)       data
87   FRIULI                                              944.0                                                623.0       321.0                                                  772.0 2026-03-01
107  FRIULI                                              928.0                                                606.0       322.0                                                  772.0 2026-02-01


```

```python
import pandas as pd

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

df = pd.read_excel("prova terna (1).xlsx", sheet_name='Foglio1')
df = df.dropna(subset=['data', 'REGIONE'])
df['regione'] = df['REGIONE'].apply(normalize_region)

# Merge political data
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
df_pol = pd.DataFrame(data_politica)

df = pd.merge(df, df_pol, on='regione', how='left')

def categorizza_schieramento(coalizione):
    if not isinstance(coalizione, str): return "Autonomisti"
    if "Centrodestra" in coalizione: return "Centrodestra"
    if "Centrosinistra" in coalizione: return "Centrosinistra"
    return "Autonomisti"

df["macro_area_politica"] = df["coalizione"].apply(categorizza_schieramento)

# Current data
latest_date = df['data'].max()
df_latest = df[df['data'] == latest_date].copy()
df_latest = df_latest.rename(columns={
    "delta installato gen 2021 - mese riferimento (MW)": "installato_mw",
    "target aree idonee gen 2021 - mese riferimento (MW)": "target_mw",
    "delta (MW)": "delta_mw"
})

print(df_latest[['regione', 'installato_mw', 'target_mw', 'delta_mw', 'macro_area_politica']].head())

# Historical Data aggregation
storico = df.groupby(['data', 'macro_area_politica'])['delta (MW)'].sum().reset_index()
storico_pivot = storico.pivot(index='data', columns='macro_area_politica', values='delta (MW)').reset_index()
print(storico_pivot.head())


```

```text
          regione  installato_mw  target_mw  delta_mw macro_area_politica
0         Abruzzo          650.0      780.0    -130.0        Centrodestra
1      Basilicata          729.0      898.0    -169.0        Centrodestra
2        Calabria          627.0     1090.0    -463.0        Centrodestra
3        Campania         1653.0     1584.0      69.0      Centrosinistra
4  Emilia-Romagna         2333.0     2286.0      46.0      Centrosinistra
macro_area_politica       data  Autonomisti  Centrodestra  Centrosinistra
0                   2025-08-01         -8.0        1459.0          -603.0
1                   2025-09-01         -9.0        1368.0          -673.0
2                   2025-10-01        -10.0        1696.0          -675.0
3                   2025-11-01        -11.0        2129.0          -664.0
4                   2025-12-01        -12.0        2331.0          -713.0


```

Ecco il codice aggiornato. Ho modificato lo script per **leggere dinamicamente sia i dati attuali che quelli storici direttamente dal file `prova terna (1).xlsx**`, eliminando la necessità di inserire i valori a mano e accorpando tutto in un'unica fonte dati.

Il codice pulisce automaticamente i nomi delle regioni (ad esempio gestendo l'anomalia di "FRIULI") e calcola in tempo reale sia la mappa relativa all'ultimo mese disponibile, sia il grafico di andamento storico raggruppato per coalizione.

```python
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
        df = pd.read_excel("prova terna (1).xlsx", sheet_name='Foglio1')
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

```
