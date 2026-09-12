from pavr.core import risk_score,choose_intervention,apply_intervention,simulate_session

def _f():
    return {k:0.5 for k in ['head_ang_vel','head_accel','trans_vel','controller_motion','turn_rate','jerk','task_errors','pauses','exposure_min','frame_drop']}

def test_risk_bounded():
    r=risk_score(_f()); assert 0<=r<=1

def test_no_intervention_low():
    assert choose_intervention(0.1).name=='none'

def test_reduces():
    a=choose_intervention(0.9); assert apply_intervention(0.9,a)<=0.9

def test_shape():
    assert len(simulate_session(1,25))==25
