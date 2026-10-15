"""Deterministic assessment and cost model. Method scores must be externally validated."""
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from decimal import Decimal, ROUND_HALF_UP

DATA = {'P':'Produktstruktur','V':'Varianten','R':'Prozessdaten','T':'Zeitdaten','Q':'Qualitätsdaten','H':'Mensch & Ergonomie'}
RESOURCES = {'R1':'Montagepersonal','R2':'Maschine / Arbeitsplatz','R3':'Werkzeug / Vorrichtung','R4':'Qualitätsprüfung','R5':'Nacharbeit','R6':'Material / Logistik'}
DISTANCES = {'A1':'Direkter Messbezug','A2':'Indirekte Prozesswirkung','A3':'Risikobasierte Wirkung','A4':'Abstrakte Kennzahl'}

def methods():
    return json.loads(Path(__file__).with_name('methods.json').read_text(encoding='utf-8'))

def evaluate_method(method, data, maturity, confirmed=False):
    missing=sorted(set(method['required_data'])-set(data))
    ready=not missing and maturity>=method['min_mrl']
    return {'id':method['id'],'name':method['name'],'missing':missing,'maturity_ok':maturity>=method['min_mrl'],'ready':ready,'approved':bool(ready and confirmed),'score_calculable':False}

def money(value):
    return Decimal(str(value)).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)

def cost_line(effect,resource,quantity=None,rate=None,unit='h',basis='',verified=False,variant='Basis'):
    if not effect.strip() or resource not in RESOURCES:
        return {'status':'offen','cost':None,'reason':'Prozesswirkung oder Ressource fehlt'}
    if quantity is None:
        return {'status':'W0','cost':None,'reason':'Verbrauch nicht quantifiziert'}
    if not 0<=float(quantity)<1e12:raise ValueError('Ungültiger Verbrauch')
    if not unit.strip():raise ValueError('Einheit fehlt')
    if rate is None:
        return {'status':'W1','cost':None,'reason':'Kostensatz fehlt'}
    if not 0<=float(rate)<1e12:raise ValueError('Ungültiger Kostensatz')
    if not verified or not basis.strip():
        return {'status':'W1','cost':None,'reason':'Einheiten-/Wirkungsnachweis nicht bestätigt'}
    return {'status':'W2','cost':str(money(money(quantity)*money(rate))),'quantity':float(quantity),'rate':float(rate),'unit':unit,'resource':resource,'effect':effect,'variant':variant,'basis':basis,'reason':'Szenariobezogene Ressourcenrechnung'}

def totals(rows):
    """Never report an incomplete portfolio total as zero or complete."""
    groups={}
    for row in rows:
        variant=row.get('variant','Basis')
        group=groups.setdefault(variant,{'rows':0,'priced':0,'cost':Decimal('0'),'complete':True})
        group['rows']+=1
        if row.get('status')=='W2' and row.get('cost') is not None:
            group['priced']+=1;group['cost']+=money(row['cost'])
        else:group['complete']=False
    return {k:{**v,'cost':str(v['cost']) if v['complete'] and v['rows'] else None,'partial_cost':str(v['cost'])} for k,v in groups.items()}

def relative_change(reference,alternative):
    if reference is None or alternative is None:return None
    return str(money(Decimal(str(alternative))-Decimal(str(reference))))
