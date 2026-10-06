# ============================================================
# INDIAN STOCK SWING TRADING DASHBOARD
# Streamlit Application - Full Featured Version
# ============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIG
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
    .main-header h1 { margin: 0; font-size: 32px; color: white; }
    .main-header p { margin: 8px 0 0 0; opacity: 0.95; color: white; }

    .regime-card {
        padding: 24px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 6px solid #95a5a6;
        background: #ffffff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    .regime-card * { color: #2c3e50 !important; }
    .regime-title { font-size: 22px; font-weight: bold; margin-bottom: 12px; }
    .regime-bullish { border-left-color: #00b894; }
    .regime-bullish .regime-title { color: #00b894 !important; }
    .regime-cautious { border-left-color: #f39c12; }
    .regime-cautious .regime-title { color: #f39c12 !important; }
    .regime-bearish { border-left-color: #d63031; }
    .regime-bearish .regime-title { color: #d63031 !important; }

    .regime-detail {
        display: inline-block;
        padding: 8px 14px;
        margin: 4px 8px 4px 0;
        border-radius: 8px;
        background: #f8f9fa;
        font-size: 14px;
        color: #2c3e50 !important;
    }

    .stock-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    .stock-card * { color: #2c3e50 !important; }
    .stock-symbol { font-size: 22px; font-weight: bold; }
    .stock-sector { color: #7f8c8d !important; font-size: 13px; }
    .stock-score { font-size: 28px; font-weight: bold; float: right; }
    .score-high { color: #00b894 !important; }
    .score-medium { color: #f39c12 !important; }
    .score-low { color: #d63031 !important; }

    .trade-plan-box {
        margin-top: 15px;
        padding: 14px;
        background: #f8f9fa;
        border-radius: 8px;
        line-height: 1.8;
    }

    .factor-badge {
        display: inline-block;
        padding: 6px 14px;
        margin: 3px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-good { background: #d4edda; color: #155724 !important; }
    .badge-ok { background: #fff3cd; color: #856404 !important; }
    .badge-weak { background: #f8d7da; color: #721c24 !important; }

    .warning-box {
        padding: 16px;
        border-radius: 10px;
        background: #fff3cd;
        border-left: 4px solid #f39c12;
        margin: 12px 0;
        line-height: 1.7;
    }

    .status-bar {
        padding: 10px 16px;
        background: #e8f4f8;
        border-radius: 8px;
        margin-bottom: 15px;
        font-size: 13px;
        color: #2c3e50 !important;
    }

    .metric-card {
        padding: 16px;
        background: #f8f9fa;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid #667eea;
    }
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
    'TCS.NS': 'IT', 'INFY.NS': 'IT', 'WIPRO.NS': 'IT', 'HCLTECH.NS': 'IT', 'TECHM.NS': 'IT',
    'HDFCBANK.NS': 'Banking', 'ICICIBANK.NS': 'Banking', 'SBIN.NS': 'Banking',
    'KOTAKBANK.NS': 'Banking', 'AXISBANK.NS': 'Banking', 'INDUSINDBK.NS': 'Banking',
    'RELIANCE.NS': 'Oil & Gas', 'ONGC.NS': 'Oil & Gas', 'BPCL.NS': 'Oil & Gas',
    'TMPV.NS': 'Auto', 'TMCV.NS': 'Auto', 'MARUTI.NS': 'Auto', 'M&M.NS': 'Auto',
    'EICHERMOT.NS': 'Auto', 'BAJAJ-AUTO.NS': 'Auto', 'HEROMOTOCO.NS': 'Auto',
    'SUNPHARMA.NS': 'Pharma', 'DRREDDY.NS': 'Pharma', 'CIPLA.NS': 'Pharma', 'DIVISLAB.NS': 'Pharma',
    'HINDUNILVR.NS': 'FMCG', 'ITC.NS': 'FMCG', 'NESTLEIND.NS': 'FMCG',
    'BRITANNIA.NS': 'FMCG', 'TATACONSUM.NS': 'FMCG',
    'TATASTEEL.NS': 'Metals', 'JSWSTEEL.NS': 'Metals', 'HINDALCO.NS': 'Metals',
    'COALINDIA.NS': 'Mining', 'NTPC.NS': 'Power', 'POWERGRID.NS': 'Power',
    'BHARTIARTL.NS': 'Telecom',
    'BAJFINANCE.NS': 'Financial Services', 'BAJAJFINSV.NS': 'Financial Services',
    'HDFCLIFE.NS': 'Insurance', 'SBILIFE.NS': 'Insurance',
    'LT.NS': 'Infrastructure', 'ULTRACEMCO.NS': 'Cement',
    'GRASIM.NS': 'Cement', 'SHREECEM.NS': 'Cement',
    'TITAN.NS': 'Consumer', 'ASIANPAINT.NS': 'Paints',
    'ADANIPORTS.NS': 'Ports', 'ADANIENT.NS': 'Diversified',
    'APOLLOHOSP.NS': 'Healthcare',
    'COLPAL.NS': 'FMCG', 'DABUR.NS': 'FMCG', 'MARICO.NS': 'FMCG',
    'HAVELLS.NS': 'Consumer', 'BERGEPAINT.NS': 'Paints',
    'ICICIPRULI.NS': 'Insurance', 'AUROPHARMA.NS': 'Pharma',
    'BANDHANBNK.NS': 'Banking', 'TORNTPHARM.NS': 'Pharma',
    'SHRIRAMFIN.NS': 'Financial Services', 'HAL.NS': 'Defense',
    'SIEMENS.NS': 'Infrastructure', 'VBL.NS': 'FMCG', 'TRENT.NS': 'Retail',
    'MOTHERSON.NS': 'Auto', 'CHOLAFIN.NS': 'Financial Services',
    'INDIGO.NS': 'Aviation', 'PFC.NS': 'Financial Services',
    'RECLTD.NS': 'Financial Services', 'AMBUJACEM.NS': 'Cement',
    'GODREJCP.NS': 'FMCG', 'GAIL.NS': 'Oil & Gas',
    'TVSMOTOR.NS': 'Auto', 'CANBK.NS': 'Banking',
    'BANKBARODA.NS': 'Banking', 'BHARATFORG.NS': 'Auto',
    'LUPIN.NS': 'Pharma', 'TATAPOWER.NS': 'Power', 'INDHOTEL.NS': 'Hospitality',
}

# Trades file path
TRADES_FILE = "data/trades.csv"


# ============================================================
# CORE FUNCTIONS
# ============================================================

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_nifty_data():
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


def compute_nifty_rsi(nifty):
    close_series = nifty['Close']
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]
    df = pd.DataFrame({'Close': close_series})
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def detect_market_regime():
    nifty = fetch_nifty_data()
    if nifty is None:
        return {'regime': 'DATA UNAVAILABLE', 'trade_ok': True, 'size_multiplier': 0.5,
                'nifty_rsi': None, 'nifty_price': None,
                'advice': 'Could not fetch Nifty data. Trading at half size as precaution.'}

    df = compute_nifty_rsi(nifty)
    df['MA_50'] = df['Close'].rolling(50).mean()
    df['MA_200'] = df['Close'].rolling(200).mean()
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
        regime, ok, size = "CAUTIOUS BULL", True, 0.75
        advice = "Mixed signals. Position size reduced by 25%."
    elif rsi < 30:
        regime, ok, size = "HIGH RISK — WAIT", False, 0
        advice = "Market is deeply oversold. Wait for stabilization before trading."
    elif not above_50 and not above_200:
        regime, ok, size = "BEARISH", False, 0
        advice = "Downtrend confirmed. Avoid long swing trades."
    elif rsi > 75:
        regime, ok, size = "OVERBOUGHT", False, 0
        advice = "Market overextended. Take profits, do not chase."
    else:
        regime, ok, size = "SIDEWAYS", True, 0.5
        advice = "Choppy market. Only highest-quality setups. Half size."

    return {'regime': regime, 'trade_ok': ok, 'size_multiplier': size,
            'nifty_price': price, 'nifty_rsi': rsi,
            'nifty_ma_50': ma_50, 'nifty_ma_200': ma_200, 'advice': advice}


def fetch_stock_data(symbols, years=5):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)
    stock_data = {}
    failed = []
    for symbol in symbols:
        try:
            sdf = yf.download(symbol,
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d'),
                progress=False, auto_adjust=True, timeout=15)
            if isinstance(sdf.columns, pd.MultiIndex):
                sdf.columns = sdf.columns.get_level_values(0)
            if not sdf.empty and len(sdf) > 200:
                stock_data[symbol] = sdf.dropna(how='all')
            else:
                failed.append(symbol)
        except:
            failed.append(symbol)
        time.sleep(0.05)
    return stock_data, failed


def calculate_indicators(df):
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
    lookback = min(50, idx)
    recent = df.iloc[idx - lookback: idx + 1]
    swing_20 = recent['High'].iloc[-20:].max() if len(recent) >= 20 else ref_close
    swing_50 = recent['High'].max()
    bb_upper = recent['Close'].mean() + (2 * recent['Close'].std())
    atr_target = ref_close + (2.5 * atr)
    min_target = ref_close + (1.5 * atr)
    levels = [l for l in [swing_20, swing_50, bb_upper, atr_target] if l > ref_close * 1.005]
    if not levels:
        return min_target
    return max(min(levels), min_target)


def score_stock(df, symbol, top_sectors, config):
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    idx = len(df) - 1
    ref_close = latest['Close']
    atr = latest['ATR']

    if ref_close < config['min_price'] or ref_close > config['max_price']:
        return None

    trend = 0
    if latest['Above_20MA']: trend += 0.2
    if latest['Above_50MA']: trend += 0.3
    if latest['Above_200MA']: trend += 0.2
    if latest['MA_20'] > latest['MA_50']: trend += 0.15
    if latest['MA_50'] > latest['MA_200']: trend += 0.15

    rsi = latest['RSI']
    mom = 0
    if 50 <= rsi <= 70: mom += 0.4
    elif 45 <= rsi < 50: mom += 0.3
    elif 40 <= rsi < 45: mom += 0.2
    if rsi > prev['RSI']: mom += 0.2
    if latest['MACD'] > latest['MACD_Signal']: mom += 0.3
    if latest['MACD_Histogram'] > 0: mom += 0.1

    vol = 0
    vr = latest['Volume_Ratio']
    if vr > 2.0: vol += 0.7
    elif vr > 1.5: vol += 0.5
    elif vr > 1.2: vol += 0.3
    elif vr > 1.0: vol += 0.2
    if latest['Volume'] > prev['Volume']: vol += 0.3

    reg = 0
    sector = SECTOR_MAP.get(symbol, 'Others')
    if top_sectors and sector == top_sectors[0]: reg += 0.6
    elif sector in top_sectors: reg += 0.4
    else: reg += 0.2
    if latest['ADX'] > 25: reg += 0.2
    elif latest['ADX'] > 20: reg += 0.1

    rq = 0
    atr_pct = latest['ATR_Pct']
    if 1.0 <= atr_pct <= 3.0: rq += 0.4
    elif 0.5 <= atr_pct < 1.0: rq += 0.3

    total = (trend * 0.30 + mom * 0.25 + vol * 0.15 + reg * 0.15 + rq * 0.15)

    entry_low = ref_close * 0.995
    entry_high = ref_close * 1.015
    suggested = (entry_low + entry_high) / 2
    stop = ref_close - (2.0 * atr)
    target = find_realistic_target(df, idx, ref_close, atr)

    risk = ref_close - stop
    reward = target - ref_close
    if risk <= 0:
        return None
    rr = reward / risk
    if rr < config['min_rr']:
        return None

    return {
        'Symbol': symbol.replace('.NS', ''),
        'Sector': sector,
        'Total_Score': round(total, 3),
        'Confidence': 'HIGH' if total >= 0.75 else 'MEDIUM' if total >= 0.65 else 'LOW',
        'Trend': round(trend, 2), 'Momentum': round(mom, 2),
        'Volume': round(vol, 2), 'Regime': round(reg, 2),
        'Risk_Quality': round(rq, 2),
        'RSI': round(rsi, 1), 'ADX': round(latest['ADX'], 1),
        'ATR_Pct': round(atr_pct, 2), 'ATR': round(atr, 2),
        'Volume_Ratio': round(vr, 2),
        'Reference_Close': round(ref_close, 2),
        'Entry_Low': round(entry_low, 2), 'Entry_High': round(entry_high, 2),
        'Entry': round(suggested, 2),
        'Stop_Loss': round(stop, 2),
        'Stop_Loss_Pct': round((ref_close - stop) / ref_close * 100, 2),
        'Target_1': round(target, 2),
        'Risk_Reward': round(rr, 2),
    }


def calc_position(entry, stop, score, capital, risk_pct, size_mult=1.0):
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
    if shares < 1:
        return 0, 0, 0, 0
    return shares, shares * entry, (shares * entry / capital) * 100, shares * stop_dist


@st.cache_data(ttl=86400, show_spinner=False)
def run_full_analysis(symbols_tuple, config_tuple, regime_dict, date_key):
    symbols = list(symbols_tuple)
    config = dict(config_tuple)
    stock_data, failed = fetch_stock_data(symbols, years=config['years'])
    if not stock_data:
        return None, None, [], failed, "No data downloaded"

    featured_data = {}
    for symbol, df in stock_data.items():
        try:
            fdf = calculate_indicators(df)
            if len(fdf) > 100:
                featured_data[symbol] = fdf
        except:
            continue

    sector_returns = {}
    for symbol, df in featured_data.items():
        sector = SECTOR_MAP.get(symbol, 'Others')
        if len(df) >= 20:
            ret = (df['Close'].iloc[-1] / df['Close'].iloc[-20] - 1) * 100
            sector_returns.setdefault(sector, []).append(ret)

    sector_strength = {}
    for sector, rets in sector_returns.items():
        sector_strength[sector] = {'avg_return': np.mean(rets), 'num_stocks': len(rets)}
    ranked_sectors = sorted(sector_strength.items(), key=lambda x: x[1]['avg_return'], reverse=True)
    top_sectors = [s[0] for s in ranked_sectors[:3]]

    if not regime_dict['trade_ok']:
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

    filtered = []
    counts = {}
    for c in candidates:
        sector = c['Sector']
        limit = 3 if sector in top_sectors else 2
        if counts.get(sector, 0) < limit:
            filtered.append(c)
            counts[sector] = counts.get(sector, 0) + 1
    candidates = filtered

    for c in candidates:
        sh, val, pct, risk = calc_position(c['Entry'], c['Stop_Loss'], c['Total_Score'],
                                            config['capital'], config['risk_pct'],
                                            regime_dict['size_multiplier'])
        c['Shares'] = sh
        c['Position_Value'] = val
        c['Position_Pct'] = round(pct, 1)
        c['Risk_Amount'] = round(risk, 0)

    candidates = [c for c in candidates if c['Shares'] >= 1]

    return featured_data, sector_strength, candidates, failed, None


# ============================================================
# TRADE TRACKER HELPERS
# ============================================================

def load_trades():
    """Load trade tracker CSV"""
    if os.path.exists(TRADES_FILE):
        try:
            return pd.read_csv(TRADES_FILE)
        except:
            pass
    return pd.DataFrame(columns=[
        'date_recommended', 'symbol', 'sector', 'entry_planned', 'entry_actual',
        'shares', 'stop_loss', 'target', 'score', 'confidence',
        'status', 'exit_price', 'exit_date', 'pnl_rs', 'pnl_pct', 'notes'
    ])


def save_trades(df):
    """Save trade tracker to CSV"""
    os.makedirs(os.path.dirname(TRADES_FILE), exist_ok=True)
    df.to_csv(TRADES_FILE, index=False)


# ============================================================
# MAIN UI
# ============================================================

st.markdown("""
<div class="main-header">
    <h1>📈 Swing Trading Dashboard</h1>
    <p>Indian Stock Market | Hybrid Factor Model</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
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
    show_shadow = st.checkbox("Show shadow picks when blocked", value=True,
                              help="Show what would have qualified if regime allowed")

    force_refresh = st.button("🔄 Force Refresh", use_container_width=True)
    if force_refresh:
        st.cache_data.clear()
        st.session_state['last_run_time'] = datetime.now()
        st.success("Cache cleared. Reloading...")
        st.rerun()

# Build config
config = {
    'capital': capital, 'risk_pct': risk_pct,
    'min_score': min_score, 'min_rr': min_rr,
    'min_price': min_price, 'max_price': max_price,
    'years': 5,
}

symbols = []
if use_nifty50: symbols.extend(NIFTY50)
if use_next50: symbols.extend(NIFTY_NEXT50)
symbols = list(dict.fromkeys(symbols))

today_key = datetime.now().strftime('%Y-%m-%d')

# ============================================================
# STATUS BAR WITH FRESHNESS INDICATOR
# ============================================================
if 'last_run_time' not in st.session_state:
    st.session_state['last_run_time'] = datetime.now()

now = datetime.now()
last_run = st.session_state['last_run_time']
age_min = (now - last_run).total_seconds() / 60

if age_min < 2:
    freshness = "🟢 Fresh"
elif age_min < 60:
    freshness = "🟢 Fresh"
elif age_min < 360:
    freshness = "🟡 Recent"
else:
    freshness = "🔴 Stale"

st.markdown(f"""
<div class="status-bar">
    🕐 <strong>Last checked:</strong> {now.strftime('%d %b %Y, %I:%M %p')} |
    📅 <strong>Analysis date:</strong> {today_key} |
    📊 <strong>Universe:</strong> {len(symbols)} stocks |
    ♻️ <strong>Data:</strong> {freshness} (cached {age_min:.0f} min ago)
</div>
""", unsafe_allow_html=True)

# ============================================================
# MARKET REGIME
# ============================================================
with st.spinner("🌍 Checking market regime..."):
    regime = detect_market_regime()

regime_class = 'regime-bearish'
if regime['regime'] == 'BULLISH':
    regime_class = 'regime-bullish'
elif regime['regime'] in ['CAUTIOUS BULL', 'SIDEWAYS']:
    regime_class = 'regime-cautious'

price_str = f"₹{regime['nifty_price']:,.2f}" if regime['nifty_price'] else "N/A"
rsi_str = f"{regime['nifty_rsi']:.1f}" if regime['nifty_rsi'] else "N/A"

st.markdown(f"""
<div class="regime-card {regime_class}">
    <div class="regime-title">Market Regime: {regime['regime']}</div>
    <p style="margin: 8px 0; font-size: 15px;">{regime['advice']}</p>
    <div style="margin-top: 14px;">
        <span class="regime-detail"><strong>Nifty:</strong> {price_str}</span>
        <span class="regime-detail"><strong>RSI:</strong> {rsi_str}</span>
        <span class="regime-detail"><strong>Position Size:</strong> {regime['size_multiplier']:.0%}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# REGIME BLOCKED PATH
# ============================================================
if not regime['trade_ok']:
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Nifty Price", price_str)
    with col2: st.metric("Nifty RSI", rsi_str)
    with col3: st.metric("Position Size", f"{regime['size_multiplier']:.0%}")
    with col4: st.metric("Trade Status", "❌ Blocked")

    st.markdown(f"""
    <div class="warning-box">
        <strong>⏸️ No trades recommended today</strong><br><br>
        The market is currently in a <strong>{regime['regime']}</strong> regime:
        <ul style="margin: 10px 0 10px 20px; line-height: 1.8;">
            <li>Nifty is trading below its key moving averages</li>
            <li>Nifty RSI is at {rsi_str} (extreme oversold)</li>
            <li>Historical data shows long trades in this regime have a low win rate</li>
        </ul>
        <strong>What to do:</strong> Sit in cash. The system will resume when conditions improve.<br><br>
        <strong>This is not a bug — it is your capital protection working as designed.</strong>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📉 Nifty RSI — Last 30 Days")
    nifty = fetch_nifty_data()
    if nifty is not None:
        df_rsi = compute_nifty_rsi(nifty)
        st.line_chart(df_rsi[['RSI']].tail(30).rename(columns={'RSI': 'Nifty RSI'}), height=250)

    # ============================================================
    # SHADOW PICKS (What would have been picked)
    # ============================================================
    if show_shadow:
        st.markdown("---")
        st.subheader("🔍 Shadow Picks — Learning Only")
        st.warning("⚠️ These stocks passed the quality filter but the regime blocks trading. **Do NOT trade these.** This is for learning what the system would pick when the market improves.")

        with st.spinner("Running shadow analysis (30-60 seconds)..."):
            config_tuple = tuple(sorted(config.items()))
            regime_sim = {'trade_ok': True, 'size_multiplier': 0.5}

            _, _, shadow_candidates, _, _ = run_full_analysis(
                tuple(symbols),
                config_tuple,
                regime_sim,
                today_key + "_shadow"
            )

        if shadow_candidates:
            st.success(f"Shadow analysis: {len(shadow_candidates)} stocks would qualify in a normal regime")

            for i, c in enumerate(shadow_candidates[:5], 1):
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
                    <div class="trade-plan-box">
                        <strong>Hypothetical Plan</strong><br>
                        Entry: <strong>₹{c['Entry']:.0f}</strong> ·
                        Stop: <strong>₹{c['Stop_Loss']:.0f}</strong> ·
                        Target: <strong>₹{c['Target_1']:.0f}</strong><br>
                        R:R <strong>1:{c['Risk_Reward']}</strong> · RSI: {c['RSI']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Even without the regime block, no stocks passed the quality filter today.")

    st.stop()


# ============================================================
# NORMAL PATH — RUN ANALYSIS
# ============================================================
st.subheader("🔍 Analyzing Market...")

config_tuple = tuple(sorted(config.items()))
regime_simple = {'trade_ok': regime['trade_ok'], 'size_multiplier': regime['size_multiplier']}

with st.spinner(f"Analyzing {len(symbols)} stocks (first run of the day takes 2-4 minutes)..."):
    featured_data, sector_strength, candidates, failed, error = run_full_analysis(
        tuple(symbols), config_tuple, regime_simple, today_key
    )

st.session_state['last_run_time'] = datetime.now()

if error:
    st.error(f"❌ {error}")
    st.stop()

# ============================================================
# SECTOR PERFORMANCE
# ============================================================
st.subheader("🏭 Sector Performance (20 Days)")
sector_rows = []
for s, v in list(sector_strength.items())[:8]:
    sector_rows.append({
        'Sector': s,
        'Avg Return': f"{v['avg_return']:+.1f}%",
        'Stocks': v['num_stocks']
    })
if sector_rows:
    st.dataframe(pd.DataFrame(sector_rows), use_container_width=True, hide_index=True)

# ============================================================
# CANDIDATES
# ============================================================
st.subheader(f"🎯 Trade Candidates ({len(candidates)} found)")

candidates_df = pd.DataFrame(candidates) if candidates else pd.DataFrame()

if not candidates:
    st.warning("No suitable trades today. Market conditions don't meet quality standards.")
    st.info("💡 This is normal. The system protects your capital by waiting for quality setups.")
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
            <div class="trade-plan-box">
                <strong>📋 Trade Plan</strong><br>
                Entry Range: <strong>₹{c['Entry_Low']:.0f} – ₹{c['Entry_High']:.0f}</strong><br>
                Stop Loss: <strong>₹{c['Stop_Loss']:.2f}</strong> ({c['Stop_Loss_Pct']:+.1f}%) ·
                Target: <strong>₹{c['Target_1']:.2f}</strong> ·
                R:R <strong>1:{c['Risk_Reward']}</strong><br>
                Shares: <strong>{c['Shares']}</strong> ·
                Invest: <strong>₹{c['Position_Value']:,.0f}</strong> ·
                Risk: <strong>₹{c['Risk_Amount']:,.0f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# DOWNLOAD + TRADE TRACKER
# ============================================================
st.markdown("---")

col_a, col_b = st.columns([1, 1])
with col_a:
    if not candidates_df.empty:
        csv = candidates_df.to_csv(index=False)
        st.download_button(
            "📥 Download Today's Picks (CSV)",
            csv,
            file_name=f"picks_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
with col_b:
    if not candidates_df.empty and st.button("➕ Add Today's Picks to Tracker", use_container_width=True):
        trades = load_trades()
        new_rows = []
        for c in candidates:
            new_rows.append({
                'date_recommended': today_key,
                'symbol': c['Symbol'],
                'sector': c['Sector'],
                'entry_planned': c['Entry'],
                'entry_actual': '',
                'shares': c['Shares'],
                'stop_loss': c['Stop_Loss'],
                'target': c['Target_1'],
                'score': c['Total_Score'],
                'confidence': c['Confidence'],
                'status': 'OPEN',
                'exit_price': '',
                'exit_date': '',
                'pnl_rs': '',
                'pnl_pct': '',
                'notes': ''
            })
        trades = pd.concat([trades, pd.DataFrame(new_rows)], ignore_index=True)
        save_trades(trades)
        st.success(f"✅ Added {len(new_rows)} trades to tracker")
        st.rerun()

# ============================================================
# TRADE TRACKER PANEL
# ============================================================
st.subheader("📓 Paper Trade Tracker")

trades = load_trades()

if len(trades) == 0:
    st.info("No trades tracked yet. Click **➕ Add Today's Picks to Tracker** above to start tracking.")
else:
    open_trades = trades[trades['status'] == 'OPEN'] if 'status' in trades.columns else pd.DataFrame()
    closed_trades = trades[trades['status'] == 'CLOSED'] if 'status' in trades.columns else pd.DataFrame()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Open Trades", len(open_trades))
    with col2:
        st.metric("Closed Trades", len(closed_trades))

    if len(closed_trades) > 0:
        closed_trades['pnl_rs'] = pd.to_numeric(closed_trades['pnl_rs'], errors='coerce')
        valid_closed = closed_trades[closed_trades['pnl_rs'].notna()]

        if len(valid_closed) > 0:
            win_rate = (valid_closed['pnl_rs'] > 0).mean() * 100
            total_pnl = valid_closed['pnl_rs'].sum()
            with col3:
                st.metric("Win Rate", f"{win_rate:.0f}%")
            with col4:
                st.metric("Total P&L", f"₹{total_pnl:,.0f}",
                          delta=f"{'+' if total_pnl >= 0 else ''}{total_pnl:,.0f}")

    # Show open trades
    if len(open_trades) > 0:
        st.markdown("**📌 Open Positions**")
        display_cols = ['date_recommended', 'symbol', 'sector', 'entry_planned',
                        'shares', 'stop_loss', 'target', 'score', 'status']
        available = [c for c in display_cols if c in open_trades.columns]
        st.dataframe(open_trades[available], use_container_width=True, hide_index=True)

    # Show closed trades
    if len(closed_trades) > 0:
        with st.expander(f"📊 Closed Trades ({len(closed_trades)})"):
            display_cols = ['date_recommended', 'symbol', 'entry_actual', 'exit_price',
                            'exit_date', 'pnl_rs', 'pnl_pct', 'notes']
            available = [c for c in display_cols if c in closed_trades.columns]
            st.dataframe(closed_trades[available], use_container_width=True, hide_index=True)

    # ============================================================
    # PERFORMANCE CHART
    # ============================================================
    if len(closed_trades) >= 3:
        st.markdown("---")
        st.subheader("📈 Performance Over Time")

        perf = closed_trades.copy()
        perf['pnl_rs'] = pd.to_numeric(perf['pnl_rs'], errors='coerce')
        perf = perf[perf['pnl_rs'].notna()].copy()
        perf['exit_date'] = pd.to_datetime(perf['exit_date'], errors='coerce')
        perf = perf.sort_values('exit_date')
        perf['cumulative_pnl'] = perf['pnl_rs'].cumsum()

        chart_data = perf[['exit_date', 'cumulative_pnl']].set_index('exit_date')
        st.line_chart(chart_data, height=280)

        col1, col2, col3, col4 = st.columns(4)
        wins = perf[perf['pnl_rs'] > 0]
        losses = perf[perf['pnl_rs'] < 0]

        with col1:
            st.metric("Avg Win", f"₹{wins['pnl_rs'].mean():,.0f}" if len(wins) else "—")
        with col2:
            st.metric("Avg Loss", f"₹{losses['pnl_rs'].mean():,.0f}" if len(losses) else "—")
        with col3:
            st.metric("Best Trade", f"₹{perf['pnl_rs'].max():,.0f}")
        with col4:
            st.metric("Worst Trade", f"₹{perf['pnl_rs'].min():,.0f}")

    # ============================================================
    # MANUAL UPDATE SECTION
    # ============================================================
    st.markdown("---")
    st.markdown("**✏️ Update Trades Manually**")
    st.caption("Edit the CSV directly in Google Sheets or Excel, then upload it back.")

    uploaded = st.file_uploader("Upload updated trades.csv", type="csv")
    if uploaded is not None:
        try:
            updated_trades = pd.read_csv(uploaded)
            save_trades(updated_trades)
            st.success("✅ Tracker updated")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to update: {e}")

    # Download current tracker
    st.download_button(
        "📥 Download Current Tracker (CSV)",
        trades.to_csv(index=False),
        file_name="trades.csv",
        mime="text/csv",
        use_container_width=True
    )

# Footer
st.markdown("---")
st.caption(f"✅ Analysis complete | Cache key: {today_key} | Refresh daily at midnight IST")
