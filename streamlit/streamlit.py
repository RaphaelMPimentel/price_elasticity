import streamlit as st

home_page = st.Page(
    page='pages/home.py',
    title='Home',
    icon=':material/home:',
)
simulation_page = st.Page(
    page='pages/simulation.py',
    title='Price Simulation',
    icon=':material/payments:',
)

pg = st.navigation(pages=[home_page, simulation_page])
pg.run()

st.sidebar.text('Made by Raphael Pimentel')