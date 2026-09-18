from html import escape
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Product Demand Explorer",
    page_icon="📊",
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
            --canvas: {OCEAN['canvas']};
            --surface: {OCEAN['surface']};
            --surface-subtle: {OCEAN['surface_subtle']};
            --text: {OCEAN['text']};
            --secondary: {OCEAN['secondary']};
            --tertiary: {OCEAN['tertiary']};
            --border: {OCEAN['border']};
            --divider: {OCEAN['divider']};
            --accent: {OCEAN['accent']};
            --accent-soft: {OCEAN['accent_soft']};
            --accent-text: {OCEAN['accent_text']};
        }}

        .stApp {{
            background:
                radial-gradient(circle at 88% 3%, rgba(14,165,233,.08), transparent 24rem),
                var(--canvas);
            color: var(--text);
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .block-container {{
            max-width: 1480px;
            padding-top: 2.4rem;
            padding-bottom: 4rem;
        }}

        .hero-kicker {{
            color: var(--accent-text);
            font-size: .74rem;
            font-weight: 750;
            letter-spacing: .12em;
            margin-bottom: .55rem;
            text-transform: uppercase;
        }}

        .hero-title {{
            color: var(--text);
            font-size: clamp(2rem, 3.1vw, 3.5rem);
            font-weight: 760;
            letter-spacing: -.045em;
            line-height: .98;
            margin: 0;
            max-width: 680px;
        }}

        .hero-intro {{
            color: var(--secondary);
            font-size: 1rem;
            line-height: 1.65;
            margin: 1rem 0 0;
            max-width: 690px;
        }}

        .filter-heading {{
            color: var(--tertiary);
            font-size: .72rem;
            font-weight: 700;
            letter-spacing: .09em;
            margin-bottom: .35rem;
            text-align: right;
            text-transform: uppercase;
        }}

        .insights-shell {{
            background: linear-gradient(110deg, var(--surface) 0%, var(--accent-soft) 150%);
            border: 1px solid var(--border);
            border-top: 3px solid var(--accent);
            border-radius: 16px;
            margin: 1.4rem 0 1.7rem;
            overflow: hidden;
            padding: 1.25rem 1.35rem 1.15rem;
        }}

        .insights-heading-row {{
            align-items: baseline;
            display: flex;
            gap: 1rem;
            justify-content: space-between;
            margin-bottom: 1rem;
        }}

        .insights-heading {{
            color: var(--text);
            font-size: 1.12rem;
            font-weight: 740;
            letter-spacing: -.018em;
        }}

        .insights-scope {{
            color: var(--tertiary);
            font-size: .78rem;
            text-align: right;
        }}

        .insight-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }}

        .insight-item {{
            min-width: 0;
            padding: .15rem 1.1rem .2rem;
        }}

        .insight-item:first-child {{
            padding-left: 0;
        }}

        .insight-item + .insight-item {{
            border-left: 1px solid var(--divider);
        }}

        .insight-label {{
            color: var(--tertiary);
            font-size: .7rem;
            font-weight: 720;
            letter-spacing: .08em;
            text-transform: uppercase;
        }}

        .insight-value {{
            color: var(--text);
            font-size: 1.12rem;
            font-weight: 760;
            letter-spacing: -.02em;
            line-height: 1.2;
            margin: .34rem 0 .38rem;
        }}

        .insight-body {{
            color: var(--secondary);
            font-size: .82rem;
            line-height: 1.48;
        }}

        .section-title {{
            color: var(--text);
            font-size: 1rem;
            font-weight: 740;
            letter-spacing: -.014em;
            margin-bottom: .15rem;
        }}

        .section-copy {{
            color: var(--secondary);
            font-size: .8rem;
            line-height: 1.45;
            margin-bottom: .5rem;
        }}

        [data-testid="stVerticalBlockBorderWrapper"] {{
            background: rgba(255,255,255,.82);
            border-color: var(--border) !important;
            border-radius: 16px;
            box-shadow: 0 12px 34px rgba(20, 48, 59, .045);
        }}

        [data-testid="stExpander"] {{
            background: var(--surface);
            border-color: var(--border);
        }}

        @media (max-width: 980px) {{
            .block-container {{ padding-top: 1.4rem; }}
            .filter-heading {{ margin-top: .8rem; text-align: left; }}
            .insight-grid {{
                grid-template-columns: repeat(2, minmax(0, 1fr));
                row-gap: 1rem;
            }}
            .insight-item:nth-child(3) {{ border-left: none; padding-left: 0; }}
            .insight-item:nth-child(n+3) {{
                border-top: 1px solid var(--divider);
                padding-top: 1rem;
            }}
        }}

        @media (max-width: 640px) {{
            .hero-title {{ font-size: 2.25rem; }}
            .insights-heading-row {{
                align-items: flex-start;
                flex-direction: column;
                gap: .3rem;
            }}
            .insights-scope {{ text-align: left; }}
            .insight-grid {{ grid-template-columns: 1fr; }}
            .insight-item,
            .insight-item:first-child,
            .insight-item:nth-child(3) {{
                border-left: none;
                padding: .85rem 0;
            }}
            .insight-item + .insight-item {{
                border-top: 1px solid var(--divider);
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                scroll-behavior: auto !important;
                transition-duration: .01ms !important;
            }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "Product_Demand_2014_2016_Top2_Daily.csv"
    data = pd.read_csv(data_path, parse_dates=["Date"])
    return data.sort_values(["Date", "Product_Code"])


def compact_number(value):
    absolute_value = abs(value)
    if absolute_value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if absolute_value >= 1_000:
        return f"{value / 1_000:.0f}K"
    return f"{value:,.0f}"


def style_cartesian_figure(figure, height=370):
    figure.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family=(
                '-apple-system, BlinkMacSystemFont, "Segoe UI Variable", '
                '"Inter", "PingFang SC", sans-serif'
            ),
            color=OCEAN["text"],
            size=12,
        ),
        hoverlabel=dict(
            bgcolor=OCEAN["surface"],
            bordercolor=OCEAN["border"],
            font_color=OCEAN["text"],
        ),
        margin=dict(l=20, r=18, t=15, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
            title=None,
        ),
    )
    figure.update_xaxes(
        gridcolor=OCEAN["chart_grid"],
        linecolor=OCEAN["border"],
        zeroline=False,
    )
    figure.update_yaxes(
        gridcolor=OCEAN["chart_grid"],
        linecolor=OCEAN["border"],
        zeroline=False,
    )
    return figure


df = load_data()
all_products = sorted(df["Product_Code"].unique())
minimum_date = df["Date"].min().date()
maximum_date = df["Date"].max().date()


header_left, header_right = st.columns(
    [1.5, 1.0],
    vertical_alignment="bottom",
    gap="large",
)

with header_left:
    st.markdown(
        """
        <div class="hero-kicker">Internal demand operations · 2014–2016</div>
        <h1 class="hero-title">Product Demand Explorer</h1>
        <p class="hero-intro">
            This dashboard is designed for internal operations managers and
            demand planners. It shows how demand and order activity for
            Product_1248 and Product_1359 changed across selected time periods,
            helping teams focus on the products, dates, and level of detail
            relevant to their planning work.
        </p>
        """,
        unsafe_allow_html=True,
    )

with header_right:
    st.markdown(
        '<div class="filter-heading">Adjust the view</div>',
        unsafe_allow_html=True,
    )
    product_column, date_column, granularity_column = st.columns(
        [1.0, 1.55, 1.0],
        gap="small",
    )

    with product_column:
        selected_products = st.multiselect(
            "Product",
            options=all_products,
            default=all_products,
            help=(
                "Select one product for an individual view or both products "
                "for comparison."
            ),
        )

    with date_column:
        selected_date_range = st.date_input(
            "Date range",
            value=(minimum_date, maximum_date),
            min_value=minimum_date,
            max_value=maximum_date,
            help="Only records within this date range will be included.",
        )

    with granularity_column:
        selected_granularity = st.selectbox(
            "Time detail",
            options=["Daily", "Monthly", "Yearly"],
            index=1,
            help="Choose whether each period represents a day, month, or year.",
        )


if not selected_products:
    st.warning("Select at least one product to continue.")
    st.stop()

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
    st.warning("No data is available for the selected filters.")
    st.stop()


frequency_map = {"Daily": "D", "Monthly": "MS", "Yearly": "YS"}
period_name_map = {"Daily": "day", "Monthly": "month", "Yearly": "year"}
date_format_map = {
    "Daily": "%B %d, %Y",
    "Monthly": "%B %Y",
    "Yearly": "%Y",
}
tick_format_map = {
    "Daily": "%b %d\n%Y",
    "Monthly": "%b\n%Y",
    "Yearly": "%Y",
}
visible_period_map = {"Daily": 14, "Monthly": 12, "Yearly": 5}

selected_frequency = frequency_map[selected_granularity]
period_name = period_name_map[selected_granularity]
date_format = date_format_map[selected_granularity]
visible_periods = visible_period_map[selected_granularity]


def format_period(date_value):
    return pd.Timestamp(date_value).strftime(date_format)


period_df = (
    filtered_df.groupby(
        [pd.Grouper(key="Date", freq=selected_frequency), "Product_Code"],
        as_index=False,
    )
    .agg(
        Period_Net_Demand=("Daily_Net_Demand", "sum"),
        Order_Records=("Order_Records", "sum"),
        Negative_Adjustment=("Negative_Adjustment", "sum"),
    )
    .sort_values(["Date", "Product_Code"])
)


product_totals = (
    filtered_df.groupby("Product_Code")["Daily_Net_Demand"]
    .sum()
    .sort_values(ascending=False)
)

if len(product_totals) == 1:
    product = product_totals.index[0]
    total_demand = product_totals.iloc[0]
    average_period_demand = period_df["Period_Net_Demand"].mean()
    demand_value = f"{compact_number(total_demand)} units"
    demand_body = (
        f"{product} averaged {average_period_demand:,.0f} units per recorded "
        f"{period_name} within the selected dates."
    )
else:
    leading_product = product_totals.index[0]
    second_product = product_totals.index[1]
    demand_gap = product_totals.iloc[0] - product_totals.iloc[1]
    demand_gap_percent = (
        demand_gap / abs(product_totals.iloc[1]) * 100
        if product_totals.iloc[1] != 0
        else None
    )
    demand_value = f"{leading_product} led"
    percentage_text = (
        f", or {demand_gap_percent:.1f}%" if demand_gap_percent is not None else ""
    )
    demand_body = (
        f"It exceeded {second_product} by {demand_gap:,.0f} units"
        f"{percentage_text} within the selected dates."
    )


window_size_map = {"Daily": 7, "Monthly": 3, "Yearly": 1}
trend_parts = []
for product in selected_products:
    product_periods = (
        period_df.loc[period_df["Product_Code"] == product]
        .sort_values("Date")
        .reset_index(drop=True)
    )
    if len(product_periods) < 2:
        trend_parts.append(f"{product} has only one recorded {period_name}.")
        continue

    window_size = min(window_size_map[selected_granularity], len(product_periods))
    starting_average = product_periods.head(window_size)["Period_Net_Demand"].mean()
    ending_average = product_periods.tail(window_size)["Period_Net_Demand"].mean()

    if starting_average == 0:
        trend_parts.append(f"{product}'s opening level was zero.")
        continue

    change_percent = (ending_average - starting_average) / abs(starting_average) * 100
    if abs(change_percent) <= 5:
        trend_parts.append(f"{product} finished near its opening level.")
    elif change_percent > 0:
        trend_parts.append(f"{product} ended {change_percent:.1f}% higher.")
    else:
        trend_parts.append(f"{product} ended {abs(change_percent):.1f}% lower.")

trend_value = "Opening → closing"
trend_body = " ".join(trend_parts)


peak_period = period_df.loc[period_df["Period_Net_Demand"].idxmax()]
lowest_period = period_df.loc[period_df["Period_Net_Demand"].idxmin()]
peak_value = format_period(peak_period["Date"])
peak_body = (
    f"{peak_period['Product_Code']} reached {peak_period['Period_Net_Demand']:,.0f} "
    f"units. The lowest recorded product-{period_name} was "
    f"{lowest_period['Product_Code']} in {format_period(lowest_period['Date'])} "
    f"at {lowest_period['Period_Net_Demand']:,.0f} units."
)


busiest_period = period_df.loc[period_df["Order_Records"].idxmax()]
adjustment_rows = filtered_df.loc[filtered_df["Negative_Adjustment"] > 0]
activity_value = f"{int(busiest_period['Order_Records']):,} records"
if adjustment_rows.empty:
    adjustment_description = "No negative demand adjustments appeared."
else:
    adjustment_description = (
        f"Adjustments appeared on {adjustment_rows['Date'].nunique()} dates across "
        f"{len(adjustment_rows)} product-date rows, totaling "
        f"{adjustment_rows['Negative_Adjustment'].sum():,.0f} units."
    )
activity_body = (
    f"{busiest_period['Product_Code']} was busiest in "
    f"{format_period(busiest_period['Date'])}. {adjustment_description}"
)


scope_text = (
    f"{' & '.join(selected_products)} · "
    f"{selected_start_date.strftime('%b %d, %Y')}–"
    f"{selected_end_date.strftime('%b %d, %Y')} · "
    f"{selected_granularity}"
)

insight_items = [
    ("Demand comparison", demand_value, demand_body),
    ("Direction", trend_value, trend_body),
    (f"Highest {period_name}", peak_value, peak_body),
    ("Order activity", activity_value, activity_body),
]

insight_html = "".join(
    f"""
    <div class="insight-item">
        <div class="insight-label">{escape(label)}</div>
        <div class="insight-value">{escape(value)}</div>
        <div class="insight-body">{escape(body)}</div>
    </div>
    """
    for label, value, body in insight_items
)

st.markdown(
    f"""
    <section class="insights-shell" aria-label="Key insights">
        <div class="insights-heading-row">
            <div class="insights-heading">Key insights</div>
            <div class="insights-scope">{escape(scope_text)}</div>
        </div>
        <div class="insight-grid">{insight_html}</div>
    </section>
    """,
    unsafe_allow_html=True,
)


product_colors = {
    product: OCEAN["accent"] if index == 0 else OCEAN["chart_comparison"]
    for index, product in enumerate(selected_products)
}

trend_column, bar_column = st.columns(2, gap="medium")

with trend_column:
    with st.container(border=True):
        st.markdown(
            '<div class="section-title">How demand changed over time</div>'
            '<div class="section-copy">Follow each selected product across the '
            'current date range.</div>',
            unsafe_allow_html=True,
        )
        trend_figure = px.line(
            period_df,
            x="Date",
            y="Period_Net_Demand",
            color="Product_Code",
            markers=selected_granularity != "Daily",
            color_discrete_map=product_colors,
            labels={
                "Date": period_name.title(),
                "Period_Net_Demand": "Net demand",
                "Product_Code": "Product",
            },
            custom_data=["Order_Records", "Negative_Adjustment"],
        )
        trend_figure.update_traces(
            line_width=2.7,
            marker_size=5,
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Period: %{x}<br>"
                "Net demand: %{y:,.0f}<br>"
                "Order records: %{customdata[0]:,.0f}<br>"
                "Negative adjustment: %{customdata[1]:,.0f}"
                "<extra></extra>"
            ),
        )
        trend_figure.update_layout(
            hovermode="x unified",
            showlegend=len(selected_products) > 1,
        )
        trend_figure.update_xaxes(tickformat=tick_format_map[selected_granularity])
        style_cartesian_figure(trend_figure)
        st.plotly_chart(
            trend_figure,
            width="stretch",
            config={"displaylogo": False, "responsive": True},
        )

