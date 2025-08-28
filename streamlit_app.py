# streamlit_app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt

st.set_page_config(page_title="Morning Market Dashboard", layout="wide")

# ---------- Config (edit symbols as needed) ----------
SYMBOLS = [
    "^NSEI", "^NSEBANK",
    "RELIANCE.NS","HDFCBANK.NS","ICICIBANK.NS","INFY.NS","TCS.NS",
    "LT.NS","SBIN.NS","AXISBANK.NS","HINDUNILVR.NS","TITAN.NS"
]
SHORT_EMA = 20
LONG_EMA = 50
RSI_PERIOD = 14
LOOKBACK_DAYS = 90

# Auto refresh seconds (meta refresh)
AUTO_REFRESH_SECONDS = 60  # change if you want faster/slower

# ---------- Helpers ----------
@st.cache_data(ttl=60)
def fetch_hist(ticker, days=LOOKBACK_DAYS):
    try:
        df = yf.download(ticker, period=f"{days}d", interval="1d", progress=False, auto_adjust=False)
        if df is None or df.empty:
            return None
        return df
    except Exception as e:
        return None

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def rsi(series, period=RSI_PERIOD):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100/(1+rs))

def compute_stats(ticker):
    df = fetch_hist(ticker)
    if df is None: return None
    c = df['Close']
    se = ema(c, SHORT_EMA).iloc[-1]
    le = ema(c, LONG_EMA).iloc[-1]
    rrsi = rsi(c).iloc[-1] if len(c) > RSI_PERIOD else np.nan
    ret1 = (c.pct_change(1).iloc[-1]) * 100 if len(c) > 1 else np.nan
    ret5 = (c.pct_change(5).iloc[-1]) * 100 if len(c) > 5 else np.nan
    trend = "Bullish" if se > le else "Bearish"
    latest = {
        "symbol": ticker,
        "close": float(c.iloc[-1]),
        "ema_short": float(se),
        "ema_long": float(le),
        "rsi": float(rrsi) if not np.isnan(rrsi) else None,
        "ret1": float(ret1) if not np.isnan(ret1) else None,
        "ret5": float(ret5) if not np.isnan(ret5) else None,
        "trend": trend
    }
    return latest

# ---------- UI ----------
st.title("🧠 Morning Market Dashboard — One-click (Auto-refresh)")

col1, col2 = st.columns([1,3])
with col1:
    st.markdown("**Settings**")
    st.write(f"Auto refresh: every {AUTO_REFRESH_SECONDS} sec (meta refresh)")
    st.write("Data source: Yahoo Finance (daily).")
    if st.button("Refresh now"):
        st.experimental_rerun()

with col2:
    now = dt.datetime.now().astimezone()
    st.markdown(f"**Last updated:** {now.strftime('%Y-%m-%d %H:%M:%S')}")
    st.info("Note: Pre-open exact orderbook data needs broker API. This dashboard gives fast, morning-ready directional ideas (EMA20/50 + RSI + momentum). Use risk controls.")

# fetch all
results = []
for s in SYMBOLS:
    stats = compute_stats(s)
    if stats:
        results.append(stats)

if not results:
    st.error("Data fetch failed. Try again in a moment.")
else:
    df = pd.DataFrame(results)
    st.subheader("Market snapshot (selected symbols)")
    df_sorted = df.sort_values(by=["trend","ret5"], ascending=[False, False])
    df_display = df_sorted[["symbol","close","trend","rsi","ret1","ret5"]]
    df_display = df_display.rename(columns={
        "symbol":"Symbol","close":"Close","trend":"Trend","rsi":"RSI","ret1":"1D %","ret5":"5D %"
    })
    st.dataframe(df_display.style.format({"Close":"{:.2f}","RSI":"{:.2f}","1D %":"{:.2f}","5D %":"{:.2f}"}), use_container_width=True)

    st.subheader("Top morning trade ideas (simple filter)")
    longs = df[(df['trend']=="Bullish") & (df['rsi']>=55)].sort_values("ret5", ascending=False).head(5)
    shorts = df[(df['trend']=="Bearish") & (df['rsi']<=45)].sort_values("ret5").head(5)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Long candidates**")
        if not longs.empty:
            for _, r in longs.iterrows():
                st.write(f"{r['symbol']} — Close: {r['close']:.2f} — 5D: {r['ret5']:.2f}% — RSI: {r['rsi']:.2f}")
        else:
            st.write("No strong longs now")

    with c2:
        st.markdown("**Short candidates**")
        if not shorts.empty:
            for _, r in shorts.iterrows():
                st.write(f"{r['symbol']} — Close: {r['close']:.2f} — 5D: {r['ret5']:.2f}% — RSI: {r['rsi']:.2f}")
        else:
            st.write("No strong shorts now")

# meta refresh for auto-reload in the browser
refresh_html = f"<meta http-equiv=\"refresh\" content=\"{AUTO_REFRESH_SECONDS}\">"
st.components.v1.html(refresh_html, height=0)