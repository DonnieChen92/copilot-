import pytest
from SACA_Dossier.py.saca_runtime import compute_stc, STCResult

def test_stc_green():
    factors = {"u": 0.1, "v": 0.1}
    res = compute_stc(factors)
    # avg = 0.1
    assert res.score <= 0.5
    assert res.band == "GREEN"
    assert res.action == "AUTO"

def test_stc_amber():
    factors = {"u": 0.6, "v": 0.6}
    res = compute_stc(factors)
    # avg = 0.6
    assert 0.5 < res.score <= 0.8
    assert res.band == "AMBER"
    assert res.action == "DEGRADE"

def test_stc_red():
    factors = {"u": 0.9, "v": 0.9}
    res = compute_stc(factors)
    # avg = 0.9
    assert res.score > 0.8
    assert res.band == "RED"
    assert res.action == "HALT"

def test_stc_mixed():
    # 0.9 + 0.1 = 1.0 / 2 = 0.5 -> Green (<= 0.5 is Green in code: score > 0.5 is Amber)
    factors = {"u": 0.9, "v": 0.1}
    res = compute_stc(factors)
    assert res.score == 0.5
    assert res.band == "GREEN"
