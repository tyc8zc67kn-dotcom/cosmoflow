from __future__ import annotations
import csv, json, math, runpy, shutil, sys, tempfile
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'CosmoFlow'/'Massless_dphi3'; OUT=ROOT/'q11_cosmoflow'/'artifacts'/'v1.5'; OUT.mkdir(parents=True,exist_ok=True)
REPS={'P334_GM':((0,334,667,1000),'GM'),'P400_GM':((0,400,600,1000),'GM'),'P334_AM':((0,334,667,1000),'AM')}; TOL=1e-12
F=[(a,b,c) for a in range(1,7) for b in range(a,7) for c in range(b,7) if math.gcd(math.gcd(a,b),c)==1]; assert len(F)==42
def lab(f): return ':'.join(map(str,f))
def feature(x,bounds,method):
    x=np.abs(x); a=[]
    for i,j in zip(bounds[:-1],bounds[1:]):
        z=x[i:j]
        if z.size==0 or np.any(z<=0): raise ValueError('invalid bin')
        a.append(float(np.exp(np.mean(np.log(z))) if method=='GM' else np.mean(z)))
    return sorted(a)
def score(x,f):
    x=np.log(x); y=np.log(np.asarray(f,float)); return float(np.sqrt(np.mean(((x-x.mean())-(y-y.mean()))**2)))
rows=[]
for d in range(2,7):
    with tempfile.TemporaryDirectory() as tmp:
        folder=Path(tmp)/'Massless_dphi3'; shutil.copytree(SRC,folder); p=folder/'MyFirstRun.py'; p.write_text(p.read_text().replace('DeltaN = 4',f'DeltaN = {d}',1))
        old=list(sys.path); sys.path.insert(0,str(folder)); ns=runpy.run_path(str(p),run_name='__main__'); sys.path[:]=old
        x=np.asarray(ns['f'][6][0,0,0],float)
        if x.shape!=(1000,) or not np.isfinite(x).all(): raise RuntimeError(f'DeltaN {d} invalid T02')
        for name,(bounds,method) in REPS.items():
            z=feature(x,bounds,method); allrows=[{'family':lab(f),'score':score(z,f)} for f in F]; vals=sorted({r['score'] for r in allrows})
            for r in allrows: r['rank']=1+sum(v<r['score']-TOL for v in vals)
            w=next(r for r in allrows if r['family']=='1:1:6'); q=next(r for r in allrows if r['family']=='1:2:3'); best=[r['family'] for r in allrows if r['rank']==1]
            rows.append({'DeltaN':d,'representation':name,'winner_families':';'.join(best),'winner_1_1_6_score':w['score'],'winner_1_1_6_rank':w['rank'],'q11_1_2_3_score':q['score'],'q11_1_2_3_rank':q['rank']})
summary={'queue':'Q11 x COSMOFLOW V1.5','target':'T02 only','rows':rows,'scope':'Descriptive sensitivity localization only; non-causal.'}
with (OUT/'scores.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
