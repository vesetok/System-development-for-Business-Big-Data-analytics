import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns

# Data loading
df = pd.read_csv("Global_Superstore - Copy - 2.csv", encoding="latin1", quotechar='\0')

# Displaying the first 5 rows
print("Review of the first lines:")
print(df.head())

# Inspection of columns
print("\nAvailable columns in the dataset:")
print(df.columns)

# Table size
print("\nDataset size:", df.shape)

# --- Cleaning ---
# Removing empty values
df.dropna(inplace=True)

# Date conversion
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

# Conversion of numeric columns
for col in ['Sales', 'Profit', 'Quantity', 'Discount']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# --- KPI computations ---
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
avg_order_value = df['Sales'].mean()
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique()

print("KEY PERFORMANCE INDICATORS (KPIs):")
print(f"Total revenue (Sales): ${total_sales:,.2f}")
print(f"Total profit: ${total_profit:,.2f}")
print(f"Average order value: ${avg_order_value:,.2f}")
print(f"Total orders: {total_orders}")
print(f"Total customers: {total_customers}")

# Addition of KPI columns
df['Expenses'] = df['Sales'] - df['Profit']
df['Profit Margin %'] = (df['Profit'] / df['Sales']) * 100
print("The data has been cleaned and KPI columns have been added.")
print(df[['Sales', 'Profit', 'Expenses', 'Profit Margin %']].head())

#Analysis of revenue and profit by year
df['Year'] = df['Order Date'].dt.year
yearly = df.groupby('Year')[['Sales', 'Profit']].sum().reset_index()

print("\nYearly aggregated data:")
print(yearly)

# Adding: Expenses = Sales - Profit
yearly['Expenses'] = yearly['Sales'] - yearly['Profit']

print("\nYearly aggregated data:")
print(yearly)

# --- Visualization: Sales & Profit per year ---
plt.figure(figsize=(8,5))
plt.plot(yearly['Year'], yearly['Sales'], marker='o', label="Sales")
plt.plot(yearly['Year'], yearly['Profit'], marker='s', label="Profit")
plt.title("Yearly Sales & Profit")
plt.xlabel("Year")
plt.ylabel("Amount ($)")
plt.legend()
plt.grid(True)
plt.show()

# --- Visualization: Sales vs Expenses per year ---
plt.figure(figsize=(10,6))
bar_width = 0.35
x = range(len(yearly['Year']))

plt.bar(x, yearly['Sales'], width=bar_width, label='Sales')
plt.bar([i + bar_width for i in x], yearly['Expenses'], width=bar_width, label='Expenses')

plt.xticks([i + bar_width/2 for i in x], yearly['Year'])
plt.title("Yearly Sales vs Expenses")
plt.xlabel("Year")
plt.ylabel("Amount ($)")
plt.legend()
plt.tight_layout()
plt.show()


# --- Top 10 countries by Profit (positive only) ---
top_profit_countries = (
    df.groupby('Country')[['Sales', 'Profit']]
    .sum()
    .reset_index()
)
top_profit_countries = top_profit_countries[top_profit_countries['Profit'] > 0]
top_profit_countries = top_profit_countries.sort_values(by='Profit', ascending=False).head(10)

print("=== Top 10 Countries by Profit ===")
print(top_profit_countries)

