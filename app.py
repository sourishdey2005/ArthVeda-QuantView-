"""
ArthVeda QuantView
------------------
Production-grade financial market data analysis dashboard.
Run with: streamlit run app.py

Dependencies:
    pip install streamlit pandas numpy plotly openpyxl scipy xlsxwriter
"""

import io
import warnings
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="ArthVeda QuantView",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# THEME
# ─────────────────────────────────────────────

DARK_THEME = {
    "bg": "#080a0f",
    "surface": "#12151c",
    "border": "#252a34",
    "text": "#e8eaed",
    "subtext": "#6b7280",
    "accent": "#3b82f6",
    "green": "#10b981",
    "red": "#ef4444",
    "yellow": "#f59e0b",
    "purple": "#8b5cf6",
    "orange": "#f97316",
    "cyan": "#06b6d4",
    "pink": "#ec4899",
    "lime": "#84cc16",
    "teal": "#14b8a6",
    "indigo": "#6366f1",
    "plotly_template": "plotly_dark",
    "paper_bg": "#12151c",
    "plot_bg": "#080a0f",
    "gridcolor": "#1e222b",
}

LIGHT_THEME = {
    "bg": "#ffffff",
    "surface": "#f6f8fa",
    "border": "#d0d7de",
    "text": "#1f2328",
    "subtext": "#656d76",
    "accent": "#0969da",
    "green": "#1a7f37",
    "red": "#cf222e",
    "yellow": "#9a6700",
    "purple": "#8250df",
    "orange": "#bc4c00",
    "plotly_template": "plotly_white",
    "paper_bg": "#f6f8fa",
    "plot_bg": "#ffffff",
    "gridcolor": "#d0d7de",
}


def get_theme():
    # App UI is dark-mode only.
    return DARK_THEME


def apply_css(t):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'IBM Plex Sans', sans-serif;
        background-color: {t['bg']};
        color: {t['text']};
    }}
    .stApp {{ background-color: {t['bg']}; }}
    section[data-testid="stSidebar"] {{
        background-color: {t['surface']};
        border-right: 1px solid {t['border']};
    }}
    section[data-testid="stSidebar"]::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, {t['accent']}, {t['purple']}, {t['cyan']});
    }}
    .block-container {{ padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }}
    h1, h2, h3, h4 {{ font-family: 'IBM Plex Sans', sans-serif; font-weight: 600; color: {t['text']}; }}
    h1 {{ 
        font-size: 1.8rem; 
        background: linear-gradient(135deg, {t['text']} 0%, {t['accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .metric-card {{
        background: linear-gradient(145deg, {t['surface']}, {t['bg']});
        border: 1px solid {t['border']};
        border-radius: 12px;
        padding: 1rem 1.25rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }}
    .metric-value {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.5rem;
        font-weight: 600;
        color: {t['accent']};
    }}
    .metric-label {{
        font-size: 0.75rem;
        color: {t['subtext']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }}
    .section-header {{
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: {t['subtext']};
        border-bottom: 1px solid {t['border']};
        padding-bottom: 0.5rem;
        margin: 1.5rem 0 1rem 0;
        position: relative;
    }}
    .section-header::after {{
        content: "";
        position: absolute;
        bottom: -1px;
        left: 0;
        width: 60px;
        height: 2px;
        background: linear-gradient(90deg, {t['accent']}, transparent);
    }}
    footer {{ color: {t['subtext']}; font-size: 0.75rem; text-align: center; padding: 1.5rem 0 0.5rem 0; border-top: 1px solid {t['border']}; margin-top: 2rem; }}
    .stDataFrame {{ border: 1px solid {t['border']}; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }}
    div[data-testid="metric-container"] {{
        background: linear-gradient(145deg, {t['surface']}, {t['bg']});
        border: 1px solid {t['border']};
        border-radius: 10px;
        padding: 0.75rem 1rem;
        box-shadow: 0 2px 15px rgba(0,0,0,0.2);
    }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 0.5rem; background: {t['surface']}; border-radius: 10px; padding: 0.25rem; }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        color: {t['subtext']};
        border-radius: 8px;
        font-weight: 500;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {t['accent']}, {t['purple']});
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(59,130,246,0.4);
    }}
    .stFileUploader {{
        background: {t['surface']};
        border-radius: 12px;
        padding: 1rem;
        border: 2px dashed {t['border']};
    }}
    .stFileUploader:hover {{
        border-color: {t['accent']};
    }}
    div[data-testid="stExpander"] {{
        background: {t['surface']};
        border-radius: 10px;
        border: 1px solid {t['border']};
    }}
    .upload-zone {{
        border: 2px dashed {t['border']};
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        background: linear-gradient(145deg, {t['surface']}, {t['bg']});
        transition: all 0.3s ease;
    }}
    .upload-zone:hover {{
        border-color: {t['accent']};
        box-shadow: 0 0 20px rgba(59,130,246,0.2);
    }}
    .logo-text {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        background: linear-gradient(90deg, {t['accent']}, {t['purple']}, {t['cyan']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATA LOADING & PREPROCESSING
# ─────────────────────────────────────────────

COLUMN_ALIASES = {
    "date": ["date", "datetime", "time", "timestamp", "trade_date", "trading_date"],
    "open": ["open", "open_price", "opening", "o"],
    "high": ["high", "high_price", "h"],
    "low": ["low", "low_price", "l"],
    "close": ["close", "close_price", "closing", "c", "last", "last_price"],
    "adj_close": ["adj close", "adj_close", "adjusted close", "adjusted_close"],
    "volume": ["volume", "vol", "shares", "shares_traded"],
    "symbol": ["symbol", "ticker", "stock", "code", "scrip"],
    "name": ["security name", "name", "company", "company_name", "security"],
    "exchange": ["listing exchange", "exchange", "market"],
}


@st.cache_data(show_spinner=False)
def load_data(uploaded_file):
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, low_memory=False)
        elif name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file format. Use CSV or Excel."
        return df, None
    except Exception as e:
        return None, str(e)


def find_column(df, key):
    aliases = COLUMN_ALIASES.get(key, [key])
    cols_lower = {c.lower().strip(): c for c in df.columns}
    for alias in aliases:
        if alias.lower() in cols_lower:
            return cols_lower[alias.lower()]
    return None


def preprocess_data(df):
    df = df.copy()
    df.columns = df.columns.str.strip()

    # Map columns
    col_map = {}
    for key in COLUMN_ALIASES:
        found = find_column(df, key)
        if found:
            col_map[key] = found

    # Parse date
    if "date" in col_map:
        try:
            df[col_map["date"]] = pd.to_datetime(df[col_map["date"]], infer_datetime_format=True)
            df = df.sort_values(col_map["date"])
        except Exception:
            pass

    # Remove duplicates
    df = df.drop_duplicates()

    # Forward-fill numeric columns, drop rows if close is missing
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    df[numeric_cols] = df[numeric_cols].ffill()

    if "close" in col_map:
        df = df.dropna(subset=[col_map["close"]])

    return df, col_map


# ─────────────────────────────────────────────
# TECHNICAL INDICATORS
# ─────────────────────────────────────────────

def compute_sma(series, window):
    return series.rolling(window=window, min_periods=1).mean()


def compute_ema(series, window):
    return series.ewm(span=window, adjust=False).mean()


def compute_bollinger(series, window=20, num_std=2):
    sma = compute_sma(series, window)
    std = series.rolling(window=window, min_periods=1).std()
    return sma, sma + num_std * std, sma - num_std * std


def compute_rsi(series, window=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(window=window, min_periods=1).mean()
    loss = (-delta.clip(upper=0)).rolling(window=window, min_periods=1).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def compute_macd(series, fast=12, slow=26, signal=9):
    ema_fast = compute_ema(series, fast)
    ema_slow = compute_ema(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = compute_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def compute_atr(df, high_col, low_col, close_col, window=14):
    high = df[high_col]
    low = df[low_col]
    close = df[close_col]
    prev_close = close.shift(1)
    tr = pd.concat([
        high - low,
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)
    return tr.rolling(window=window, min_periods=1).mean()


def compute_momentum(series, window=10):
    return series - series.shift(window)


def compute_rolling_slope(series, window=20):
    slopes = []
    for i in range(len(series)):
        if i < window:
            slopes.append(np.nan)
        else:
            y = series.iloc[i - window:i].values
            x = np.arange(window)
            slope = np.polyfit(x, y, 1)[0]
            slopes.append(slope)
    return pd.Series(slopes, index=series.index)


def compute_drawdown(series):
    rolling_max = series.cummax()
    drawdown = (series - rolling_max) / rolling_max
    return drawdown


def compute_zscore(series, window=20):
    mean = series.rolling(window=window, min_periods=1).mean()
    std = series.rolling(window=window, min_periods=1).std()
    return (series - mean) / std.replace(0, np.nan)


def compute_support_resistance(series, window=20):
    support = series.rolling(window=window, min_periods=1).min()
    resistance = series.rolling(window=window, min_periods=1).max()
    return support, resistance


# ─────────────────────────────────────────────
# PLOTTING HELPERS
# ─────────────────────────────────────────────

def get_chart_style():
    # Charts stay white + high-contrast regardless of the Streamlit theme.
    return {
        "plotly_template": "plotly_white",
        "paper_bg": "#ffffff",
        "plot_bg": "#ffffff",
        "surface": "#ffffff",
        "border": "#d0d7de",
        "gridcolor": "#e5e7eb",
        "text": "#111827",
        "subtext": "#374151",
        "neutral_bar": "#334155",
    }


def base_layout(t, title="", height=420):
    chart = get_chart_style()
    return dict(
        template=chart["plotly_template"],
        paper_bgcolor=chart["paper_bg"],
        plot_bgcolor=chart["plot_bg"],
        font=dict(family="IBM Plex Sans, sans-serif", color=chart["text"], size=12),
        title=dict(text=title, font=dict(size=13, color=chart["subtext"]), x=0),
        height=height,
        margin=dict(l=48, r=20, t=42, b=40),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font=dict(size=11, color=chart["text"])),
        xaxis=dict(gridcolor=chart["gridcolor"], linecolor=chart["border"], showgrid=True),
        yaxis=dict(gridcolor=chart["gridcolor"], linecolor=chart["border"], showgrid=True),
        hoverlabel=dict(bgcolor=chart["surface"], bordercolor=chart["border"], font_size=12),
    )


def fig_update(fig, t, title="", height=420):
    layout = base_layout(t, title, height)
    fig.update_layout(**layout)
    chart = get_chart_style()
    fig.update_xaxes(
        showgrid=True,
        gridcolor=chart["gridcolor"],
        linecolor=chart["border"],
        tickfont=dict(color=chart["text"]),
        title_font=dict(color=chart["subtext"]),
        zerolinecolor=chart["border"],
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=chart["gridcolor"],
        linecolor=chart["border"],
        tickfont=dict(color=chart["text"]),
        title_font=dict(color=chart["subtext"]),
        zerolinecolor=chart["border"],
    )
    is_3d = any(
        isinstance(trace, (go.Surface, go.Scatter3d, go.Mesh3d))
        for trace in fig.data
    )
    if is_3d:
        fig.update_layout(
            scene=dict(
                bgcolor=chart["plot_bg"],
                xaxis=dict(
                    backgroundcolor=chart["paper_bg"],
                    gridcolor=chart["gridcolor"],
                    showbackground=True,
                ),
                yaxis=dict(
                    backgroundcolor=chart["paper_bg"],
                    gridcolor=chart["gridcolor"],
                    showbackground=True,
                ),
                zaxis=dict(
                    backgroundcolor=chart["paper_bg"],
                    gridcolor=chart["gridcolor"],
                    showbackground=True,
                ),
            )
        )
    return fig


def plot_line_close(df, date_col, close_col, t, symbol=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[close_col],
        mode="lines", name="Close",
        line=dict(color=t["accent"], width=1.5),
        fill="tozeroy", fillcolor=f"rgba(88,166,255,0.06)"
    ))
    title = f"Close Price" + (f" — {symbol}" if symbol else "")
    return fig_update(fig, t, title)


def plot_candlestick(df, col_map, t, symbol=None):
    d = df[col_map["date"]]
    fig = go.Figure(data=[go.Candlestick(
        x=d,
        open=df[col_map["open"]] if "open" in col_map else df[col_map["close"]],
        high=df[col_map["high"]] if "high" in col_map else df[col_map["close"]],
        low=df[col_map["low"]] if "low" in col_map else df[col_map["close"]],
        close=df[col_map["close"]],
        increasing_line_color=t["green"],
        decreasing_line_color=t["red"],
        name="OHLC"
    )])
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig_update(fig, t, f"Candlestick Chart" + (f" — {symbol}" if symbol else ""), 460)


def plot_moving_averages(df, date_col, close_col, t, windows=(20, 50, 100, 200)):
    colors = [t["accent"], t["green"], t["yellow"], t["purple"]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[close_col],
        mode="lines", name="Close",
        line=dict(color=t["subtext"], width=1)
    ))
    for w, c in zip(windows, colors):
        if len(df) >= w:
            ma = compute_sma(df[close_col], w)
            fig.add_trace(go.Scatter(
                x=df[date_col], y=ma,
                mode="lines", name=f"SMA {w}",
                line=dict(color=c, width=1.5)
            ))
    return fig_update(fig, t, "Moving Averages (SMA)")


def plot_bollinger(df, date_col, close_col, t):
    sma, upper, lower = compute_bollinger(df[close_col])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=upper, name="Upper Band",
        line=dict(color=t["yellow"], width=1, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=df[date_col], y=lower, name="Lower Band",
        line=dict(color=t["yellow"], width=1, dash="dash"),
        fill="tonexty", fillcolor="rgba(210,153,34,0.06)"
    ))
    fig.add_trace(go.Scatter(
        x=df[date_col], y=sma, name="SMA 20",
        line=dict(color=t["subtext"], width=1)
    ))
    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[close_col], name="Close",
        line=dict(color=t["accent"], width=1.5)
    ))
    return fig_update(fig, t, "Bollinger Bands (20, 2σ)")


def plot_price_distribution(df, close_col, t):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df[close_col], nbinsx=60,
        name="Price Freq",
        marker_color=t["accent"], opacity=0.7,
        histnorm="probability density"
    ))
    # KDE approximation via smoothed histogram
    from numpy import histogram, linspace
    counts, bins = histogram(df[close_col].dropna(), bins=60, density=True)
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    fig.add_trace(go.Scatter(
        x=bin_centers, y=counts, mode="lines",
        name="Density", line=dict(color=t["orange"], width=2)
    ))
    return fig_update(fig, t, "Price Distribution (Density)")


def plot_log_price(df, date_col, close_col, t):
    fig = go.Figure()
    log_p = np.log(df[close_col].replace(0, np.nan))
    fig.add_trace(go.Scatter(
        x=df[date_col], y=log_p, mode="lines",
        name="Log Close", line=dict(color=t["purple"], width=1.5)
    ))
    return fig_update(fig, t, "Log Price")


