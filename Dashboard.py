import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import streamlit as st
import os

st.set_page_config(
    page_icon="🛒",
    page_title="Etsy Data Analysis",
    layout="wide",
    initial_sidebar_state="collapsed")

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


#-----------------------------SECTION 1-----------------------------------#

c1,c2 = st.columns(2)
c1.title("Etsy data analysis")
c1.info('''
Information
''')

#For Informatin

# Create a nested column layout within c1
nested_c1_left, nested_c1_right = c1.columns(2)
nested_c1_left.metric("Total Listing", len(df))
nested_c1_left.metric("Average Price ($)", round(df["Price"].mean(), 2))
nested_c1_left.metric("Average Revenue ($)", round(df["Est. Revenue"].mean(), 2))

# right metric
nested_c1_right.metric("Average Sales ($)", df["Est. Sales"].mean())
nested_c1_right.metric("Average Heart", df["Hearts"].mean())
nested_c1_right.metric("Average Views", df["Total Views"].mean())

# nested_c1_right.metric("New Metric 2", value_of_metric_2)

c2.header("All Listing Data")
c2.dataframe(df, width=1000)


#------------------------------SECTION 2---------------------------------#

c1, c2= st.columns(2)
c1.header("WordCloud")
text_data = df['Listing'].str.cat(sep=' ')
wordcloud = WordCloud(width=800, height=600, background_color='white').generate(text_data)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
fig = plt.gcf()
c1.pyplot(plt)


word_frequencies = wordcloud.words_
c2.subheader("Word Frequencies in Listings")
df2 = pd.DataFrame(word_frequencies.items())
df2.rename(columns={0:'Word',1:'Freq%'}, inplace=True)
df2['Freq%'] = round(df2['Freq%'] * 100,2)
c2.dataframe(df2, width=1000, height=500)



#----------------------------SECTION 3-----------------------------------#

metric_col = [
    'Listing Age (Days)',
    'Total Views',
    'Daily Views',
    'Est. Sales',
    'Price',
    'Est. Revenue',
    'Hearts']

st.header("Top Shops Vs Metric")
c1, c2 = st.columns(2)
nested_c1_left, nested_c1_right = c1.columns(2)
Metric = nested_c1_left.selectbox('Select Metric', metric_col, help="Select Metric from this list")
Days = nested_c1_right.number_input("Under (Days)",format='%d',value=365)
top_shops = df[df["Listing Age (Days)"] < Days].groupby("ShopName")[Metric].sum().sort_values(ascending=False).head(10).reset_index()
fig = px.bar(top_shops, x='ShopName',y=Metric,labels={'x':'ShopName','y':'Metric'},title=f'Top 5 Shops with Highest {Metric}', width=600)
fig.update_traces(marker=dict(color='#ff4b4b'))
c1.plotly_chart(fig)

c2.header(f"Listings with Highest {Metric}")
top_shops = df[df["Listing Age (Days)"] < Days].groupby("ShopName")[["Listing",Metric]].sum().sort_values(by=Metric, ascending=False).head(15).reset_index()
c2.dataframe(top_shops, width=1000, height=400)