# --- Bar chart for Profit ---
plt.figure(figsize=(10,6))
plt.bar(top_profit_countries['Country'], top_profit_countries['Profit'], color='green')
plt.title("Top 10 Countries by Profit (Positive Only)")
plt.xlabel("Country")
plt.ylabel("Profit ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Top 10 countries by Sales ---
top_sales_countries = (
    df.groupby('Country')[['Sales', 'Profit']]
    .sum()
    .reset_index()
    .sort_values(by='Sales', ascending=False)
    .head(10)
)

print("\n=== Top 10 Countries by Sales & Profit ===")
print(top_sales_countries)

# --- Bar chart for Sales ---
plt.figure(figsize=(10,6))
plt.bar(top_sales_countries['Country'], top_sales_countries['Sales'], color='blue')
plt.title("Top 10 Countries by Sales")
plt.xlabel("Country")
plt.ylabel("Sales ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Global data by country ---
country_agg = df.groupby('Country')[['Sales', 'Profit']].sum().reset_index()


# --- Deep dive analysis ---

# Top Categories by Sales & Profit
category_agg = df.groupby('Category')[['Sales', 'Profit']].sum().reset_index().sort_values(by='Sales', ascending=False)
print("=== Top Categories by Sales & Profit ===")
print(category_agg)

# Bar chart for categories
plt.figure(figsize=(8,5))
plt.bar(category_agg['Category'], category_agg['Sales'], color='skyblue', label='Sales')
plt.bar(category_agg['Category'], category_agg['Profit'], color='orange', label='Profit', alpha=0.7)
plt.title("Sales & Profit by Category")
plt.xlabel("Category")
plt.ylabel("Amount ($)")
plt.legend()
plt.tight_layout()
plt.show()

# Top Sub-categories by Sales
subcat_agg = df.groupby('Sub-Category')[['Sales', 'Profit']].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
print("\n=== Top 10 Sub-Categories by Sales ===")
print(subcat_agg)

# Interactive Plotly Bar chart
fig = px.bar(subcat_agg, x='Sub-Category', y=['Sales','Profit'],
             title="Top 10 Sub-Categories by Sales & Profit",
             labels={'value':'Amount ($)', 'Sub-Category':'Sub-Category'},
             barmode='group', height=450)
fig.show()

# Top Customers by Sales
customer_agg = df.groupby('Customer Name')[['Sales', 'Profit']].sum().reset_index().sort_values(by='Sales', ascending=False).head(10)
print("\n=== Top 10 Customers by Sales & Profit ===")
print(customer_agg)

# Interactive Plotly Bar chart
fig = px.bar(customer_agg, x='Customer Name', y=['Sales','Profit'],
             title="Top 10 Customers by Sales & Profit",
             labels={'value':'Amount ($)', 'Customer Name':'Customer'},
             barmode='group', height=450)
fig.show()

# Monthly Sales Trend
df['Month'] = df['Order Date'].dt.to_period('M')
monthly_agg = df.groupby('Month')[['Sales', 'Profit']].sum().reset_index()
monthly_agg['Month'] = monthly_agg['Month'].dt.to_timestamp()

print("\n=== Monthly Aggregated Sales & Profit ===")
print(monthly_agg.head())

# Line chart for monthly trends
plt.figure(figsize=(12,6))
plt.plot(monthly_agg['Month'], monthly_agg['Sales'], marker='o', label='Sales')
plt.plot(monthly_agg['Month'], monthly_agg['Profit'], marker='s', label='Profit')
plt.title("Monthly Sales & Profit trend")
plt.xlabel("Month")
plt.ylabel("Amount ($)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Interactive monthly trend with Plotly
fig = px.line(monthly_agg, x='Month', y=['Sales','Profit'],
              title='Monthly Sales & Profit trend',
              labels={'value':'Amount ($)', 'Month':'Month'})
fig.show()

# --- Regional, Product & Seasonal analysis ---

# --- Revenue & Profit by Region ---
region_agg = df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
print("\n Revenue & Profit by Region:")
print(region_agg)

# Bar chart: Sales vs Profit per Region
plt.figure(figsize=(8,5))
x = region_agg['Region']
plt.bar(x, region_agg['Sales'], width=0.4, label='Sales', align='edge')
plt.bar(x, region_agg['Profit'], width=-0.4, label='Profit', align='edge')
plt.title("Sales & Profit by Region")
plt.xlabel("Region")
plt.ylabel("Amount ($)")
plt.legend()
plt.tight_layout()
plt.show()

# --- Top 10 Products by Profit ---
top_products = df.groupby('Product Name')[['Sales', 'Profit']].sum().reset_index()
top_products = top_products.sort_values(by='Profit', ascending=False).head(10)
print("\n=== Top 10 Products by Profit ===")
print(top_products)

# Bar chart: Top 10 Products by Profit
plt.figure(figsize=(10,6))
plt.barh(top_products['Product Name'], top_products['Profit'], color='orange')
plt.xlabel("Profit ($)")
plt.ylabel("Product Name")
plt.title("Top 10 Products by Profit")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# --- Seasonal analysis: Sales & Profit by Month ---
df['Month'] = df['Order Date'].dt.month
monthly_agg = df.groupby('Month')[['Sales', 'Profit']].sum().reset_index()
print("\n Monthly aggregated data:")
print(monthly_agg)

# --- Heatmap: Profit Margin per Region & Category ---
region_category = df.groupby(['Region','Category'])['Profit Margin %'].mean().unstack()
plt.figure(figsize=(8,5))
sns.heatmap(region_category, annot=True, fmt=".1f", cmap="YlGnBu")
plt.title("Average Profit Margin % by Region & Category")
plt.show()

# --- Revenue & Profit by Region (Interactive) ---
fig_region = go.Figure()
fig_region.add_trace(go.Bar(x=region_agg['Region'], y=region_agg['Sales'], name='Sales'))
fig_region.add_trace(go.Bar(x=region_agg['Region'], y=region_agg['Profit'], name='Profit'))
fig_region.update_layout(title="Sales & Profit by Region",
                         xaxis_title="Region",
                         yaxis_title="Amount ($)",
                         barmode='group')
fig_region.show()

# --- Top 10 Products by Profit (Interactive) ---
fig_products = px.bar(top_products, x='Profit', y='Product Name', orientation='h',
                      title="Top 10 Products by Profit",
                      labels={'Profit':'Profit ($)', 'Product Name':'Product'})
fig_products.update_layout(yaxis=dict(autorange="reversed"))  
fig_products.show()

# --- Heatmap: Average Profit Margin % by Region & Category (Interactive) ---
region_category = df.groupby(['Region','Category'])['Profit Margin %'].mean().unstack().reset_index()
fig_heatmap = px.imshow(region_category.set_index('Region').T,
                        labels=dict(x="Region", y="Category", color="Profit Margin %"),
                        text_auto=".1f",
                        aspect="auto",
                        title="Average Profit Margin % by Region & Category")
fig_heatmap.show()

# --- Creating the figure ---
fig = go.Figure()

# Trace за Global Profit
fig.add_trace(go.Choropleth(
    locations=country_agg['Country'],
    locationmode='country names',
    z=country_agg['Profit'],
    colorscale='Plasma',
    colorbar_title="Global Profit",
    text=country_agg['Country'],
    hovertemplate='<b>%{text}</b><br>Profit: $%{z:,.2f}<extra></extra>',
    visible=True
))

# Trace за Global Sales (will be hidden initially)
fig.add_trace(go.Choropleth(
    locations=country_agg['Country'],
    locationmode='country names',
    z=country_agg['Sales'],
    colorscale='Viridis',
    colorbar_title="Global Sales",
    text=country_agg['Country'],
    hovertemplate='<b>%{text}</b><br>Sales: $%{z:,.2f}<extra></extra>',
    visible=False
))

# --- Replaceable button ---
fig.update_layout(
    title_text='Global Metrics',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    ),
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.1,
            y=1.15,
            showactive=True,
            buttons=list([
                dict(label="Profit",
                     method="update",
                     args=[{"visible": [True, False, True, False]},
                           {"title": "Global Profit"}]),
                dict(label="Sales",
                     method="update",
                     args=[{"visible": [False, True, False, True]},
                           {"title": "Global Sales"}]),
            ]),
        )
    ]
)