def plot_rolling_minmax(df, date_col, close_col, t, window=20):
    rolling_max = df[close_col].rolling(window, min_periods=1).max()
    rolling_min = df[close_col].rolling(window, min_periods=1).min()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=rolling_max, name=f"Roll Max ({window})",
        line=dict(color=t["green"], width=1, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=df[date_col], y=rolling_min, name=f"Roll Min ({window})",
        line=dict(color=t["red"], width=1, dash="dot"),
        fill="tonexty", fillcolor="rgba(63,185,80,0.05)"
    ))
    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[close_col], name="Close",
        line=dict(color=t["accent"], width=1.5)
    ))
    return fig_update(fig, t, f"Rolling Min/Max Band ({window}d)")


def plot_volume_bar(df, date_col, vol_col, close_col, t):
    colors = [t["green"] if c >= o else t["red"]
              for c, o in zip(df[close_col], df[close_col].shift(1).fillna(df[close_col]))]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[date_col], y=df[vol_col],
        marker_color=colors, name="Volume", opacity=0.9
    ))
    return fig_update(fig, t, "Volume")


def plot_volume_ma(df, date_col, vol_col, t, window=20):
    vol_ma = compute_sma(df[vol_col], window)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[date_col], y=df[vol_col],
        name="Volume", marker_color=t["accent"], opacity=0.75
    ))
    fig.add_trace(go.Scatter(
        x=df[date_col], y=vol_ma, name=f"Volume MA ({window})",
        line=dict(color=t["orange"], width=2)
    ))
    return fig_update(fig, t, f"Volume with MA ({window}d)")


def plot_volume_spikes(df, date_col, vol_col, t, threshold=2.0):
    vol_mean = df[vol_col].mean()
    vol_std = df[vol_col].std()
    spike_mask = df[vol_col] > (vol_mean + threshold * vol_std)
    neutral = get_chart_style()["neutral_bar"]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[date_col], y=df[vol_col],
        marker_color=[t["red"] if s else neutral for s in spike_mask],
        name="Volume", opacity=0.9
    ))
    fig.add_hline(y=vol_mean + threshold * vol_std,
                  line_dash="dash", line_color=t["yellow"],
                  annotation_text=f"Spike Threshold ({threshold}σ)")
    return fig_update(fig, t, "Volume Spike Detection")


def plot_volume_distribution(df, vol_col, t):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df[vol_col], nbinsx=50,
        marker_color=t["purple"], opacity=0.75, name="Volume"
    ))
    return fig_update(fig, t, "Volume Distribution")


def plot_daily_returns(df, date_col, close_col, t):
    returns = df[close_col].pct_change().dropna()
    colors = [t["green"] if r >= 0 else t["red"] for r in returns]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[date_col].iloc[1:], y=returns,
        marker_color=colors, name="Daily Return", opacity=0.9
    ))
    return fig_update(fig, t, "Daily Returns")


def plot_cumulative_returns(df, date_col, close_col, t):
    cum_ret = (1 + df[close_col].pct_change().fillna(0)).cumprod() - 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=cum_ret * 100,
        mode="lines", name="Cumulative Return (%)",
        line=dict(color=t["green"], width=2),
        fill="tozeroy", fillcolor="rgba(63,185,80,0.07)"
    ))
    fig.update_yaxes(ticksuffix="%")
    return fig_update(fig, t, "Cumulative Returns")


def plot_rolling_volatility(df, date_col, close_col, t, window=20):
    vol = df[close_col].pct_change().rolling(window, min_periods=1).std() * np.sqrt(252) * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=vol,
        mode="lines", name=f"Rolling Volatility ({window}d)",
        line=dict(color=t["yellow"], width=2),
        fill="tozeroy", fillcolor="rgba(210,153,34,0.07)"
    ))
    fig.update_yaxes(ticksuffix="%")
    return fig_update(fig, t, f"Rolling Annualised Volatility ({window}d)")


def plot_drawdown(df, date_col, close_col, t):
    dd = compute_drawdown(df[close_col]) * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=dd,
        mode="lines", name="Drawdown",
        line=dict(color=t["red"], width=1.5),
        fill="tozeroy", fillcolor="rgba(248,81,73,0.1)"
    ))
    fig.update_yaxes(ticksuffix="%")
    return fig_update(fig, t, "Drawdown (%)")


def plot_rsi(df, date_col, close_col, t, window=14):
    rsi = compute_rsi(df[close_col], window)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=rsi, name=f"RSI ({window})",
        line=dict(color=t["purple"], width=2)
    ))
    fig.add_hline(y=70, line_dash="dash", line_color=t["red"], opacity=0.6)
    fig.add_hline(y=30, line_dash="dash", line_color=t["green"], opacity=0.6)
    fig.add_hrect(y0=30, y1=70, fillcolor="rgba(88,166,255,0.04)", line_width=0)
    fig.update_yaxes(range=[0, 100])
    return fig_update(fig, t, f"RSI ({window})")


def plot_macd(df, date_col, close_col, t):
    macd_line, signal_line, histogram = compute_macd(df[close_col])
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.6, 0.4], vertical_spacing=0.04)
    fig.add_trace(go.Scatter(
        x=df[date_col], y=macd_line, name="MACD",
        line=dict(color=t["accent"], width=1.5)
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df[date_col], y=signal_line, name="Signal",
        line=dict(color=t["orange"], width=1.5)
    ), row=1, col=1)
    colors = [t["green"] if h >= 0 else t["red"] for h in histogram]
    fig.add_trace(go.Bar(
        x=df[date_col], y=histogram,
        marker_color=colors, name="Histogram", opacity=0.7
    ), row=2, col=1)
    fig = fig_update(fig, t, "MACD (12, 26, 9)", 460)
    fig.update_xaxes(gridcolor="#e5e7eb", linecolor="#d0d7de", showgrid=True)
    fig.update_yaxes(gridcolor="#e5e7eb", linecolor="#d0d7de", showgrid=True)
    return fig


def plot_ema_multi(df, date_col, close_col, t, windows=(9, 21, 55)):
    colors = [t["accent"], t["green"], t["orange"]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[close_col], name="Close",
        line=dict(color=t["subtext"], width=1)
    ))
    for w, c in zip(windows, colors):
        ema = compute_ema(df[close_col], w)
        fig.add_trace(go.Scatter(
            x=df[date_col], y=ema, name=f"EMA {w}",
            line=dict(color=c, width=1.5)
        ))
    return fig_update(fig, t, f"EMA ({', '.join(map(str, windows))})")


def plot_momentum(df, date_col, close_col, t, window=10):
    mom = compute_momentum(df[close_col], window)
    colors = [t["green"] if v >= 0 else t["red"] for v in mom.fillna(0)]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[date_col], y=mom, marker_color=colors,
        name=f"Momentum ({window})", opacity=0.9
    ))
    return fig_update(fig, t, f"Momentum ({window}d)")


def plot_atr(df, col_map, t, window=14):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    atr = compute_atr(df, col_map["high"], col_map["low"], col_map["close"], window)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[col_map["date"]], y=atr, name=f"ATR ({window})",
        line=dict(color=t["yellow"], width=2),
        fill="tozeroy", fillcolor="rgba(210,153,34,0.07)"
    ))
    return fig_update(fig, t, f"Average True Range (ATR, {window}d)")


def plot_trend(df, date_col, close_col, t, window=20):
    slope = compute_rolling_slope(df[close_col], window)
    colors = [t["green"] if s > 0 else t["red"] for s in slope.fillna(0)]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[date_col], y=slope,
        marker_color=colors, name="Rolling Slope", opacity=0.9
    ))
    return fig_update(fig, t, f"Trend Direction — Rolling Slope ({window}d)")


def plot_support_resistance(df, date_col, close_col, t, window=20):
    support, resistance = compute_support_resistance(df[close_col], window)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[close_col], name="Close",
        line=dict(color=t["accent"], width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df[date_col], y=resistance, name="Resistance",
        line=dict(color=t["red"], width=1, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=df[date_col], y=support, name="Support",
        line=dict(color=t["green"], width=1, dash="dash"),
        fill="tonexty", fillcolor="rgba(63,185,80,0.04)"
    ))
    return fig_update(fig, t, f"Support & Resistance ({window}d)")


def plot_breakout(df, date_col, close_col, t, window=20):
    resistance = df[close_col].rolling(window, min_periods=1).max().shift(1)
    support = df[close_col].rolling(window, min_periods=1).min().shift(1)
    breakout_up = df[close_col] > resistance
    breakout_down = df[close_col] < support
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=df[close_col], name="Close",
        line=dict(color=t["subtext"], width=1)
    ))
    if breakout_up.any():
        fig.add_trace(go.Scatter(
            x=df[date_col][breakout_up], y=df[close_col][breakout_up],
            mode="markers", name="Breakout Up",
            marker=dict(color=t["green"], symbol="triangle-up", size=9)
        ))
    if breakout_down.any():
        fig.add_trace(go.Scatter(
            x=df[date_col][breakout_down], y=df[close_col][breakout_down],
            mode="markers", name="Breakout Down",
            marker=dict(color=t["red"], symbol="triangle-down", size=9)
        ))
    return fig_update(fig, t, f"Breakout Detection ({window}d High/Low)")


def plot_zscore_anomalies(df, date_col, close_col, t, window=20, threshold=2.5):
    z = compute_zscore(df[close_col], window)
    anomaly = z.abs() > threshold
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=z, name="Z-Score",
        line=dict(color=t["accent"], width=1.5)
    ))
    if anomaly.any():
        fig.add_trace(go.Scatter(
            x=df[date_col][anomaly], y=z[anomaly],
            mode="markers", name="Anomaly",
            marker=dict(color=t["red"], symbol="circle-open", size=10, line_width=2)
        ))
    fig.add_hline(y=threshold, line_dash="dash", line_color=t["red"], opacity=0.5)
    fig.add_hline(y=-threshold, line_dash="dash", line_color=t["red"], opacity=0.5)
    return fig_update(fig, t, f"Z-Score Anomaly Detection ({window}d, ±{threshold}σ)")


def plot_volume_anomalies(df, date_col, vol_col, t, threshold=2.5):
    z = compute_zscore(df[vol_col], 20)
    anomaly = z.abs() > threshold
    neutral = get_chart_style()["neutral_bar"]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df[date_col], y=df[vol_col],
        marker_color=[t["red"] if a else neutral for a in anomaly],
        name="Volume", opacity=0.9
    ))
    return fig_update(fig, t, f"Volume Anomalies (Z-Score > {threshold}σ)")


def plot_correlation_heatmap(df_pivot, t):
    corr = df_pivot.corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index,
        colorscale="RdBu", zmid=0,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        colorbar=dict(title="Corr")
    ))
    return fig_update(fig, t, "Return Correlation Heatmap", 420)


def plot_scatter_price_volume(df, close_col, vol_col, date_col, t):
    returns = df[close_col].pct_change() * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[vol_col], y=returns,
        mode="markers",
        marker=dict(
            color=df[date_col].astype(np.int64),
            colorscale="Viridis", size=4, opacity=0.6,
            colorbar=dict(title="Time →")
        ),
        name="Price Change vs Volume"
    ))
    fig.update_xaxes(title_text="Volume")
    fig.update_yaxes(title_text="Daily Return (%)")
    return fig_update(fig, t, "Price Change vs Volume (Scatter)")


def plot_boxplot_price(df, date_col, close_col, t):
    df2 = df.copy()
    df2["Month"] = df2[date_col].dt.to_period("M").astype(str)
    fig = go.Figure()
    for month in sorted(df2["Month"].unique()):
        subset = df2[df2["Month"] == month][close_col]
        if len(subset) > 1:
            fig.add_trace(go.Box(y=subset, name=month, showlegend=False,
                                 marker_color=t["accent"], line_color=t["accent"]))
    return fig_update(fig, t, "Monthly Price Distribution (Box)", 420)


def plot_boxplot_volume(df, date_col, vol_col, t):
    df2 = df.copy()
    df2["Quarter"] = df2[date_col].dt.to_period("Q").astype(str)
    fig = go.Figure()
    for q in sorted(df2["Quarter"].unique()):
        subset = df2[df2["Quarter"] == q][vol_col]
        if len(subset) > 1:
            fig.add_trace(go.Box(y=subset, name=q, showlegend=False,
                                 marker_color=t["purple"], line_color=t["purple"]))
    return fig_update(fig, t, "Quarterly Volume Distribution (Box)", 380)


def plot_cumulative_volume(df, date_col, vol_col, t):
    cum_vol = df[vol_col].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[date_col], y=cum_vol, mode="lines",
        name="Cumulative Volume",
        line=dict(color=t["orange"], width=2),
        fill="tozeroy", fillcolor="rgba(255,166,87,0.07)"
    ))
    return fig_update(fig, t, "Cumulative Volume")


def plot_returns_distribution(df, close_col, t):
    returns = df[close_col].pct_change().dropna() * 100
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=returns, nbinsx=60, histnorm="probability density",
        marker_color=t["accent"], opacity=0.7, name="Returns"
    ))
    mean_r, std_r = returns.mean(), returns.std()
    x = np.linspace(returns.min(), returns.max(), 200)
    y = (1 / (std_r * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean_r) / std_r) ** 2)
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Normal Fit",
                             line=dict(color=t["orange"], width=2)))
    fig.update_xaxes(title_text="Daily Return (%)")
    return fig_update(fig, t, "Returns Distribution + Normal Fit")


def plot_lag_autocorr(df, close_col, t, max_lag=30):
    returns = df[close_col].pct_change().dropna()
    lags = range(1, min(max_lag + 1, len(returns) - 1))
    acf_vals = [returns.autocorr(lag=lag) for lag in lags]
    colors = [t["green"] if v >= 0 else t["red"] for v in acf_vals]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=list(lags), y=acf_vals, marker_color=colors, name="ACF"))
    fig.add_hline(y=1.96 / np.sqrt(len(returns)), line_dash="dash",
                  line_color=t["yellow"], opacity=0.7)
    fig.add_hline(y=-1.96 / np.sqrt(len(returns)), line_dash="dash",
                  line_color=t["yellow"], opacity=0.7)
    fig.update_xaxes(title_text="Lag (days)")
    fig.update_yaxes(title_text="Autocorrelation")
    return fig_update(fig, t, "Return Autocorrelation (ACF)")


def plot_rolling_mean_multi(df, date_col, close_col, t):
    windows = [5, 10, 20, 60]
    colors = [t["accent"], t["green"], t["yellow"], t["orange"]]
    fig = go.Figure()
    for w, c in zip(windows, colors):
        if len(df) >= w:
            fig.add_trace(go.Scatter(
                x=df[date_col], y=compute_sma(df[close_col], w),
                name=f"SMA {w}", line=dict(color=c, width=1.5)
            ))
    return fig_update(fig, t, "Rolling Mean Comparison (5, 10, 20, 60)")


