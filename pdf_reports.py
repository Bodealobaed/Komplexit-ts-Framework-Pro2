"""Downloadable, paginated German PDF decision reports (ReportLab)."""
from io import BytesIO
from datetime import datetime
from decimal import Decimal
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from xml.sax.saxutils import escape

BASE=Path(__file__).parent
FONT=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
if FONT.exists():
    pdfmetrics.registerFont(TTFont('DejaVuReport',str(FONT)))
FONTNAME='DejaVuReport' if FONT.exists() else 'Helvetica'
INK=colors.HexColor('#152642'); BLUE=colors.HexColor('#155EEF'); LIGHT=colors.HexColor('#EDF3FF')

def build_pdf(project,selection,lines,summary,notes,methods_catalog):
    buffer=BytesIO(); doc=SimpleDocTemplate(buffer,pagesize=A4,leftMargin=42,rightMargin=42,topMargin=48,bottomMargin=48)
    styles=getSampleStyleSheet(); styles.add(ParagraphStyle(name='CoverCustom',fontName=FONTNAME,fontSize=20,leading=27,textColor=INK,spaceAfter=14))
    styles.add(ParagraphStyle(name='SubCustom',fontName=FONTNAME,fontSize=11,leading=16,textColor=BLUE,spaceBefore=17,spaceAfter=8))
    styles.add(ParagraphStyle(name='BodyCustom',fontName=FONTNAME,fontSize=8.5,leading=13,spaceAfter=8))
    styles.add(ParagraphStyle(name='SmallCustom',fontName=FONTNAME,fontSize=7,leading=10))
    def p(t,sty='BodyCustom'):return Paragraph(escape(str(t)),styles[sty])
    story=[p('Komplexity | Assessment Report','CoverCustom'),p('Projekt: '+project),p('Erstellt: '+datetime.now().strftime('%d.%m.%Y %H:%M'))]
    story.append(p('Methodenauswahl','SubCustom'))
    story.append(p('Datenklassen: '+', '.join(selection.get('data',[]))+' | Informationsreife: '+str(selection.get('maturity','–'))))
    story.append(p('Ausgewählte Methode: '+str(selection.get('method','Nicht festgelegt'))))
    story.append(p('Fachliche Freigabe: '+('Ja' if selection.get('confirmed') else 'Nein')))
    story.append(p('Methodenportfolio','SubCustom'))
    for m in methods_catalog:story.append(p(f"{m['id']} | {m['name']} | Daten: {m['data_signature']} | MRL: {m['mrl_label']} | Output: {m['output']}" ,'SmallCustom'))
    story.append(p('Ressourcen- und Kostenbewertung','SubCustom'))
    if lines:
        header=[p(x,'SmallCustom') for x in ['Variante','Ressource','Wirkung','Status','Kosten EUR']]
        rows=[header]
        for r in lines:
            rows.append([p(str(r.get(k,'–'))[:65],'SmallCustom') for k in ['variant','resource','effect','status']]+[p(str(r.get('cost') or '–'),'SmallCustom')])
        table=Table(rows,colWidths=[62,65,205,47,62],repeatRows=1,hAlign='LEFT')
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),LIGHT),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),0.8,BLUE),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F8FAFC')])]))
        story.append(table)
    else:story.append(p('Keine Ressourcenpositionen erfasst.'))
    story.append(p('Variantenübersicht','SubCustom'))
    for key,val in summary.items():
        complete='vollständig' if val['complete'] else 'unvollständig'
        story.append(p(f"{key}: {val['priced']}/{val['rows']} Positionen W2 | {complete} | Gesamt: {val['cost'] if val['cost'] is not None else 'nicht verfügbar'} EUR"))
    story.append(p('Annahmen und Nachweise','SubCustom'))
    story.append(p(notes or 'Keine zusätzlichen Anmerkungen.'))
    story.append(p('Methodischer Hinweis','SubCustom'))
    story.append(p('Die Auswahlprüfung ist keine Berechnung der wissenschaftlichen Originalmethoden. Kostenbeträge sind nur szenariobezogene Ressourcenrechnungen aus dokumentierten Mengen und Kostensätzen. Fehlende Werte gelten nicht als Null. Kausalität und Übertragbarkeit sind gesondert zu validieren.'))
    def footer(canvas,document):
        canvas.setFont(FONTNAME,8);canvas.setFillColor(colors.HexColor('#667085'))
        canvas.drawString(42,28,'KOMPLEXITY  /  DECISION INTELLIGENCE')
        canvas.drawRightString(A4[0]-42,28,f'Seite {document.page}')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    return buffer.getvalue()