with bar_column:
    with st.container(border=True):
        st.markdown(
            '<div class="section-title">Demand in each selected period</div>'
            '<div class="section-copy">Values stay separate by product. Use the '
            'range slider when more periods are available.</div>',
            unsafe_allow_html=True,
        )
        bar_source = period_df.copy()
        bar_source["Demand_Label"] = bar_source["Period_Net_Demand"].map(
            compact_number
        )
        bar_figure = px.bar(
            bar_source,
            x="Date",
            y="Period_Net_Demand",
            color="Product_Code",
            barmode="group",
            text="Demand_Label",
            color_discrete_map=product_colors,
            labels={
                "Date": period_name.title(),
                "Period_Net_Demand": "Net demand",
                "Product_Code": "Product",
            },
            custom_data=["Order_Records", "Negative_Adjustment"],
        )
        bar_figure.update_traces(
            textposition="outside",
            cliponaxis=False,
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Period: %{x}<br>"
                "Net demand: %{y:,.0f}<br>"
                "Order records: %{customdata[0]:,.0f}<br>"
                "Negative adjustment: %{customdata[1]:,.0f}"
                "<extra></extra>"
            ),
        )
        available_dates = (
            bar_source["Date"].drop_duplicates().sort_values().reset_index(drop=True)
        )
        bar_figure.update_xaxes(tickformat=tick_format_map[selected_granularity])
        if len(available_dates) > visible_periods:
            date_padding = {
                "Daily": pd.Timedelta(days=1),
                "Monthly": pd.Timedelta(days=15),
                "Yearly": pd.Timedelta(days=150),
            }[selected_granularity]
            bar_figure.update_xaxes(
                range=[
                    available_dates.iloc[0] - date_padding,
                    available_dates.iloc[visible_periods - 1] + date_padding,
                ],
                rangeslider=dict(visible=True, thickness=0.08),
            )
        bar_figure.update_layout(
            hovermode="x unified",
            showlegend=len(selected_products) > 1,
            dragmode="pan",
        )
        style_cartesian_figure(bar_figure)
        st.plotly_chart(
            bar_figure,
            width="stretch",
            config={"displaylogo": False, "responsive": True, "scrollZoom": True},
        )


