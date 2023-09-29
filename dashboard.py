import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
import os

st.title("Etsy Marketplace Analysis App")
#For custom files
file1 = st.file_uploader("Upload a CSV file", type=["csv"])

#For Files in dataset
csv_files = []
if file1 is None:
        csv_folder_path = "CSV_Files"
        csv_files = []
        for file in os.listdir(csv_folder_path):
                if file.endswith(".csv"):
                        csv_files.append(file)
        selected_csv = st.selectbox("Select a CSV file", csv_files)
        data = pd.read_csv(os.path.join(csv_folder_path, selected_csv))
else:
        data = pd.read_csv(file1)

#data cleaning
columns_to_keep = ['bold','bold 2']
last_7_cols = data.columns[-7:].tolist()
df = data[columns_to_keep+last_7_cols].copy()
new_column_names = {
        df.columns[0]: 'ShopName',
        df.columns[1]: 'Listing',
        df.columns[-7]: 'Listing Age (Days)',
        df.columns[-6]: 'Total Views',
        df.columns[-5]: 'Daily Views',
        df.columns[-4]: 'Est. Sales',
        df.columns[-3]: 'Price',
        df.columns[-2]: 'Est. Revenue',
        df.columns[-1]: 'Hearts'
}
df.rename(columns=new_column_names, inplace=True)
for i in range(2,9):
        if type(df[df.columns[i]][0]) == str:
                df[df.columns[i]] = df[df.columns[i]].str.replace('[\$,]', '', regex=True)
                df[df.columns[i]] = df[df.columns[i]].astype(float)

filtered_df = df.iloc[:,-7:]

