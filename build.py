import json,datetime,zoneinfo
t=open("tpl.txt").read()
d=json.load(open("data_all.json"))
out=[r if r["rsi"] is not None else dict(sym=r["sym"],group=r["group"],ccy=r["ccy"],wl=r["wl"],rsi=None) for r in d]
gen=datetime.datetime.now(zoneinfo.ZoneInfo("America/Sao_Paulo")).strftime("%d/%m %H:%M (Brasília)")
open("rastreador-rsi.html","w").write(t.replace("__DATA__",json.dumps(out,separators=(",",":"))).replace("__GEN__",json.dumps(gen)))
ok=[r for r in out if r["rsi"] is not None]
print(gen,len(out),"ativos;",sum(r["rsi"]>=70 for r in ok),"sobrecompra;",sum(r["rsi"]<=30 for r in ok),"sobrevenda")
