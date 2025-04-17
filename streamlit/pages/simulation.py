import pandas as pd
import streamlit as st

# load datasets
df_bp = pd.read_csv('data/invoicing.csv')
df_bp = df_bp.drop('Unnamed: 0', axis=1)
df_c = pd.read_csv('data/crossprice.csv')
df_e = pd.read_csv('data/df_elasticity.csv')
x_price = pd.read_csv('data/x_price.csv')
y_demand = pd.read_csv('data/y_demand.csv')

# layout
st.set_page_config(layout='wide')

# for price change simulation
st.sidebar.header("Simulate Price Change")
price_change = st.sidebar.slider(
    "What percentage price change would you like to apply?", min_value=-50, max_value=50, value=0
)

st.title("Interactive Pricing Simulation")
st.subheader("Price Change Impact on Products")

df_ranking = df_e[['ranking', 'name', 'price_elasticity']].sort_values(by='price_elasticity', ascending=False)

invoicing_results = {
    'name': [],
    'current_revenue': [],
    'predicted_revenue': [],
    'variation': [],
    'percentage_variation': []
}

for i in range(len(df_ranking)):
    current_average_price = x_price[df_ranking['name'][i]].mean()
    current_demand = y_demand[df_ranking['name'][i]].sum()
    
    reduced_price = current_average_price * (1 + price_change / 100)
    
    demand_change = (price_change / 100) * df_ranking['price_elasticity'][i]
    
    new_demand = current_demand * demand_change
    
    current_revenue = round(current_average_price * current_demand, 2)
    
    predicted_revenue = round(reduced_price * new_demand, 2)
    
    variation = round(predicted_revenue - current_revenue, 2)
    percentage_variation = round(((predicted_revenue - current_revenue) / current_revenue) * 100, 2)
    
    # add to invoicing_results
    invoicing_results['name'].append(df_ranking['name'][i])
    invoicing_results['current_revenue'].append(current_revenue)
    invoicing_results['predicted_revenue'].append(predicted_revenue)
    invoicing_results['variation'].append(variation)
    invoicing_results['percentage_variation'].append(percentage_variation)

# final dataframe
invoicing_df = pd.DataFrame(invoicing_results)
st.dataframe(invoicing_df, use_container_width=True)

# summarize overall impact
total_products = len(invoicing_df)
revenue_before_change = invoicing_df['current_revenue'].sum()
revenue_variation = invoicing_df['variation'].sum()
predicted_revenue = invoicing_df["predicted_revenue"].sum()
percentage_revenue_change = (predicted_revenue / invoicing_df["current_revenue"].sum()) * 100

st.subheader("Overall Impact")
st.markdown(f"""
- Total products analyzed: **{total_products}**
- Revenue before change: **${revenue_before_change:,.2f}**
- New predicted revenue **${predicted_revenue:,.2f}**
- Revenue variation: **${revenue_variation:,.2f}**
- Percent revenue change: **{percentage_revenue_change:.2f}%**
""")

# detailed breakdown
st.subheader("Detailed Product Impact")
for index, row in invoicing_df.iterrows():
    st.write(f"**{row['name']}**:")
    st.write(f"Price change {price_change}%")
    st.write(f"Predicted revenue change: ${row['predicted_revenue']:,.2f}")
    st.write('---')