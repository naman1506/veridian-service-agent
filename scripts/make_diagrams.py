"""Write lightweight, offline SVG diagrams matching the console palette."""
from pathlib import Path
OUT=Path(__file__).resolve().parents[1]/'docs/images'; OUT.mkdir(parents=True,exist_ok=True)
BG='#0b0d10'; S='#171c24'; L='#4c8dff'; T='#edf2f7'; M='#97a3b2'
def svg(title, labels, name):
    boxes=''.join(f'<rect x="{40+i*225}" y="150" width="180" height="74" rx="7" fill="{S}" stroke="{L}"/><text x="{130+i*225}" y="180" text-anchor="middle" fill="{T}" font-size="14" font-family="Arial">{x}</text>' + (f'<path d="M {220+i*225} 187 H {255+i*225}" stroke="{L}"/>' if i<len(labels)-1 else '') for i,x in enumerate(labels))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="360" viewBox="0 0 1000 360"><rect width="100%" height="100%" fill="{BG}"/><text x="40" y="65" fill="{T}" font-size="30" font-family="Arial" font-weight="bold">{title}</text><text x="40" y="98" fill="{M}" font-size="15" font-family="Arial">Veridian Service Agent · deterministic-first controls</text>{boxes}</svg>'
(OUT/'architecture.svg').write_text(svg('Architecture',['Console','FastAPI','Policy engine','Audit trail'],'architecture'),encoding='utf-8')
(OUT/'agent-loop.svg').write_text(svg('Per-case agent loop',['Retrieve','Decide','Guard','Audit'],'loop'),encoding='utf-8')
(OUT/'decision-taxonomy.svg').write_text(svg('Decision taxonomy',['Resolve','Need info','Route','Risk'],'taxonomy'),encoding='utf-8')
(OUT/'guardrails.svg').write_text(svg('Guardrails',['Citations','Authority','Confidence','Conflict'],'guardrails'),encoding='utf-8')
print(f'Wrote SVG diagrams to {OUT}')
