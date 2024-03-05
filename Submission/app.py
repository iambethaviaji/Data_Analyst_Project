import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Change seaborn style
sns.set(style='dark')

#Importing data
all_data = pd.read_csv('all_data = pd.read_csv('https://raw.githubusercontent.com/iambethaviaji/Data_Analyst_Project/main/Submission/main_data.csv')
')

datetime_columns = ['date']
all_data.sort_values(by='date', inplace=True)
all_data.reset_index(inplace=True)
 
for column in datetime_columns:
    all_data[column] = pd.to_datetime(all_data[column])

#Prepare dataframe that needed
def create_month_recap(df):
    plot_month = df['month'].astype(str)
    plot_year = df['year'].astype(str)
    df['year_month'] = plot_month + ' ' + plot_year
    df['total_sum'] = df.groupby('year_month')['total'].transform('sum')
    return df[['year_month', 'total_sum']]

def create_season_recap(df):
    season_recap = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_recap

def create_weather_recap(df):
    weather_recap = df.groupby(by='weather').agg({
    'total': 'mean'
    }).reset_index()
    return weather_recap

#Create side bar filter
max_date = pd.to_datetime(all_data['date']).dt.date.max()
min_date = pd.to_datetime(all_data['date']).dt.date.min()

with st.sidebar:

    #input start_date dan end_date
    start_date, end_date = st.date_input(
        label='Select a Time Range',
        max_value=max_date,
        min_value=min_date,
        value=[min_date, max_date]
    )
    if st.checkbox("Display Dataset"):
        st.subheader("Dataset")
        st.write(all_data)
    
    st.write(
        """ 
        **Andrian Satrio Bethaviaji**\n
        Dicoding ID: **andrian_s_bethaviaji**\n
        Email: **m258d4ky1987@bangkit.academy**
        """
    )

main_df = all_data[(all_data['date'] >= str(start_date)) & 
                (all_data['date'] <= str(end_date))]

month_recap_df = create_month_recap(main_df)
season_recap_df = create_season_recap(main_df)
weather_recap_df = create_weather_recap(main_df)

# Creating UI display
st.header('GOWES BIKE RENT ANALYTICS DASHBOARD')

st.subheader('Relationship Between Weather Conditions and the Number of Bicycle Rentals per Hour')
plt.figure(figsize=(10, 6))
sns.set(style='whitegrid')
sns.lineplot(
    data=main_df,  # Menggunakan main_df yang sudah difilter berdasarkan rentang tanggal yang dipilih
    x='temp',  # Menggunakan suhu sebagai sumbu x
    y='total',  # Menggunakan jumlah sewa sepeda sebagai sumbu y
    marker='o'
)
plt.title("Relationship Between Weather Conditions and the Number of Bicycle Rentals per Hour")
plt.xlabel("Suhu (°C)")
plt.ylabel("Jumlah Sewa Sepeda")

# Get the current figure
fig = plt.gcf()

# Displaying the plot using Streamlit
st.pyplot(fig)

# Subheader Performance Graph
st.subheader('Bike Rental Performance Graph')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    month_recap_df['year_month'],
    month_recap_df['total_sum'],
    marker='o',
    linewidth=5,
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation=45)

# Get the current figure
fig = plt.gcf()

# Displaying the plot using Streamlit
st.pyplot(fig)

# Subheader Season and Weather Recap
st.subheader('Recap Based on Season and Weather')

# Create a subplot with a figure size of 20x10
fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    y='registered',
    x='season',
    data=season_recap_df.sort_values(by='registered', ascending=False),
    color='tab:green',
    label='Registered User',
    ax=ax
)

sns.barplot(
    y='casual',
    x='season',
    data=season_recap_df.sort_values(by='casual', ascending=False),
    color='tab:blue',
    label='Casual User',
    ax=ax
)

ax.set_title('Number of Rent by Season and Weather', loc='center', fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
ax.legend(fontsize=20)

# Get the current figure
fig = plt.gcf()

# Displaying the plot using Streamlit
st.pyplot(fig)