fig.show()

# --- Export results to Excel ---
output_file = "business_analytics_results1.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    # KPIs
    kpi_summary = pd.DataFrame({
        "Metric": [
            "Total Sales", "Total Profit", "Total Expenses",
            "Average Order Value", "Total Orders", "Total Customers"
        ],
        "Value": [
            total_sales, total_profit, total_sales - total_profit,
            avg_order_value, total_orders, total_customers
        ]
    })
    kpi_summary.to_excel(writer, sheet_name="KPIs", index=False)

    # Yearly aggregates
    yearly.to_excel(writer, sheet_name="Yearly aggregates", index=False)

    # Top 10 countries (Profit & Sales)
    top_profit_countries.to_excel(writer, sheet_name="Top 10 Profit", index=False)
    top_sales_countries.to_excel(writer, sheet_name="Top 10 Sales", index=False)

    # Regional aggregates
    region_agg.to_excel(writer, sheet_name="Regional aggregates", index=False)

    # Category & Sub-Category aggregates
    category_agg.to_excel(writer, sheet_name="Category aggregates", index=False)
    subcat_agg.to_excel(writer, sheet_name="Sub - Category aggregates", index=False)

    # Top 10 Customers
    customer_agg.to_excel(writer, sheet_name="Top 10 Customers", index=False)

    # Monthly aggregates
    monthly_agg.to_excel(writer, sheet_name="Monthly aggregates", index=False)

    # Top 10 Products by Profit
    top_products.to_excel(writer, sheet_name="Top 10 Products", index=False)

print(f"All results have been exported successfully to {output_file}")











