import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout='wide',page_title='Startup Analysis')
df = pd.read_csv('startup_cleaned.csv')
df['vertical'] = df['vertical'].replace('ECommerce','Ecommerce')
df['vertical'] = df['vertical'].replace('eCommerce','Ecommerce')
df['vertical'] = df['vertical'].replace('E-Commerce','Ecommerce')
df['city'] = df['city'].replace('Bangalore','Bengaluru')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['startup'] = df['startup'].replace("BYJU\\'S", "BYJU'S")

def load_overall_analysis():
    st.title("Overall Analysis")
    col1, col2, col3, col4 = st.columns(4)
    # overall invested money
    total = round(df['amount'].sum())
    # maximum amount invested in startup
    max_funding = round(df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).values[0])
    # avg funding in startup
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())
    # total startup funded
    total_startup = df['startup'].nunique()

    with col1:
        st.metric("Total amount invested", str(total)+ 'Cr')
    with col2:
        st.metric("Max", str(max_funding) + " " + 'Cr')
    with col3:
        st.metric("Avg",str(avg_funding) + " " + 'Cr')
    with col4:
        st.metric("Funded Startup", str(total_startup))

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df1 = df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df1 = df.groupby(['year','month'])['amount'].count().reset_index()
    temp_df1['x-axis'] = temp_df1['month'].astype(str) + ' - ' + temp_df1['year'].astype(str)

    fig4, ax4 = plt.subplots()
    ax4.plot(temp_df1['x-axis'], temp_df1['amount'])
    st.pyplot(fig4)

    col5,col6 = st.columns(2)
    with col5:
        st.subheader('Year Wise Investment')
        year_wise = df.groupby('year')['amount'].sum().reset_index()
        st.bar_chart(data=year_wise, x='year',y='amount')

    with col6:
        st.subheader('Types of Funding')
        top_rounds = df.groupby('round')['amount'].sum().sort_values(ascending=False).head(5)
        fig10, ax10 = plt.subplots()
        ax10.pie(top_rounds.values, labels=top_rounds.index, autopct='%1.1f%%')
        st.pyplot(fig10)

    col7,col8 = st.columns(2)
    with col7:
        st.subheader("Amount Invested in Sectors")
        sectors_sum = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(7)
        fig5, ax5 = plt.subplots()
        ax5.pie(sectors_sum.values, labels=sectors_sum.index, autopct='%1.1f%%')
        st.pyplot(fig5)

    with col8:
        st.subheader("Sectors which got funding more times")
        sector_count = df.groupby('vertical')['startup'].count().sort_values(ascending=False).head(7)
        fig6, ax6 = plt.subplots()
        ax6.pie(sector_count.values, labels=sector_count.index, autopct='%1.1f%%')
        st.pyplot(fig6)

    st.subheader("Investment in top 10 city")
    top_city = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10).reset_index()
    st.bar_chart(data=top_city, x='city',y='amount')

    st.subheader("Top startup")
    option1 = st.selectbox('Based On',['Overall','Year'])
    if option1 == 'Year':
        top_startup = df.sort_values(by='amount',ascending=False).groupby('year').head(1)[['year','startup','amount']]
        top_startup['year'] = pd.Categorical(top_startup['year'])
        fig7, ax7 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=top_startup,x='year',y='amount',hue='startup',ax=ax7)
        st.pyplot(fig7)
    else:
        based_on_year = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10).reset_index()
        fig8, ax8 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=based_on_year,x='startup',y='amount',ax=ax8)
        st.pyplot(fig8)

    st.subheader("Top Investor")
    selected_sector = st.selectbox("Sector",df['vertical'].unique().tolist())
    btn3 = st.button('Find details')
    if btn3:
        temp_df = df[df['vertical'] == selected_sector]
        investor_df = temp_df.groupby('investors')['amount'].sum().sort_values(ascending=False).head(5).reset_index()

        st.bar_chart(data=investor_df,x='investors',y='amount')

def load_startup_details(startup):
    st.title(startup)
    st.subheader("Investors Name")
    investor = df[df['startup'] == startup].groupby('startup')['investors'].sum().values[0]
    st.text(investor)
    col9,col10 = st.columns(2)
    with col9:
        st.subheader("Industry Name")
        industry = df[df['startup'] == startup].groupby('startup')['vertical'].sum().values[0]
        st.text(industry)

    with col10:
        st.subheader("Subindustry Name")
        industry = df[df['startup'] == startup].groupby('startup')['subvertical'].sum().values[0]
        st.text(industry)

    col11,col12 = st.columns(2)
    with col11:
        st.subheader("Located In")
        location = df[df['startup'] == startup]['city'].values[0]
        st.text(location)

    with col12:
        st.subheader("Total Funding")
        funds = df[df['startup'] == startup].groupby('startup')['amount'].sum().values[0]
        st.text(str(funds) + " " + 'Cr')

    st.subheader("Last Funding Date")
    date = df[df['startup'] == startup]['date'].iloc[0]
    st.text(date)

def load_investor_details(investor):
    # load recent 5 investment of investor
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','investors','round','amount']]

    # biggest investment
    big_df = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head().reset_index()

    # top sectors
    top_sectors = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head(7)

    # stage wise investment
    stage = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending=False).head(7)

    # top cities
    top_city = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False).head(7)

    # year wise
    year = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()

    st.title(investor)
    st.subheader("Most Recent Investment")
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Biggest Investment")
        st.bar_chart(data=big_df,x="startup",y='amount')

    with col2:
        st.subheader("Top Investment Sectors")
        fig, ax = plt.subplots()
        ax.pie(top_sectors.values, labels=top_sectors.index, autopct='%1.1f%%')
        st.pyplot(fig)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Stage Investment")
        fig1, ax1 = plt.subplots()
        ax1.pie(stage.values, labels=stage.index, autopct='%1.1f%%')
        st.pyplot(fig1)

    with col4:
        st.subheader("Investment in Top City")
        fig2, ax2 = plt.subplots()
        ax2.pie(top_city.values, labels=top_city.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    st.subheader("Year wise Investment")
    fig3, ax3 = plt.subplots()
    ax3.plot(year.index, year.values)
    st.pyplot(fig3)

st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One",["Overall Analysis",'Startup','Investor'])

if(option == "Overall Analysis"):
    load_overall_analysis()

elif(option == 'Startup'):
    selected_startup = st.sidebar.selectbox("Startup",sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button("Find startup details")
    if btn1:
        load_startup_details(selected_startup)


else:
    selected_investor = st.sidebar.selectbox("Investor",sorted((df['investors'].unique().tolist())))
    btn2 = st.sidebar.button("Find Investor details")
    if btn2:
        load_investor_details(selected_investor)
