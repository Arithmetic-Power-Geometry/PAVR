from pavr.experiments import evaluate,summarize

def test_three():
    assert set(summarize(evaluate(12,30)))=={'fixed','threshold','pavr'}

def test_risk_lower():
    s=summarize(evaluate(24,60)); assert s['pavr']['mean_risk']<s['fixed']['mean_risk']

def test_burden_lower():
    s=summarize(evaluate(24,60)); assert s['pavr']['burden']<=s['threshold']['burden']

def test_deterministic():
    assert summarize(evaluate(8,20,11))==summarize(evaluate(8,20,11))
