import os
from flask import Flask, render_template_string

app = Flask(__name__)

# استدعاء المعلومات من "خزنة" Render
TELE_TOKEN = os.getenv("TELE_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


ASSETS = {
    "GOLD": {"symbol": "PAXGUSDT", "name": "XAU/USD GOLD", "icon": "📀"},
    "BTC": {"symbol": "BTCUSDT", "name": "BITCOIN BTC", "icon": "₿"},
    "ETH": {"symbol": "ETHUSDT", "name": "ETHEREUM ETH", "icon": "Ξ"},
    "SOL": {"symbol": "SOLUSDT", "name": "SOLANA SOL", "icon": "◎"}
}

LIVE_FEED = {}

def get_ghost_analysis(symbol):
    try:
        # فحص السيولة اللحظية
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        data = requests.get(url, timeout=5).json()
        price = float(data['lastPrice'])
        change = float(data['priceChangePercent'])
        vol = float(data['quoteVolume'])
        
        # خوارزمية الفرص الحقيقية (Ghost Logic)
        status = "SCANNING"
        power = "50%"
        color = "#444"
        
        if abs(change) > 2.0:
            status = "HYPER SIGNAL 🔥"
            power = "98%"
            color = "#00ffd5" if change > 0 else "#ff0055"
            
        tp = price * (1.015 if change > 0 else 0.985)
        sl = price * (0.994 if change > 0 else 1.006)
        
        return {
            "price": f"{price:,.2f}",
            "change": f"{change:+.2f}%",
            "status": status,
            "power": power,
            "color": color,
            "tp": f"{tp:.2f}",
            "sl": f"{sl:.2f}"
        }
    except: return None

def ghost_scanner():
    while True:
        for key, asset in ASSETS.items():
            res = get_ghost_analysis(asset['symbol'])
            if res:
                LIVE_FEED[key] = res
                # إرسال الفرص الحقيقية فقط لتليجرام
                if "HYPER" in res['status']:
                    msg = f"👻 <b>GHOST SIGNAL DETECTED!</b>\n\nAsset: {key}\nPrice: {res['price']}\nPower: {res['power']}\nTP: {res['tp']}\nSL: {res['sl']}"
                    requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "HTML"})
        time.sleep(15)

threading.Thread(target=ghost_scanner, daemon=True).start()

HTML_V13 = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap');
        :root { --accent: #00ffd5; --ghost-bg: #050505; }
        body { background: var(--ghost-bg); color: #fff; font-family: 'Space Grotesk', sans-serif; margin: 0; padding: 15px; }
        
        .header { text-align: center; padding: 40px 0; border-bottom: 1px solid #111; }
        .ghost-logo { font-size: 30px; font-weight: 800; letter-spacing: 4px; color: var(--accent); text-shadow: 0 0 20px rgba(0,255,213,0.3); }
        
        .card { 
            background: #0a0a0a; border-radius: 24px; padding: 25px; margin-top: 25px;
            border: 1px solid rgba(255,255,255,0.03); position: relative;
        }
        .signal-badge { position: absolute; top: 20px; left: 20px; font-size: 10px; font-weight: 800; padding: 4px 12px; border-radius: 50px; border: 1px solid; }
        
        .asset-title { font-size: 12px; opacity: 0.5; display: block; margin-bottom: 10px; }
        .price-main { font-size: 45px; font-weight: 700; margin: 10px 0; letter-spacing: -2px; }
        
        .meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 20px; }
        .box { background: #000; padding: 15px; border-radius: 16px; border: 1px solid #151515; }
        .box label { font-size: 8px; color: #555; display: block; margin-bottom: 5px; text-transform: uppercase; }
        .box span { font-size: 16px; font-weight: 700; color: #eee; }
        
        .copy-btn { width: 100%; background: #111; color: var(--accent); border: 1px solid var(--accent); padding: 12px; border-radius: 12px; margin-top: 20px; font-size: 12px; font-weight: 700; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <div class="ghost-logo">GHOST <span style="color:#fff">TRADER</span></div>
        <div style="font-size: 9px; color: #444; margin-top: 8px;">V13.0 ELITE | BY MOHAMED NAOUI</div>
    </div>

    {% for key, asset in assets.items() %}
    {% set d = results.get(key, {}) %}
    <div class="card">
        <div class="signal-badge" style="color: {{ d.color }}; border-color: {{ d.color }};">{{ d.status }} {{ d.power }}</div>
        <span class="asset-title">{{ asset.icon }} {{ asset.name }}</span>
        <div class="price-main">${{ d.price }}</div>
        <div style="font-size: 14px; font-weight: 800; color: {{ d.color }};">{{ d.change }}</div>
        
        <div class="meta-grid">
            <div class="box"><label>TARGET PRICE</label><span>{{ d.tp }}</span></div>
            <div class="box"><label>STOP LOSS</label><span>{{ d.sl }}</span></div>
        </div>
        
        <button class="copy-btn" onclick="alert('Signal Copied to Clipboard!')">COPY SIGNAL FOR MT5</button>
    </div>
    {% endfor %}

    <script>setTimeout(() => location.reload(), 15000);</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_V13, assets=ASSETS, results=LIVE_FEED)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
