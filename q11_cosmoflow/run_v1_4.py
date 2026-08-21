from __future__ import annotations
import csv, hashlib, json, math, runpy, shutil, sys, tempfile
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import numpy as np

ROOT=Path(__file__).resolve().parents[1]; SOURCE=ROOT/"CosmoFlow"/"Massless_dphi3"; OUT=ROOT/"q11_cosmoflow"/"artifacts"/"v1.4"; OUT.mkdir(parents=True,exist_ok=True)
CONFIGS={"D3_EQ":("DeltaN = 3","k1, k2, k3 = k, k, k"),"D5_EQ":("DeltaN = 5","k1, k2, k3 = k, k, k"),"D4_SQ":("DeltaN = 4","k1, k2, k3 = k, k, 0.5 * k")}
PARTS={"P334":(0,334,667,1000),"P250":(0,250,750,1000),"P400":(0,400,600,1000)}; SUMS=("GM","AM","RMS"); WIN=(1,1,6); Q11=(1,2,3); TOL=1e-12
def h(p):
 x=hashlib.sha256(); x.update(p.read_bytes()); return x.hexdigest()
def label(f): return ":".join(map(str,f))
def feat(a,b,s):
 a=np.abs(a); z=[]
 for i,j in zip(b[:-1],b[1:]):
  x=a[i:j]
  if x.size==0 or np.any(x<=0): raise ValueError("invalid absolute bin")
  z.append(float(np.exp(np.mean(np.log(x))) if s=="GM" else np.mean(x) if s=="AM" else np.sqrt(np.mean(x*x))))
 return sorted(z)
def score(x,f):
 x=np.log(x); y=np.log(np.asarray(f,float)); return float(np.sqrt(np.mean(((x-x.mean())-(y-y.mean()))**2)))
def ranks(rows,key,out):
 vals=sorted({r[key] for r in rows})
 for r in rows:r[out]=1+sum(v<r[key]-TOL for v in vals)
source_hashes={p.name:h(p) for p in (SOURCE/"MyFirstRun.py",SOURCE/"Parameters.py",SOURCE/"Theory.py",SOURCE/"Solver.py")}
families=[(a,b,c) for a in range(1,7) for b in range(a,7) for c in range(b,7) if math.gcd(math.gcd(a,b),c)==1]; assert len(families)==42
rows=[]; cells=[]; raws={}
for name,(delta,kin) in CONFIGS.items():
 with tempfile.TemporaryDirectory() as d:
  copy=Path(d)/"Massless_dphi3"; shutil.copytree(SOURCE,copy); script=copy/"MyFirstRun.py"; text=script.read_text(); text=text.replace("DeltaN = 4",delta,1).replace("k1, k2, k3 = k, k, k",kin,1); script.write_text(text)
  old=list(sys.path); sys.path.insert(0,str(copy)); ns=runpy.run_path(str(script),run_name="__main__"); sys.path[:]=old
  target={"T01":np.abs(np.asarray(ns["f"][0][0,0],float)),"T02":np.abs(np.asarray(ns["f"][6][0,0,0],float))}
  if any(v.shape!=(1000,) or not np.isfinite(v).all() for v in target.values()): raise RuntimeError(f"{name} invalid output")
  raw=OUT/f"{name}_raw.npz"; np.savez_compressed(raw,N=np.asarray(ns["N"]),field_field=target["T01"],field_field_field=target["T02"]); raws[name]=h(raw)
  for pn,bounds in PARTS.items():
   for sm in SUMS:
    rep=f"{pn}_{sm}"; vs={k:feat(v,bounds,sm) for k,v in target.items()}; local=[]
    for f in families:
     a,b=score(vs["T01"],f),score(vs["T02"],f);local.append({"config":name,"representation":rep,"family":label(f),"T01_RMSE":a,"T02_RMSE":b,"pooled_RMSE":(a+b)/2})
    for k,o in (("T01_RMSE","T01_rank"),("T02_RMSE","T02_rank"),("pooled_RMSE","pooled_rank")):ranks(local,k,o)
    w=next(r for r in local if r["family"]==label(WIN)); q=next(r for r in local if r["family"]==label(Q11)); cells.append({"config":name,"representation":rep,"winner_unique_rank_1":w["pooled_rank"]==1 and sum(r["pooled_rank"]==1 for r in local)==1,"winner_T01_rank":w["T01_rank"],"winner_T02_rank":w["T02_rank"],"q11_pooled_rank":q["pooled_rank"]});rows+=local
unique=sum(x["winner_unique_rank_1"] for x in cells); never=all(x["winner_T01_rank"]<=3 and x["winner_T02_rank"]<=3 for x in cells)
summary={"queue":"Q11 x COSMOFLOW V1.4","source_sha256":source_hashes,"raw_sha256":raws,"family_count":42,"cell_count":len(cells),"v12_winner":"1:1:6","winner_unique_rank_1_count":unique,"winner_never_below_rank_3_target_specific":never,"classification":"OUT_OF_SAMPLE_STABLE" if unique==27 and never else "OUT_OF_SAMPLE_SENSITIVE","q11":{"family":"1:2:3","pooled_ranks":[x["q11_pooled_rank"] for x in cells],"best_rank":min(x["q11_pooled_rank"] for x in cells)},"cells":cells,"claim_scope":"Fixed V1.4 out-of-sample configurations and V1.3 grid only; non-causal."}
with (OUT/"scores.csv").open("w",newline="") as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/"summary.json").write_text(json.dumps(summary,indent=2,sort_keys=True));print(json.dumps(summary,indent=2,sort_keys=True))
