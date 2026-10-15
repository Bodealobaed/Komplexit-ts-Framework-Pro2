"""Komplexity | Commercial-style assembly complexity decision workspace."""
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
import streamlit as st
from engine import DATA, RESOURCES, DISTANCES, methods, evaluate_method, cost_line, totals, relative_change
from pdf_reports import build_pdf

st.set_page_config(page_title='Komplexity | Decision Intelligence',page_icon='◆',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp {font-family:'DM Sans',sans-serif!important}
.stApp {background:linear-gradient(145deg,#f5f8ff 0%,#f9fbfe 45%,#f4f7fc 100%)}
.block-container{padding-top:1.6rem;max-width:1460px}
h1,h2,h3{color:#142542;letter-spacing:-.035em} h1{font-weight:800!important;font-size:2.5rem!important}
[data-testid="stSidebar"]{background:#101f3a} [data-testid="stSidebar"] *{color:#f0f4ff!important}
[data-testid="stSidebar"] input{color:#172b4d!important;background:#fff!important}
[data-testid="stMetric"]{border:1px solid #e3eaf6;border-radius:18px;background:#fff;padding:16px 20px;box-shadow:0 8px 22px rgba(23,43,77,.04)}
[data-testid="stMetricLabel"]{color:#64748b!important} [data-testid="stMetricValue"]{color:#112649!important}
.stButton>button[kind="primary"],.stDownloadButton>button[kind="primary"]{background:#155eef;border:0;border-radius:12px;padding:.65rem 1.3rem;font-weight:700}
.stTabs [data-baseweb="tab-list"]{gap:10px;border-bottom:1px solid #e6edf7}
.stTabs [data-baseweb="tab"]{border-radius:12px 12px 0 0;padding:12px 16px;font-weight:650}
[data-testid="stDataFrame"],.stAlert{border-radius:14px;overflow:hidden}
.hero{background:linear-gradient(110deg,#142e61,#155eef);padding:32px 36px;border-radius:24px;color:white;margin-bottom:24px;box-shadow:0 14px 30px rgba(21,94,239,.14)}
.hero h1{color:white!important;margin:0;font-size:2.5rem}.hero p{color:#dce7ff;margin:10px 0 0;font-size:1rem}
.kicker{font-size:.72rem;text-transform:uppercase;letter-spacing:.17em;color:#a8c6ff;font-weight:800}
.section-lead{color:#61718c;margin-bottom:18px}
.info-card{padding:20px 22px;border-radius:18px;background:#fff;border:1px solid #e4ebf5;margin-bottom:14px}
.info-card strong{color:#152642}
</style>''',unsafe_allow_html=True)
CATALOG=methods()
if 'lines' not in st.session_state:st.session_state.lines=[]
if 'confirmed' not in st.session_state:st.session_state.confirmed=False
if 'selection_method' not in st.session_state:st.session_state.selection_method='M3'
if 'data' not in st.session_state:st.session_state.data=['P','R']
if 'maturity' not in st.session_state:st.session_state.maturity=2
if 'project' not in st.session_state:st.session_state.project='Montageanalyse'

with st.sidebar:
    st.image(str(Path(__file__).parent / "ktd_logo.jpg"), use_container_width=True)
    st.markdown('## ◆ KOMPLEXITY')
    st.caption('DECISION INTELLIGENCE PLATFORM')
    st.divider()
    st.text_input('Projekt / Produkt',key='project')
    st.markdown('**Arbeitsbereich**')
    st.caption('Methodenportfolio · Technische Auswahl · Ressourcenwirkung · Varianten · Bericht')
    st.divider()
    st.markdown('**Analyseprinzip**')
    st.caption('Nachvollziehbare Methodeneignung, dokumentierte Prozesswirkungen und prüfbare Ressourcenrechnung.')
    st.caption('© Komplexity · Assessment Workspace')

st.markdown('''<div class="hero"><div class="kicker">Engineering analytics / Assembly intelligence</div><h1>Komplexität verstehen.<br>Entscheidungen fundieren.</h1><p>Von der Methodenauswahl über Prozess- und Ressourcenwirkungen bis zum professionellen PDF-Report.</p></div>''',unsafe_allow_html=True)

tabs=st.tabs(['◈  Übersicht','▦  Methodenportfolio','◎  Methodenauswahl','↗  Ressourcen & Kosten','⇄  Variantenvergleich','▤  PDF-Bericht'])

with tabs[0]:
    results=[evaluate_method(m,st.session_state.data,st.session_state.maturity) for m in CATALOG]
    ready=sum(r['ready'] for r in results); sums=totals(st.session_state.lines)
    priced=sum(1 for r in st.session_state.lines if r.get('status')=='W2')
    a,b,c,d=st.columns(4)
    a.metric('Methoden im Portfolio',len(CATALOG));b.metric('Technisch einsetzbar',ready);c.metric('Ressourcenpositionen',len(st.session_state.lines));d.metric('Monetär bewertet',priced)
    st.markdown('### Analyse-Workflow')
    st.markdown('<div class="info-card"><strong>01 · Daten prüfen</strong> — Verfügbare Informationen und Planungsreife erfassen.<br><br><strong>02 · Methode wählen</strong> — Technische Eignung und fachliche Freigabe dokumentieren.<br><br><strong>03 · Wirkungen modellieren</strong> — Prozesswirkung, Ressource, Menge und Kostensatz nachvollziehbar verknüpfen.<br><br><strong>04 · Alternativen vergleichen</strong> — Vollständige Szenarien mit gleicher Bewertungsgrenze vergleichen.<br><br><strong>05 · PDF erzeugen</strong> — Entscheidungsgrundlagen mit Annahmen und Grenzen exportieren.</div>',unsafe_allow_html=True)
    st.info('Eine methodische Zulassung ist nicht gleichbedeutend mit einer berechneten Komplexitätskennzahl. Wissenschaftliche Originalmodelle benötigen separat geprüfte Formeln und Eingabedaten.')

with tabs[1]:
    st.header('Methodenportfolio')
    st.markdown('<p class="section-lead">Acht strukturierte Bewertungsansätze für Produkt-, Montage-, Prozess-, Qualitäts- und Humanfaktoren.</p>',unsafe_allow_html=True)
    frame=pd.DataFrame([{'ID':m['id'],'Bewertungsansatz':m['name'],'Datenprofil':m['data_signature'],'Informationsreife':m['mrl_label'],'Ergebnis':m['output'],'Evidenz':m['evidence'],'Perspektive':m['lens']} for m in CATALOG])
    st.dataframe(frame,hide_index=True,use_container_width=True,height=360)
    chosen=st.selectbox('Methodendetails',options=[m['id'] for m in CATALOG],format_func=lambda x:next(m['name'] for m in CATALOG if m['id']==x))
    m=next(m for m in CATALOG if m['id']==chosen)
    c1,c2,c3=st.columns(3)
    c1.metric('Mindest-Informationsreife',m['mrl_label']);c2.metric('Output-Typ',m['output']);c3.metric('Evidenzprofil',m['evidence'])
    st.write('**Benötigte Daten:** '+', '.join(DATA[x] for x in m['required_data']))
    st.caption('Die Methodenprofile unterstützen die Auswahl. Originalformeln werden nicht durch vereinfachte Ersatzindizes simuliert.')

with tabs[2]:
    st.header('Technische Methodenauswahl')
    st.markdown('<p class="section-lead">Transparente Eignungsprüfung anhand bestätigter Datenklassen und Informationsreife.</p>',unsafe_allow_html=True)
    l,r=st.columns([2,1],gap='large')
    with l:
        st.multiselect('Verfügbare Datenklassen',options=list(DATA),format_func=lambda x:f'{x} · {DATA[x]}',key='data')
        st.slider('Informationsreife',1,4,key='maturity')
    with r:
        st.markdown('<div class="info-card"><strong>Entscheidungsregel</strong><br>Eine Methode wird technisch freigegeben, wenn alle Pflichtdaten vorliegen und die benötigte Informationsreife erreicht ist. Die fachliche Eignung bleibt eine separate Entscheidung.</div>',unsafe_allow_html=True)
    rows=[]
    for m in CATALOG:
        result=evaluate_method(m,st.session_state.data,st.session_state.maturity)
        rows.append({'ID':m['id'],'Methode':m['name'],'Status':'Einsetzbar' if result['ready'] else 'Prüfung erforderlich','Fehlende Daten':', '.join(result['missing']) or '–','Reife ausreichend':'Ja' if result['maturity_ok'] else 'Nein'})
    st.dataframe(pd.DataFrame(rows),hide_index=True,use_container_width=True)
    st.selectbox('Ausgewählte Methode',options=[m['id'] for m in CATALOG],format_func=lambda x:f"{x} · {next(m['name'] for m in CATALOG if m['id']==x)}",key='selection_method')
    selected=next(m for m in CATALOG if m['id']==st.session_state.selection_method)
    assessment=evaluate_method(selected,st.session_state.data,st.session_state.maturity)
    if assessment['ready']:
        st.success('Technische Eingangsvoraussetzungen erfüllt.')
        st.checkbox('Fachliche Eignung wurde anhand des Anwendungsfalls geprüft',key='confirmed')
    else:
        st.warning('Auswahl derzeit nicht freigegeben. Fehlende Daten: '+(', '.join(assessment['missing']) or 'keine')+'; Informationsreife: '+('ausreichend' if assessment['maturity_ok'] else 'nicht ausreichend'))
        st.session_state.confirmed=False

with tabs[3]:
    st.header('Prozesswirkungen & Ressourcenrechnung')
    st.markdown('<p class="section-lead">Wirkung → Ressource → Verbrauch → Kosten. Monetarisierung nur mit dokumentierten, konsistenten Eingaben.</p>',unsafe_allow_html=True)
    # Reactive controls must not be inside st.form: checkbox changes must immediately
    # enable dependent numeric inputs on the next Streamlit rerun.
    with st.container():
        a,b=st.columns(2)
        with a:
            variant=st.text_input('Variante / Szenario','Basis')
            effect=st.text_area('Konkrete Prozesswirkung',placeholder='z. B. zusätzliche Prüfzeit aufgrund veränderter Zugänglichkeit')
            resource=st.selectbox('Betroffene Ressource',list(RESOURCES),format_func=lambda x:f'{x} · {RESOURCES[x]}')
            distance=st.selectbox('Wirkungsbezug',list(DISTANCES),format_func=lambda x:f'{x} · {DISTANCES[x]}')
        with b:
            quantify=st.checkbox('Ressourcenverbrauch ist quantifiziert')
            quantity=st.number_input('Verbrauchsmenge U',min_value=0.0,value=0.0,step=0.5,disabled=not quantify)
            unit=st.selectbox('Verbrauchseinheit',['h','min','Stück','kg','kWh','Zyklen','Andere'])
            priced=st.checkbox('Passender Kostensatz liegt vor',disabled=not quantify)
            rate=st.number_input(f'Kostensatz K (EUR pro {unit})',min_value=0.0,value=0.0,step=1.0,disabled=not priced)
            basis=st.text_input('Nachweis / Datenquelle',placeholder='z. B. Zeitstudie, ERP, kalkulierter Stundensatz')
            verified=st.checkbox('Einheiten und Wirkungsbezug geprüft')
        submit=st.button('Position berechnen und hinzufügen',type='primary',use_container_width=True)
    if submit:
        try:
            row=cost_line(effect,resource,quantity if quantify else None,rate if priced else None,unit,basis,verified,variant.strip() or 'Basis')
            row.update({'effect':effect,'resource':resource,'variant':variant.strip() or 'Basis','resource_name':RESOURCES[resource],'distance':distance,'method':st.session_state.selection_method,'basis':basis})
            if row['status']=='offen':st.error('Bitte Prozesswirkung und Ressource angeben.')
            else:
                st.session_state.lines.append(row)
                st.success(f"Position gespeichert · Status {row['status']}"+(f" · {row['cost']} EUR" if row.get('cost') is not None else ' · noch kein belastbarer Kostenbetrag'))
        except ValueError as exc:st.error(str(exc))
    if st.session_state.lines:
        st.subheader('Erfasste Positionen')
        st.dataframe(pd.DataFrame([{'Variante':x.get('variant'),'Wirkung':x.get('effect',effect if 'effect' in locals() else ''),'Ressource':x.get('resource_name'),'Status':x.get('status'),'Kosten EUR':x.get('cost') if x.get('cost') is not None else '–','Hinweis':x.get('reason','')} for x in st.session_state.lines]),hide_index=True,use_container_width=True)
        if st.button('Letzte Position entfernen'):st.session_state.lines.pop();st.rerun()
        if st.button('Alle Positionen löschen'):st.session_state.lines=[];st.rerun()
    else:st.caption('Noch keine Ressourcenpositionen angelegt.')

with tabs[4]:
    st.header('Variantenvergleich')
    st.markdown('<p class="section-lead">Vergleich der erfassten Varianten auf Basis vollständiger, gleichartig abgegrenzter Ressourcenpositionen.</p>',unsafe_allow_html=True)
    sums=totals(st.session_state.lines)
    if sums:
        display=pd.DataFrame([{'Variante':v,'Positionen':s['rows'],'Mit Kostensatz':s['priced'],'Vollständigkeit':'Vollständig' if s['complete'] else 'Unvollständig','Gesamtkosten EUR':s['cost'] if s['cost'] is not None else '–'} for v,s in sums.items()])
        st.dataframe(display,hide_index=True,use_container_width=True)
        chart={k:float(v['cost']) for k,v in sums.items() if v['cost'] is not None}
        if chart:st.bar_chart(pd.DataFrame({'Kosten EUR':chart}),color='#155eef')
        keys=list(chart)
        if len(keys)>1:
            a,b=st.columns(2)
            with a:base=st.selectbox('Referenzvariante',keys)
            with b:alt=st.selectbox('Vergleichsvariante',keys,index=1)
            delta=relative_change(chart[base],chart[alt]);st.metric('Differenz (Vergleich − Referenz)',f'{float(delta):,.2f} EUR')
        st.info('Vergleiche sind nur aussagekräftig, wenn die Varianten denselben Betrachtungsumfang und dieselbe Bezugsmenge besitzen.')
    else:st.info('Bitte zunächst im Bereich „Ressourcen & Kosten“ Positionen für mindestens eine Variante erfassen.')

with tabs[5]:
    st.header('Professioneller PDF-Bericht')
    st.markdown('<p class="section-lead">Ein konsolidiertes Dokument mit Projektkontext, Methodenprofilen, Entscheidungsstatus, Ressourcenpositionen und Variantenübersicht.</p>',unsafe_allow_html=True)
    notes=st.text_area('Projektannahmen / Bewertungsgrenzen',placeholder='Datenquellen, Bezugsmenge, Annahmen, Verantwortlichkeiten, offene Punkte ...',height=135)
    selection={'data':st.session_state.data,'maturity':st.session_state.maturity,'method':st.session_state.selection_method,'confirmed':bool(st.session_state.confirmed and evaluate_method(next(m for m in CATALOG if m['id']==st.session_state.selection_method),st.session_state.data,st.session_state.maturity)['ready'])}
    summary=totals(st.session_state.lines)
    pdf=build_pdf(st.session_state.project,selection,st.session_state.lines,summary,notes,CATALOG)
    st.download_button('PDF-Bericht herunterladen',pdf,file_name=f"Komplexity_Report_{datetime.now().strftime('%Y%m%d')}.pdf",mime='application/pdf',type='primary',use_container_width=True)
    st.caption('Der PDF-Bericht enthält auch unvollständige Positionen und weist fehlende Kostendaten ausdrücklich aus.')
