import streamlit as st
from plotly import graph_objs as go
from plotly.offline import init_notebook_mode
import pandas as pd
import plotly.express as px
from PIL import Image
import time
init_notebook_mode(connected=True)

st.title("Analisis Keadaan Kecelakaan Di Amerika Serikat Tahun 2016")
with st.spinner("Mohon Untuk Menunggu"):
    time.sleep(5)

st.header("Identifikasi Masalah")
gambar = Image.open("Diagram Fish Bone Milestone 1 New.jpg")
st.image(gambar)

data_mentah = pd.read_csv("h8dsft_milestone1_dataset_mnfakhri.csv")
data_mentah.sort_values(by="state_number",inplace=True)
data_mentah.reset_index(drop=True,inplace=True)
data_mentah.rename(columns={"state_number":"State Number","state_name":"State Name","latitude":"Latitude",
                            "longitude":"Longitude","relation_to_junction_specific_location_name":"Junction Location",
                            "relation_to_trafficway_name":"Trafficway Location","light_condition_name":"Light Condition",
                            "atmospheric_conditions_1_name":"Atmosphere Condition 1",
                            "atmospheric_conditions_2_name":"Atmosphere Condition 2",
                            "atmospheric_conditions_name":"Atmosphere Conditions",
                            "number_of_fatalities":"Amount Of Fatality",
                            "number_of_drunk_drivers":"Amount Of Drunk Drivers"},inplace=True)

list_state_name = data_mentah["State Name"].unique()
list_junction = data_mentah["Junction Location"].unique()
list_trafficway = data_mentah["Trafficway Location"].unique()
list_light_condition = data_mentah["Light Condition"].unique()
list_atmo_con = data_mentah["Atmosphere Conditions"].unique()
list_atmo_con1 = data_mentah["Atmosphere Condition 1"].unique()
list_atmo_con2 = data_mentah["Atmosphere Condition 2"].unique()
data_fatal = data_mentah["Amount Of Fatality"]
data_drunks = data_mentah["Amount Of Drunk Drivers"]

def buat_grafik(i,j):
    colours = ['#00FFFF', '#7FFFD4', '#000000', '#0000FF', '#8A2BE2', '#A52A2A', '#DEB887', '#5F9EA0', '#7FFF00', '#D2691E',
                '#FF7F50', '#6495ED', '#DC143C', '#00FFFF', '#00008B', '#008B8B', '#B8860B', '#A9A9A9', '#006400', '#BDB76B',
                '#8B008B', '#556B2F', '#FF8C00', '#9932CC', '#8B0000', '#E9967A', '#8FBC8F', '#483D8B', '#2F4F4F', '#00CED1',
                '#9400D3', '#FF1493', '#00BFFF', '#696969', '#1E90FF', '#B22222', '#228B22', '#FF00FF', '#FFD700', '#DAA520',
                '#808080', '#008000', '#ADFF2F', '#FF69B4', '#CD5C5C', '#4B0082', '#F0E68C', '#7CFC00', '#ADD8E6', '#F08080',
                '#90EE90', '#FFB6C1', '#FFA07A', '#20B2AA', '#87CEFA', '#778899', '#B0C4DE', '#00FF00', '#32CD32', '#FF00FF',
                '#800000', '#66CDAA', '#0000CD', '#BA55D3', '#9370DB', '#3CB371', '#7B68EE', '#00FA9A', '#48D1CC', '#C71585',
                '#191970', '#FFE4B5', '#FFDEAD', '#000080', '#808000', '#6B8E23', '#FFA500', '#FF4500', '#DA70D6', '#EEE8AA',
                '#98FB98', '#AFEEEE', '#DB7093', '#CD853F', '#FFC0CB', '#DDA0DD', '#B0E0E6', '#800080', '#663399', '#FF0000',
                '#BC8F8F', '#4169E1', '#8B4513', '#FA8072', '#F4A460', '#2E8B57', '#A0522D', '#C0C0C0', '#87CEEB', '#6A5ACD',
                '#708090', '#00FF7F', '#4682B4', '#D2B48C', '#008080', '#D8BFD8', '#FF6347', '#40E0D0', '#EE82EE', '#F5DEB3',
                '#FFFF00', '#9ACD32']
    list_jumlah = []
    for a in i:
        nama = data_mentah[j] == a
        list_jumlah.append(len(data_mentah[nama]))
    grafik_bar = go.Bar(x = i,y = list_jumlah, marker=dict(color=colours[:len(list_jumlah)]))
    layout_bar = go.Layout(title=f"<b>Amount Of Accident Based On {j}</b>",height=650,margin=go.layout.Margin())
    data = [grafik_bar]
    figure = go.Figure(data=data, layout=layout_bar)
    st.plotly_chart(figure)

