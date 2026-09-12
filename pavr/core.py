from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple
import math, random

@dataclass(frozen=True)
class Intervention:
    name: str
    sickness_reduction: float
    presence_cost: float
    task_cost: float
    burden: float

INTERVENTIONS: Tuple[Intervention,...] = (
    Intervention("none",0.00,0.00,0.00,0.00),
    Intervention("reduce_speed",0.12,0.02,0.01,0.02),
    Intervention("reduce_rotation",0.16,0.03,0.01,0.03),
    Intervention("dynamic_fov",0.21,0.06,0.02,0.05),
    Intervention("stabilize_motion",0.24,0.05,0.03,0.06),
    Intervention("teleport",0.30,0.10,0.05,0.09),
)

def _sigmoid(x): return 1/(1+math.exp(-x))

def risk_score(features: Dict[str,float], personal_bias: float=0.0) -> float:
    x=(0.85*features['head_ang_vel']+0.65*features['head_accel']+0.75*features['trans_vel']+0.35*features['controller_motion']+0.55*features['turn_rate']+0.70*features['jerk']+0.40*features['task_errors']+0.25*features['pauses']+0.30*features['exposure_min']+0.50*features['frame_drop']+personal_bias-2.35)
    return _sigmoid(x)

def choose_intervention(predicted_risk, lambda_presence=1.0, lambda_task=1.0, lambda_burden=1.0, risk_threshold=0.45):
    if predicted_risk<risk_threshold: return INTERVENTIONS[0]
    best,best_obj=INTERVENTIONS[0],float('inf')
    for a in INTERVENTIONS:
        residual=max(0.0,predicted_risk-a.sickness_reduction)
        obj=residual+lambda_presence*a.presence_cost+lambda_task*a.task_cost+lambda_burden*a.burden
        if obj<best_obj: best,best_obj=a,obj
    return best

def apply_intervention(risk,intervention): return max(0.0,min(1.0,risk-intervention.sickness_reduction))

def simulate_session(seed=0,steps=120,personal_bias=0.0):
    rng=random.Random(seed); rows=[]; prev=0.0
    for t in range(steps):
        fatigue=t/max(1,steps-1)
        f={'head_ang_vel':max(0,rng.gauss(0.55+0.25*fatigue,0.12)),'head_accel':max(0,rng.gauss(0.45+0.20*fatigue,0.10)),'trans_vel':max(0,rng.gauss(0.50+0.15*fatigue,0.10)),'controller_motion':max(0,rng.gauss(0.40,0.12)),'turn_rate':max(0,rng.gauss(0.42+0.22*fatigue,0.11)),'jerk':max(0,rng.gauss(0.38+0.25*fatigue,0.10)),'task_errors':max(0,rng.gauss(0.18+0.20*fatigue,0.08)),'pauses':max(0,rng.gauss(0.10+0.15*fatigue,0.06)),'exposure_min':t/60.0,'frame_drop':max(0,rng.gauss(0.08,0.04))}
        raw=risk_score(f,personal_bias); pred=0.75*raw+0.25*prev; a=choose_intervention(pred); post=apply_intervention(pred,a)
        rows.append({'t':t,**f,'risk_raw':raw,'risk_pred':pred,'intervention':a.name,'risk_post':post,'presence_cost':a.presence_cost,'task_cost':a.task_cost,'burden':a.burden})
        prev=post
    return rows