def plot_price_change_freq(df, close_col, t):
    changes = df[close_col].pct_change().dropna() * 100
    bins = pd.cut(changes, bins=[-np.inf, -2, -1, 0, 1, 2, np.inf],
                  labels=["<-2%", "-2% to -1%", "-1% to 0%", "0% to 1%", "1% to 2%", ">2%"])
    freq = bins.value_counts().sort_index()
    colors = [t["red"], t["red"], t["subtext"], t["subtext"], t["green"], t["green"]]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=freq.index.astype(str), y=freq.values,
                         marker_color=colors, name="Frequency"))
    fig.update_xaxes(title_text="Return Bucket")
    fig.update_yaxes(title_text="Days")
    return fig_update(fig, t, "Price Change Frequency Distribution")


def plot_multi_symbol_compare(df, date_col, close_col, symbol_col, t, max_symbols=10):
    symbols = df[symbol_col].unique()[:max_symbols]
    fig = go.Figure()
    palette = [t["accent"], t["green"], t["yellow"], t["purple"], t["orange"],
               t["red"], "#64ffda", "#ff80ab", "#ea80fc", "#ffd180"]
    for i, sym in enumerate(symbols):
        sub = df[df[symbol_col] == sym].sort_values(date_col)
        if len(sub) < 2:
            continue
        norm = sub[close_col] / sub[close_col].iloc[0]
        fig.add_trace(go.Scatter(
            x=sub[date_col], y=norm, name=str(sym),
            line=dict(color=palette[i % len(palette)], width=1.5)
        ))
    fig.update_yaxes(title_text="Normalised Price")
    return fig_update(fig, t, "Multi-Symbol Normalised Comparison")


def plot_volatility_heatmap(df, date_col, close_col, t):
    df2 = df.copy()
    df2["Year"] = df2[date_col].dt.year.astype(str)
    df2["Month"] = df2[date_col].dt.month
    df2["Return"] = df2[close_col].pct_change()
    monthly_vol = df2.groupby(["Year", "Month"])["Return"].std().unstack() * np.sqrt(21) * 100
    if monthly_vol.empty:
        return None
    fig = go.Figure(data=go.Heatmap(
        z=monthly_vol.values, x=monthly_vol.columns.astype(str),
        y=monthly_vol.index.astype(str),
        colorscale="Oranges", colorbar=dict(title="Vol %")
    ))
    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Year")
    return fig_update(fig, t, "Monthly Volatility Heatmap (%)", 380)


def plot_returns_heatmap(df, date_col, close_col, t):
    df2 = df.copy()
    df2["Year"] = df2[date_col].dt.year.astype(str)
    df2["Month"] = df2[date_col].dt.month
    df2["Return"] = df2[close_col].pct_change()
    monthly_ret = df2.groupby(["Year", "Month"])["Return"].sum().unstack() * 100
    if monthly_ret.empty:
        return None
    fig = go.Figure(data=go.Heatmap(
        z=monthly_ret.values, x=monthly_ret.columns.astype(str),
        y=monthly_ret.index.astype(str),
        colorscale="RdYlGn", zmid=0, colorbar=dict(title="Ret %")
    ))
    fig.update_xaxes(title_text="Month")
    fig.update_yaxes(title_text="Year")
    return fig_update(fig, t, "Monthly Returns Heatmap (%)", 380)


def plot_ranking_chart(df, date_col, close_col, symbol_col, t):
    symbols = df[symbol_col].unique()
    returns = []
    for sym in symbols:
        sub = df[df[symbol_col] == sym][close_col]
        if len(sub) > 1:
            ret = (sub.iloc[-1] / sub.iloc[0] - 1) * 100
            returns.append({"Symbol": str(sym), "Return (%)": ret})
    if not returns:
        return None
    rdf = pd.DataFrame(returns).sort_values("Return (%)", ascending=True)
    colors = [t["green"] if r >= 0 else t["red"] for r in rdf["Return (%)"]]
    fig = go.Figure(go.Bar(
        y=rdf["Symbol"], x=rdf["Return (%)"],
        orientation="h", marker_color=colors, name="Total Return"
    ))
    fig.update_xaxes(title_text="Total Return (%)", ticksuffix="%")
    return fig_update(fig, t, "Symbol Ranking by Total Return", max(350, len(rdf) * 22))


def plot_rolling_corr(df, date_col, close_col, symbol_col, t, window=30):
    symbols = df[symbol_col].unique()
    if len(symbols) < 2:
        return None
    sym1, sym2 = symbols[0], symbols[1]
    s1 = df[df[symbol_col] == sym1].set_index(date_col)[close_col].pct_change()
    s2 = df[df[symbol_col] == sym2].set_index(date_col)[close_col].pct_change()
    aligned = pd.DataFrame({"s1": s1, "s2": s2}).dropna()
    if len(aligned) < window:
        return None
    roll_corr = aligned["s1"].rolling(window).corr(aligned["s2"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=aligned.index, y=roll_corr,
        mode="lines", name=f"Rolling Corr ({window}d)",
        line=dict(color=t["purple"], width=2)
    ))
    fig.add_hline(y=0, line_dash="dash", line_color=t["subtext"])
    return fig_update(fig, t, f"Rolling Correlation: {sym1} vs {sym2} ({window}d)")


def plot_exchange_volume(df, vol_col, exchange_col, t):
    grp = df.groupby(exchange_col)[vol_col].sum().sort_values(ascending=False)
    fig = go.Figure(go.Bar(
        x=grp.index.astype(str), y=grp.values,
        marker_color=t["accent"], name="Total Volume"
    ))
    fig.update_xaxes(title_text="Exchange")
    fig.update_yaxes(title_text="Total Volume")
    return fig_update(fig, t, "Volume by Exchange")


def plot_intraday_variation(df, date_col, col_map, t):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    df2 = df.copy()
    df2["HL_pct"] = (df2[col_map["high"]] - df2[col_map["low"]]) / df2[col_map["close"]] * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df2[date_col], y=df2["HL_pct"],
        mode="lines", name="H-L Range %",
        line=dict(color=t["yellow"], width=1.5),
        fill="tozeroy", fillcolor="rgba(210,153,34,0.06)"
    ))
    fig.update_yaxes(ticksuffix="%", title_text="(High-Low)/Close %")
    return fig_update(fig, t, "Intraday Price Range (H-L) %")


def plot_heikin_ashi(df, col_map, t, symbol=None):
    if not all(k in col_map for k in ["open", "high", "low", "close"]):
        return None
    df2 = df.copy()
    df2["HA_Close"] = (df2[col_map["open"]] + df2[col_map["high"]] + df2[col_map["low"]] + df2[col_map["close"]]) / 4
    df2["HA_Open"] = (df2[col_map["open"]].shift(1) + df2[col_map["close"]].shift(1)) / 2
    df2["HA_Open"].iloc[0] = df2[col_map["open"]].iloc[0]
    df2["HA_High"] = df2[[col_map["high"], "HA_Close", "HA_Open"]].max(axis=1)
    df2["HA_Low"] = df2[[col_map["low"], "HA_Close", "HA_Open"]].min(axis=1)
    d = df2[col_map.get("date", df2.index)]
    fig = go.Figure(data=[go.Candlestick(
        x=d, open=df2["HA_Open"], high=df2["HA_High"],
        low=df2["HA_Low"], close=df2["HA_Close"],
        increasing_line_color=t["green"], decreasing_line_color=t["red"],
        name="Heikin-Ashi"
    )])
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig_update(fig, t, f"Heikin-Ashi Chart" + (f" — {symbol}" if symbol else ""), 460)


def plot_keltner_channels(df, date_col, close_col, t, window=20, mult=2):
    ema = compute_ema(df[close_col], window)
    atr_val = df[close_col].diff().abs().rolling(window).mean()
    upper = ema + mult * atr_val
    lower = ema - mult * atr_val
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=upper, name="Upper Channel",
                            line=dict(color=t["orange"], width=1, dash="dash")))
    fig.add_trace(go.Scatter(x=df[date_col], y=lower, name="Lower Channel",
                            line=dict(color=t["orange"], width=1, dash="dash")))
    fig.add_trace(go.Scatter(x=df[date_col], y=ema, name="EMA",
                            line=dict(color=t["cyan"], width=1.5)))
    fig.add_trace(go.Scatter(x=df[date_col], y=df[close_col], name="Close",
                            line=dict(color=t["accent"], width=1.5)))
    return fig_update(fig, t, f"Keltner Channels ({window}, {mult}x)")


def plot_donchian_channels(df, date_col, close_col, t, window=20):
    upper = df[close_col].rolling(window).max()
    lower = df[close_col].rolling(window).min()
    mid = (upper + lower) / 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=upper, name="Upper",
                            line=dict(color=t["red"], width=1)))
    fig.add_trace(go.Scatter(x=df[date_col], y=lower, name="Lower",
                            line=dict(color=t["green"], width=1)))
    fig.add_trace(go.Scatter(x=df[date_col], y=mid, name="Mid",
                            line=dict(color=t["subtext"], width=1, dash="dot")))
    fig.add_trace(go.Scatter(x=df[date_col], y=df[close_col], name="Close",
                            line=dict(color=t["accent"], width=1.5)))
    return fig_update(fig, t, f"Donchian Channels ({window}d)")


def plot_ichimoku(df, col_map, t):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    high, low, close = df[col_map["high"]], df[col_map["low"]], df[col_map["close"]]
    nine_period_high = high.rolling(9).max()
    nine_period_low = low.rolling(9).min()
    tenkan_sen = (nine_period_high + nine_period_low) / 2
    fiftytwo_period_high = high.rolling(52).max()
    fiftytwo_period_low = low.rolling(52).min()
    kijun_sen = (fiftytwo_period_high + fiftytwo_period_low) / 2
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)
    senkou_span_b = ((fiftytwo_period_high + fiftytwo_period_low) / 2).shift(26)
    date_col = col_map.get("date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=senkou_span_a, name="Span A",
                            line=dict(color=t["cyan"], width=1)))
    fig.add_trace(go.Scatter(x=df[date_col], y=senkou_span_b, name="Span B",
                            line=dict(color=t["pink"], width=1)))
    fig.add_trace(go.Scatter(x=df[date_col], y=tenkan_sen, name="Tenkan-Sen",
                            line=dict(color=t["red"], width=1))
                 )
    fig.add_trace(go.Scatter(x=df[date_col], y=kijun_sen, name="Kijun-Sen",
                            line=dict(color=t["blue"], width=1))
                 )
    fig.add_trace(go.Scatter(x=df[date_col], y=close, name="Close",
                            line=dict(color=t["accent"], width=1.5)))
    return fig_update(fig, t, "Ichimoku Cloud", 500)


def plot_stochastic_oscillator(df, date_col, close_col, t, k_window=14, d_window=3):
    low_min = df[close_col].rolling(k_window).min()
    high_max = df[close_col].rolling(k_window).max()
    k = 100 * (df[close_col] - low_min) / (high_max - low_min)
    d = k.rolling(d_window).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=k, name="%K",
                            line=dict(color=t["accent"], width=1.5)))
    fig.add_trace(go.Scatter(x=df[date_col], y=d, name="%D",
                            line=dict(color=t["orange"], width=1.5)))
    fig.add_hline(y=80, line_dash="dash", line_color=t["red"], opacity=0.6)
    fig.add_hline(y=20, line_dash="dash", line_color=t["green"], opacity=0.6)
    fig.update_yaxes(range=[0, 100])
    return fig_update(fig, t, f"Stochastic Oscillator ({k_window},{d_window})")


def plot_cci(df, col_map, t, window=20):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    tp = (df[col_map["high"]] + df[col_map["low"]] + df[col_map["close"]]) / 3
    sma_tp = tp.rolling(window).mean()
    mad = tp.rolling(window).apply(lambda x: np.abs(x - x.mean()).mean())
    cci = (tp - sma_tp) / (0.015 * mad)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[col_map["date"]], y=cci, name="CCI",
                            line=dict(color=t["purple"], width=1.5)))
    fig.add_hline(y=100, line_dash="dash", line_color=t["red"], opacity=0.6)
    fig.add_hline(y=-100, line_dash="dash", line_color=t["green"], opacity=0.6)
    return fig_update(fig, t, f"Commodity Channel Index ({window})")


def plot_williams_r(df, col_map, t, window=14):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    high_max = df[col_map["high"]].rolling(window).max()
    low_min = df[col_map["low"]].rolling(window).min()
    wr = -100 * (high_max - df[col_map["close"]]) / (high_max - low_min)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[col_map["date"]], y=wr, name="Williams %R",
                            line=dict(color=t["lime"], width=1.5)))
    fig.add_hline(y=-20, line_dash="dash", line_color=t["red"], opacity=0.6)
    fig.add_hline(y=-80, line_dash="dash", line_color=t["green"], opacity=0.6)
    fig.update_yaxes(range=[-100, 0])
    return fig_update(fig, t, f"Williams %R ({window})")


def plot_OBV(df, date_col, close_col, vol_col, t):
    obv = (np.sign(df[close_col].diff()) * df[vol_col]).fillna(0).cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=obv, name="OBV",
                            line=dict(color=t["teal"], width=1.5),
                            fill="tozeroy", fillcolor="rgba(20,184,166,0.06)"))
    return fig_update(fig, t, "On-Balance Volume (OBV)")


def plot_mfi(df, col_map, t, window=14):
    if not all(k in col_map for k in ["high", "low", "close", "volume"]):
        return None
    tp = (df[col_map["high"]] + df[col_map["low"]] + df[col_map["close"]]) / 3
    mf = tp * df[col_map["volume"]]
    pos_mf = mf.rolling(window).apply(lambda x: x[x > 0].sum(), raw=True)
    neg_mf = abs(mf.rolling(window).apply(lambda x: x[x < 0].sum(), raw=True))
    mfr = pos_mf / neg_mf.replace(0, np.nan)
    mfi = 100 - (100 / (1 + mfr))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[col_map["date"]], y=mfi, name="MFI",
                            line=dict(color=t["indigo"], width=1.5)))
    fig.add_hline(y=80, line_dash="dash", line_color=t["red"], opacity=0.6)
    fig.add_hline(y=20, line_dash="dash", line_color=t["green"], opacity=0.6)
    fig.update_yaxes(range=[0, 100])
    return fig_update(fig, t, f"Money Flow Index ({window})")


def plot_vwap(df, col_map, t):
    if not all(k in col_map for k in ["high", "low", "close", "volume"]):
        return None
    df2 = df.copy()
    df2["TP"] = (df2[col_map["high"]] + df2[col_map["low"]] + df2[col_map["close"]]) / 3
    df2["VWAP"] = (df2["TP"] * df2[col_map["volume"]]).cumsum() / df2[col_map["volume"]].cumsum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df2[col_map["date"]], y=df2["VWAP"], name="VWAP",
                            line=dict(color=t["yellow"], width=2))
                 )
    fig.add_trace(go.Scatter(x=df2[col_map["date"]], y=df2[col_map["close"]], name="Close",
                            line=dict(color=t["accent"], width=1)))
    return fig_update(fig, t, "Volume Weighted Average Price (VWAP)")


