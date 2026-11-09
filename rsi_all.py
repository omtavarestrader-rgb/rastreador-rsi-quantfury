import json,sys,time,urllib.request,urllib.parse
ns={}; exec(open("tickers.py").read(),ns)
UA="quantfury-rsi-tracker/1.0"
WL=set("BTC/USDT ETH/USDT XRP/USDT AAVE/USDT SOL/USDT LTC/USDT LINK/USDT AVAX/USDT INJ/USDT UNI/USDT NEAR/USDT DOT/USDT SUI/USDT FIL/USDT ONDO/USDT ADA/USDT XLM/USDT HBAR/USDT DOGE/USDT SAND/USDT NQZ6 DXZ6 SMTO3 WEGE3 USIM5 SLCE3 TTWO IONQ QBTS QS BBAI META GOOGL AMZN AAPL IBIT NVDA PINFRA SPY ENR TLN MSFT MSTR PETR4 VBBR3 TAEE11 SAPR11 SANB11 KLBN11 JBS ITUB4 ITSA4 EMBJ3 BPAC11 BBDC4 BBAS3 AGRO3 VIVT3".split())
rows=[]  # display,yahoo,group,ccy
crypto="AAVE ADA APT ARB ATOM AVAX BCH BTC DOGE DOT ETC ETH FIL FTM HBAR HYPE INJ LINK LTC MANA POL NEAR NEO ONDO OP RUNE SAND SUI SOL TAO THETA UNI VIRTUAL XLM XRP ZEC".split()
CM={"UNI":"UNI7083-USD","SUI":"SUI20947-USD","APT":"APT21794-USD","POL":"POL28321-USD","TAO":"TAO22974-USD","HYPE":"HYPE32196-USD","VIRTUAL":"VIRTUAL-USD"}
for c in crypto: rows.append((c+"/USDT",CM.get(c,c+"-USD"),"Cripto","USDT"))
rows.append(("BTC/BRL","BTC-BRL","Cripto","BRL"))
rows+= [("NQZ6","NQ=F","Futuros e outros","USD"),("DXZ6","DX-Y.NYB","Futuros e outros","USD"),("ENR","ENR.DE","Futuros e outros","EUR")]
for t in ns["NYSE"]: rows.append((t,t,"Ações NYSE","USD"))
for t in ns["NASDAQ"]: rows.append((t,t,"Ações NASDAQ","USD"))
for t in ns["B3"]: rows.append((t,t+".SA","Ações B3","BRL"))
for t in ns["BMV"]: rows.append((t,t+".MX","Ações BMV (México)","MXN"))

FUT=[("Prata (COMEX)","SI=F"),("Cobre (COMEX)","HG=F"),("Ouro (COMEX)","GC=F"),("Platina (NYMEX)","PL=F"),("Paládio (NYMEX)","PA=F"),("WTI petróleo (NYMEX)","CL=F"),("Gás natural (NYMEX)","NG=F"),("RBOB Gasoline (NYMEX)","RB=F"),("Heating Oil (NYMEX)","HO=F"),("VIX (CBOE)","^VIX"),("Milho (CBOT)","ZC=F"),("Trigo SRW (CBOT)","ZW=F"),("Soja (CBOT)","ZS=F"),("S&P 500 E-mini","ES=F"),("NASDAQ 100 E-mini","NQ=F"),("Nikkei/Yen (CME)","NIY=F"),("Dow E-mini","YM=F"),("Russell 2000 E-mini","RTY=F"),("Bitcoin (CME)","BTC=F"),("DAX Futures","^GDAXI"),("CAC 40 Futures","^FCHI"),("Bovespa Futures","^BVSP"),("T-Note 10 anos","ZN=F")]
for d,y in FUT: rows.append((d,y,"Futuros","USD"))
for p in "USD/CAD USD/CHF USD/CNY USD/HKD USD/JPY USD/NOK USD/BRL USD/KRW USD/MXN AUD/USD EUR/USD GBP/USD".split():
    rows.append((p,p.replace("/","")+"=X","Câmbio",p.split("/")[1]))
etf_b3=["BOVA11"]
etf_us="KSA UAE BOTZ ETHA IBIT IEF JEPQ MCHI QQQ ROBT SHY SMH TLT TUR WOOD ARGT ARKK BOIL COPX DIA EEM EWA EWG EWH EWJ EWP EWQ EWT EWU EWW EWY EWZ EZA FBTC FXI GBTC GDX GLD ILF INDA IWM IXN IYW JEPI LIT METV OIH PPLT ROBO SCHD SLV SPY UNG URA URNM USO UUP VBR VGK VNQ VT XLB XLC XLE XLF XLI XLK XLP XLRE XLU XLV XLY XME".split()
for t in etf_b3: rows.append((t,t+".SA","ETFs","BRL"))
for t in etf_us: rows.append((t,t,"ETFs","USD"))
seen=set();R0=[]
for r in rows:
    if r[1] in seen: continue
    seen.add(r[1]); R0.append(r)

