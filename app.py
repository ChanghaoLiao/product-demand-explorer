from html import escape
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Exploring Company Product Demand",
    page_icon="↗",
    layout="wide",
)

OCEAN = {
    "canvas": "#F7FAFB",
    "surface": "#FFFFFF",
    "surface_subtle": "#EFF5F7",
    "text": "#182024",
    "secondary": "#59676E",
    "tertiary": "#62767F",
    "border": "#DCE8EC",
    "divider": "#E6EEF1",
    "accent": "#0EA5E9",
    "accent_soft": "#E8F7FE",
    "accent_text": "#036B9D",
    "chart_comparison": "#62767F",
    "chart_grid": "#E6EEF1",
}

st.markdown(
    f"""
    <style>
        :root {{
            --canvas:{OCEAN['canvas']}; --surface:{OCEAN['surface']};
            --surface-subtle:{OCEAN['surface_subtle']}; --text:{OCEAN['text']};
            --secondary:{OCEAN['secondary']}; --tertiary:{OCEAN['tertiary']};
            --border:{OCEAN['border']}; --divider:{OCEAN['divider']};
            --accent:{OCEAN['accent']}; --accent-soft:{OCEAN['accent_soft']};
            --accent-text:{OCEAN['accent_text']};
        }}
        .stApp {{
            background:radial-gradient(circle at 88% 2%,rgba(14,165,233,.075),transparent 25rem),var(--canvas);
            color:var(--text);
        }}
        [data-testid="stHeader"] {{background:transparent}}
        .block-container {{max-width:1240px;padding-top:2.5rem;padding-bottom:4rem}}
        .eyebrow {{color:var(--accent-text);font-size:.72rem;font-weight:760;letter-spacing:.13em;margin-bottom:.7rem;text-transform:uppercase}}
        .hero-title {{color:var(--text);font-size:clamp(2.5rem,5vw,4.8rem);font-weight:780;letter-spacing:-.055em;line-height:.98;margin:0;max-width:1000px}}
        .hero-intro {{color:var(--secondary);font-size:1.04rem;line-height:1.72;margin:1.25rem 0 0;max-width:890px}}
        .data-strip {{align-items:stretch;border-bottom:1px solid var(--divider);border-top:1px solid var(--divider);display:grid;grid-template-columns:repeat(4,minmax(0,1fr));margin:2rem 0 1.5rem;padding:1rem 0}}
        .data-fact {{padding:.1rem 1.25rem}}
        .data-fact:first-child {{padding-left:0}}
        .data-fact + .data-fact {{border-left:1px solid var(--divider)}}
        .data-value {{color:var(--text);font-size:1.35rem;font-weight:760;letter-spacing:-.025em;line-height:1.1}}
        .data-label {{color:var(--tertiary);font-size:.76rem;margin-top:.32rem}}
        .purpose-band {{background:linear-gradient(110deg,var(--surface) 0%,var(--accent-soft) 165%);border-left:3px solid var(--accent);border-radius:0 14px 14px 0;margin:0 0 3rem;padding:1.15rem 1.35rem}}
        .purpose-title {{color:var(--text);font-size:1rem;font-weight:750;letter-spacing:-.015em;margin-bottom:.32rem}}
        .purpose-copy {{color:var(--secondary);font-size:.9rem;line-height:1.55;max-width:920px}}
        .step-head {{border-top:1px solid var(--divider);margin-top:2.4rem;padding-top:1.8rem}}
        .step-index {{color:var(--accent-text);font-size:.7rem;font-weight:760;letter-spacing:.12em;margin-bottom:.45rem;text-transform:uppercase}}
        .step-title {{color:var(--text);font-size:clamp(1.45rem,2.7vw,2.15rem);font-weight:760;letter-spacing:-.035em;line-height:1.08;margin:0}}
        .step-copy {{color:var(--secondary);font-size:.9rem;line-height:1.55;margin:.55rem 0 .85rem;max-width:760px}}
        .selection-note {{background:var(--accent-soft);border-radius:12px;color:var(--accent-text);font-size:.84rem;line-height:1.55;margin-top:.55rem;padding:.8rem 1rem}}
        .chapter-head {{align-items:flex-end;display:flex;gap:1.25rem;justify-content:space-between;margin:2rem 0 .75rem}}
        .chapter-title {{color:var(--text);font-size:1.17rem;font-weight:750;letter-spacing:-.022em}}
        .chapter-copy {{color:var(--secondary);font-size:.8rem;line-height:1.45;margin-top:.25rem}}
        .chapter-scope {{color:var(--tertiary);font-size:.74rem;max-width:440px;text-align:right}}
        .chart-rule {{border-top:1px solid var(--divider);margin-top:.15rem;padding-top:.35rem}}
        .summary-shell {{background:linear-gradient(110deg,var(--surface) 0%,var(--accent-soft) 155%);border:1px solid var(--border);border-top:3px solid var(--accent);border-radius:16px;margin:3.2rem 0 1.4rem;overflow:hidden;padding:1.35rem}}
        .summary-heading-row {{align-items:baseline;display:flex;gap:1rem;justify-content:space-between;margin-bottom:1.05rem}}
        .summary-heading {{color:var(--text);font-size:1.2rem;font-weight:760;letter-spacing:-.02em}}
        .summary-grid {{display:grid;grid-template-columns:repeat(4,minmax(0,1fr))}}
        .summary-item {{min-width:0;padding:.1rem 1.1rem .2rem}}
        .summary-item:first-child {{padding-left:0}}
        .summary-item + .summary-item {{border-left:1px solid var(--divider)}}
        .summary-label {{color:var(--tertiary);font-size:.68rem;font-weight:730;letter-spacing:.08em;text-transform:uppercase}}
        .summary-value {{color:var(--text);font-size:1.08rem;font-weight:760;letter-spacing:-.02em;line-height:1.2;margin:.34rem 0 .4rem}}
        .summary-body {{color:var(--secondary);font-size:.8rem;line-height:1.48}}
        .method-note {{color:var(--secondary);font-size:.82rem;line-height:1.62}}
        [data-testid="stExpander"] {{background:rgba(255,255,255,.75);border-color:var(--border)}}
        div[data-testid="stSelectbox"],div[data-testid="stMultiSelect"],div[data-testid="stDateInput"] {{max-width:620px}}
        @media(max-width:900px) {{
            .block-container {{padding-top:1.5rem}}
            .data-strip {{grid-template-columns:repeat(2,minmax(0,1fr))}}
            .data-fact:nth-child(3) {{border-left:0;padding-left:0}}
            .data-fact:nth-child(n+3) {{border-top:1px solid var(--divider);margin-top:.8rem;padding-top:.9rem}}
            .summary-grid {{grid-template-columns:repeat(2,minmax(0,1fr));row-gap:1rem}}
            .summary-item:nth-child(3) {{border-left:0;padding-left:0}}
            .summary-item:nth-child(n+3) {{border-top:1px solid var(--divider);padding-top:1rem}}
        }}
        @media(max-width:640px) {{
            .hero-title {{font-size:2.45rem}}
            .chapter-head,.summary-heading-row {{align-items:flex-start;flex-direction:column;gap:.35rem}}
            .chapter-scope {{text-align:left}}
            .summary-grid {{grid-template-columns:1fr}}
            .summary-item,.summary-item:first-child,.summary-item:nth-child(3) {{border-left:0;padding:.85rem 0}}
            .summary-item + .summary-item {{border-top:1px solid var(--divider)}}
        }}
        @media(prefers-reduced-motion:reduce) {{*,*::before,*::after {{scroll-behavior:auto!important;transition-duration:.01ms!important}}}}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    path = Path(__file__).parent / "Product_Demand_2014_2016_Top2_Daily.csv"
    return pd.read_csv(path, parse_dates=["Date"]).sort_values(["Date", "Product_Code"])


def compact_number(value):
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.0f}K"
    return f"{value:,.0f}"


def style_cartesian_figure(figure, height=400):
    figure.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family='-apple-system,BlinkMacSystemFont,"Segoe UI Variable","Inter",sans-serif',
            color=OCEAN["text"],
            size=12,
        ),
        hoverlabel=dict(bgcolor=OCEAN["surface"], bordercolor=OCEAN["border"], font_color=OCEAN["text"]),
        margin=dict(l=20, r=18, t=18, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, title=None),
    )
    figure.update_xaxes(gridcolor=OCEAN["chart_grid"], linecolor=OCEAN["border"], zeroline=False)
    figure.update_yaxes(gridcolor=OCEAN["chart_grid"], linecolor=OCEAN["border"], zeroline=False)
    return figure


def step_header(index, title, copy):
    st.markdown(
        f"""
        <section class="step-head">
            <div class="step-index">Step {index}</div>
            <h2 class="step-title">{escape(title)}</h2>
            <p class="step-copy">{escape(copy)}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


df = load_data()
all_products = sorted(df["Product_Code"].unique())
minimum_date = df["Date"].min().date()
maximum_date = df["Date"].max().date()

st.markdown(
    """
    <div class="eyebrow">Kaggle data · cleaned for exploration</div>
    <h1 class="hero-title">Exploring Company Product Demand</h1>
    <p class="hero-intro">
        This app uses a cleaned subset of FelixZhao’s <em>Forecasts for Product
        Demand</em> dataset from Kaggle. The original order-level records were
        limited to 2014–2016, the two products with the highest cleaned net
        demand were retained, and the records were aggregated by product and
        day. The resulting dataset contains 1,448 daily records across eight
        fields, with no missing values.
    </p>
    <div class="data-strip" aria-label="Dataset profile">
        <div class="data-fact"><div class="data-value">1,448</div><div class="data-label">Daily records</div></div>
        <div class="data-fact"><div class="data-value">8</div><div class="data-label">Data fields</div></div>
        <div class="data-fact"><div class="data-value">2</div><div class="data-label">Products retained</div></div>
        <div class="data-fact"><div class="data-value">2014–2016</div><div class="data-label">Time coverage</div></div>
    </div>
    <section class="purpose-band">
        <div class="purpose-title">Built for operations managers and demand planners</div>
        <div class="purpose-copy">Use the three questions below to focus on the products and time periods relevant to planning. The app then explains the demand pattern, period totals, and underlying order activity for the exact selection you made.</div>
    </section>
    """,
    unsafe_allow_html=True,
)

step_header(
    "1 of 3 · Product",
    "Which product do you want to explore?",
    "Select one product for an individual view or keep both products to compare them throughout the app.",
)
selected_products = st.multiselect(
    "Products",
    options=all_products,
    default=all_products,
    label_visibility="collapsed",
    help="Select one product or both products for comparison.",
)
if not selected_products:
    st.warning("Select at least one product to continue.")
    st.stop()

full_totals = (
    df[df["Product_Code"].isin(selected_products)]
    .groupby("Product_Code")["Daily_Net_Demand"]
    .sum()
    .sort_values(ascending=False)
)
if len(full_totals) == 1:
    selection_note = f"Across the full cleaned dataset, {full_totals.index[0]} recorded {full_totals.iloc[0]:,.0f} units of net demand."
else:
    selection_note = (
        f"Across the full cleaned dataset, {full_totals.index[0]} recorded {full_totals.iloc[0]:,.0f} units of net demand, "
        f"compared with {full_totals.iloc[1]:,.0f} for {full_totals.index[1]}."
    )
st.markdown(f'<div class="selection-note">{escape(selection_note)}</div>', unsafe_allow_html=True)

step_header(
    "2 of 3 · Time range",
    "Which time period do you want to examine?",
    "Choose a start and end date. Every result below will update to use only records inside this period.",
)
selected_date_range = st.date_input(
    "Date range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date,
    label_visibility="collapsed",
    help="Only records within this date range will be included.",
)
if len(selected_date_range) != 2:
    st.info("Select both a start date and an end date.")
    st.stop()

selected_start_date = pd.Timestamp(selected_date_range[0])
selected_end_date = pd.Timestamp(selected_date_range[1])
filtered_df = df.loc[
    df["Product_Code"].isin(selected_products)
    & df["Date"].between(selected_start_date, selected_end_date)
].copy()
if filtered_df.empty:
    st.warning("No data is available for the selected products and dates.")
    st.stop()

product_colors = {
    product: OCEAN["accent"] if index == 0 else OCEAN["chart_comparison"]
    for index, product in enumerate(selected_products)
}
st.markdown(
    f"""
    <div class="chapter-head">
        <div><div class="chapter-title">How did daily demand change during this period?</div><div class="chapter-copy">The lines preserve the daily pattern before the data is summarized into larger periods.</div></div>
        <div class="chapter-scope">{escape(selected_start_date.strftime('%b %d, %Y'))}–{escape(selected_end_date.strftime('%b %d, %Y'))}</div>
    </div><div class="chart-rule"></div>
    """,
    unsafe_allow_html=True,
)
daily_figure = px.line(
    filtered_df,
    x="Date",
    y="Daily_Net_Demand",
    color="Product_Code",
    color_discrete_map=product_colors,
    labels={"Date": "Date", "Daily_Net_Demand": "Daily net demand", "Product_Code": "Product"},
    custom_data=["Order_Records", "Negative_Adjustment"],
)
daily_figure.update_traces(
    line_width=2.2,
    hovertemplate=(
        "<b>%{fullData.name}</b><br>Date: %{x|%b %d, %Y}<br>Daily net demand: %{y:,.0f}<br>"
        "Order records: %{customdata[0]:,.0f}<br>Negative adjustment: %{customdata[1]:,.0f}<extra></extra>"
    ),
)
daily_figure.update_layout(hovermode="x unified", showlegend=len(selected_products) > 1)
daily_figure.update_xaxes(tickformat="%b\n%Y")
style_cartesian_figure(daily_figure, height=410)
st.plotly_chart(daily_figure, width="stretch", config={"displaylogo": False, "responsive": True})

step_header(
    "3 of 3 · Time detail",
    "How detailed should the comparison be?",
    "Choose daily, monthly, or yearly periods. This controls how the app groups demand and order activity below.",
)
selected_granularity = st.selectbox(
    "Time detail",
    options=["Daily", "Monthly", "Yearly"],
    index=1,
    label_visibility="collapsed",
    help="Choose whether each period represents a day, month, or year.",
)

frequency_map = {"Daily": "D", "Monthly": "MS", "Yearly": "YS"}
period_name_map = {"Daily": "day", "Monthly": "month", "Yearly": "year"}
date_format_map = {"Daily": "%B %d, %Y", "Monthly": "%B %Y", "Yearly": "%Y"}
tick_format_map = {"Daily": "%b %d\n%Y", "Monthly": "%b\n%Y", "Yearly": "%Y"}
visible_period_map = {"Daily": 14, "Monthly": 12, "Yearly": 5}
selected_frequency = frequency_map[selected_granularity]
period_name = period_name_map[selected_granularity]
date_format = date_format_map[selected_granularity]
visible_periods = visible_period_map[selected_granularity]


def format_period(date_value):
    return pd.Timestamp(date_value).strftime(date_format)


period_df = (
    filtered_df.groupby([pd.Grouper(key="Date", freq=selected_frequency), "Product_Code"], as_index=False)
    .agg(
        Period_Net_Demand=("Daily_Net_Demand", "sum"),
        Order_Records=("Order_Records", "sum"),
        Negative_Adjustment=("Negative_Adjustment", "sum"),
    )
    .sort_values(["Date", "Product_Code"])
)
scope_text = (
    f"{' & '.join(selected_products)} · {selected_start_date.strftime('%b %d, %Y')}–"
    f"{selected_end_date.strftime('%b %d, %Y')} · {selected_granularity}"
)

st.markdown(
    f"""
    <div class="chapter-head">
        <div><div class="chapter-title">How much demand was recorded in each {escape(period_name)}?</div><div class="chapter-copy">Each product remains separate so the comparison is not hidden inside a combined total.</div></div>
        <div class="chapter-scope">{escape(scope_text)}</div>
    </div><div class="chart-rule"></div>
    """,
    unsafe_allow_html=True,
)
bar_source = period_df.copy()
bar_source["Demand_Label"] = bar_source["Period_Net_Demand"].map(compact_number)
bar_figure = px.bar(
    bar_source,
    x="Date",
    y="Period_Net_Demand",
    color="Product_Code",
    barmode="group",
    text="Demand_Label",
    color_discrete_map=product_colors,
    labels={"Date": period_name.title(), "Period_Net_Demand": "Net demand", "Product_Code": "Product"},
    custom_data=["Order_Records", "Negative_Adjustment"],
)
bar_figure.update_traces(
    textposition="outside",
    cliponaxis=False,
    hovertemplate=(
        "<b>%{fullData.name}</b><br>Period: %{x}<br>Net demand: %{y:,.0f}<br>"
        "Order records: %{customdata[0]:,.0f}<br>Negative adjustment: %{customdata[1]:,.0f}<extra></extra>"
    ),
)
available_dates = bar_source["Date"].drop_duplicates().sort_values().reset_index(drop=True)
bar_figure.update_xaxes(tickformat=tick_format_map[selected_granularity])
if len(available_dates) > visible_periods:
    padding = {"Daily": pd.Timedelta(days=1), "Monthly": pd.Timedelta(days=15), "Yearly": pd.Timedelta(days=150)}[selected_granularity]
    bar_figure.update_xaxes(
        range=[available_dates.iloc[0] - padding, available_dates.iloc[visible_periods - 1] + padding],
        rangeslider=dict(visible=True, thickness=0.08),
    )
bar_figure.update_layout(hovermode="x unified", showlegend=len(selected_products) > 1, dragmode="pan")
style_cartesian_figure(bar_figure, height=450)
st.plotly_chart(
    bar_figure,
    width="stretch",
    config={"displaylogo": False, "responsive": True, "scrollZoom": True},
)

st.markdown(
    f"""
    <div class="chapter-head">
        <div><div class="chapter-title">When was order activity most concentrated?</div><div class="chapter-copy">Darker cells represent more underlying order records—not higher demand volume.</div></div>
        <div class="chapter-scope">Grouped by {escape(selected_granularity.lower())} period</div>
    </div><div class="chart-rule"></div>
    """,
    unsafe_allow_html=True,
)
activity_matrix = (
    period_df.pivot(index="Product_Code", columns="Date", values="Order_Records")
    .fillna(0)
    .reindex(selected_products)
)
activity_dates = list(activity_matrix.columns)
show_heatmap_text = len(activity_dates) <= 24
heatmap_figure = go.Figure(
    data=go.Heatmap(
        z=activity_matrix.values,
        x=activity_dates,
        y=list(activity_matrix.index),
        text=activity_matrix.values if show_heatmap_text else None,
        texttemplate="%{text:,.0f}" if show_heatmap_text else None,
        colorscale=[[0.00, "#EFF5F7"], [0.30, "#CDEDFC"], [0.65, "#68C7F1"], [1.00, "#036B9D"]],
        colorbar=dict(title="Records", thickness=12),
        hovertemplate="<b>%{y}</b><br>Period: %{x}<br>Underlying demand records: %{z:,.0f}<extra></extra>",
    )
)
heatmap_figure.update_layout(
    height=330,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=OCEAN["text"], size=12),
    dragmode="pan",
    margin=dict(l=20, r=20, t=10, b=30),
    xaxis_title=period_name.title(),
    yaxis_title=None,
)
heatmap_figure.update_xaxes(tickformat=tick_format_map[selected_granularity], linecolor=OCEAN["border"])
heatmap_figure.update_yaxes(linecolor=OCEAN["border"])
heatmap_visible_periods = {"Daily": 30, "Monthly": 18, "Yearly": 5}[selected_granularity]
if len(activity_dates) > heatmap_visible_periods:
    heatmap_figure.update_xaxes(
        range=[activity_dates[0], activity_dates[heatmap_visible_periods - 1]],
        rangeslider=dict(visible=True, thickness=0.10),
    )
