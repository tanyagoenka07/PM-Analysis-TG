from preswald import connect, get_df, text, table, plotly, sidebar
import pandas as pd
import plotly.express as px

connect()
sidebar()

df = get_df("pm25")
df.columns = [col.strip().replace('\ufeff', '') for col in df.columns]
year_cols = [str(y) for y in range(2010, 2018)]
for y in year_cols:
    if y in df.columns:
        df[y] = pd.to_numeric(df[y], errors="coerce")

text("# 🌫️ PM2.5 Global Pollution Dashboard")
text("#### Built with by Tanya Goyanka")
text("> Explore PM2.5 pollution levels globally from 2010 to 2017.")

if not df.empty:
    table(df.head(10), title="📋 First 10 Records of Dataset")

if "2017" in df.columns:
    filtered = df[df["2017"] > 30]
    if not filtered.empty:
        table(filtered, title="🔎 Countries with PM2.5 > 30 µg/m³ (in 2017)")
    else:
        text("⚠️ No countries exceeded threshold.", variant="warning")
else:
    text("❌ Column `2017` not found", variant="error")

if "2017" in df.columns and "Country Name" in df.columns:
    top5 = df.nlargest(5, "2017").dropna(subset=["Country Name"])
    if not top5.empty:
        melted = top5.melt(id_vars=["Country Name"], value_vars=year_cols)
        fig1 = px.line(
            melted, x="variable", y="value", color="Country Name",
            title="📈 PM2.5 Trend (Top 5 Most Polluted)",
            labels={"variable": "Year", "value": "PM2.5 (µg/m³)"},
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Set1
        )
        fig1.update_layout(template="plotly_white", title_font_color="#E74C3C")
        plotly(fig1)

if "2017" in df.columns and "Country Name" in df.columns:
    fig2 = px.choropleth(
        df, locations="Country Name", locationmode="country names",
        color="2017", color_continuous_scale="Reds",
        title="🌍 PM2.5 by Country (2017)"
    )
    fig2.update_layout(title_font_color="#3498DB", template="plotly_white")
    plotly(fig2)

if "2017" in df.columns:
    fig3 = px.histogram(
        df, x="2017", nbins=30,
        title="📊 PM2.5 Distribution (2017)",
        labels={"2017": "PM2.5 (µg/m³)"},
        color_discrete_sequence=["#9B59B6"]
    )
    fig3.update_layout(title_font_color="#2ECC71", template="plotly_white")
    plotly(fig3)

text("---")
text("### Perfect Summary")
text("✔️ Data loaded & cleaned")
text("✔️ Tables displayed")
text("✔️ Charts visualized")
text("🎉 Dashboard by Tanya Goyanka")