import datetime,zoneinfo,os
def is_open(r,now=None):
    """Pregão aberto agora, ou fechou há menos de 1h (para capturar o fechamento final). Feriados não são tratados."""
    now=now or datetime.datetime.now(datetime.timezone.utc)
    dis,y,g,c=r
    if g=="Cripto": return True
    def loc(z): return now.astimezone(zoneinfo.ZoneInfo(z))
    def window(z,o,cl):
        t=loc(z)
        if t.weekday()>=5: return False
        m=t.hour*60+t.minute
        return o<=m<cl+60
    et=loc("America/New_York"); wd=et.weekday(); m=et.hour*60+et.minute
    if y.endswith("=F"):   # CME: dom 18h ET a sex 17h ET (+1h)
        return not (wd==5 or (wd==6 and m<18*60) or (wd==4 and m>=18*60))
    if y.endswith("=X") or y=="DX-Y.NYB":  # câmbio: dom 17h ET a sex 17h ET (+1h)
        return not (wd==5 or (wd==6 and m<17*60) or (wd==4 and m>=18*60))
    if y.endswith(".SA") or y=="^BVSP": return window("America/Sao_Paulo",10*60,17*60)
    if y.endswith(".MX"): return window("America/Mexico_City",8*60+30,15*60)
    if y.endswith(".DE") or y=="^GDAXI": return window("Europe/Berlin",9*60,17*60+30)
    if y=="^FCHI": return window("Europe/Paris",9*60,17*60+30)
    return window("America/New_York",9*60+30,16*60)
AUTO="--auto" in sys.argv and os.path.exists("data_all.json")
def rsi(cl,n=14):
    if len(cl)<n+1: return None
    g=l=0
    for i in range(1,n+1):
        d=cl[i]-cl[i-1]; g+=max(d,0); l+=max(-d,0)
    g/=n;l/=n
    for i in range(n+1,len(cl)):
        d=cl[i]-cl[i-1]; g=(g*(n-1)+max(d,0))/n; l=(l*(n-1)+max(-d,0))/n
    return 100.0 if l==0 else 100-100/(1+g/l)
def spark(batch):
    u="https://query1.finance.yahoo.com/v8/finance/spark?range=6mo&interval=1d&symbols="+urllib.parse.quote(",".join(batch),safe=",")
    for k in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA}),timeout=30))
        except Exception as e:
            if "429" in str(e): time.sleep(5*(k+1)); continue
            if "404" in str(e) or "400" in str(e): return {}
            time.sleep(2)
    return {}
meta={r[1]:r for r in R0}
out={}
prev={r["yahoo"]:r for r in json.load(open("data_all.json"))} if AUTO else {}
syms=[r[1] for r in R0 if (not AUTO) or is_open(r)]; B=20
if AUTO: print("abertos agora:",len(syms),"de",len(R0))
for i in range(0,len(syms),B):
    d=spark(syms[i:i+B])
    for s,v in d.items():
        try:
            ts=v["timestamp"]; cl=v.get("close") or v["indicators"]["quote"][0]["close"]
            p=[(t,c) for t,c in zip(ts,cl) if c is not None]
            cs=[c for _,c in p]; x=rsi(cs)
            if x is None or len(cs)<16: continue
            dis,y,g,c=meta[s]
            out[s]=dict(sym=dis,yahoo=s,group=g,ccy=c,wl=dis in WL,price=cs[-1],chg=(cs[-1]/cs[-2]-1)*100,rsi=round(x,1),prev=round(rsi(cs[:-1]),1),rsi2=round(rsi(cs,2),1),rsi2p=round(rsi(cs[:-1],2),1),last=p[-1][0],upd=int(time.time()),spark=[float('%.5g'%q) for q in cs[-30:]])
        except Exception as e: pass
    time.sleep(0.8)
    if (i//B)%10==0: print(i,len(out),flush=True)
res=[]
for r in R0:
    res.append(out.get(r[1]) or ((prev.get(r[1]) if r[1] not in syms else None)) or dict(sym=r[0],yahoo=r[1],group=r[2],ccy=r[3],wl=r[0] in WL,rsi=None,rsi2=None))
json.dump(res,open("data_all.json","w"))
ok=[r for r in res if r["rsi"] is not None]
print(len(res),"ativos;",len(ok),"com RSI;",len(res)-len(ok),"sem dados")
print("sobrecompra",sum(r["rsi"]>=70 for r in ok),"sobrevenda",sum(r["rsi"]<=30 for r in ok))
print("sem dados wl:",[r["sym"] for r in res if r["rsi"] is None and r["wl"]])