st.plotly_chart(
    heatmap_figure,
    width="stretch",
    config={"displaylogo": False, "responsive": True, "scrollZoom": True},
)

# The final summary is calculated only after all three choices are known.
product_totals = filtered_df.groupby("Product_Code")["Daily_Net_Demand"].sum().sort_values(ascending=False)
if len(product_totals) == 1:
    product = product_totals.index[0]
    demand_value = f"{compact_number(product_totals.iloc[0])} units"
    demand_body = f"{product} averaged {period_df['Period_Net_Demand'].mean():,.0f} units per recorded {period_name}."
else:
    leader, second = product_totals.index[:2]
    gap = product_totals.iloc[0] - product_totals.iloc[1]
    gap_percent = gap / abs(product_totals.iloc[1]) * 100 if product_totals.iloc[1] != 0 else None
    demand_value = f"{leader} led"
    percent_text = f", or {gap_percent:.1f}%" if gap_percent is not None else ""
    demand_body = f"It exceeded {second} by {gap:,.0f} units{percent_text} within the selected dates."

window_size_map = {"Daily": 7, "Monthly": 3, "Yearly": 1}
trend_parts = []
for product in selected_products:
    product_periods = period_df[period_df["Product_Code"] == product].sort_values("Date").reset_index(drop=True)
    if len(product_periods) < 2:
        trend_parts.append(f"{product} has only one recorded {period_name}.")
        continue
    window_size = min(window_size_map[selected_granularity], len(product_periods))
    opening = product_periods.head(window_size)["Period_Net_Demand"].mean()
    closing = product_periods.tail(window_size)["Period_Net_Demand"].mean()
    if opening == 0:
        trend_parts.append(f"{product}'s opening level was zero.")
        continue
    change = (closing - opening) / abs(opening) * 100
    if abs(change) <= 5:
        trend_parts.append(f"{product} finished near its opening level.")
    elif change > 0:
        trend_parts.append(f"{product} ended {change:.1f}% higher.")
    else:
        trend_parts.append(f"{product} ended {abs(change):.1f}% lower.")

