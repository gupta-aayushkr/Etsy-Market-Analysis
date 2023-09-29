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

#Data Visulisation (Column Wise)
# plt.clf()
# st.header("Correlation Matrix")
# filtered_df = df.iloc[:, -7:]
# correlation_matrix = filtered_df.corr()
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
# plt.title("Correlation Matrix Heatmap")
# st.pyplot(plt)

#Listings
st.header("Shop with Most Listings")
fig = px.bar(df.ShopName.value_counts().head(20))
st.plotly_chart(fig)

#Wordcloud
st.header("WordCloud")
text_data = df['Listing'].str.cat(sep=' ')
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)


#Revenue Vs Listing Age
st.header("Most Revenue Vs Listing Age")
days = st.number_input("Enter Age of Listing", format='%d',value=30)
st.write(f"Most Revenue by Listings Under {days} Days")
listing_byage = df[(df["Listing Age (Days)"] < days) & (df["Est. Revenue"] > 0)]
result = listing_byage.groupby('Listing')['Est. Revenue'].sum().sort_values(ascending=False).head(10)
st.dataframe(result, width=1000)


# Listing Age
st.header("Listing Age")
plt.clf()
Listing_age = df["Listing Age (Days)"]
Listing_age_plot = plt.hist(Listing_age, color='blue', edgecolor='white', alpha=0.7)
for i in range(len(Listing_age_plot[0])):
        plt.text(Listing_age_plot[1][i] + 5, Listing_age_plot[0][i] + .2, str(Listing_age_plot[0][i]))
plt.xlabel("Listing Age")
plt.ylabel("Shops")
st.pyplot(plt) 

st.write("Old Listing")
old_listing = Listing_age.sort_values().tail(10).values
st.dataframe(df[df["Listing Age (Days)"].isin(old_listing)],width=1000)
st.write("New Listing")
new_listing = Listing_age.sort_values().head(10).values
df[df["Listing Age (Days)"].isin(new_listing)]

#Total Views
st.header("Total Views")
total_views = df['Total Views']
plt.clf()
plt.hist(total_views, color='blue', edgecolor='white', alpha=0.7)
st.pyplot(plt)
most_views = total_views.sort_values().tail(5).values
least_views = total_views.sort_values().head(5).values
st.write("Most Views")
st.dataframe(df[df["Total Views"].isin(most_views)], width=1000)
st.write("Least Views")
st.dataframe(df[df["Total Views"].isin(least_views)], width=1000)

plt.clf()

st.subheader("Total View Metic Comparison")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
ax1.scatter(df["Total Views"], df["Est. Sales"])
ax1.set_xlabel("Total Views")
ax1.set_ylabel("Est. Sales")
ax1.set_title("Total Views vs. Est. Sales")

ax2.scatter(df["Total Views"], df["Daily Views"])
ax2.set_xlabel("Total Views")
ax2.set_ylabel("Daily Views")
ax2.set_title("Total Views vs. Daily Views")

ax3.scatter(df["Total Views"], df["Est. Revenue"])
ax3.set_xlabel("Total Views")
ax3.set_ylabel("Est. Revenue")
ax3.set_title("Total Views vs. Est. Revenue")

ax4.scatter(df["Total Views"], df["Hearts"])
ax4.set_xlabel("Total Views")
ax4.set_ylabel("Hearts")
ax4.set_title("Total Views vs. Hearts")
plt.tight_layout()
st.pyplot(plt)

#Daily Views
plt.clf()
st.header("Daily Views")
daily_views = df["Daily Views"]
daily_views.plot(kind='hist',edgecolor='black', color='green', alpha=.5, hatch='//')
plt.xlabel("Daily Views")
st.pyplot(plt)

filtered_df = df.iloc[:,-7:]

#Sales
st.header('Sales Estimates')
sales = df["Est. Sales"]
plt.clf()
sales_plot = plt.hist(sales, edgecolor='black', color='green', alpha=.5,hatch='//' )
plt.xticks(range(0, max(sales), max(sales) // 10))
for i in range(len(sales_plot[0])):
        if sales_plot[0][i] != 0:
                plt.text(sales_plot[1][i]+6,sales_plot[0][i]+1,str(sales_plot[0][i]))
plt.xlabel("Est. Sales")
plt.ylabel("Shops")
st.pyplot(plt)

st.write('Shops with Most Sales')
most_sales = df.groupby('ShopName')["Est. Sales"].sum().sort_values(ascending=False).reset_index().head(5)
st.dataframe(most_sales, width=1000)

#Price
st.header("Price Comparison")
price = df["Price"]
plt.clf()
price_plot = plt.hist(price, color='green', edgecolor='black', alpha=0.5)
plt.xticks(range(0, int(max(price+1)), int(max(price+1)) // 10))
for i in range(0, len(price_plot[0])):
        plt.text(price_plot[1][i]+1,price_plot[0][i]+.5,str(int(price_plot[0][i])))
plt.xlabel("Price")
plt.ylabel("Shop Count")
st.pyplot(plt)

price1 = df.groupby("Listing")[["Price","Est. Sales","Listing Age (Days)"]].mean().sort_values(by='Price',ascending=False).reset_index().head(5)
st.write("Most Priced Listings")
st.dataframe(price1, width=1000)

#Revenue
st.header("Revenue Performance")
revenue = df.groupby('ShopName')['Est. Revenue'].sum().sort_values(ascending=False).head(10)
st.write("Shops with Most Revenue")
plt.clf()
revenue.plot(kind='bar',color='green', edgecolor='black', alpha=0.5)
plt.xlabel('ShopName')
plt.ylabel('Total Revenue')
plt.title('Top 5 Shops by Total Revenue')
st.pyplot(plt)

