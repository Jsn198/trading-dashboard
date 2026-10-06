# ============================================================
# INDIAN STOCK SWING TRADING DASHBOARD
# Streamlit Application
# ============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIG (MUST BE FIRST)
# ============================================================
st.set_page_config(
    page_title="Swing Trading Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
    }
    .main-header h1 { margin: 0; font-size: 32px; }
    .main-header p { margin: 8px 0 0 0; opacity: 0.9; }
    
        .regime-card {
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 6px solid #95a5a6;
        background: white;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        color: #2c3e50 !important;
    }
    .regime-card p {
        color: #2c3e50 !important;
        margin: 6px 0;
    }
    .regime-bullish { border-left-color: #00b894; }
    .regime-cautious { border-left-color: #fdcb6e; }
    .regime-bearish { border-left-color: #d63031; }
    
    .regime-title { font-size: 22px; font-weight: bold; margin-bottom: 8px; }
    .regime-bullish .regime-title { color: #00b894; }
    .regime-cautious .regime-title { color: #f39c12; }
    .regime-bearish .regime-title { color: #d63031; }    
    .stock-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    .stock-symbol { font-size: 22px; font-weight: bold; color: #2c3e50; }
    .stock-sector { color: #7f8c8d; font-size: 13px; }
    .stock-score { font-size: 28px; font-weight: bold; float: right; }
    .score-high { color: #00b894; }
    .score-medium { color: #f39c12; }
    .score-low { color: #d63031; }
    
    .metric-box {
        background: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        margin: 5px 0;
    }
    .metric-value { font-size: 18px; font-weight: bold; color: #2c3e50; }
    .metric-label { font-size: 11px; color: #7f8c8d; margin-top: 4px; }
    
    .factor-badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 3px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-good { background: #d4edda; color: #155724; }
    .badge-ok { background: #fff3cd; color: #856404; }
    .badge-weak { background: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# STOCK UNIVERSE
# ============================================================
NIFTY50 = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'KOTAKBANK.NS',
    'BAJFINANCE.NS', 'LT.NS', 'WIPRO.NS', 'AXISBANK.NS', 'TITAN.NS',
    'ASIANPAINT.NS', 'MARUTI.NS', 'SUNPHARMA.NS', 'HCLTECH.NS', 'ONGC.NS',
    'NTPC.NS', 'POWERGRID.NS', 'NESTLEIND.NS', 'ULTRACEMCO.NS', 'JSWSTEEL.NS',
    'TECHM.NS', 'BAJAJFINSV.NS', 'TMPV.NS', 'TMCV.NS', 'ADANIPORTS.NS',
    'ADANIENT.NS', 'INDUSINDBK.NS', 'HDFCLIFE.NS', 'SBILIFE.NS', 'DRREDDY.NS',
    'GRASIM.NS', 'EICHERMOT.NS', 'M&M.NS', 'COALINDIA.NS', 'TATASTEEL.NS',
    'HINDALCO.NS', 'BPCL.NS', 'BRITANNIA.NS', 'DIVISLAB.NS', 'CIPLA.NS',
    'UPL.NS', 'HEROMOTOCO.NS', 'SHREECEM.NS', 'TATACONSUM.NS',
    'BAJAJ-AUTO.NS', 'APOLLOHOSP.NS'
]

NIFTY_NEXT50 = [
    'COLPAL.NS', 'DABUR.NS', 'HAVELLS.NS', 'MARICO.NS', 'BERGEPAINT.NS',
    'ICICIPRULI.NS', 'AUROPHARMA.NS', 'BANDHANBNK.NS', 'TORNTPHARM.NS',
    'SHRIRAMFIN.NS', 'HAL.NS', 'SIEMENS.NS', 'VBL.NS', 'TRENT.NS',
    'MOTHERSON.NS', 'CHOLAFIN.NS', 'INDIGO.NS', 'PFC.NS', 'RECLTD.NS',
    'AMBUJACEM.NS', 'GODREJCP.NS', 'GAIL.NS', 'TVSMOTOR.NS', 'CANBK.NS',
    'BANKBARODA.NS', 'BHARATFORG.NS', 'LUPIN.NS', 'TATAPOWER.NS', 'INDHOTEL.NS'
]

SECTOR_MAP = {
    'TCS.NS': 'IT', 'INFY.NS': 'IT', 'WIPRO.NS': 'IT',
    'HCLTECH.NS': 'IT', 'TECHM.NS': 'IT',
    'HDFCBANK.NS': 'Banking', 'ICICIBANK.NS': 'Banking',
    'SBIN.NS': 'Banking', 'KOTAKBANK.NS': 'Banking',
    'AXISBANK.NS': 'Banking', 'INDUSINDBK.NS': 'Banking',
    'RELIANCE.NS': 'Oil & Gas', 'ONGC.NS': 'Oil & Gas', 'BPCL.NS': 'Oil & Gas',
    'TMPV.NS': 'Auto', 'TMCV.NS': 'Auto', 'MARUTI.NS': 'Auto',
    'M&M.NS': 'Auto', 'EICHERMOT.NS': 'Auto',
    'BAJAJ-AUTO.NS': 'Auto', 'HEROMOTOCO.NS': 'Auto',
    'SUNPHARMA.NS': 'Pharma', 'DRREDDY.NS': 'Pharma',
    'CIPLA.NS': 'Pharma', 'DIVISLAB.NS': 'Pharma',
    'HINDUNILVR.NS': 'FMCG', 'ITC.NS': 'FMCG',
    'NESTLEIND.NS': 'FMCG', 'BRITANNIA.NS': 'FMCG', 'TATACONSUM.NS': 'FMCG',
    'TATASTEEL.NS': 'Metals', 'JSWSTEEL.NS': 'Metals',
    'HINDALCO.NS': 'Metals', 'COALINDIA.NS': 'Mining',
    'NTPC.NS': 'Power', 'POWERGRID.NS': 'Power',
    'BHARTIARTL.NS': 'Telecom',
    'BAJFINANCE.NS': 'Financial Services', 'BAJAJFINSV.NS': 'Financial Services',
    'HDFCLIFE.NS': 'Insurance', 'SBILIFE.NS': 'Insurance',
    'LT.NS': 'Infrastructure',
    'ULTRACEMCO.NS': 'Cement', 'GRASIM.NS': 'Cement', 'SHREECEM.NS': 'Cement',
    'TITAN.NS': 'Consumer', 'ASIANPAINT.NS': 'Paints',
    'ADANIPORTS.NS': 'Ports', 'ADANIENT.NS': 'Diversified',
    'APOLLOHOSP.NS': 'Healthcare',
}


# ============================================================
# CORE FUNCTIONS
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_nifty_data():
    """Fetch Nifty index data with caching for 1 hour"""
    tickers_to_try = ['^NSEI', 'NIFTYBEES.NS']
    
    for ticker in tickers_to_try:
        try:
            data = yf.download(ticker, period='1y', progress=False, timeout=15)
            if not data.empty and len(data) > 100:
                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)
                data = data.loc[:, ~data.columns.duplicated()]
                return data
        except:
            continue
    return None


def detect_market_regime():
    """Detect market regime from Nifty"""
    nifty = fetch_nifty_data()
    
    if nifty is None:
        return {
            'regime': 'DATA_UNAVAILABLE', 'trade_ok': True,
            'size_multiplier': 0.5, 'nifty_rsi': None,
            'nifty_price': None, 'advice': 'Data unavailable. Half size.'
        }
    
    close_series = nifty['Close']
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]
    
    df = pd.DataFrame({'Close': close_series})
    df['MA_50'] = df['Close'].rolling(50).mean()
    df['MA_200'] = df['Close'].rolling(200).mean()
    
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    latest = df.iloc[-1]
    
    def to_float(v):
        return float(v.item()) if hasattr(v, 'item') else float(v)
    
    price = to_float(latest['Close'])
    ma_50 = to_float(latest['MA_50']) if not pd.isna(latest['MA_50']) else price
    ma_200 = to_float(latest['MA_200']) if not pd.isna(latest['MA_200']) else price
    rsi = to_float(latest['RSI']) if not pd.isna(latest['RSI']) else 50.0
    
    above_50 = price > ma_50
    above_200 = price > ma_200
    golden_cross = ma_50 > ma_200
    
    if above_50 and above_200 and golden_cross and rsi > 50:
        regime, ok, size = "BULLISH", True, 1.0
        advice = "Excellent conditions. Trade with confidence."
    elif above_200 and rsi > 40:
        regime, ok, size = "CAUTIOUS_BULL", True, 0.75
        advice = "Mixed signals. Reduce size by 25%."
    elif rsi < 30:
        regime, ok, size = "OVERSOLD_PANIC", False, 0
        advice = "WAIT. Do not catch falling knives."
    elif not above_50 and not above_200:
        regime, ok, size = "BEARISH", False, 0
        advice = "Downtrend. Avoid long swings."
    elif rsi > 75:
        regime, ok, size = "OVERBOUGHT", False, 0
        advice = "Take profits, don't chase."
    else:
        regime, ok, size = "SIDEWAYS", True, 0.5
        advice = "Choppy market. Half size only."
    
    return {
        'regime': regime, 'trade_ok': ok, 'size_multiplier': size,
        'nifty_price': price, 'nifty_rsi': rsi,
        'nifty_ma_50': ma_50, 'nifty_ma_200': ma_200,
        'advice': advice
    }


def fetch_stock_data(symbols, years=5):
    """Download stock data one by one"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    
    stock_data = {}
    failed = []
    
    progress = st.progress(0, text="Downloading market data...")
    
    for i, symbol in enumerate(symbols):
        try:
            sdf = yf.download(
                symbol,
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                progress=False, auto_adjust=True, timeout=15
            )
            
            if isinstance(sdf.columns, pd.MultiIndex):
                sdf.columns = sdf.columns.get_level_values(0)
            
            if not sdf.empty and len(sdf) > 200:
                stock_data[symbol] = sdf.dropna(how='all')
            else:
                failed.append(symbol)
        except:
            failed.append(symbol)
        
        progress.progress((i + 1) / len(symbols), 
                         text=f"Downloaded {i+1}/{len(symbols)}")
        time.sleep(0.1)
    
    progress.empty()
    return stock_data, failed


def calculate_indicators(df):
    """Add all technical indicators"""
    df = df.copy()
    
    df['MA_20'] = df['Close'].rolling(20).mean()
    df['MA_50'] = df['Close'].rolling(50).mean()
    df['MA_200'] = df['Close'].rolling(200).mean()
    df['Above_20MA'] = (df['Close'] > df['MA_20']).astype(int)
    df['Above_50MA'] = (df['Close'] > df['MA_50']).astype(int)
    df['Above_200MA'] = (df['Close'] > df['MA_200']).astype(int)
    
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    exp1 = df['Close'].ewm(span=12).mean()
    exp2 = df['Close'].ewm(span=26).mean()
    df['MACD'] = exp1 - exp2
    df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    
    hl = df['High'] - df['Low']
    hc = np.abs(df['High'] - df['Close'].shift())
    lc = np.abs(df['Low'] - df['Close'].shift())
    tr = np.maximum(hl, np.maximum(hc, lc))
    df['ATR'] = tr.rolling(14).mean()
    df['ATR_Pct'] = df['ATR'] / df['Close'] * 100
    
    df['TR'] = tr
    plus_dm = df['High'] - df['High'].shift()
    minus_dm = df['Low'].shift() - df['Low']
    df['+DM'] = np.where((plus_dm > minus_dm) & (plus_dm > 0), plus_dm, 0)
    df['-DM'] = np.where((minus_dm > plus_dm) & (minus_dm > 0), minus_dm, 0)
    tr_14 = df['TR'].rolling(14).sum()
    plus_dm_14 = df['+DM'].rolling(14).sum()
    minus_dm_14 = df['-DM'].rolling(14).sum()
    df['+DI'] = (plus_dm_14 / tr_14) * 100
    df['-DI'] = (minus_dm_14 / tr_14) * 100
    dx = np.abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI']) * 100
    df['ADX'] = dx.rolling(14).mean()
    
    df['Volume_MA_20'] = df['Volume'].rolling(20).mean()
    df['Volume_Ratio'] = df['Volume'] / df['Volume_MA_20']
    df['Returns_1D'] = df['Close'].pct_change()
    df['Returns_20D'] = df['Close'].pct_change(20)
    
    return df.dropna()


def find_realistic_target(df, idx, ref_close, atr):
    """Find resistance-based target"""
    lookback = min(50, idx)
    recent = df.iloc[idx - lookback: idx + 1]
    
    swing_20 = recent['High'].iloc[-20:].max() if len(recent) >= 20 else ref_close
    swing_50 = recent['High'].max()
    bb_upper = recent['Close'].mean() + (2 * recent['Close'].std())
    atr_target = ref_close + (2.5 * atr)
    min_target = ref_close + (1.5 * atr)
    
    levels = [l for l in [swing_20, swing_50, bb_upper, atr_target]
              if l > ref_close * 1.005]
    
    if not levels:
        return min_target
    return max(min(levels), min_target)


def score_stock(df, symbol, top_sectors, config):
    """Score a single stock"""
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    idx = len(df) - 1
    
    ref_close = latest['Close']
    atr = latest['ATR']
    
    if ref_close < config['min_price'] or ref_close > config['max_price']:
        return None
    
    # Trend
    trend = 0
    if latest['Above_20MA']: trend += 0.2
    if latest['Above_50MA']: trend += 0.3
    if latest['Above_200MA']: trend += 0.2
    if latest['MA_20'] > latest['MA_50']: trend += 0.15
    if latest['MA_50'] > latest['MA_200']: trend += 0.15
    
    # Momentum
    rsi = latest['RSI']
    mom = 0
    if 50 <= rsi <= 70: mom += 0.4
    elif 45 <= rsi < 50: mom += 0.3
    elif 40 <= rsi < 45: mom += 0.2
    if rsi > prev['RSI']: mom += 0.2
    if latest['MACD'] > latest['MACD_Signal']: mom += 0.3
    if latest['MACD_Histogram'] > 0: mom += 0.1
    
    # Volume
    vol = 0
    vr = latest['Volume_Ratio']
    if vr > 2.0: vol += 0.7
    elif vr > 1.5: vol += 0.5
    elif vr > 1.2: vol += 0.3
    elif vr > 1.0: vol += 0.2
    if latest['Volume'] > prev['Volume']: vol += 0.3
    
    # Regime
    reg = 0
    sector = SECTOR_MAP.get(symbol, 'Others')
    if top_sectors and sector == top_sectors[0]: reg += 0.6
    elif sector in top_sectors: reg += 0.4
    else: reg += 0.2
    if latest['ADX'] > 25: reg += 0.2
    elif latest['ADX'] > 20: reg += 0.1
    
    # Risk quality
    rq = 0
    atr_pct = latest['ATR_Pct']
    if 1.0 <= atr_pct <= 3.0: rq += 0.4
    elif 0.5 <= atr_pct < 1.0: rq += 0.3
    
    # Weighted total
    total = (trend * 0.30 + mom * 0.25 + vol * 0.15 + reg * 0.15 + rq * 0.15)
    
    # Entry range
    entry_low = ref_close * 0.995
    entry_high = ref_close * 1.015
    suggested = (entry_low + entry_high) / 2
    
    # Stop
    stop = ref_close - (2.0 * atr)
    
    # Target
    target = find_realistic_target(df, idx, ref_close, atr)
    
    # R:R filter
    risk = ref_close - stop
    reward = target - ref_close
    if risk <= 0: return None
    rr = reward / risk
    if rr < config['min_rr']: return None
    
    return {
        'Symbol': symbol.replace('.NS', ''),
        'Sector': sector,
        'Total_Score': round(total, 3),
        'Confidence': 'HIGH' if total >= 0.75 else 'MEDIUM' if total >= 0.65 else 'LOW',
        'Trend': round(trend, 2),
        'Momentum': round(mom, 2),
        'Volume': round(vol, 2),
        'Regime': round(reg, 2),
        'Risk_Quality': round(rq, 2),
        'RSI': round(rsi, 1),
        'ADX': round(latest['ADX'], 1),
        'ATR_Pct': round(atr_pct, 2),
        'ATR': round(atr, 2),
        'Volume_Ratio': round(vr, 2),
        'Reference_Close': round(ref_close, 2),
        'Entry_Low': round(entry_low, 2),
        'Entry_High': round(entry_high, 2),
        'Entry': round(suggested, 2),
        'Stop_Loss': round(stop, 2),
        'Stop_Loss_Pct': round((ref_close - stop) / ref_close * 100, 2),
        'Target_1': round(target, 2),
        'Risk_Reward': round(rr, 2),
    }


def calc_position(entry, stop, score, capital, risk_pct, size_mult=1.0):
    """Position sizing"""
    risk_amount = capital * risk_pct * size_mult
    stop_dist = entry - stop
    if stop_dist <= 0 or size_mult == 0:
        return 0, 0, 0, 0
    
    shares = int(risk_amount / stop_dist)
    if score >= 0.80: shares = int(shares * 1.15)
    elif score < 0.70: shares = int(shares * 0.8)
    
    max_value = capital * 0.35
    if shares * entry > max_value:
        shares = int(max_value / entry)
    
    if shares < 1: return 0, 0, 0, 0
    
    return shares, shares * entry, (shares * entry / capital) * 100, shares * stop_dist


def run_full_analysis(symbols, config, market_regime):
    """Run complete analysis pipeline"""
    
    # Step 1: Fetch data
    stock_data, failed = fetch_stock_data(symbols, years=config['years'])
    
    if not stock_data:
        return None, None, None, None, "No data downloaded"
    
    # Step 2: Calculate indicators
    progress = st.progress(0, text="Calculating indicators...")
    featured_data = {}
    for i, (symbol, df) in enumerate(stock_data.items()):
        try:
            fdf = calculate_indicators(df)
            if len(fdf) > 100:
                featured_data[symbol] = fdf
        except:
            continue
        progress.progress((i + 1) / len(stock_data))
    progress.empty()
    
    # Step 3: Sector strength
    sector_returns = {}
    for symbol, df in featured_data.items():
        sector = SECTOR_MAP.get(symbol, 'Others')
        if len(df) >= 20:
            ret = (df['Close'].iloc[-1] / df['Close'].iloc[-20] - 1) * 100
            sector_returns.setdefault(sector, []).append(ret)
    
    sector_strength = {}
    for sector, rets in sector_returns.items():
        sector_strength[sector] = {
            'avg_return': np.mean(rets),
            'num_stocks': len(rets)
        }
    ranked_sectors = sorted(sector_strength.items(), 
                           key=lambda x: x[1]['avg_return'], reverse=True)
    top_sectors = [s[0] for s in ranked_sectors[:3]]
    
    # Step 4: Score all stocks
    if not market_regime['trade_ok']:
        return featured_data, sector_strength, [], failed, "Market regime hostile"
    
    candidates = []
    for symbol, df in featured_data.items():
        try:
            s = score_stock(df, symbol, top_sectors, config)
            if s is None: continue
            if s['Total_Score'] < config['min_score']: continue
            if s['Trend'] < 0.40: continue
            if s['Momentum'] < 0.30: continue
            candidates.append(s)
        except:
            continue
    
    candidates.sort(key=lambda x: x['Total_Score'], reverse=True)
    
    # Step 5: Sector limits
    filtered = []
    counts = {}
    for c in candidates:
        sector = c['Sector']
        limit = 3 if sector in top_sectors else 2
        if counts.get(sector, 0) < limit:
            filtered.append(c)
            counts[sector] = counts.get(sector, 0) + 1
    candidates = filtered
    
    # Step 6: Position sizing
    for c in candidates:
        sh, val, pct, risk = calc_position(
            c['Entry'], c['Stop_Loss'], c['Total_Score'],
            config['capital'], config['risk_pct'], market_regime['size_multiplier']
        )
        c['Shares'] = sh
        c['Position_Value'] = val
        c['Position_Pct'] = round(pct, 1)
        c['Risk_Amount'] = round(risk, 0)
    
    candidates = [c for c in candidates if c['Shares'] >= 1]
    
    return featured_data, sector_strength, candidates, failed, None


# ============================================================
# MAIN UI
# ============================================================

# Header
st.markdown("""
<div class="main-header">
    <h1>📈 Swing Trading Dashboard</h1>
    <p>Indian Stock Market | Hybrid Factor Model</p>
</div>
""", unsafe_allow_html=True)

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    capital = st.number_input("Capital (₹)", min_value=5000, value=20000, step=5000)
    risk_pct = st.slider("Risk per Trade (%)", 0.5, 5.0, 2.0, 0.5) / 100
    
    st.markdown("---")
    st.subheader("📊 Stock Universe")
    use_nifty50 = st.checkbox("Nifty 50", value=True)
    use_next50 = st.checkbox("Nifty Next 50", value=False)
    
    st.markdown("---")
    st.subheader("🎯 Filters")
    min_score = st.slider("Min Score", 0.5, 0.9, 0.60, 0.05)
    min_rr = st.slider("Min R:R Ratio", 1.0, 3.0, 1.5, 0.1)
    min_price = st.number_input("Min Price (₹)", value=100)
    max_price = st.number_input("Max Price (₹)", value=4000)
    
    st.markdown("---")
    run_btn = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

# Main area
if run_btn:
    # Build config
    config = {
        'capital': capital,
        'risk_pct': risk_pct,
        'min_score': min_score,
        'min_rr': min_rr,
        'min_price': min_price,
        'max_price': max_price,
        'years': 5,
    }
    
    # Build stock list
    symbols = []
    if use_nifty50: symbols.extend(NIFTY50)
    if use_next50: symbols.extend(NIFTY50 + NIFTY50)  # placeholder
    symbols = list(dict.fromkeys(symbols))
    
    st.info(f"Analyzing {len(symbols)} stocks...")
    
    # Step 1: Regime check
    with st.spinner("🌍 Checking market regime..."):
        regime = detect_market_regime()
    
    # Display regime card
    regime_class = 'regime-bearish'
    if regime['regime'] in ['BULLISH']:
        regime_class = 'regime-bullish'
    elif regime['regime'] in ['CAUTIOUS_BULL', 'SIDEWAYS']:
        regime_class = 'regime-cautious'
    
    st.markdown(f"""
    <div class="regime-card {regime_class}">
        <div class="regime-title">Market Regime: {regime['regime']}</div>
        <p>{regime['advice']}</p>
        <p><strong>Nifty Price:</strong> ₹{regime['nifty_price']:,.2f} | 
           <strong>Nifty RSI:</strong> {regime['nifty_rsi']:.1f} |
           <strong>Position Size:</strong> {regime['size_multiplier']:.0%}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not regime['trade_ok']:
        st.error("🛑 **DO NOT TRADE TODAY** — Market regime is hostile.")
        st.info("💡 This is normal. Wait for market to stabilize. Run again tomorrow.")
        st.stop()
    
    # Step 2: Run analysis
    with st.spinner("🔍 Running full analysis..."):
        featured_data, sector_strength, candidates, failed, error = run_full_analysis(
            symbols, config, regime
        )
    
    if error:
        st.error(f"❌ {error}")
        st.stop()
    
    # Step 3: Show sector strength
    st.subheader("🏭 Sector Performance (20 Days)")
    sector_df = pd.DataFrame([
        {'Sector': s, 'Avg Return': f"{v['avg_return']:+.1f}%", 
         'Stocks': v['num_stocks']}
        for s, v in list(sector_strength.items())[:8]
    ])
    st.dataframe(sector_df, use_container_width=True, hide_index=True)
    
    # Step 4: Show candidates
    st.subheader(f"🎯 Trade Candidates ({len(candidates)} found)")
    
    if not candidates:
        st.warning("No suitable trades today. Market conditions don't meet quality standards.")
        st.info("💡 This is normal. The system protects your capital.")
    else:
        for i, c in enumerate(candidates[:10], 1):
            score_class = 'score-high' if c['Total_Score'] >= 0.75 else 'score-medium' if c['Total_Score'] >= 0.65 else 'score-low'
            
            def badge(s):
                return 'badge-good' if s >= 0.6 else 'badge-ok' if s >= 0.4 else 'badge-weak'
            
            st.markdown(f"""
            <div class="stock-card">
                <span class="stock-score {score_class}">{c['Total_Score']:.0%}</span>
                <span class="stock-symbol">#{i} {c['Symbol']}</span>
                <span class="stock-sector">({c['Sector']}) · {c['Confidence']}</span>
                <div style="margin-top: 15px;">
                    <span class="factor-badge {badge(c['Trend'])}">Trend: {c['Trend']:.0%}</span>
                    <span class="factor-badge {badge(c['Momentum'])}">Mom: {c['Momentum']:.0%}</span>
                    <span class="factor-badge {badge(c['Volume'])}">Vol: {c['Volume']:.0%}</span>
                    <span class="factor-badge {badge(c['Risk_Quality'])}">Risk: {c['Risk_Quality']:.0%}</span>
                </div>
                <div style="margin-top: 15px; padding: 12px; background: #f8f9fa; border-radius: 8px;">
                    <strong>📋 Trade Plan:</strong><br>
                    Entry Range: <strong>₹{c['Entry_Low']:.0f} – ₹{c['Entry_High']:.0f}</strong><br>
                    Stop: <strong>₹{c['Stop_Loss']:.2f}</strong> ({c['Stop_Loss_Pct']:+.1f}%) · 
                    Target: <strong>₹{c['Target_1']:.2f}</strong> · 
                    R:R <strong>1:{c['Risk_Reward']}</strong><br>
                    Shares: <strong>{c['Shares']}</strong> · 
                    Invest: <strong>₹{c['Position_Value']:,.0f}</strong> · 
                    Risk: <strong>₹{c['Risk_Amount']:,.0f}</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Export button
        st.markdown("---")
        candidates_df = pd.DataFrame(candidates)
        csv = candidates_df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            csv,
            file_name=f"swing_trades_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

else:
    # Welcome screen
    st.markdown("""
    ### 👋 Welcome to your Swing Trading Dashboard
    
    **How to use:**
    1. Configure settings in the sidebar ⚙️
    2. Click **🚀 Run Analysis**
    3. Review market regime and trade candidates
    
    **What this does:**
    - Checks Nifty market regime first (protects your capital)
    - Scores every stock on 5 factors (trend, momentum, volume, regime, risk)
    - Filters out poor risk/reward setups
    - Calculates exact position sizes for your capital
    
    **First-time note:** The first run takes 3-5 minutes to download data.
    Subsequent runs use caching for speed.
    """)
    
    st.info("💡 **Tip:** Click **Run Analysis** to begin. If market regime is hostile, no trades will be recommended.")
