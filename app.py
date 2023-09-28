import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Etsy Marketplace Analysis")
df = pd.read_csv('erank.csv')
#Data Cleaning
columns_to_drop = [0, 1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
df.drop(columns=df.columns[columns_to_drop], inplace=True)
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
for i in range(3,9):
    if type(df[df.columns[i]][0]) == str:
        df[df.columns[i]] = df[df.columns[i]].str.replace('[\$,]', '', regex=True)
        df[df.columns[i]] = df[df.columns[i]].astype(float)

st.dataframe(df)

# Top 10 Shops
st.title("Top 10 Shops (By Revenue)")
result = df.groupby('ShopName')['Est. Revenue'].sum().sort_values(ascending=False).head(10)
plot_df = pd.DataFrame({'ShopName': result.index, 'Total Revenue': result.values})
fig = px.bar(plot_df, x='ShopName', y='Total Revenue', title='Top 10 Shops by Total Revenue')
# fig.show()
st.plotly_chart(fig)

#Treding Shops
# days = 30
st.title("Trending Listing (Revenue Wise)")
days = st.number_input("Enter the Days", step=1, value=30, format="%d")
filtered_df = df[(df["Listing Age (Days)"] < days) & (df["Est. Revenue"] > 0)]
result2 = filtered_df.groupby('Listing')['Est. Revenue'].sum().sort_values(ascending=False).head(10)
trending = df[df['Listing'].isin(result2.index.to_list())].sort_values(by='Est. Revenue', ascending=False)
st.dataframe(result2, width=1000)