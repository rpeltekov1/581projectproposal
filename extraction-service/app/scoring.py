from .schema import Layout
COUNT_FIELDS=('bedrooms','bathrooms','doors','windows')

def score(prediction:Layout,key:Layout):
    fields=[{'field':k,'expected':getattr(key,k),'actual':getattr(prediction,k),'correct':getattr(prediction,k)==getattr(key,k)} for k in COUNT_FIELDS if getattr(key,k) is not None]
    def relative(a,b):
        if a is None or b is None:return None
        pa=a*(10.76391041671 if prediction.unit=='sqm' else 1)
        kb=b*(10.76391041671 if key.unit=='sqm' else 1)
        return abs(pa-kb)/(kb or 1)
    basis=prediction.area_basis==key.area_basis and key.area_basis!='unknown'
    rooms=[]
    for expected in key.rooms:
        actual=next((r for r in prediction.rooms if r.id==expected.id),None)
        rooms.append({'id':expected.id,'name':expected.name,'matched':actual is not None,'typeCorrect':actual.type==expected.type if actual else False,'areaError':relative(actual.area,expected.area) if actual else None})
    return {'metric_version':'exact-count-relative-area-v1','count_accuracy':sum(f['correct'] for f in fields)/len(fields) if fields else None,'count_fields':fields,'area_basis_match':basis,'total_area_relative_error':relative(prediction.total_area,key.total_area) if basis else None,'room_recall':sum(r['matched'] for r in rooms)/len(rooms) if rooms else None,'room_fields':rooms,'extra_rooms':len([r for r in prediction.rooms if r.id not in {k.id for k in key.rooms}])}