peak = period_df.loc[period_df["Period_Net_Demand"].idxmax()]
lowest = period_df.loc[period_df["Period_Net_Demand"].idxmin()]
busiest = period_df.loc[period_df["Order_Records"].idxmax()]
adjustments = filtered_df[filtered_df["Negative_Adjustment"] > 0]
adjustment_text = (
    "No negative demand adjustments appeared."
    if adjustments.empty
    else f"Adjustments appeared on {adjustments['Date'].nunique()} dates and totaled {adjustments['Negative_Adjustment'].sum():,.0f} units."
)
summary_items = [
    ("Demand comparison", demand_value, demand_body),
    ("Direction", "Opening → closing", " ".join(trend_parts)),
    (
        f"Highest {period_name}",
        format_period(peak["Date"]),
        f"{peak['Product_Code']} reached {peak['Period_Net_Demand']:,.0f} units. The lowest product-{period_name} was {lowest['Product_Code']} in {format_period(lowest['Date'])} at {lowest['Period_Net_Demand']:,.0f} units.",
    ),
    (
        "Order activity",
        f"{int(busiest['Order_Records']):,} records",
        f"{busiest['Product_Code']} was busiest in {format_period(busiest['Date'])}. {adjustment_text}",
    ),
]
summary_html = "".join(
    f'<div class="summary-item"><div class="summary-label">{escape(label)}</div><div class="summary-value">{escape(value)}</div><div class="summary-body">{escape(body)}</div></div>'
    for label, value, body in summary_items
)
st.markdown(
    f"""
    <section class="summary-shell" aria-label="Dynamic exploration summary">
        <div class="summary-heading-row"><div class="summary-heading">What did we learn from your selection?</div><div class="chapter-scope">{escape(scope_text)}</div></div>
        <div class="summary-grid">{summary_html}</div>
    </section>
    """,
    unsafe_allow_html=True,
)

