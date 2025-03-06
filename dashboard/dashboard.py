import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_daily_rentals_df(df):
    daily_rentals_df = df.resample(rule='D', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })
    daily_rentals_df = daily_rentals_df.reset_index()
    daily_rentals_df.rename(columns={
        "registered": "total_registered",
        "casual": "total_casual",
        "cnt": "total_customer"
    }, inplace=True)
    
    return daily_rentals_df

def create_monthly_rentals_df(df):
    monthly_rentals_df = df.resample(rule='M', on='dteday').agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    })
    monthly_rentals_df = monthly_rentals_df.reset_index()
    monthly_rentals_df.rename(columns={
        "registered": "total_registered",
        "casual": "total_casual",
        "cnt": "total_customer"
    }, inplace=True)
    
    return monthly_rentals_df

def create_byseasons_df(df):
    byseason_df = df.groupby("season")["cnt"].mean().round(2).reset_index()
    byseason_df.rename(columns={"cnt": "total_customer"}, inplace=True)
    return byseason_df

def create_byweather_df(df):
    byweather_df = df.groupby("weathersit")["cnt"].mean().round(2).reset_index()
    byweather_df.rename(columns={"cnt": "total_customer"}, inplace=True)
    return byweather_df

all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
all_df['year'] = all_df['dteday'].dt.year

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("logo.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]


daily_rentals_df = create_daily_rentals_df(main_df)
monthly_rentals_df = create_monthly_rentals_df(main_df)
byseason_df = create_byseasons_df(main_df)
byweather_df = create_byweather_df(main_df)

st.header('Bike Rent Dashboard')

st.subheader('Peminjam Harian')
 
col1, col2, col3 = st.columns(3)
 
with col1:
    total_rentals = daily_rentals_df.total_customer.sum()
    st.metric("Total Peminjam", value=total_rentals)
 
with col2:
    total_registered = daily_rentals_df.total_registered.sum()
    st.metric("Total Pengguna Terdaftar", value=total_registered)

with col3:
    total_casual = daily_rentals_df.total_casual.sum()
    st.metric("Total Pengguna Casual", value=total_casual)

st.subheader('Laporan Peminjaman Bulanan')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_rentals_df["dteday"],
    monthly_rentals_df["total_customer"],
    marker='o', 
    linewidth=2,
    label='Total Peminjam',
    color="orangered"
)
ax.set_xlabel("Tanggal", fontsize=15)
ax.set_ylabel("Jumlah Peminjam", fontsize=15)
ax.set_title("Laporan Bulanan (Total Peminjam)", fontsize=20)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True)
ax.legend()

st.pyplot(fig)

season_colors = {
    'Musim Dingin': 'lightskyblue',
    'Musim Semi': 'lightgreen',
    'Musim Panas': 'gold',
    'Musim Gugur': 'lightcoral'
}

weather_colors = {
    "Mendung": "lightskyblue", 
    "Cerah": "gold", 
    "Salju Ringan/Hujan": "grey",
}

st.subheader("Pengaruh Musim dan Cuaca terhadap Rata-Rata Peminjaman Sepeda")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(30,15))
    sorted_byseason_df = byseason_df.sort_values(by='total_customer', ascending=False)
    sns.barplot(
        y='total_customer', 
        x='season',
        data=sorted_byseason_df,
        palette=season_colors,
        ax=ax
    )
    ax.set_title("Rata-Rata Peminjaman Berdasarkan Musim", loc="center", fontsize=50, pad=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.2f}',
                    (p.get_x() + p.get_width() / 2, height),
                    ha='center', va='bottom',
                    fontsize=35, color='black', fontweight='bold')
    
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(30,15))
    sorted_byweather_df = byweather_df.sort_values(by='total_customer', ascending=False)
    sns.barplot(
        y='total_customer', 
        x='weathersit',
        data=sorted_byweather_df,
        palette=weather_colors,
        ax=ax
    )
    ax.set_title("Rata-Rata Peminjaman Berdasarkan Cuaca", loc="center", fontsize=50, pad=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.2f}',
                    (p.get_x() + p.get_width() / 2, height),
                    ha='center', va='bottom',
                    fontsize=35, color='black', fontweight='bold')
    
    st.pyplot(fig)

st.subheader('Perbandingan Pengguna Terdaftar dan Casual per Tahun')

data_2011 = all_df[all_df['year'] == 2011]
data_2012 = all_df[all_df['year'] == 2012]

total_registered_2011 = data_2011['registered'].sum()
total_casual_2011 = data_2011['casual'].sum()

total_registered_2012 = data_2012['registered'].sum()
total_casual_2012 = data_2012['casual'].sum()

labels = ['Registered', 'Casual']
colors = ['dodgerblue', 'skyblue']

sizes_2011 = [total_registered_2011, total_casual_2011]
sizes_2012 = [total_registered_2012, total_casual_2012]

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

axes[0].pie(
    sizes_2011, 
    labels=labels, 
    autopct='%1.1f%%',
    startangle=90, 
    colors=colors, 
    shadow=False
)
axes[0].set_title('Proporsi Pengguna (2011)')
axes[0].axis('equal')

axes[1].pie(
    sizes_2012, 
    labels=labels, 
    autopct='%1.1f%%',
    startangle=90, 
    colors=colors, 
    shadow=False
)
axes[1].set_title('Proporsi Pengguna (2012)')
axes[1].axis('equal')

plt.suptitle('Perbandingan Pengguna Terdaftar vs Casual per Tahun')
plt.tight_layout()

st.pyplot(fig)


st.caption('Copyright © Rafly Herdianto 2025')