st.header("Grafik Jumlah Kecelakaan Berdasarkan Negara Bagian")
buat_grafik(list_state_name,"State Name")

st.header("Grafik Jumlah Kecelakaan Berdasarkan Letak Persimpangan")
buat_grafik(list_junction,"Junction Location")

st.header("Grafik Jumlah Kecelakaan Berdasarkan Lokasi Lalu Lintas")
buat_grafik(list_trafficway,"Trafficway Location")

st.header("Grafik Jumlah Kecelakaan Berdasarkan Kondisi Pencahayaan")
buat_grafik(list_light_condition,"Light Condition")

list_cuaca = ["Atmosphere Condition","Atmosphere Condition 1","Atmosphere Condition 2"]
st.header("Grafik Jumlah Kecelakaan Berdasarkan Kondisi Cuaca")
pilihan = st.selectbox("Pilih grafik yang ingin anda tampilkan",list_cuaca)
if pilihan == "Atmosphere Condition":
    buat_grafik(list_atmo_con,"Atmosphere Conditions")
elif pilihan == "Atmosphere Condition 1":
    buat_grafik(list_atmo_con1,"Atmosphere Condition 1")
else:
    buat_grafik(list_atmo_con2,"Atmosphere Condition 2")

st.header("Peta Persebaran Lokasi Kecelakaan")
fig = px.scatter_mapbox(data_mentah,lat="Latitude",lon="Longitude",hover_name="State Number",
                        hover_data=["State Name","Amount Of Fatality"],color_discrete_sequence=["red"],zoom=3,
                        height=500)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)

list_orang = ["Jumlah Kecelakaan Fatal","Jumlah Pengendara Dalam Pengaruh Miras"]
st.header("Grafik Jumlah Kecelakaan Fatal Dan Pengendara Dalam Pengaruh Miras")
tombol = st.radio("Pilih Untuk Menampilkan Grafik",list_orang)
if tombol == "Jumlah Kecelakaan Fatal":
    st.header("Grafik Jumlah Korban Kecelakaan Fatal")
    histo_fatal = px.histogram(data_fatal,x="Amount Of Fatality")
    st.plotly_chart(histo_fatal)
else:
    st.header("Grafik Jumlah Pengemudi Dalam Pengaruh Miras")
    histo_drunks = px.histogram(data_drunks,x="Amount Of Drunk Drivers")
    st.plotly_chart(histo_drunks)

st.header("Analisis Data")
st.write("- Kecelakaan terbanyak terjadi di daerah amerika serikat bagian timur, sedangkan untuk daerah amerika serikat bagian barat tengah cenderung lebih sedikit.")
st.write("- Rata-rata kecelakaan fatal itu tidak sama dengan rata-rata jumlah pengemudi yang terpengaruh minuman keras")
st.write("- Jumlah Kecelakaan fatal tidak ada keterkaitan dengan Jumlah Pengemudi yang terpengaruh minuman keras")

st.header("Kesimpulan")
st.write("Maka Kebijakan yang perlu dibuat Kementrian Perhubungan adalah membuat aturan berkendara yang baru untuk negara bagian timur amerika serikat mengenai:")
st.write("- Berkendara di area non junction")
st.write("- Berkendara di area roadway")
st.write("- Berkendara di waktu daylight")
st.write("- Berkendara di cuaca clear")
st.write("- Membuat program razia rutin untuk mencegah pengemudi yang terpengaruh minuman keras")

