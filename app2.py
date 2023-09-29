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
ax1.set_ylabel("Est. Revenue")
ax1.set_title("Est. Revenue vs. Est. Revenue")

ax2.scatter(df["Est. Revenue"], df["Est. Revenue"])
ax2.set_xlabel("Est. Revenue")
ax2.set_ylabel("Est. Revenue")
ax2.set_title("Est. Revenue vs. Est. Revenue")

ax3.scatter(df["Est. Revenue"], df["Est. Revenue"])
ax3.set_xlabel("Est. Revenue")
ax3.set_ylabel("Est. Revenue")
ax3.set_title("Est. Revenue vs. Est. Revenue")

ax4.scatter(df["Est. Revenue"], df["Hearts"])
ax4.set_xlabel("Est. Revenue")
ax4.set_ylabel("Hearts")
ax4.set_title("Est. Revenue vs. Hearts")
plt.tight_layout()
st.pyplot(plt)
#---------
