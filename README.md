# Rastreador RSI Quantfury

RSI(14) e RSI(2) diários (candles do Yahoo Finance) de cripto, ações, ETFs, futuros e câmbio negociáveis na Quantfury.
Uma rotina do GitHub Actions roda a cada hora e atualiza só os ativos com pregão aberto. A página é publicada pelo GitHub Pages.

- `rsi_all.py`: busca candles e calcula o RSI (`--auto` pula mercados fechados)
- `tickers.py`: lista de ações
- `build.py` e `tpl.txt`: geram `index.html`
- `data_all.json`: último valor de cada ativo