def plot_pivot_points(df, col_map, t):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    df2 = df.copy()
    df2["PP"] = (df2[col_map["high"]] + df2[col_map["low"]] + df2[col_map["close"]]) / 3
    df2["R1"] = 2 * df2["PP"] - df2[col_map["low"]]
    df2["S1"] = 2 * df2["PP"] - df2[col_map["high"]]
    df2["R2"] = df2["PP"] + (df2[col_map["high"]] - df2[col_map["low"]])
    df2["S2"] = df2["PP"] - (df2[col_map["high"]] - df2[col_map["low"]])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df2[col_map["date"]], y=df2[col_map["close"]], name="Close",
                            line=dict(color=t["accent"], width=1.5)))
    fig.add_trace(go.Scatter(x=df2[col_map["date"]], y=df2["PP"], name="Pivot",
                            line=dict(color=t["subtext"], width=1, dash="dot")))
    fig.add_trace(go.Scatter(x=df2[col_map["date"]], y=df2["R1"], name="R1",
                            line=dict(color=t["red"], width=1)))
    fig.add_trace(go.Scatter(x=df2[col_map["date"]], y=df2["S1"], name="S1",
                            line=dict(color=t["green"], width=1)))
    return fig_update(fig, t, "Pivot Points (Classic)")


def plot_fibonacci_retrace(df, close_col, t):
    max_p = df[close_col].max()
    min_p = df[close_col].min()
    diff = max_p - min_p
    levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    fibs = {f"Level {int(l*100)}%": max_p - l * diff for l in levels}
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[close_col], name="Close",
                            line=dict(color=t["accent"], width=1.5)))
    for name, val in fibs.items():
        fig.add_hline(y=val, line_dash="dash", line_color=t["yellow"],
                     annotation_text=name, annotation_position="right")
    return fig_update(fig, t, "Fibonacci Retracement")


def plot_parabolic_sar(df, col_map, t, accel=0.02, max_af=0.2):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    close = df[col_map["close"]]
    high = df[col_map["high"]]
    low = df[col_map["low"]]
    sar = [low.iloc[0]]
    trend = [1]
    af = accel
    ep = high.iloc[0]
    for i in range(1, len(df)):
        if trend[-1] == 1:
            sar.append(sar[-1] + af * (ep - sar[-1]))
            if low.iloc[i] < sar[-1]:
                trend.append(-1)
                ep = low.iloc[i]
                af = accel
            else:
                trend.append(1)
                if high.iloc[i] > ep:
                    ep = high.iloc[i]
                    af = min(af + accel, max_af)
        else:
            sar.append(sar[-1] + af * (ep - sar[-1]))
            if high.iloc[i] > sar[-1]:
                trend.append(1)
                ep = high.iloc[i]
                af = accel
            else:
                trend.append(-1)
                if low.iloc[i] < ep:
                    ep = low.iloc[i]
                    af = min(af + accel, max_af)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[col_map["date"]], y=close, name="Close",
                            line=dict(color=t["accent"], width=1.5)))
    fig.add_trace(go.Scatter(x=df[col_map["date"]], y=sar, name="SAR",
                            mode="markers", marker=dict(color=t["red"], size=4)))
    return fig_update(fig, t, "Parabolic SAR")


def plot_trix(df, date_col, close_col, t, window=15):
    close = df[close_col]
    ema1 = compute_ema(close, window)
    ema2 = compute_ema(ema1, window)
    ema3 = compute_ema(ema2, window)
    trix = ema3.pct_change() * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=trix, name="TRIX",
                            line=dict(color=t["cyan"], width=1.5),
                            fill="tozeroy", fillcolor="rgba(6,182,212,0.06)"))
    fig.add_hline(y=0, line_dash="dash", line_color=t["subtext"])
    return fig_update(fig, t, f"TRIX ({window})")


def plot_kama(df, date_col, close_col, t, window=10):
    def kama(series, window):
        fast = 2 / (2 + 1)
        slow = 2 / (30 + 1)
        vol = series.diff().abs()
        er = vol.rolling(window).sum() / series.diff().abs().rolling(window).sum()
        sc = er * (fast - slow) + slow
        sc = sc ** 2
        kama = [series.iloc[0]]
        for i in range(1, len(series)):
            kama.append(kama[-1] + sc.iloc[i] * (series.iloc[i] - kama[-1]))
        return pd.Series(kama, index=series.index)
    k = kama(df[close_col], window)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=df[close_col], name="Close",
                            line=dict(color=t["subtext"], width=1),
                            opacity=0.6))
    fig.add_trace(go.Scatter(x=df[date_col], y=k, name=f"KAMA ({window})",
                            line=dict(color=t["pink"], width=1.5)))
    return fig_update(fig, t, f"Kaufman Adaptive MA ({window})")


def plot_aroon(close_col, t, window=25):
    aroon_down = close_col.rolling(window + 1).apply(lambda x: x.argmin(), raw=True)
    aroon_up = close_col.rolling(window + 1).apply(lambda x: x.argmax(), raw=True)
    aroon_osc = aroon_up - aroon_down
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=aroon_up, name="Aroon Up", line=dict(color=t["green"], width=1.5)))
    fig.add_trace(go.Scatter(y=aroon_down, name="Aroon Down", line=dict(color=t["red"], width=1.5)))
    fig.add_trace(go.Scatter(y=aroon_osc, name="Aroon Oscillator", line=dict(color=t["purple"], width=1)))
    return fig_update(fig, t, f"Aroon Indicator ({window})")


def plot_chandelier_exit(df, col_map, t, window=22, mult=3):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    high, low, close = df[col_map["high"]], df[col_map["low"]], df[col_map["close"]]
    date_col = col_map.get("date")
    long_stop = high.rolling(window).max() - mult * (high - low).rolling(window).mean()
    short_stop = low.rolling(window).min() + mult * (high - low).rolling(window).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=close, name="Close",
                            line=dict(color=t["accent"], width=1.5)))
    fig.add_trace(go.Scatter(x=df[date_col], y=long_stop, name="Long Stop",
                            line=dict(color=t["red"], width=1)))
    fig.add_trace(go.Scatter(x=df[date_col], y=short_stop, name="Short Stop",
                            line=dict(color=t["green"], width=1)))
    return fig_update(fig, t, f"Chandelier Exit ({window},{mult})")


def plot_ulcer_index(df, close_col, t, window=14):
    close = df[close_col]
    ui = ((close.rolling(window).apply(lambda x: ((x - x.max()) ** 2).mean() ** 0.5, raw=True)) / close) * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=ui, name="Ulcer Index",
                            line=dict(color=t["orange"], width=1.5),
                            fill="tozeroy", fillcolor="rgba(249,115,22,0.06)"))
    return fig_update(fig, t, f"Ulcer Index ({window})")


def plot_chaikin_oscillator(df, col_map, t):
    if not all(k in col_map for k in ["high", "low", "close", "volume"]):
        return None
    high, low, close, vol = df[col_map["high"]], df[col_map["low"]], df[col_map["close"]], df[col_map["volume"]]
    clv = ((close - low) - (high - low)) / (high - low).replace(0, np.nan)
    ad = clv * vol
    ema_fast = ad.ewm(span=3, adjust=False).mean()
    ema_slow = ad.ewm(span=10, adjust=False).mean()
    chaikin = ema_fast - ema_slow
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=chaikin, name="Chaikin Oscillator",
                            line=dict(color=t["lime"], width=1.5),
                            fill="tozeroy", fillcolor="rgba(132,204,22,0.06)"))
    fig.add_hline(y=0, line_dash="dash", line_color=t["subtext"])
    return fig_update(fig, t, "Chaikin Oscillator")


def plot_mass_index(df, col_map, t, fast=9, slow=25):
    if not all(k in col_map for k in ["high", "low"]):
        return None
    high, low = df[col_map["high"]], df[col_map["low"]]
    range_ = high - low
    ema1 = range_.ewm(span=fast, adjust=False).mean()
    ema2 = ema1.ewm(span=fast, adjust=False).mean()
    mi = ema2 / ema1.ewm(span=fast, adjust=False).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=mi, name="Mass Index",
                            line=dict(color=t["teal"], width=1.5)))
    fig.add_hline(y=27, line_dash="dash", line_color=t["red"], opacity=0.6)
    fig.add_hline(y=26.5, line_dash="dash", line_color=t["green"], opacity=0.6)
    return fig_update(fig, t, f"Mass Index ({fast},{slow})")


def plot_dpo(df, date_col, close_col, t, window=20):
    ma = compute_sma(df[close_col], window)
    dpo = df[close_col].shift(window // 2 + 1) - ma
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=dpo, name="DPO",
                            line=dict(color=t["indigo"], width=1.5),
                            fill="tozeroy", fillcolor="rgba(99,102,241,0.06)"))
    fig.add_hline(y=0, line_dash="dash", line_color=t["subtext"])
    return fig_update(fig, t, f"Detrended Price Oscillator ({window})")


def plot_kst(close_col, t):
    roc1 = close_col.pct_change(10) * 100
    roc2 = close_col.pct_change(15) * 100
    roc3 = close_col.pct_change(20) * 100
    roc4 = close_col.pct_change(30) * 100
    ma1 = roc1.rolling(10).mean()
    ma2 = roc2.rolling(10).mean()
    ma3 = roc3.rolling(10).mean()
    ma4 = roc4.rolling(10).mean()
    kst = (ma1 * 1) + (ma2 * 2) + (ma3 * 3) + (ma4 * 4)
    signal = kst.rolling(9).mean()
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=kst, name="KST", line=dict(color=t["accent"], width=1.5)))
    fig.add_trace(go.Scatter(y=signal, name="Signal", line=dict(color=t["orange"], width=1)))
    fig.add_hline(y=0, line_dash="dash", line_color=t["subtext"])
    return fig_update(fig, t, "Know Sure Thing (KST)")


def plot_ppo(close_col, t):
    ema12 = compute_ema(close_col, 12)
    ema26 = compute_ema(close_col, 26)
    ppo = ((ema12 - ema26) / ema26) * 100
    signal = compute_ema(ppo, 9)
    hist = ppo - signal
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=ppo, name="PPO", line=dict(color=t["cyan"], width=1.5)))
    fig.add_trace(go.Scatter(y=signal, name="Signal", line=dict(color=t["pink"], width=1)))
    colors = [t["green"] if h >= 0 else t["red"] for h in hist]
    fig.add_trace(go.Bar(y=hist, name="Histogram", marker_color=colors, opacity=0.6))
    fig.add_hline(y=0, line_dash="dash", line_color=t["subtext"])
    return fig_update(fig, t, "Percentage Price Oscillator")


def plot_zigzag(df, close_col, t, threshold=0.05):
    close = df[close_col]
    zigzag = [close.iloc[0]]
    direction = 0
    for price in close[1:]:
        if direction == 0:
            if price > zigzag[-1] * (1 + threshold):
                direction = 1
                zigzag.append(price)
            elif price < zigzag[-1] * (1 - threshold):
                direction = -1
                zigzag.append(price)
            else:
                zigzag.append(zigzag[-1])
        elif direction == 1:
            if price > zigzag[-1]:
                zigzag[-1] = price
            elif price < zigzag[-1] * (1 - threshold):
                direction = -1
                zigzag.append(price)
            else:
                zigzag[-1] = price
        else:
            if price < zigzag[-1]:
                zigzag[-1] = price
            elif price > zigzag[-1] * (1 + threshold):
                direction = 1
                zigzag.append(price)
            else:
                zigzag[-1] = price
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=close, name="Close", line=dict(color=t["subtext"], width=1)))
    fig.add_trace(go.Scatter(y=zigzag, name="ZigZag", line=dict(color=t["accent"], width=2)))
    return fig_update(fig, t, f"ZigZag ({int(threshold*100)}%)")


def plot_renko(df, col_map, t, brick_size=None):
    if not all(k in col_map for k in ["close"]):
        return None
    close = df[col_map["close"]]
    if brick_size is None:
        brick_size = close.std() * 0.02
    bricks = []
    direction = 0
    for price in close:
        if not bricks:
            bricks.append(price)
        elif direction >= 0 and price >= bricks[-1] + brick_size:
            bricks.append(bricks[-1] + brick_size)
            direction = 1
        elif direction <= 0 and price <= bricks[-1] - brick_size:
            bricks.append(bricks[-1] - brick_size)
            direction = -1
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=bricks, name="Renko", mode="lines",
                            line=dict(color=t["purple"], width=2)))
    return fig_update(fig, t, f"Renko Chart (Size: {brick_size:.2f})")


def plot_line_break(df, close_col, t, lines=3):
    close = df[close_col]
    lb = [close.iloc[0]]
    for price in close[1:]:
        if price > lb[-1] and (len(lb) < lines or price > lb[-lines]):
            lb.append(price)
        elif price < lb[-1] and (len(lb) < lines or price < lb[-lines]):
            lb.append(price)
        else:
            lb.append(lb[-1])
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=lb, name="Line Break", line=dict(color=t["lime"], width=1.5)))
    fig.add_trace(go.Scatter(y=close, name="Close", line=dict(color=t["subtext"], width=1)))
    return fig_update(fig, t, f"Line Break Chart ({lines} Lines)")


def plot_keltner_breakout(df, col_map, t, window=20, mult=2):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    close = df[col_map["close"]]
    high, low = df[col_map["high"]], df[col_map["low"]]
    ema = compute_ema(close, window)
    atr = (high - low).rolling(window).mean()
    upper = ema + mult * atr
    lower = ema - mult * atr
    long_cond = close > upper
    short_cond = close < lower
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[col_map["date"]], y=close, name="Close",
                            line=dict(color=t["subtext"], width=1)))
    fig.add_trace(go.Scatter(x=df[col_map["date"]], y=upper, name="Upper",
                            line=dict(color=t["red"], width=1, dash="dash")))
    fig.add_trace(go.Scatter(x=df[col_map["date"]], y=lower, name="Lower",
                            line=dict(color=t["green"], width=1, dash="dash")))
    if long_cond.any():
        fig.add_trace(go.Scatter(
            x=df[col_map["date"]][long_cond], y=close[long_cond],
            mode="markers", name="Long", marker=dict(color=t["green"], symbol="triangle-up", size=10)
        ))
    if short_cond.any():
        fig.add_trace(go.Scatter(
            x=df[col_map["date"]][short_cond], y=close[short_cond],
            mode="markers", name="Short", marker=dict(color=t["red"], symbol="triangle-down", size=10)
        ))
    return fig_update(fig, t, f"Keltner Breakout ({window},{mult})")