with st.container(border=True):
    st.markdown(
        '<div class="section-title">When demand records were most active</div>'
        '<div class="section-copy">Darker cells represent more underlying demand '
        'records, not higher demand volume.</div>',
        unsafe_allow_html=True,
    )

    activity_matrix = (
        period_df.pivot(
            index="Product_Code",
            columns="Date",
            values="Order_Records",
        )
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
            colorscale=[
                [0.00, "#EFF5F7"],
                [0.30, "#CDEDFC"],
                [0.65, "#68C7F1"],
                [1.00, "#036B9D"],
            ],
            colorbar=dict(title="Records", thickness=12),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Period: %{x}<br>"
                "Underlying demand records: %{z:,.0f}"
                "<extra></extra>"
            ),
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
    heatmap_figure.update_xaxes(
        tickformat=tick_format_map[selected_granularity],
        linecolor=OCEAN["border"],
    )
    heatmap_figure.update_yaxes(linecolor=OCEAN["border"])

    heatmap_visible_periods = {
        "Daily": 30,
        "Monthly": 18,
        "Yearly": 5,
    }[selected_granularity]
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


is_partial_period = False
if selected_granularity == "Monthly":
    is_partial_period = (
        selected_start_date.day != 1
        or selected_end_date != selected_end_date + pd.offsets.MonthEnd(0)
    )
elif selected_granularity == "Yearly":
    is_partial_period = not (
        selected_start_date.month == 1
        and selected_start_date.day == 1
        and selected_end_date.month == 12
        and selected_end_date.day == 31
    )

if is_partial_period:
    st.caption(
        "The first or final aggregated period may be partial because the selected "
        "date range begins or ends inside that month or year."
    )


with st.expander("View filtered data"):
    st.caption(
        "Each row represents one product on one recorded day. Missing dates are "
        "not automatically treated as zero demand."
    )
    st.dataframe(
        filtered_df,
        width="stretch",
        height=360,
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
            "Daily_Net_Demand": st.column_config.NumberColumn(
                "Daily net demand", format="localized"
            ),
            "Positive_Demand": st.column_config.NumberColumn(
                "Positive demand", format="localized"
            ),
            "Negative_Adjustment": st.column_config.NumberColumn(
                "Negative adjustment", format="localized"
            ),
            "Order_Records": st.column_config.NumberColumn(
                "Order records", format="localized"
            ),
        },
    )

