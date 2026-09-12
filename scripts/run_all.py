import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import csv,json
from pavr.experiments import evaluate,summarize
out=Path('results'); out.mkdir(exist_ok=True)
s=summarize(evaluate())
(out/'summary.json').write_text(json.dumps(s,indent=2),encoding='utf-8')
with open(out/'summary.csv','w',newline='',encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['system','mean_risk','high_risk_fraction','presence_cost','task_cost','burden'])
    for name,v in s.items(): w.writerow([name,v['mean_risk'],v['high_risk_fraction'],v['presence_cost'],v['task_cost'],v['burden']])
fixed,th,p=s['fixed'],s['threshold'],s['pavr']
pct=lambda a,b:100*(a-b)/a if a else 0
report=f'''# PAVR Reproducibility Report

| System | Mean risk | High-risk fraction | Presence cost | Task cost | Intervention burden |
|---|---:|---:|---:|---:|---:|
| Fixed VR | {fixed['mean_risk']:.6f} | {fixed['high_risk_fraction']:.6f} | 0 | 0 | 0 |
| Threshold-Adaptive | {th['mean_risk']:.6f} | {th['high_risk_fraction']:.6f} | {th['presence_cost']:.6f} | {th['task_cost']:.6f} | {th['burden']:.6f} |
| PAVR | {p['mean_risk']:.6f} | {p['high_risk_fraction']:.6f} | {p['presence_cost']:.6f} | {p['task_cost']:.6f} | {p['burden']:.6f} |

PAVR synthetic mean-risk reduction versus Fixed VR: **{pct(fixed['mean_risk'],p['mean_risk']):.2f}%**.

PAVR synthetic intervention-burden reduction versus Threshold-Adaptive VR: **{pct(th['burden'],p['burden']):.2f}%**.

These are controlled synthetic results. They do not establish human-subject efficacy or clinical validity.
'''
(out/'REPORT.md').write_text(report,encoding='utf-8')
print(report)