def plot_volume_profile(df, date_col, vol_col, close_col, t, bins=50):
    df2 = df.copy()
    price_range = df2[close_col].max() - df2[close_col].min()
    bin_size = price_range / bins
    df2["PriceBin"] = (df2[close_col] // bin_size) * bin_size
    profile = df2.groupby("PriceBin")[vol_col].sum()
    colors = [t["green"] if p >= profile.idxmax() else t["accent"] for p in profile.index]
    fig = go.Figure(go.Bar(x=profile.values, y=profile.index, orientation="h",
                         marker_color=colors, name="Vol Profile"))
    return fig_update(fig, t, "Volume Profile", 450)


def plot_gap_analysis(df, col_map, t):
    if not all(k in col_map for k in ["open", "close"]):
        return None
    open_p = df[col_map["open"]]
    prev_close = df[col_map["close"]].shift(1)
    gap_up = open_p > prev_close * 1.01
    gap_down = open_p < prev_close * 0.99
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[col_map["date"]], y=df[col_map["close"]], name="Close",
                            line=dict(color=t["accent"], width=1.5)))
    if gap_up.any():
        fig.add_trace(go.Scatter(
            x=df[col_map["date"]][gap_up], y=df[col_map["close"]][gap_up],
            mode="markers", name="Gap Up", marker=dict(color=t["green"], size=12, symbol="arrow-up")
        ))
    if gap_down.any():
        fig.add_trace(go.Scatter(
            x=df[col_map["date"]][gap_down], y=df[col_map["close"]][gap_down],
            mode="markers", name="Gap Down", marker=dict(color=t["red"], size=12, symbol="arrow-down")
        ))
    return fig_update(fig, t, "Gap Analysis")


def plot_price_velocity(df, date_col, close_col, t, window=10):
    velocity = df[close_col].diff() / window
    fig = go.Figure()
    colors = [t["green"] if v >= 0 else t["red"] for v in velocity.fillna(0)]
    fig.add_trace(go.Bar(x=df[date_col], y=velocity, marker_color=colors, name="Velocity", opacity=0.9))
    return fig_update(fig, t, f"Price Velocity ({window}d)")


def plot_acceleration(df, date_col, close_col, t, window=10):
    velocity = df[close_col].diff() / window
    acceleration = velocity.diff()
    fig = go.Figure()
    colors = [t["green"] if a >= 0 else t["red"] for a in acceleration.fillna(0)]
    fig.add_trace(go.Bar(x=df[date_col], y=acceleration, marker_color=colors, name="Acceleration", opacity=0.9))
    return fig_update(fig, t, f"Price Acceleration ({window}d)")


def plot_median_price(df, col_map, t):
    if not all(k in col_map for k in ["high", "low"]):
        return None
    median = (df[col_map["high"]] + df[col_map["low"]]) / 2
    date_col = col_map.get("date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=median, name="Median Price",
                            line=dict(color=t["cyan"], width=1.5)))
    fig.add_trace(go.Scatter(x=df[date_col], y=df[col_map["close"]], name="Close",
                            line=dict(color=t["subtext"], width=1)))
    return fig_update(fig, t, "Median Price")


def plot_typical_price(df, col_map, t):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    typical = (df[col_map["high"]] + df[col_map["low"]] + df[col_map["close"]]) / 3
    date_col = col_map.get("date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=typical, name="Typical Price",
                            line=dict(color=t["orange"], width=1.5)))
    return fig_update(fig, t, "Typical Price (HLC/3)")


def plot_weighted_close(df, col_map, t):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    wc = (df[col_map["high"]] + df[col_map["low"]] + 2 * df[col_map["close"]]) / 4
    date_col = col_map.get("date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=wc, name="Weighted Close",
                            line=dict(color=t["pink"], width=1.5)))
    return fig_update(fig, t, "Weighted Close (HLC+Close)/4")


def plot_qstick(df, date_col, close_col, t, window=14):
    qstick = (df[close_col] - df[close_col].shift(1)).rolling(window).mean()
    fig = go.Figure()
    colors = [t["green"] if q >= 0 else t["red"] for q in qstick.fillna(0)]
    fig.add_trace(go.Bar(x=df[date_col], y=qstick, marker_color=colors, name="QStick", opacity=0.9))
    fig.add_hline(y=0, line_dash="dash", line_color=get_chart_style()["subtext"])
    return fig_update(fig, t, f"QStick ({window})")


def plot_tema(df, date_col, close_col, t, window=5):
    ema1 = compute_ema(df[close_col], window)
    ema2 = compute_ema(ema1, window)
    ema3 = compute_ema(ema2, window)
    tema = 3 * ema1 - 3 * ema2 + ema3
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=tema, name=f"TEMA ({window})",
                            line=dict(color=t["lime"], width=1.5)))
    fig.add_trace(go.Scatter(x=df[date_col], y=df[close_col], name="Close",
                            line=dict(color=t["subtext"], width=1)))
    return fig_update(fig, t, f"Triple EMA ({window})")


def plot_liquidity_zones(df, col_map, t, window=20):
    high = df[col_map["high"]] if "high" in col_map else df[col_map["close"]]
    low = df[col_map["low"]] if "low" in col_map else df[col_map["close"]]
    date_col = col_map.get("date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=df[col_map["close"]], name="Close",
                            line=dict(color=t["accent"], width=1.5))
                 )
    for q in [0.9, 0.7, 0.5, 0.3, 0.1]:
        zone_high = high.quantile(q)
        fig.add_hline(y=zone_high, line_dash="dash",
                     line_color=t["yellow"], opacity=0.4,
                     annotation_text=f"P{int(q*100)}")
    return fig_update(fig, t, f"Liquidity Zones ({window}d)")


def plot_spread_analysis(df, col_map, t):
    if not all(k in col_map for k in ["high", "low"]):
        return None
    spread = df[col_map["high"]] - df[col_map["low"]]
    date_col = col_map.get("date")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df[date_col], y=spread, name="Spread (H-L)",
                            line=dict(color=t["purple"], width=1.5),
                            fill="tozeroy", fillcolor="rgba(139,92,246,0.06)"))
    fig.update_yaxes(title_text="Spread Value")
    return fig_update(fig, t, "High-Low Spread Analysis")


def plot_correlation_with_index(df, close_col, index_col, t):
    if index_col not in df.columns:
        return None
    corr = df[close_col].rolling(30).corr(df[index_col])
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=corr, name="Correlation",
                            line=dict(color=t["teal"], width=1.5)))
    fig.add_hline(y=0, line_dash="dash", line_color=t["subtext"])
    return fig_update(fig, t, "Correlation with Index")


def plot_beta(df, close_col, market_col, t, window=60):
    if market_col not in df.columns:
        return None
    returns = df[close_col].pct_change()
    market_returns = df[market_col].pct_change()
    beta = returns.rolling(window).cov(market_returns) / market_returns.rolling(window).var()
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=beta, name="Beta",
                            line=dict(color=t["indigo"], width=1.5)))
    fig.add_hline(y=1, line_dash="dash", line_color=t["subtext"], opacity=0.5)
    return fig_update(fig, t, f"Beta vs Market ({window}d)")


# ─────────────────────────────────────────────
# ADDITIONAL CANDLESTICK CHARTS (10 more)
# ─────────────────────────────────────────────

def plot_hlc(df, col_map, t, symbol=None):
    if not all(k in col_map for k in ["high", "low", "close"]):
        return None
    d = df[col_map["date"]]
    fig = go.Figure(data=[go.Candlestick(
        x=d,
        open=df[col_map["close"]],
        high=df[col_map["high"]],
        low=df[col_map["low"]],
        close=df[col_map["close"]],
        increasing_line_color=t["green"],
        decreasing_line_color=t["red"],
        name="HLC"
    )])
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig_update(fig, t, f"HLC Chart" + (f" — {symbol}" if symbol else ""), 460)


def plot_ohlc_wide(df, col_map, t, symbol=None):
    if not all(k in col_map for k in ["open", "high", "low", "close"]):
        return None
    d = df[col_map["date"]]
    fig = go.Figure(data=[go.Candlestick(
        x=d,
        open=df[col_map["open"]],
        high=df[col_map["high"]],
        low=df[col_map["low"]],
        close=df[col_map["close"]],
        increasing_line_color=t["cyan"],
        decreasing_line_color=t["pink"],
        name="Wide OHLC"
    )])
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig_update(fig, t, f"Wide OHLC Chart" + (f" — {symbol}" if symbol else ""), 480)


def plot_candle_colors(df, col_map, t, symbol=None):
    if not all(k in col_map for k in ["open", "close"]):
        return None
    d = df[col_map["date"]]
    colors = [t["green"] if c >= o else t["red"] for c, o in zip(df[col_map["close"]], df[col_map["open"]])]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d, y=df[col_map["close"]] - df[col_map["open"]],
                        marker_color=colors, name="Candle Body"))
    return fig_update(fig, t, f"Candle Body Colors" + (f" — {symbol}" if symbol else ""), 400)


def plot_price_range_bars(df, col_map, t, symbol=None):
    if not all(k in col_map for k in ["high", "low"]):
        return None
    d = df[col_map["date"]]
    range_bars = df[col_map["high"]] - df[col_map["low"]]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=d, y=range_bars, marker_color=t["purple"], name="Range"))
    return fig_update(fig, t, f"Price Range Bars" + (f" — {symbol}" if symbol else ""), 400)


def plot_point_figure(df, close_col, t, symbol=None, boxes=3):
    close = df[close_col]
    pgf = []
    direction = 0
    last_price = close.iloc[0]
    for price in close:
        if direction == 0:
            if price >= last_price + boxes:
                direction = 1
                pgf.append(price)
                last_price = price
            elif price <= last_price - boxes:
                direction = -1
                pgf.append(price)
                last_price = price
        elif direction == 1:
            if price >= last_price + boxes:
                pgf[-1] = price
                last_price = price
            elif price <= last_price - boxes:
                direction = -1
                pgf.append(price)
                last_price = price
        else:
            if price <= last_price - boxes:
                pgf[-1] = price
                last_price = price
            elif price >= last_price + boxes:
                direction = 1
                pgf.append(price)
                last_price = price
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=pgf, mode="lines+markers", name="P&F",
                            line=dict(color=t["teal"], width=1.5),
                            marker=dict(size=4)))
    return fig_update(fig, t, f"Point & Figure ({boxes})" + (f" — {symbol}" if symbol else ""), 450)


def plot_kagi(df, close_col, t, symbol=None, reversal=3):
    close = df[close_col]
    kagi = [close.iloc[0]]
    direction = 0
    threshold = close.std() * reversal / 100
    for price in close[1:]:
        if direction == 0:
            if price > kagi[-1] + threshold:
                direction = 1
                kagi.append(price)
            elif price < kagi[-1] - threshold:
                direction = -1
                kagi.append(price)
        elif direction == 1:
            if price > kagi[-1]:
                kagi[-1] = price
            elif price < kagi[-1] - threshold:
                direction = -1
                kagi.append(price)
        else:
            if price < kagi[-1]:
                kagi[-1] = price
            elif price > kagi[-1] + threshold:
                direction = 1
                kagi.append(price)
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=kagi, mode="lines", name="Kagi",
                            line=dict(color=t["lime"], width=2)))
    return fig_update(fig, t, f"Kagi Chart ({reversal}%)" + (f" — {symbol}" if symbol else ""), 450)


def plot_range_bars(df, close_col, t, symbol=None, bar_size=1):
    close = df[close_col]
    range_bars = []
    bar = [close.iloc[0]]
    for price in close[1:]:
        if abs(price - bar[0]) >= bar_size:
            range_bars.append(bar[-1])
            bar = [price]
        else:
            bar = [bar[0], price]
    if bar:
        range_bars.append(bar[-1])
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=range_bars, mode="lines", name="Range Bars",
                            line=dict(color=t["orange"], width=1.5)))
    return fig_update(fig, t, f"Range Bars ({bar_size})" + (f" — {symbol}" if symbol else ""), 450)


def plot_dollar_bars(df, close_col, vol_col, t, symbol=None, dollar_threshold=10000):
    close = df[close_col]
    vol = df[vol_col] if vol_col else pd.Series(np.ones(len(close)))
    dollar_volume = close * vol
    bars = []
    cumulative = 0
    bar = [close.iloc[0]]
    for i in range(len(close)):
        cumulative += dollar_volume.iloc[i]
        if cumulative >= dollar_threshold:
            bars.append(bar[-1])
            cumulative = 0
            bar = [close.iloc[i]]
        else:
            bar = [bar[0], close.iloc[i]]
    if bar and cumulative > 0:
        bars.append(bar[-1])
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=bars, mode="lines", name="Dollar Bars",
                            line=dict(color=t["pink"], width=1.5)))
    return fig_update(fig, t, f"Dollar Bars (${dollar_threshold/1000}k)" + (f" — {symbol}" if symbol else ""), 450)


def plot_volumetric_bars(df, close_col, vol_col, t, symbol=None, vol_threshold=1000000):
    close = df[close_col]
    vol = df[vol_col] if vol_col else pd.Series(np.ones(len(close)))
    bars = []
    cumulative_vol = 0
    bar = [close.iloc[0]]
    for i in range(len(close)):
        cumulative_vol += vol.iloc[i]
        if cumulative_vol >= vol_threshold:
            bars.append(bar[-1])
            cumulative_vol = 0
            bar = [close.iloc[i]]
        else:
            bar = [bar[0], close.iloc[i]]
    if bar and cumulative_vol > 0:
        bars.append(bar[-1])
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=bars, mode="lines", name="Volume Bars",
                            line=dict(color=t["cyan"], width=1.5)))
    return fig_update(fig, t, f"Volumetric Bars ({vol_threshold/1000000:.1f}M)" + (f" — {symbol}" if symbol else ""), 450)


def plot_ticks(df, close_col, t, symbol=None, n_ticks=50):
    close = df[close_col]
    if len(close) < n_ticks:
        n_ticks = len(close) // 2
    ticks = close.iloc[::max(1, len(close) // n_ticks)]
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=ticks, mode="lines+markers", name="Ticks",
                            line=dict(color=t["accent"], width=1),
                            marker=dict(size=3)))
    return fig_update(fig, t, f"Tick Chart ({n_ticks})" + (f" — {symbol}" if symbol else ""), 400)


# ─────────────────────────────────────────────
# 3D VISUALIZATIONS (10 more)
# ─────────────────────────────────────────────

def plot_3d_price_surface(df, col_map, t):
    if not all(k in col_map for k in ["date", "high", "low", "close"]):
        return None

    df2 = df.copy()
    dt = pd.to_datetime(df2[col_map["date"]], errors="coerce")
    df2 = df2.loc[dt.notna()].copy()
    if df2.empty:
        return None

    df2["_dt"] = pd.to_datetime(df2[col_map["date"]], errors="coerce")
    df2["Price"] = (df2[col_map["high"]] + df2[col_map["low"]] + df2[col_map["close"]]) / 3
    df2["Day"] = df2["_dt"].dt.date.astype(str)
    df2["Hour"] = df2["_dt"].dt.hour.astype(int)

    surf = (
        df2.pivot_table(index="Day", columns="Hour", values="Price", aggfunc="mean")
        .sort_index(axis=0)
        .sort_index(axis=1)
    )
    if surf.empty:
        return None
    surf = surf.ffill(axis=1).bfill(axis=1).ffill(axis=0).bfill(axis=0)
    surf = surf.fillna(surf.stack().median() if not surf.stack().empty else 0.0)

    if surf.shape[0] == 1:
        surf = pd.concat([surf, surf], axis=0)
    if surf.shape[1] == 1:
        surf[surf.columns[0] + 1] = surf.iloc[:, 0]
        surf = surf.sort_index(axis=1)

    fig = go.Figure(
        data=[
            go.Surface(
                x=surf.columns.astype(int).tolist(),
                y=list(range(len(surf.index))),
                z=surf.values,
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Price"),
            )
        ]
    )
    fig = fig_update(fig, t, "3D Price Surface", 520)
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Hour"),
            yaxis=dict(
                title="Day",
                tickmode="array",
                tickvals=list(range(len(surf.index))),
                ticktext=surf.index.tolist(),
            ),
            zaxis=dict(title="Price"),
        )
    )
    return fig


