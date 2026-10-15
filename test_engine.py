import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
from engine import methods,evaluate_method,cost_line,totals,relative_change

def test_eight_methods():assert len(methods())==8
def test_gate():
 m=methods()[3]; assert not evaluate_method(m,['P','R'],2)['ready']
def test_w0():assert cost_line('Zusatzprüfung','R4')['status']=='W0'
def test_w1():assert cost_line('Zusatzprüfung','R4',2)['status']=='W1'
def test_w2():assert cost_line('Zusatzprüfung','R4',2,35,'h','Zeitstudie',True)['cost']=='70.00'
def test_unverified_no_cost():assert cost_line('Zusatzprüfung','R4',2,35,'h','',True)['cost'] is None
def test_no_false_total():assert totals([{'variant':'A','status':'W0','cost':None}])['A']['cost'] is None
def test_delta():assert relative_change('100','80')=='-20.00'
def test_negative_rejected():
 with pytest.raises(ValueError):cost_line('Prüfung','R4',-1)
