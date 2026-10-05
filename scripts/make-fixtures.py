from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import hashlib,json
root=Path(__file__).resolve().parents[1]
rooms=[('r1','living','Living room',280),('r2','kitchen','Kitchen',160),('r3','bedroom','Bedroom 1',180),('r4','bedroom','Bedroom 2',160),('r5','bathroom','Bathroom',80),('r6','hall','Hall',100)]
key=dict(unit='sqft',area_basis='internal',total_area=960,bedrooms=2,bathrooms=1,doors=7,windows=6,rooms=[dict(id=i,type=t,name=n,area=a) for i,t,n,a in rooms],warnings=[])
folder=root/'extraction-service/fixtures'
(folder/'answer-key.json').write_text(json.dumps(key,indent=2))
for tier in ['tagged','labelled','bare']:
 p=folder/f'{tier}.pdf';c=canvas.Canvas(str(p),pagesize=(612,792));c.setTitle('Parcel synthetic floor plan - '+tier)
 c.setFillColor(HexColor('#176951'));c.setFont('Helvetica-Bold',20);c.drawString(42,747,'PARCEL / Synthetic test fixture')
 c.setFont('Helvetica',10);c.setFillColor(HexColor('#607565'));c.drawString(42,724,f'{tier.title()} tier - schematic, not to scale. Not a Gridsnap export.')
 # Exact diagram geometry is deliberately schematic; labelled areas are authoritative.
 c.setLineWidth(2);c.setStrokeColor(HexColor('#213e2e'))
 for i,(rid,typ,name,area) in enumerate(rooms):
  x=60+(i%2)*245;y=560-(i//2)*105;c.rect(x,y,245,105)
  if tier!='bare':
   c.setFillColor(HexColor('#213e2e'));c.setFont('Helvetica-Bold',12);c.drawString(x+17,y+62,(rid+' / ' if tier=='tagged' else '')+name);c.setFont('Helvetica',10);c.drawString(x+17,y+44,f'{area} sq ft')
  # One opening symbol on the exterior vertical wall of each room = six windows.
  wx=x if i%2==0 else x+245;c.setStrokeColor(HexColor('#47a181'));c.setLineWidth(5);c.line(wx,y+30,wx,y+58);c.setStrokeColor(HexColor('#213e2e'));c.setLineWidth(2)
 # Seven schematic door symbols, each with a leaf and swing arc.
 for x,y in [(112,560),(357,560),(112,455),(357,455),(112,350),(357,350),(500,350)]:
  c.setStrokeColor(HexColor('#ffffff'));c.setLineWidth(4);c.line(x,y,x+20,y);c.setStrokeColor(HexColor('#213e2e'));c.setLineWidth(1);c.line(x,y,x,y+20);c.arc(x-20,y-20,x+20,y+20,0,90)
 c.setFont('Helvetica',9);c.setFillColor(HexColor('#607565'));c.drawString(60,327,'Green marks: windows. Quarter-circle marks: doors. All areas are internal.')
 if tier=='tagged':
  lines=['UNIT: sqft','AREA_BASIS: internal','TOTAL_AREA: 960','BEDROOMS: 2','BATHROOMS: 1','DOORS: 7','WINDOWS: 6']+[f'ROOM {rid} | {typ} | {name} | {area}' for rid,typ,name,area in rooms]
  c.setFont('Courier',9)
  for j,line in enumerate(lines):c.drawString(60,300-j*15,line)
 elif tier=='labelled':
  c.setFont('Helvetica',11);c.drawString(60,295,'Declared internal area: 960 sq ft. Interpret room and opening symbols.')
 else:
  c.setFont('Helvetica',11);c.drawString(60,295,'No room labels or area scale supplied. Areas and room functions may be unknown.')
 c.setFont('Helvetica',8);c.drawString(42,35,'Fixture only. Geometric dimensions are not a measurement source.');c.showPage();c.save()
(root/'public/fixtures/demo-plan.pdf').write_bytes((folder/'tagged.pdf').read_bytes())
(root/'public/fixtures/answer-key.json').write_bytes((folder/'answer-key.json').read_bytes())
# Bare truth retains the drawing's design inventory to measure abstention/coverage, not to imply observability.
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'test_set_id':'parcel-synthetic-smoke-v1','synthetic':True,'notes':'Smoke tests, not a Gridsnap benchmark. Three tiers share one layout; never split these across train/test. Bare room types/areas are intentionally unobservable.','cases':[{'id':t+'-01','tier':t,'file':t+'.pdf','sha256':sha(folder/(t+'.pdf')),'answer_key':'answer-key.json','key_sha256':sha(folder/'answer-key.json')} for t in ['tagged','labelled','bare']]}
(folder/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Created three synthetic fixtures, fixed manifest, and answer key.')
