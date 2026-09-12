from .core import simulate_session, INTERVENTIONS, apply_intervention
import random, statistics

def _threshold(risk):
    if risk<0.45: return risk,0,0,0
    a=next(x for x in INTERVENTIONS if x.name=='teleport')
    return apply_intervention(risk,a),a.presence_cost,a.task_cost,a.burden

def evaluate(n_sessions=240,steps=120,seed=7):
    rng=random.Random(seed); out={'fixed':[],'threshold':[],'pavr':[]}
    for i in range(n_sessions):
        rows=simulate_session(seed+i,steps,rng.uniform(-0.35,0.35)); fr=[]; tr=[]; pr=[]; tpc=ttc=tb=ppc=ptc=pb=0.0
        for r in rows:
            risk=r['risk_pred']; fr.append(risk); x,pc,tc,b=_threshold(risk); tr.append(x); tpc+=pc; ttc+=tc; tb+=b; pr.append(r['risk_post']); ppc+=r['presence_cost']; ptc+=r['task_cost']; pb+=r['burden']
        out['fixed'].append({'mean_risk':statistics.mean(fr),'high_risk_fraction':sum(x>=0.6 for x in fr)/steps,'presence_cost':0,'task_cost':0,'burden':0})
        out['threshold'].append({'mean_risk':statistics.mean(tr),'high_risk_fraction':sum(x>=0.6 for x in tr)/steps,'presence_cost':tpc/steps,'task_cost':ttc/steps,'burden':tb/steps})
        out['pavr'].append({'mean_risk':statistics.mean(pr),'high_risk_fraction':sum(x>=0.6 for x in pr)/steps,'presence_cost':ppc/steps,'task_cost':ptc/steps,'burden':pb/steps})
    return out

def summarize(results):
    return {name:{k:statistics.mean(r[k] for r in rows) for k in rows[0]} for name,rows in results.items()}
