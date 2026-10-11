import json
from pathlib import Path
def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0
from systems.multimodal_ocr.app import extract_fields

def evaluate():
 cases=json.loads((Path(__file__).parent/'eval'/'cases.json').read_text()); scores=[]
 for c in cases:
  got=extract_fields(c['lines']); gold=c['gold']; scores.append(sum(got[k]==v for k,v in gold.items())/len(gold))
 return {'documents':len(cases),'field_exact_match':mean(scores),'scope':'synthetic OCR line records; OCR engine itself is not evaluated'}
if __name__=='__main__': print(json.dumps(evaluate(),indent=2))
