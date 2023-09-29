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


#Coplete dataframe
st.header("Etsy Marketplace Listings Data")
st.dataframe(df, width=1000)

#Listings
st.header("Shops with Most Listings")
fig = px.bar(df.ShopName.value_counts().head(20))
st.plotly_chart(fig)

# Data Visulisation (Column Wise)
plt.clf()
st.header("Correlation Matrix")
filtered_df = df.iloc[:, -7:]
correlation_matrix = filtered_df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
plt.title("Correlation Matrix Heatmap")
st.pyplot(plt)

#Wordcloud
st.header("WordCloud")
text_data = df['Listing'].str.cat(sep=' ')
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
st.pyplot(plt)

word_frequencies = wordcloud.words_

st.write("Word Frequencies in Listings")
df2 = pd.DataFrame(word_frequencies.items())
df2.rename(columns={0:'Word',1:'Freq%'}, inplace=True)
df2['Freq%'] = round(df2['Freq%'] * 100,2)
st.dataframe(df2, width=1000)

#Revenue Vs Listing Age
st.header("Most Revenue Vs Listing Age")
days = st.number_input("Enter Age of Listing", format='%d',value=30)
st.write(f"Most Revenue by Listings Under {days} Days")
listing_byage = df[(df["Listing Age (Days)"] < days) & (df["Est. Revenue"] > 0)]
result = listing_byage.groupby('Listing')['Est. Revenue'].sum().sort_values(ascending=False).head(10)
st.dataframe(result, width=1000)


# Listing Age & Revenue
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
old_listing = df[["Listing","Listing Age (Days)","Est. Revenue"]].sort_values(by="Listing Age (Days)", ascending=False).head(10)
st.dataframe(old_listing,width=1000)
st.write("New Listing")
new_listing = df[["Listing","Listing Age (Days)","Est. Revenue"]].sort_values(by="Listing Age (Days)").head(10)
st.dataframe(new_listing, width=1000)

plt.clf()

#---------
plt.clf()
st.write("Correlation of Columns with Listing Age (Days)")
correlations = filtered_df.corr()["Listing Age (Days)"].sort_values(ascending=False)
plt.bar(correlations.index, correlations.values)
st.pyplot(plt)

plt.clf()
st.subheader("Listing Age (Days) Metric Comparison")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
ax1.scatter(df["Listing Age (Days)"], df["Est. Sales"])
ax1.set_xlabel("Listing Age (Days)")
ax1.set_ylabel("Est. Sales")
ax1.set_title("Listing Age (Days) vs. Est. Sales")

ax2.scatter(df["Listing Age (Days)"], df["Daily Views"])
ax2.set_xlabel("Listing Age (Days)")
ax2.set_ylabel("Daily Views")
ax2.set_title("Listing Age (Days) vs. Daily Views")

ax3.scatter(df["Listing Age (Days)"], df["Est. Revenue"])
ax3.set_xlabel("Listing Age (Days)")
ax3.set_ylabel("Est. Revenue")
ax3.set_title("Listing Age (Days) vs. Est. Revenue")

ax4.scatter(df["Listing Age (Days)"], df["Hearts"])
ax4.set_xlabel("Listing Age (Days)")
ax4.set_ylabel("Hearts")
ax4.set_title("Listing Age (Days) vs. Hearts")
plt.tight_layout()
st.pyplot(plt)
#---------


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

#---------
plt.clf()
st.write("Correlation of Columns with Total Views")
correlations = filtered_df.corr()["Total Views"].sort_values(ascending=False)
plt.bar(correlations.index, correlations.values)
st.pyplot(plt)

plt.clf()
st.subheader("Total Views Metric Comparison")
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
#---------


#Daily Views
plt.clf()
st.header("Daily Views")
daily_views = df["Daily Views"]
daily_views.plot(kind='hist',edgecolor='black', color='green', alpha=.5, hatch='//')
plt.xlabel("Daily Views")
st.pyplot(plt)
most_views2 = daily_views.sort_values().tail(5).values
least_views2 = daily_views.sort_values().head(5).values
st.write("Most Daily Views")
st.dataframe(df[df["Daily Views"].isin(most_views2)], width=1000)
st.write("Least Daily Views")
st.dataframe(df[df["Daily Views"].isin(least_views2)], width=1000)

#---------
plt.clf()
st.write("Correlation of Columns with Daily Views")
correlations = filtered_df.corr()["Daily Views"].sort_values(ascending=False)
plt.bar(correlations.index, correlations.values)
st.pyplot(plt)

plt.clf()
st.subheader("Daily Views Metric Comparison")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
ax1.scatter(df["Daily Views"], df["Est. Sales"])
ax1.set_xlabel("Daily Views")
ax1.set_ylabel("Est. Sales")
ax1.set_title("Daily Views vs. Est. Sales")

ax2.scatter(df["Daily Views"], df["Daily Views"])
ax2.set_xlabel("Daily Views")
ax2.set_ylabel("Listing Age (Days)")
ax2.set_title("Daily Views vs. Listing Age (Days)")

ax3.scatter(df["Daily Views"], df["Est. Revenue"])
ax3.set_xlabel("Daily Views")
ax3.set_ylabel("Est. Revenue")
ax3.set_title("Daily Views vs. Est. Revenue")