def plot_3d_volume_price(df, col_map, t):
    if not all(k in col_map for k in ["close", "volume"]):
        return None
    df2 = df.copy()
    df2 = df2[[col_map["close"], col_map["volume"]]].dropna()
    if df2.empty:
        return None

    time_idx = np.arange(len(df2))
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=time_idx,
                y=df2[col_map["close"]],
                z=df2[col_map["volume"]],
                mode="markers",
                marker=dict(
                    size=3,
                    opacity=0.75,
                    color=df2[col_map["close"]],
                    colorscale="Plasma",
                    showscale=True,
                    colorbar=dict(title="Close"),
                ),
                name="Volume-Price",
            )
        ]
    )
    fig = fig_update(fig, t, "3D Volume-Price", 520)
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="Time Index"),
            yaxis=dict(title="Close"),
            zaxis=dict(title="Volume"),
        )
    )
    return fig


def plot_3d_returns_evolution(df, close_col, t):
    close = df[close_col].dropna()
    if len(close) < 3:
        return None

    horizons = [h for h in [1, 5, 10, 20, 60] if h < len(close)]
    if not horizons:
        return None

    z_rows = []
    for h in horizons:
        z_rows.append(close.pct_change(periods=h).fillna(0).values * 100)

    z = np.vstack(z_rows)
    x = np.arange(z.shape[1]).tolist()
    y = horizons

    fig = go.Figure(
        data=[
            go.Surface(
                x=x,
                y=y,
                z=z,
                colorscale="RdYlGn",
                showscale=True,
                colorbar=dict(title="Return %"),
            )
        ]
    )
    fig = fig_update(fig, t, "3D Returns Evolution", 520)
    fig.update_layout(scene=dict(xaxis=dict(title="Time Index"), yaxis=dict(title="Horizon (bars)"), zaxis=dict(title="Return %")))
    return fig


def plot_3d_rolling_std(df, close_col, t, window=20):
    close = df[close_col].dropna()
    if len(close) < 5:
        return None

    returns = close.pct_change().fillna(0) * 100
    windows = [w for w in [5, 10, window, 50] if w < len(returns)]
    windows = sorted(set(windows))
    if not windows:
        return None

    z_rows = []
    for w in windows:
        z_rows.append(returns.rolling(w, min_periods=max(2, w // 2)).std().fillna(0).values)

    z = np.vstack(z_rows)
    x = np.arange(z.shape[1]).tolist()
    y = windows

    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale="Blues", showscale=True, colorbar=dict(title="Std %"))])
    fig = fig_update(fig, t, f"3D Rolling Std Dev", 520)
    fig.update_layout(scene=dict(xaxis=dict(title="Time Index"), yaxis=dict(title="Window (bars)"), zaxis=dict(title="Std Dev (%)")))
    return fig


def plot_3d_correlation_surface(df, close_col, t):
    returns = df[close_col].pct_change().dropna()
    if len(returns) < 35:
        return None
    lags = list(range(1, 31))
    corr_surface = np.zeros((len(lags),), dtype=float)
    for i, lag in enumerate(lags):
        corr_surface[i] = returns.autocorr(lag=lag)
    z = np.vstack([corr_surface, corr_surface])
    fig = go.Figure(
        data=[
            go.Surface(
                x=lags,
                y=[0, 1],
                z=z,
                colorscale="IceFire",
                showscale=True,
                colorbar=dict(title="Corr"),
            )
        ]
    )
    fig = fig_update(fig, t, "3D Autocorrelation", 520)
    fig.update_layout(scene=dict(xaxis=dict(title="Lag"), yaxis=dict(title=""), zaxis=dict(title="Autocorr")))
    return fig


def plot_3d_price_distribution(df, close_col, t, bins=30):
    hist, bin_edges = np.histogram(df[close_col].dropna(), bins=bins)
    if hist.size < 2:
        return None
    centers = ((bin_edges[:-1] + bin_edges[1:]) / 2.0).tolist()
    z = np.vstack([hist, hist])
    fig = go.Figure(
        data=[
            go.Surface(
                x=centers,
                y=[0, 1],
                z=z,
                colorscale="Magma",
                showscale=True,
                colorbar=dict(title="Count"),
            )
        ]
    )
    fig = fig_update(fig, t, f"3D Price Distribution ({bins} bins)", 520)
    fig.update_layout(scene=dict(xaxis=dict(title="Price"), yaxis=dict(title=""), zaxis=dict(title="Count")))
    return fig


def plot_3d_volatility_cone(df, close_col, t):
    returns = df[close_col].pct_change().dropna()
    if len(returns) < 30:
        return None

    time_horizons = [h for h in [5, 10, 20, 30, 60] if h < len(returns)]
    if not time_horizons:
        return None

    vols = []
    for h in time_horizons:
        vol = returns.rolling(h, min_periods=h).std() * np.sqrt(252) * 100
        series = vol.dropna().values
        vols.append(series[-200:] if len(series) > 200 else series)

    if not vols or max(len(v) for v in vols) < 2:
        return None

    max_len = max(len(v) for v in vols)
    z = np.full((len(time_horizons), max_len), np.nan, dtype=float)
    for i, arr in enumerate(vols):
        if len(arr) > 0:
            z[i, -len(arr):] = arr

    fig = go.Figure(
        data=[
            go.Surface(
                x=list(range(max_len)),
                y=time_horizons,
                z=z,
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Vol %"),
            )
        ]
    )
    fig = fig_update(fig, t, "3D Volatility Cone", 520)
    fig.update_layout(scene=dict(xaxis=dict(title="Observation"), yaxis=dict(title="Window (bars)"), zaxis=dict(title="Volatility (%)")))
    return fig


def plot_3d_multi_timeframe(df, col_map, t):
    if "close" not in col_map:
        return None
    close = df[col_map["close"]]
    if close.dropna().empty or len(close) < 5:
        return None

    sma_5 = close.rolling(5, min_periods=1).mean().values
    sma_20 = close.rolling(20, min_periods=1).mean().values
    sma_50 = close.rolling(50, min_periods=1).mean().values
    time_idx = list(range(len(close)))

    z = np.vstack([sma_5, sma_20, sma_50])
    y = [5, 20, 50]
    fig = go.Figure(data=[go.Surface(x=time_idx, y=y, z=z, colorscale="Twilight", showscale=True, colorbar=dict(title="MA"))])
    fig = fig_update(fig, t, "3D Multi-Timeframe MA", 520)
    fig.update_layout(scene=dict(xaxis=dict(title="Time Index"), yaxis=dict(title="Window (bars)"), zaxis=dict(title="MA Value")))
    return fig


def plot_3d_volume_profile_3d(df, col_map, t, bins=20):
    if "close" not in col_map or "volume" not in col_map:
        return None
    try:
        close = df[col_map["close"]]
        vol = df[col_map["volume"]]
        price_bins = pd.cut(close, bins=bins, duplicates="drop")
        profile = vol.groupby(price_bins, observed=True).sum()
        if profile.empty or len(profile) < 2:
            return None

        if hasattr(profile.index, "mid"):
            x_vals = [float(i.mid) for i in profile.index]
        else:
            x_vals = list(range(len(profile)))

        z = np.vstack([profile.values, profile.values])
        fig = go.Figure(
            data=[
                go.Surface(
                    x=x_vals,
                    y=[0, 1],
                    z=z,
                    colorscale="Turbo",
                    showscale=True,
                    colorbar=dict(title="Volume"),
                )
            ]
        )
        fig = fig_update(fig, t, "3D Volume Profile", 520)
        fig.update_layout(scene=dict(xaxis=dict(title="Price Bin"), yaxis=dict(title=""), zaxis=dict(title="Volume")))
        return fig
    except Exception:
        return None


def plot_3d_heatmap_3d(df, close_col, t):
    df2 = df.copy()
    dt_col = None
    for c in df2.columns:
        if np.issubdtype(df2[c].dtype, np.datetime64):
            dt_col = c
            break
    if dt_col is None:
        for c in df2.columns:
            if str(c).strip().lower() in {"date", "datetime", "time", "timestamp"}:
                dt_col = c
                break

    if dt_col is None:
        return None

    df2["_dt"] = pd.to_datetime(df2[dt_col], errors="coerce")
    df2 = df2.loc[df2["_dt"].notna()].sort_values("_dt")
    if df2.empty:
        return None

    s = df2.set_index("_dt")[close_col].dropna()
    if len(s) < 35:
        return None

    monthly_close = s.resample("ME").last()
    monthly_ret = monthly_close.pct_change() * 100
    monthly_ret = monthly_ret.dropna()
    if monthly_ret.empty:
        return None

    mr = pd.DataFrame({"Year": monthly_ret.index.year, "Month": monthly_ret.index.month, "Return": monthly_ret.values})
    pivot = mr.pivot_table(index="Year", columns="Month", values="Return", aggfunc="mean").sort_index()
    if pivot.empty or pivot.shape[0] < 1 or pivot.shape[1] < 2:
        return None

    fig = go.Figure(
        data=[
            go.Surface(
                x=pivot.columns.tolist(),
                y=pivot.index.tolist(),
                z=pivot.values,
                colorscale="RdYlGn",
                showscale=True,
                colorbar=dict(title="Return %"),
            )
        ]
    )
    fig = fig_update(fig, t, "3D Monthly Returns", 520)
    fig.update_layout(scene=dict(xaxis=dict(title="Month"), yaxis=dict(title="Year"), zaxis=dict(title="Return %")))
    return fig


# ─────────────────────────────────────────────
# SUMMARY STATISTICS
# ─────────────────────────────────────────────

def compute_sharpe(close_series, risk_free=0.0):
    returns = close_series.pct_change().dropna()
    excess = returns - risk_free / 252
    if excess.std() == 0:
        return np.nan
    return (excess.mean() / excess.std()) * np.sqrt(252)


def build_stats_table(df, col_map):
    close = df[col_map["close"]]
    returns = close.pct_change().dropna()
    stats = {
        "Total Rows": len(df),
        "Start Date": df[col_map["date"]].min().date() if "date" in col_map else "N/A",
        "End Date": df[col_map["date"]].max().date() if "date" in col_map else "N/A",
        "Mean Close": round(close.mean(), 4),
        "Median Close": round(close.median(), 4),
        "Std Dev Close": round(close.std(), 4),
        "Min Close": round(close.min(), 4),
        "Max Close": round(close.max(), 4),
        "Mean Daily Return": f"{returns.mean()*100:.4f}%",
        "Return Std Dev": f"{returns.std()*100:.4f}%",
        "Annualised Volatility": f"{returns.std()*np.sqrt(252)*100:.2f}%",
        "Sharpe Ratio": round(compute_sharpe(close), 3),
        "Max Drawdown": f"{compute_drawdown(close).min()*100:.2f}%",
        "Cumulative Return": f"{((close.iloc[-1]/close.iloc[0])-1)*100:.2f}%" if len(close) > 1 else "N/A",
        "Skewness": round(returns.skew(), 4),
        "Kurtosis": round(returns.kurt(), 4),
    }
    return pd.DataFrame(list(stats.items()), columns=["Metric", "Value"])


# ─────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────

def to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df_dict):
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        for sheet, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet[:31], index=False)
    return buf.getvalue()


# ─────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────

