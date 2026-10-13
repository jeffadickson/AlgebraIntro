"""Audit the built editions, question/key coverage, and generated arithmetic."""
from pathlib import Path
import json,re
from pypdf import PdfReader
r=Path(__file__).resolve().parents[1]/'workbook'
manifest=json.loads((r/'exercise-manifest-200.json').read_text());key=json.loads((r/'answer-key-200.json').read_text())
answers={(p,n):a for chapter in key for p,n,a in chapter};count=0;eq=0
for page in manifest:
 for n,item in enumerate(page['questions'],1):
  assert answers[(page['page'],n)]==item['a'];q=item['q'];a=item['a']
  m=re.fullmatch(r'([0-9x +−]+) = ([0-9x +−]+)',q)
  if m and 'x' in q:
   x=int(re.search(r'x = (\d+)',a)[1])
   def value(s):
    s=re.sub(r'(\d)x',r'\1*x',s).replace('x',str(x)).replace('−','-')
    assert re.fullmatch(r'[0-9 *+\-]+',s)
    return eval(s,{'__builtins__':{}})
   assert value(m[1])==value(m[2]),(q,a);eq+=1
  if 'altogether. Find both counts.' in q:
   nums=list(map(int,re.findall(r'\d+',q)));vals=list(map(int,re.findall(r'\d+',a)))[:2]
   assert sum(vals)==nums[1] and vals[1]-vals[0]==nums[0],(q,a)
  count+=1
assert count==len(answers)==376
color=PdfReader(r/'Algebra_Adventure_200_Color.pdf');mono=PdfReader(r/'Algebra_Adventure_200_Monochrome.pdf')
assert len(color.pages)==len(mono.pages)==200
for n,(a,b) in enumerate(zip(color.pages,mono.pages)):
 ta=a.extract_text();tb=b.extract_text()
 if n==0:ta=ta.replace('color edition','edition');tb=tb.replace('monochrome edition','edition')
 assert ta==tb,(n+1,'edition mismatch')
 for obj in b['/Resources'].get('/XObject',{}).values():
  obj=obj.get_object()
  if obj.get('/Subtype')=='/Image':assert obj['/ColorSpace']=='/DeviceGray'
 for m in re.finditer(r'([\d.]+) ([\d.]+) ([\d.]+) (?:rg|RG)\b',b.get_contents().get_data().decode('latin1')):assert m[1]==m[2]==m[3]
print(f'PASS: two matched 200-page editions; {count} matched exercise/key entries; {eq} generated equations independently checked; neutral monochrome page colors and DeviceGray art.')
