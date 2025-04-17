import pandas as pd
import streamlit as st

df_e = pd.read_csv('data/df_elasticity.csv')

st.set_page_config(layout='wide')
st.title('Welcome to my Price Elasticity Dashboard!')

st.subheader('This application was developed for a company seeking an AI model designed to predict price elasticity.')

st.markdown("""
- Price elasticity is an economic concept that gauges how sensitive the demand for a product is to price changes.
- Using this predictive model, you can make strategic decisions to maximize your business revenue. It allows you to simulate scenarios like price increases or discounts and receive real-time insights into their financial impact on revenue.
""")

df_ra = df_e[['ranking', 'name', 'price_elasticity']].sort_values(by='price_elasticity', ascending=True)
df_ra = df_ra.set_index('ranking')
st.dataframe(df_ra, use_container_width=True)

st.subheader('Click on Price Simulation in the sidebar menu and try it yourself!')