ax4.scatter(df["Daily Views"], df["Hearts"])
ax4.set_xlabel("Daily Views")
ax4.set_ylabel("Hearts")
ax4.set_title("Daily Views vs. Hearts")
plt.tight_layout()
st.pyplot(plt)
#---------




#Sales
st.header('Sales Estimates')
sales = df["Est. Sales"]
plt.clf()
sales_plot = plt.hist(sales, edgecolor='black', color='blue', alpha=.5,hatch='//' )
plt.xticks(range(0, max(sales), max(sales) // 10))
for i in range(len(sales_plot[0])):
        if sales_plot[0][i] != 0:
                plt.text(sales_plot[1][i]+6,sales_plot[0][i]+1,str(sales_plot[0][i]))
plt.xlabel("Est. Sales")
plt.ylabel("Shops")
st.pyplot(plt)

st.write('Shops with Most Sales')
most_sales = df.groupby('ShopName')["Est. Sales"].sum().sort_values(ascending=False).reset_index().head(10)
st.dataframe(most_sales, width=1000)

st.write('Shops with Least Sales')
least_sales = df.groupby('ShopName')["Est. Sales"].sum().sort_values(ascending=False).reset_index().tail(10)
st.dataframe(most_sales, width=1000)

#---------
plt.clf()
st.write("Correlation of Columns with Est. Sales")
correlations = filtered_df.corr()["Est. Sales"].sort_values(ascending=False)
plt.bar(correlations.index, correlations.values)
st.pyplot(plt)

plt.clf()
st.subheader("Est. Sales Metric Comparison")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
ax1.scatter(df["Est. Sales"], df["Est. Sales"])
ax1.set_xlabel("Est. Sales")
ax1.set_ylabel("Price")
ax1.set_title("Est. Sales vs. Price")

ax2.scatter(df["Est. Sales"], df["Est. Sales"])
ax2.set_xlabel("Est. Sales")
ax2.set_ylabel("Total Views")
ax2.set_title("Est. Sales vs. Total Views")

ax3.scatter(df["Est. Sales"], df["Est. Revenue"])
ax3.set_xlabel("Est. Sales")
ax3.set_ylabel("Est. Revenue")
ax3.set_title("Est. Sales vs. Est. Revenue")

ax4.scatter(df["Est. Sales"], df["Hearts"])
ax4.set_xlabel("Est. Sales")
ax4.set_ylabel("Hearts")
ax4.set_title("Est. Sales vs. Hearts")
plt.tight_layout()
st.pyplot(plt)
#---------




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

#---------
plt.clf()
st.write("Correlation of Columns with Price")
correlations = filtered_df.corr()["Price"].sort_values(ascending=False)
plt.bar(correlations.index, correlations.values)
st.pyplot(plt)

plt.clf()
st.subheader("Price Metric Comparison")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
ax1.scatter(df["Price"], df["Price"])
ax1.set_xlabel("Price")
ax1.set_ylabel("Listing Age (Days)")
ax1.set_title("Price vs. Listing Age (Days)")

ax2.scatter(df["Price"], df["Price"])
ax2.set_xlabel("Price")
ax2.set_ylabel("Price")
ax2.set_title("Price vs. Price")

ax3.scatter(df["Price"], df["Est. Revenue"])
ax3.set_xlabel("Price")
ax3.set_ylabel("Est. Revenue")
ax3.set_title("Price vs. Est. Revenue")

ax4.scatter(df["Price"], df["Hearts"])
ax4.set_xlabel("Price")
ax4.set_ylabel("Hearts")
ax4.set_title("Price vs. Hearts")
plt.tight_layout()
st.pyplot(plt)
#---------




#Revenue
st.header("Revenue Performance")
revenue = df.groupby('ShopName')['Est. Revenue'].sum().sort_values(ascending=False).head(10)
st.write("Shops with Most Revenue")
plt.clf()
revenue.plot(kind='bar',color='blue', edgecolor='black', alpha=0.5)
plt.xlabel('ShopName')
plt.ylabel('Total Revenue')
plt.title('Top 5 Shops by Total Revenue')
st.pyplot(plt)
st.write("Top 5 Shops by Revenue")
st.dataframe(revenue,width=1000)


#---------
plt.clf()
st.write("Correlation of Columns with Est. Revenue")
correlations = filtered_df.corr()["Est. Revenue"].sort_values(ascending=False)
plt.bar(correlations.index, correlations.values)
st.pyplot(plt)

plt.clf()
st.subheader("Est. Revenue Metic Comparison")
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
ax1.scatter(df["Est. Revenue"], df["Est. Revenue"])
ax1.set_xlabel("Est. Revenue")
ax1.set_ylabel("Sales")
ax1.set_title("Est. Revenue vs. Sales")

ax2.scatter(df["Est. Revenue"], df["Est. Revenue"])
ax2.set_xlabel("Total Views")
ax2.set_ylabel("Views")
ax2.set_title("Est. Revenue vs. Total Views")

ax3.scatter(df["Est. Revenue"], df["Est. Revenue"])
ax3.set_xlabel("Est. Revenue")
ax3.set_ylabel("Price")
ax3.set_title("Est. Revenue vs. Price")

ax4.scatter(df["Est. Revenue"], df["Hearts"])
ax4.set_xlabel("Est. Revenue")
ax4.set_ylabel("Hearts")
ax4.set_title("Est. Revenue vs. Hearts")
plt.tight_layout()
st.pyplot(plt)
#---------
