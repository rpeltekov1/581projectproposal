from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).resolve().parents[1]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ParcelBody',fontName='Helvetica',fontSize=10.2,leading=15,textColor=HexColor('#24392d'),spaceAfter=10))
styles.add(ParagraphStyle(name='ParcelHeading',fontName='Helvetica-Bold',fontSize=22,leading=28,textColor=HexColor('#176951'),spaceAfter=20))
styles.add(ParagraphStyle(name='ParcelTitle',fontName='Helvetica-Bold',fontSize=32,leading=39,textColor=HexColor('#176951'),spaceAfter=18))
styles.add(ParagraphStyle(name='ParcelSmall',fontName='Helvetica',fontSize=10,leading=15,textColor=HexColor('#738277'),spaceAfter=18))
text=(ROOT/'docs/software-design.md').read_text()
parts=text.split('\n## ')
story=[Paragraph('PARCEL',styles['ParcelTitle']),Paragraph('Property visualization<br/>&amp; floor-plan intake',styles['ParcelHeading']),Paragraph('Software design and implementation handoff<br/>Version 0.1 / 4 October 2026',styles['ParcelSmall']),Spacer(1,28),Paragraph('A working prototype with explicit integration boundaries',styles['ParcelHeading']),Paragraph('The prototype separates original extraction, human review, publication and evaluation. This document identifies what is implemented, how to run it, and what remains unconnected.',styles['ParcelBody']),Spacer(1,20)]
for i,part in enumerate(parts[1:],1):
 title,body=part.split('\n',1)
 if i==1:story.append(Paragraph('Contents',styles['ParcelHeading']))
 story.append(Paragraph(escape(title),styles['ParcelBody']))
story.append(PageBreak())
for idx,part in enumerate(parts[1:]):
 title,body=part.split('\n',1)
 story.append(Paragraph(escape(title),styles['ParcelHeading']))
 for p in body.strip().split('\n\n'):
  story.append(Paragraph(escape(p.strip()).replace('\n','<br/>'),styles['ParcelBody']))
 if idx<len(parts)-2:story.append(PageBreak())
def page(c,d):
 c.setStrokeColor(HexColor('#dce5de'));c.line(45,747,567,747)
 c.setFont('Helvetica-Bold',9);c.setFillColor(HexColor('#176951'));c.drawString(45,759,'PARCEL / SOFTWARE DESIGN')
 c.setFont('Helvetica',8);c.setFillColor(HexColor('#78867b'));c.drawString(45,28,'Version 0.1  |  4 October 2026  |  Prototype boundaries documented')
 c.drawRightString(567,28,str(d.page))
path=ROOT/'public/software-design.pdf'
SimpleDocTemplate(str(path),pagesize=(612,792),rightMargin=45,leftMargin=45,topMargin=62,bottomMargin=48,title='Parcel Software Design',author='Parcel project').build(story,onFirstPage=page,onLaterPages=page)
print(path)