is_partial_period = False
if selected_granularity == "Monthly":
    is_partial_period = selected_start_date.day != 1 or selected_end_date != selected_end_date + pd.offsets.MonthEnd(0)
elif selected_granularity == "Yearly":
    is_partial_period = not (
        selected_start_date.month == 1
        and selected_start_date.day == 1
        and selected_end_date.month == 12
        and selected_end_date.day == 31
    )
if is_partial_period:
    st.caption("The first or final aggregated period may be partial because the selected date range begins or ends inside that month or year.")

with st.expander(f"View the {len(filtered_df):,} filtered daily records"):
    st.caption("Each row represents one product on one recorded day. Missing dates are not automatically treated as zero demand.")
    st.dataframe(
        filtered_df,
        width="stretch",
        height=360,
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
            "Daily_Net_Demand": st.column_config.NumberColumn("Daily net demand", format="localized"),
            "Positive_Demand": st.column_config.NumberColumn("Positive demand", format="localized"),
            "Negative_Adjustment": st.column_config.NumberColumn("Negative adjustment", format="localized"),
            "Order_Records": st.column_config.NumberColumn("Order records", format="localized"),
        },
    )

with st.expander("Source, cleaning, and limitations"):
    st.markdown(
        """
        <div class="method-note">
            <strong>Source.</strong> FelixZhao, <em>Forecasts for Product Demand</em>, available on
            <a href="https://www.kaggle.com/datasets/felixzhao/productdemandforecasting" target="_blank">Kaggle</a> under the GPL 2 license.<br><br>
            <strong>Cleaning.</strong> The data was limited to 2014–2016 and to Product_1248 and Product_1359, the two products with the highest cleaned net demand. Parenthesized demand values were interpreted as negative adjustments, and records were aggregated by date and product. Exact duplicate source rows were retained rather than silently removed.<br><br>
            <strong>Limitations.</strong> Demand is not the same as confirmed sales, and a missing product-date is not automatically treated as zero demand. The app describes historical patterns and does not make a forecast.
        </div>
        """,
        unsafe_allow_html=True,
    )