def apply_sidebar_filters(df, col_map):
    with st.sidebar:
        st.markdown("### Filters")

        # Date range
        if "date" in col_map:
            d = col_map["date"]
            df[d] = pd.to_datetime(df[d], errors="coerce")
            min_d = df[d].min().date()
            max_d = df[d].max().date()
            if min_d < max_d:
                date_range = st.date_input(
                    "Date Range",
                    value=(min_d, max_d),
                    min_value=min_d, max_value=max_d
                )
                if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                    df = df[(df[d].dt.date >= date_range[0]) & (df[d].dt.date <= date_range[1])]

        # Symbol filter
        if "symbol" in col_map:
            s = col_map["symbol"]
            symbols = sorted(df[s].dropna().unique().tolist())
            if len(symbols) > 1:
                selected = st.multiselect(
                    "Symbol",
                    options=symbols,
                    default=symbols[:min(5, len(symbols))]
                )
                if selected:
                    df = df[df[s].isin(selected)]

        # Exchange filter
        if "exchange" in col_map:
            exc_col = col_map["exchange"]
            exchanges = sorted(df[exc_col].dropna().unique().tolist())
            if len(exchanges) > 1:
                sel_exc = st.multiselect("Exchange", options=exchanges, default=exchanges)
                if sel_exc:
                    df = df[df[exc_col].isin(sel_exc)]

        # Volume slider
        if "volume" in col_map:
            vol_col = col_map["volume"]
            vmin = int(df[vol_col].min())
            vmax = int(df[vol_col].max())
            if vmin < vmax:
                vol_range = st.slider("Volume Range", vmin, vmax, (vmin, vmax), step=max(1, (vmax - vmin) // 100))
                df = df[(df[vol_col] >= vol_range[0]) & (df[vol_col] <= vol_range[1])]

        st.markdown("---")
        st.caption(f"{len(df):,} rows after filters")

    return df


# ─────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────

def main():
    # Dark-mode only
    st.session_state["dark_mode"] = True

    t = get_theme()
    apply_css(t)

    # Header
    col_title, _ = st.columns([8, 1])
    with col_title:
        st.markdown(f"""
        <div style="margin-bottom:0.25rem">
            <span class="logo-text">Quantitative Analytics Platform</span>
        </div>
        <h1 style="margin:0;font-size:1.7rem;font-weight:700;">
            <span style="color:{t['text']}">Arth</span><span style="color:{t['accent']}">Veda</span> <span style="color:{t['subtext']}">Quant</span><span style="color:{t['purple']}">View</span>
        </h1>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # File upload
    with st.sidebar:
        st.markdown(f"<div style='font-size:0.7rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:{t['subtext']};margin-bottom:0.5rem'>Data Source</div>", unsafe_allow_html=True)
        uploaded_files = st.file_uploader("Upload CSV or Excel (Multiple)", type=["csv", "xlsx", "xls"], accept_multiple_files=True)
        
        if uploaded_files:
            st.markdown("### Uploaded Files")
            for f in uploaded_files:
                st.caption(f"📄 {f.name}")
            st.markdown("---")
        else:
            # Sample Excel template: realistic OHLCV (High >= max(Open,Close), Low <= min(Open,Close))
            rng = np.random.default_rng(42)
            dates = pd.date_range("2025-01-01", periods=60, freq="D")
            symbols = (["AAPL"] * 30) + (["MSFT"] * 30)
            base = np.concatenate([np.full(30, 180.0), np.full(30, 420.0)])
            drift = rng.normal(0, 1.2, size=60).cumsum()
            close = base + drift
            open_ = close + rng.normal(0, 0.9, size=60)
            high = np.maximum(open_, close) + np.abs(rng.normal(0.8, 0.5, size=60))
            low = np.minimum(open_, close) - np.abs(rng.normal(0.8, 0.5, size=60))
            volume = rng.integers(1_000_000, 6_000_000, size=60)

            df_sample = pd.DataFrame(
                {
                    "Date": dates.astype("datetime64[ns]"),
                    "Symbol": symbols,
                    "Open": np.round(open_, 2),
                    "High": np.round(high, 2),
                    "Low": np.round(low, 2),
                    "Close": np.round(close, 2),
                    "Adj Close": np.round(close, 2),
                    "Volume": volume.astype(int),
                    "Exchange": ["NASDAQ"] * 60,
                }
            )

            template_buffer = io.BytesIO()
            with pd.ExcelWriter(template_buffer, engine="xlsxwriter") as writer:
                df_sample.to_excel(writer, index=False, sheet_name="OHLCV")
                notes = pd.DataFrame(
                    {
                        "Notes": [
                            "Required columns: Date + Close. Recommended: Open, High, Low, Volume, Symbol (for multi-symbol).",
                            "Date formats supported: YYYY-MM-DD, Excel dates, or timestamps.",
                            "One row = one bar (daily/intraday). Keep symbols consistent (e.g., AAPL, MSFT).",
                            "You can delete sample rows and paste your own data under the same headers.",
                        ]
                    }
                )
                notes.to_excel(writer, index=False, sheet_name="README")
            template_buffer.seek(0)
            st.markdown("#### Download Sample Excel Template")
            st.download_button(
                label="Download Excel Template",
                data=template_buffer.getvalue(),
                file_name="ArthVeda_QuantView_Sample_Template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.markdown("---")

    if uploaded_files is None or len(uploaded_files) == 0:
        st.markdown(f"""
        <div style="border:1px dashed {t['border']};border-radius:12px;padding:3rem 2rem;
                    text-align:center;background:{t['surface']};margin-top:2rem">
            <div style="font-size:2rem;margin-bottom:1rem">📂</div>
            <div style="font-size:1rem;font-weight:500;color:{t['text']};margin-bottom:0.5rem">
                Upload a Market Data File to Begin
            </div>
            <div style="font-size:0.82rem;color:{t['subtext']}">
                Supports CSV and Excel (.xlsx). Accepts OHLCV, multi-symbol, and Nasdaq-style datasets.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"<footer>Made by Sourish Dey</footer>", unsafe_allow_html=True)
        return

    # Load data
    with st.spinner("Loading data..."):
        all_dfs = []
        for uploaded in uploaded_files:
            raw_df, err = load_data(uploaded)
            if err:
                st.error(f"Error loading {uploaded.name}: {err}")
                continue
            if raw_df is not None:
                all_dfs.append(raw_df)
        
        if not all_dfs:
            st.error("No data could be loaded from uploaded files.")
            return
        
        if len(all_dfs) == 1:
            raw_df = all_dfs[0]
        else:
            raw_df = pd.concat(all_dfs, ignore_index=True)
            st.success(f"Combined {len(all_dfs)} files into single dataset.")

    df_proc, col_map = preprocess_data(raw_df)

    if not col_map:
        st.error("Could not detect any recognised columns. Please check your file structure.")
        return

    is_multi = "symbol" in col_map and df_proc[col_map["symbol"]].nunique() > 1

    # Sidebar filters
    df = apply_sidebar_filters(df_proc, col_map)

    if df.empty:
        st.warning("No data matches the current filters.")
        return

    # Pick primary symbol for single-stock views
    if is_multi and "symbol" in col_map:
        syms = sorted(df[col_map["symbol"]].unique().tolist())
        with st.sidebar:
            primary_sym = st.selectbox("Primary Symbol (for single-stock charts)", syms)
        df_primary = df[df[col_map["symbol"]] == primary_sym].sort_values(col_map.get("date", df.columns[0]))
    else:
        primary_sym = None
        df_primary = df

    date_col = col_map.get("date")
    close_col = col_map.get("close")
    vol_col = col_map.get("volume")

    # ── TABS ──────────────────────────────────
    tabs = st.tabs([
        "Overview",
        "Price Analytics",
        "Volume Analytics",
        "Statistical Insights",
        "Technical Indicators",
        "Trend & Pattern",
        "Risk & Outliers",
        "Candlestick Charts",
        "3D Visualizations",
        "Multi-Symbol",
        "Export",
    ])

    # ── 1. OVERVIEW ───────────────────────────
    with tabs[0]:
        st.markdown(f"<div class='section-header'>Dataset Overview</div>", unsafe_allow_html=True)

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Rows", f"{len(df):,}")
        m2.metric("Columns", f"{df.shape[1]}")
        m3.metric("Date Range", f"{df[date_col].dt.date.min() if date_col else 'N/A'}")
        m4.metric("Symbols", f"{df[col_map['symbol']].nunique() if 'symbol' in col_map else 1}")
        m5.metric("Missing %", f"{(df.isnull().sum().sum() / df.size * 100):.2f}%")

        st.markdown(f"<div class='section-header'>Column Types</div>", unsafe_allow_html=True)
        dtype_df = pd.DataFrame({
            "Column": df.columns,
            "Type": df.dtypes.astype(str).values,
            "Non-Null": df.notnull().sum().values,
            "Null": df.isnull().sum().values,
            "Unique": df.nunique().values,
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

        st.markdown(f"<div class='section-header'>Missing Values</div>", unsafe_allow_html=True)
        miss = df.isnull().sum()
        miss = miss[miss > 0]
        if miss.empty:
            st.success("No missing values detected.")
        else:
            st.dataframe(
                pd.DataFrame({"Column": miss.index, "Missing": miss.values,
                               "%": (miss.values / len(df) * 100).round(2)}),
                use_container_width=True, hide_index=True
            )

        st.markdown(f"<div class='section-header'>Data Preview</div>", unsafe_allow_html=True)
        r1, r2 = st.columns(2)
        with r1:
            st.caption("Head (10 rows)")
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)
        with r2:
            st.caption("Tail (10 rows)")
            st.dataframe(df.tail(10), use_container_width=True, hide_index=True)

        st.markdown(f"<div class='section-header'>Numeric Summary</div>", unsafe_allow_html=True)
        st.dataframe(df.describe().round(4).T, use_container_width=True)

    # ── 2. PRICE ANALYTICS ────────────────────
    with tabs[1]:
        if close_col is None:
            st.info("Close price column not found.")
        elif date_col is None:
            st.info("Date column not found.")
        else:
            st.markdown(f"<div class='section-header'>Close Price</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_line_close(df_primary, date_col, close_col, t, primary_sym),
                            use_container_width=True)

            st.markdown(f"<div class='section-header'>Candlestick</div>", unsafe_allow_html=True)
            if "open" in col_map and "high" in col_map and "low" in col_map:
                st.plotly_chart(plot_candlestick(df_primary, col_map, t, primary_sym),
                                use_container_width=True)
            else:
                st.info("Open/High/Low columns not found — candlestick unavailable.")

            st.markdown(f"<div class='section-header'>Moving Averages</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(plot_moving_averages(df_primary, date_col, close_col, t),
                                use_container_width=True)
            with c2:
                st.plotly_chart(plot_rolling_mean_multi(df_primary, date_col, close_col, t),
                                use_container_width=True)

            st.markdown(f"<div class='section-header'>Bollinger Bands & Bands</div>", unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                st.plotly_chart(plot_bollinger(df_primary, date_col, close_col, t),
                                use_container_width=True)
            with c4:
                st.plotly_chart(plot_rolling_minmax(df_primary, date_col, close_col, t),
                                use_container_width=True)

            st.markdown(f"<div class='section-header'>Distribution & Log Price</div>", unsafe_allow_html=True)
            c5, c6 = st.columns(2)
            with c5:
                st.plotly_chart(plot_price_distribution(df_primary, close_col, t),
                                use_container_width=True)
            with c6:
                st.plotly_chart(plot_log_price(df_primary, date_col, close_col, t),
                                use_container_width=True)

            st.markdown(f"<div class='section-header'>Box Plots</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_boxplot_price(df_primary, date_col, close_col, t),
                            use_container_width=True)

            if "high" in col_map and "low" in col_map:
                intra = plot_intraday_variation(df_primary, date_col, col_map, t)
                if intra:
                    st.markdown(f"<div class='section-header'>Intraday Variation</div>", unsafe_allow_html=True)
                    st.plotly_chart(intra, use_container_width=True)

    # ── 3. VOLUME ANALYTICS ───────────────────
    with tabs[2]:
        if vol_col is None:
            st.info("Volume column not found.")
        elif date_col is None:
            st.info("Date column not found.")
        else:
            st.markdown(f"<div class='section-header'>Volume Overview</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_volume_bar(df_primary, date_col, vol_col, close_col or vol_col, t),
                            use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(plot_volume_ma(df_primary, date_col, vol_col, t),
                                use_container_width=True)
            with c2:
                st.plotly_chart(plot_volume_spikes(df_primary, date_col, vol_col, t),
                                use_container_width=True)

            st.markdown(f"<div class='section-header'>Volume Distribution & Cumulative</div>", unsafe_allow_html=True)
            c3, c4 = st.columns(2)
            with c3:
                st.plotly_chart(plot_volume_distribution(df_primary, vol_col, t),
                                use_container_width=True)
            with c4:
                st.plotly_chart(plot_cumulative_volume(df_primary, date_col, vol_col, t),
                                use_container_width=True)

            st.markdown(f"<div class='section-header'>Volume by Quarter (Box)</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_boxplot_volume(df_primary, date_col, vol_col, t),
                            use_container_width=True)

            if close_col:
                st.markdown(f"<div class='section-header'>Price vs Volume</div>", unsafe_allow_html=True)
                st.plotly_chart(plot_scatter_price_volume(df_primary, close_col, vol_col, date_col, t),
                                use_container_width=True)

            if "exchange" in col_map:
                st.markdown(f"<div class='section-header'>Volume by Exchange</div>", unsafe_allow_html=True)
                st.plotly_chart(plot_exchange_volume(df, vol_col, col_map["exchange"], t),
                                use_container_width=True)

    # ── 4. STATISTICAL INSIGHTS ───────────────
    with tabs[3]:
        if close_col is None or date_col is None:
            st.info("Close/Date columns required for statistical analysis.")
        else:
            st.markdown(f"<div class='section-header'>Returns Analysis</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(plot_daily_returns(df_primary, date_col, close_col, t),
                                use_container_width=True)
            with c2:
                st.plotly_chart(plot_cumulative_returns(df_primary, date_col, close_col, t),
                                use_container_width=True)

            c3, c4 = st.columns(2)
            with c3:
                st.plotly_chart(plot_rolling_volatility(df_primary, date_col, close_col, t),
                                use_container_width=True)
            with c4:
                st.plotly_chart(plot_returns_distribution(df_primary, close_col, t),
                                use_container_width=True)

            st.markdown(f"<div class='section-header'>Autocorrelation & Frequency</div>", unsafe_allow_html=True)
            c5, c6 = st.columns(2)
            with c5:
                st.plotly_chart(plot_lag_autocorr(df_primary, close_col, t), use_container_width=True)
            with c6:
                st.plotly_chart(plot_price_change_freq(df_primary, close_col, t), use_container_width=True)

            st.markdown(f"<div class='section-header'>Seasonal Heatmaps</div>", unsafe_allow_html=True)
            c7, c8 = st.columns(2)
            with c7:
                rh = plot_returns_heatmap(df_primary, date_col, close_col, t)
                if rh:
                    st.plotly_chart(rh, use_container_width=True)
            with c8:
                vh = plot_volatility_heatmap(df_primary, date_col, close_col, t)
                if vh:
                    st.plotly_chart(vh, use_container_width=True)

            st.markdown(f"<div class='section-header'>Summary Statistics</div>", unsafe_allow_html=True)
            stats_df = build_stats_table(df_primary, col_map)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)

            if is_multi and "symbol" in col_map:
                st.markdown(f"<div class='section-header'>Return Correlation (Multi-Symbol)</div>", unsafe_allow_html=True)
                pivot = df.pivot_table(index=date_col, columns=col_map["symbol"],
                                       values=close_col, aggfunc="last")
                pivot_ret = pivot.pct_change().dropna()
                if not pivot_ret.empty and pivot_ret.shape[1] > 1:
                    st.plotly_chart(plot_correlation_heatmap(pivot_ret, t), use_container_width=True)

    # ── 5. TECHNICAL INDICATORS ───────────────
    with tabs[4]:
        if close_col is None or date_col is None:
            st.info("Close/Date columns required.")
        else:
            st.markdown(f"<div class='section-header'>RSI</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_rsi(df_primary, date_col, close_col, t), use_container_width=True)

            st.markdown(f"<div class='section-header'>MACD</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_macd(df_primary, date_col, close_col, t), use_container_width=True)

            st.markdown(f"<div class='section-header'>EMA & Momentum</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(plot_ema_multi(df_primary, date_col, close_col, t), use_container_width=True)
            with c2:
                st.plotly_chart(plot_momentum(df_primary, date_col, close_col, t), use_container_width=True)

            if "high" in col_map and "low" in col_map:
                st.markdown(f"<div class='section-header'>ATR</div>", unsafe_allow_html=True)
                atr_fig = plot_atr(df_primary, col_map, t)
                if atr_fig:
                    st.plotly_chart(atr_fig, use_container_width=True)

            st.markdown(f"<div class='section-header'>Advanced Indicators</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                ha_fig = plot_heikin_ashi(df_primary, col_map, t, primary_sym)
                if ha_fig:
                    st.plotly_chart(ha_fig, use_container_width=True)
            with c2:
                kc_fig = plot_keltner_channels(df_primary, date_col, close_col, t)
                if kc_fig:
                    st.plotly_chart(kc_fig, use_container_width=True)

            c3, c4 = st.columns(2)
            with c3:
                dc_fig = plot_donchian_channels(df_primary, date_col, close_col, t)
                st.plotly_chart(dc_fig, use_container_width=True)
            with c4:
                stoch_fig = plot_stochastic_oscillator(df_primary, date_col, close_col, t)
                if stoch_fig:
                    st.plotly_chart(stoch_fig, use_container_width=True)

            c5, c6 = st.columns(2)
            with c5:
                cci_fig = plot_cci(df_primary, col_map, t)
                if cci_fig:
                    st.plotly_chart(cci_fig, use_container_width=True)
            with c6:
                wr_fig = plot_williams_r(df_primary, col_map, t)
                if wr_fig:
                    st.plotly_chart(wr_fig, use_container_width=True)

            c7, c8 = st.columns(2)
            with c7:
                obv_fig = plot_OBV(df_primary, date_col, close_col, vol_col or close_col, t)
                if obv_fig and vol_col:
                    st.plotly_chart(obv_fig, use_container_width=True)
            with c8:
                mfi_fig = plot_mfi(df_primary, col_map, t)
                if mfi_fig:
                    st.plotly_chart(mfi_fig, use_container_width=True)

            if all(k in col_map for k in ["high", "low", "close", "volume"]):
                st.markdown(f"<div class='section-header'>Volume Indicators</div>", unsafe_allow_html=True)
                c9, c10 = st.columns(2)
                with c9:
                    vwap_fig = plot_vwap(df_primary, col_map, t)
                    if vwap_fig:
                        st.plotly_chart(vwap_fig, use_container_width=True)
                with c10:
                    vp_fig = plot_volume_profile(df_primary, date_col, vol_col, close_col, t)
                    if vp_fig:
                        st.plotly_chart(vp_fig, use_container_width=True)

            st.markdown(f"<div class='section-header'>Advanced Patterns</div>", unsafe_allow_html=True)
            c11, c12 = st.columns(2)
            with c11:
                pivot_fig = plot_pivot_points(df_primary, col_map, t)
                if pivot_fig:
                    st.plotly_chart(pivot_fig, use_container_width=True)
            with c12:
                fib_fig = plot_fibonacci_retrace(df_primary, close_col, t)
                st.plotly_chart(fib_fig, use_container_width=True)

            c13, c14 = st.columns(2)
            with c13:
                sar_fig = plot_parabolic_sar(df_primary, col_map, t)
                if sar_fig:
                    st.plotly_chart(sar_fig, use_container_width=True)
            with c14:
                trix_fig = plot_trix(df_primary, date_col, close_col, t)
                st.plotly_chart(trix_fig, use_container_width=True)

            c15, c16 = st.columns(2)
            with c15:
                kama_fig = plot_kama(df_primary, date_col, close_col, t)
                st.plotly_chart(kama_fig, use_container_width=True)
            with c16:
                if close_col:
                    aroon_fig = plot_aroon(df_primary[close_col], t)
                    st.plotly_chart(aroon_fig, use_container_width=True)

            c17, c18 = st.columns(2)
            with c17:
                if close_col:
                    kst_fig = plot_kst(df_primary[close_col], t)
                    st.plotly_chart(kst_fig, use_container_width=True)
            with c18:
                if close_col:
                    ppo_fig = plot_ppo(df_primary[close_col], t)
                    st.plotly_chart(ppo_fig, use_container_width=True)

            c19, c20 = st.columns(2)
            with c19:
                dpo_fig = plot_dpo(df_primary, date_col, close_col, t)
                st.plotly_chart(dpo_fig, use_container_width=True)
            with c20:
                tema_fig = plot_tema(df_primary, date_col, close_col, t)
                st.plotly_chart(tema_fig, use_container_width=True)

    # ── 6. TREND & PATTERN ────────────────────
    with tabs[5]:
        if close_col is None or date_col is None:
            st.info("Close/Date columns required.")
        else:
            st.markdown(f"<div class='section-header'>Trend Direction</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_trend(df_primary, date_col, close_col, t), use_container_width=True)

            st.markdown(f"<div class='section-header'>Advanced Trend Analysis</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                zz_fig = plot_zigzag(df_primary, close_col, t)
                st.plotly_chart(zz_fig, use_container_width=True)
            with c2:
                lb_fig = plot_line_break(df_primary, close_col, t)
                st.plotly_chart(lb_fig, use_container_width=True)

            c3, c4 = st.columns(2)
            with c3:
                vel_fig = plot_price_velocity(df_primary, date_col, close_col, t)
                st.plotly_chart(vel_fig, use_container_width=True)
            with c4:
                acc_fig = plot_acceleration(df_primary, date_col, close_col, t)
                st.plotly_chart(acc_fig, use_container_width=True)

            c5, c6 = st.columns(2)
            with c5:
                qstick_fig = plot_qstick(df_primary, date_col, close_col, t)
                st.plotly_chart(qstick_fig, use_container_width=True)
            with c6:
                kelt_break_fig = plot_keltner_breakout(df_primary, col_map, t)
                if kelt_break_fig:
                    st.plotly_chart(kelt_break_fig, use_container_width=True)

            st.markdown(f"<div class='section-header'>Support & Resistance + Breakouts</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(plot_support_resistance(df_primary, date_col, close_col, t),
                                use_container_width=True)
            with c2:
                st.plotly_chart(plot_breakout(df_primary, date_col, close_col, t),
                                use_container_width=True)

    # ── 7. RISK & OUTLIERS ────────────────────
    with tabs[6]:
        if close_col is None or date_col is None:
            st.info("Close/Date columns required.")
        else:
            st.markdown(f"<div class='section-header'>Drawdown</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_drawdown(df_primary, date_col, close_col, t), use_container_width=True)

            st.markdown(f"<div class='section-header'>Anomaly Detection</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(plot_zscore_anomalies(df_primary, date_col, close_col, t),
                                use_container_width=True)
            with c2:
                if vol_col:
                    st.plotly_chart(plot_volume_anomalies(df_primary, date_col, vol_col, t),
                                    use_container_width=True)
                else:
                    st.info("Volume column not available.")

            # Price outlier table
            st.markdown(f"<div class='section-header'>Price Outlier Table</div>", unsafe_allow_html=True)
            z = compute_zscore(df_primary[close_col], 20)
            outliers = df_primary[z.abs() > 2.5].copy()
            if not outliers.empty:
                st.dataframe(outliers[[c for c in [date_col, close_col, vol_col,
                                                    col_map.get("symbol")] if c]].head(50),
                             use_container_width=True, hide_index=True)
            else:
                st.success("No significant price outliers detected.")

    # ── 9. CANDLESTICK CHARTS ───────────────────
    with tabs[7]:
        if close_col is None or date_col is None:
            st.info("Close/Date columns required.")
        elif not all(k in col_map for k in ["open", "high", "low", "close"]):
            st.info("OHLC data required for candlestick charts.")
        else:
            st.markdown(f"<div class='section-header'>HLC Chart</div>", unsafe_allow_html=True)
            hlc_fig = plot_hlc(df_primary, col_map, t, primary_sym)
            if hlc_fig:
                st.plotly_chart(hlc_fig, use_container_width=True)
            
            st.markdown(f"<div class='section-header'>Wide OHLC Chart</div>", unsafe_allow_html=True)
            ohlc_fig = plot_ohlc_wide(df_primary, col_map, t, primary_sym)
            if ohlc_fig:
                st.plotly_chart(ohlc_fig, use_container_width=True)
            
            st.markdown(f"<div class='section-header'>Candle Body Colors</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_candle_colors(df_primary, col_map, t, primary_sym), use_container_width=True)
            
            st.markdown(f"<div class='section-header'>Price Range Bars</div>", unsafe_allow_html=True)
            st.plotly_chart(plot_price_range_bars(df_primary, col_map, t, primary_sym), use_container_width=True)
            
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div class='section-header'>Point & Figure</div>", unsafe_allow_html=True)
                st.plotly_chart(plot_point_figure(df_primary, close_col, t, primary_sym), use_container_width=True)
            with c2:
                st.markdown(f"<div class='section-header'>Kagi Chart</div>", unsafe_allow_html=True)
                st.plotly_chart(plot_kagi(df_primary, close_col, t, primary_sym), use_container_width=True)
            
            c3, c4 = st.columns(2)
            with c3:
                st.markdown(f"<div class='section-header'>Range Bars</div>", unsafe_allow_html=True)
                st.plotly_chart(plot_range_bars(df_primary, close_col, t, primary_sym), use_container_width=True)
            with c4:
                st.markdown(f"<div class='section-header'>Dollar Bars</div>", unsafe_allow_html=True)
                if vol_col:
                    st.plotly_chart(plot_dollar_bars(df_primary, close_col, vol_col, t, primary_sym), use_container_width=True)
            
            c5, c6 = st.columns(2)
            with c5:
                st.markdown(f"<div class='section-header'>Volumetric Bars</div>", unsafe_allow_html=True)
                if vol_col:
                    st.plotly_chart(plot_volumetric_bars(df_primary, close_col, vol_col, t, primary_sym), use_container_width=True)
            with c6:
                st.markdown(f"<div class='section-header'>Tick Chart</div>", unsafe_allow_html=True)
                st.plotly_chart(plot_ticks(df_primary, close_col, t, primary_sym), use_container_width=True)

    # ── 10. 3D VISUALIZATIONS ───────────────────
    with tabs[8]:
        if close_col is None:
            st.info("Close column required.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"<div class='section-header'>3D Price Surface</div>", unsafe_allow_html=True)
                ps_fig = plot_3d_price_surface(df_primary, col_map, t)
                if ps_fig:
                    st.plotly_chart(ps_fig, use_container_width=True)
            with c2:
                st.markdown(f"<div class='section-header'>3D Volume-Price</div>", unsafe_allow_html=True)
                vp_fig = plot_3d_volume_price(df_primary, col_map, t)
                if vp_fig:
                    st.plotly_chart(vp_fig, use_container_width=True)
            
            c3, c4 = st.columns(2)
            with c3:
                st.markdown(f"<div class='section-header'>3D Returns Evolution</div>", unsafe_allow_html=True)
                re_fig = plot_3d_returns_evolution(df_primary, close_col, t)
                if re_fig:
                    st.plotly_chart(re_fig, use_container_width=True)
                else:
                    st.info("Not enough data to render 3D returns evolution.")
            with c4:
                st.markdown(f"<div class='section-header'>3D Rolling Std Dev</div>", unsafe_allow_html=True)
                rs_fig = plot_3d_rolling_std(df_primary, close_col, t)
                if rs_fig:
                    st.plotly_chart(rs_fig, use_container_width=True)
                else:
                    st.info("Not enough data to render 3D rolling std dev.")
            
            c5, c6 = st.columns(2)
            with c5:
                st.markdown(f"<div class='section-header'>3D Autocorrelation</div>", unsafe_allow_html=True)
                ac_fig = plot_3d_correlation_surface(df_primary, close_col, t)
                if ac_fig:
                    st.plotly_chart(ac_fig, use_container_width=True)
                else:
                    st.info("Not enough data to render 3D autocorrelation.")
            with c6:
                st.markdown(f"<div class='section-header'>3D Price Distribution</div>", unsafe_allow_html=True)
                pd_fig = plot_3d_price_distribution(df_primary, close_col, t)
                if pd_fig:
                    st.plotly_chart(pd_fig, use_container_width=True)
                else:
                    st.info("Not enough data to render 3D price distribution.")
            
            st.markdown(f"<div class='section-header'>3D Volatility Cone</div>", unsafe_allow_html=True)
            vc_fig = plot_3d_volatility_cone(df_primary, close_col, t)
            if vc_fig:
                st.plotly_chart(vc_fig, use_container_width=True)
            else:
                st.info("Not enough data to render 3D volatility cone.")
            
            st.markdown(f"<div class='section-header'>3D Multi-Timeframe MA</div>", unsafe_allow_html=True)
            mt_fig = plot_3d_multi_timeframe(df_primary, col_map, t)
            if mt_fig:
                st.plotly_chart(mt_fig, use_container_width=True)
            
            c7, c8 = st.columns(2)
            with c7:
                st.markdown(f"<div class='section-header'>3D Volume Profile</div>", unsafe_allow_html=True)
                if vol_col:
                    vp3d_fig = plot_3d_volume_profile_3d(df_primary, col_map, t)
                    if vp3d_fig:
                        st.plotly_chart(vp3d_fig, use_container_width=True)
                    else:
                        st.info("Not enough data to render 3D volume profile.")
            with c8:
                st.markdown(f"<div class='section-header'>3D Monthly Returns</div>", unsafe_allow_html=True)
                mr_fig = plot_3d_heatmap_3d(df_primary, close_col, t)
                if mr_fig:
                    st.plotly_chart(mr_fig, use_container_width=True)
                else:
                    st.info("Not enough data to render 3D monthly returns.")

    # ── 11. MULTI-SYMBOL ───────────────────────
    with tabs[9]:
        if not is_multi:
            st.info("Multi-symbol views require a dataset with multiple symbols (Symbol/Ticker column).")
        elif close_col is None or date_col is None:
            st.info("Close/Date columns required.")
        else:
            st.markdown(f"<div class='section-header'>Normalised Price Comparison</div>", unsafe_allow_html=True)
            st.plotly_chart(
                plot_multi_symbol_compare(df, date_col, close_col, col_map["symbol"], t),
                use_container_width=True
            )

            st.markdown(f"<div class='section-header'>Symbol Ranking</div>", unsafe_allow_html=True)
            rank_fig = plot_ranking_chart(df, date_col, close_col, col_map["symbol"], t)
            if rank_fig:
                st.plotly_chart(rank_fig, use_container_width=True)

            st.markdown(f"<div class='section-header'>Rolling Correlation</div>", unsafe_allow_html=True)
            rc = plot_rolling_corr(df, date_col, close_col, col_map["symbol"], t)
            if rc:
                st.plotly_chart(rc, use_container_width=True)
            else:
                st.info("Need at least 2 symbols with sufficient data for rolling correlation.")

            st.markdown(f"<div class='section-header'>Return Correlation Heatmap</div>", unsafe_allow_html=True)
            pivot = df.pivot_table(index=date_col, columns=col_map["symbol"],
                                   values=close_col, aggfunc="last")
            pivot_ret = pivot.pct_change().dropna()
            if not pivot_ret.empty and pivot_ret.shape[1] > 1:
                st.plotly_chart(plot_correlation_heatmap(pivot_ret, t), use_container_width=True)

    # ── 12. EXPORT ─────────────────────────────
    with tabs[10]:
        st.markdown(f"<div class='section-header'>Export Data</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                label="Download Cleaned Data (CSV)",
                data=to_csv_bytes(df),
                file_name="arthveda_cleaned.csv",
                mime="text/csv"
            )
        with c2:
            if close_col:
                stats_df = build_stats_table(df_primary, col_map)
                st.download_button(
                    label="Download Summary Stats (CSV)",
                    data=to_csv_bytes(stats_df),
                    file_name="arthveda_summary.csv",
                    mime="text/csv"
                )
        with c3:
            if close_col:
                stats_df = build_stats_table(df_primary, col_map)
                excel_bytes = to_excel_bytes({
                    "Cleaned Data": df.head(50000),
                    "Summary Stats": stats_df,
                })
                st.download_button(
                    label="Download Full Report (Excel)",
                    data=excel_bytes,
                    file_name="arthveda_report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

        st.markdown(f"<div class='section-header'>Detected Column Mapping</div>", unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame(list(col_map.items()), columns=["Logical Field", "Dataset Column"]),
            use_container_width=True, hide_index=True
        )

    # Footer
    st.markdown(f"<footer>Made by Sourish Dey &nbsp;·&nbsp; ArthVeda QuantView &nbsp;·&nbsp; Powered by Streamlit & Plotly</footer>",
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
