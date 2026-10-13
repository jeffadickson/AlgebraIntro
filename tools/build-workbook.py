"""Build matching 200-page color and monochrome algebra coursebooks.
Python dependencies: workbook/requirements.txt. All math diagrams are vector art.
Generated Pip artwork remains unmodified; monochrome PDF embeds it as DeviceGray.
"""
from pathlib import Path
import json,html,os,sys,argparse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color,white,black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from PIL import Image
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'workbook'))
from content import EXPLAIN,problem
L=json.loads((ROOT/'course/lessons.json').read_text());D=json.loads((ROOT/'workbook/expanded-lessons.json').read_text())
FONT=Path(os.environ.get('ALGEBRA_FONT_DIR','/usr/share/fonts/truetype/dejavu'))
for face,file in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(face,str(FONT/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold')
W,H=612,792;M=48
class Book:
 def __init__(self,mono=False):
  self.mono=mono;self.mode='Monochrome' if mono else 'Color';self.out=ROOT/'workbook'/f'Algebra_Adventure_200_{self.mode}.pdf'
  self.c=canvas.Canvas(str(self.out),pagesize=(W,H),pageCompression=1);self.c.setTitle(f'Algebra Adventure | 200-page {self.mode} Coursebook');self.c.setAuthor('AlgebraIntro')
  self.ink=black if mono else HexColor('#193b40');self.green=black if mono else HexColor('#176b59');self.pale=white if mono else HexColor('#edf5ef');self.line=Color(.68,.68,.68) if mono else HexColor('#bdcec4');self.gold=white if mono else HexColor('#fff1d9')
  self.page=0;self.keys=[[] for _ in L];self.manifest=[];self.bounds=[];self.images={}
  for pose in ['learning','checking']:
   img=Image.open(ROOT/'workbook/art'/f'pip-{pose}-{"mono" if mono else "color"}.png')
   self.images[pose]=ImageReader(img.convert('L') if mono else img)
 def fill(self,color):
  if self.mono:self.c.setFillGray(color.red)
  else:self.c.setFillColor(color)
 def stroke(self,color):
  if self.mono:self.c.setStrokeGray(color.red)
  else:self.c.setStrokeColor(color)
 def text(self,s,x,y,size=11,bold=False,color=None):
  self.fill(color or self.ink);self.c.setFont('Bold' if bold else 'Body',size);self.c.drawString(x,y,s)
 def para(self,s,x,y,width=516,size=11,leading=None,color=None):
  p=Paragraph(s,ParagraphStyle('p',fontName='Body',fontSize=size,leading=leading or size*1.5,textColor=color or self.ink))
  _,h=p.wrap(width,1000);assert y-h>=49,(self.page,'text overflow',s[:80],y,h)
  p.drawOn(self.c,x,y-h);self.bounds.append((self.page,x,y-h,width,h));return y-h
 def start(self,title,section,subtitle='',bookmark=None):
  self.page+=1;self.fill(white);self.c.rect(0,0,W,H,fill=1,stroke=0);self.fill(self.green);self.c.rect(M,H-50,32,4,fill=1,stroke=0)
  self.text(section.upper(),M+42,H-51,9,True,self.green)
  y=self.para('<b>'+html.escape(title)+'</b>',M,H-74,size=25,leading=30)
  if subtitle:y=self.para(html.escape(subtitle),M,y-8,size=10,color=self.green)
  self.stroke(self.line);self.c.setLineWidth(.6);self.c.line(M,42,W-M,42)
  self.text('ALGEBRA ADVENTURE  •  Think · Try · Explain · Check',M,26,8)
  self.text(str(self.page),W-M-20,26,9,True)
  self.c.bookmarkPage('p'+str(self.page))
  if bookmark:self.c.addOutlineEntry(bookmark,'p'+str(self.page),level=0)
  return y-24
 def end(self):self.c.showPage()
 def lines(self,x,y,n=3,width=516,gap=23):
  assert y-(n-1)*gap>=58,(self.page,'writing lines overflow',y,n)
  self.stroke(self.line);self.c.setLineWidth(.6)
  for i in range(n):self.c.line(x,y-i*gap,x+width,y-i*gap)
 def box(self,s,y,height=72,width=516,x=M,size=12):
  self.fill(self.pale);self.stroke(self.line);self.c.roundRect(x,y-height,width,height,10,fill=not self.mono,stroke=1)
  bottom=self.para(s,x+14,y-11,width-28,size=size);assert bottom>=y-height+8,(self.page,'box overflow',s)
  return y-height-18
 def art(self,pose,x,y,w,h):self.c.drawImage(self.images[pose],x,y,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
 def bars(self,y,extra=5,base='C',larger='Adults',smaller='Children'):
  self.text(smaller,M,y-17,10);self.text(larger,M,y-65,10)
  for dy in [0,-48]:
   self.fill(self.pale);self.stroke(self.green);self.c.rect(M+88,y+dy-30,210,32,fill=not self.mono);self.text(base,M+178,y+dy-19,13,True)
  self.fill(self.gold);self.c.rect(M+298,y-78,92,32,fill=not self.mono);self.text('+ '+str(extra),M+325,y-67,13,True)
  self.text('Matching labels mean matching amounts; picture is schematic.',M,y-101,9)
  return y-123
 def dots(self,x,y,n):
  self.stroke(self.green);self.fill(self.pale)
  for i in range(n):self.c.circle(x+(i%5)*17,y-(i//5)*17,5,stroke=1,fill=not self.mono)
 def diagram(self,ch,y):
  if ch in [8,9]:return self.bars(y,2 if ch==8 else 5,base='R' if ch==8 else 'C',larger='Blue' if ch==8 else 'Adults',smaller='Red' if ch==8 else 'Children')
  if ch==0:
   self.dots(M+50,y-30,5);self.dots(M+300,y-30,3);self.dots(M+390,y-30,2);self.text('=',M+235,y-38,24,True);self.text('+',M+368,y-38,20,True)
   self.text('5',M+78,y-85,14,True);self.text('3 + 2',M+325,y-85,14,True);return y-115
  if ch in [5,7]:
   self.stroke(self.green)
   for x in [M+30,M+165]:
    self.fill(self.pale);self.c.roundRect(x,y-72,90,65,12,fill=not self.mono);self.text('x',x+35,y-45,20,True)
   self.text('+',M+136,y-44,20,True)
   if ch==7:self.text('+',M+270,y-44,20,True);self.dots(M+310,y-37,3);self.text('= 11',M+401,y-44,20,True)
   else:self.text('= 8',M+302,y-44,20,True)
   self.text('Each bag holds the SAME count. The bags begin unknown.',M,y-101,10);return y-125
  if ch==11:
   self.dots(M+50,y-28,3);self.dots(M+238,y-28,3);self.dots(M+436,y-28,1)
   self.text('one group',M+45,y-63,10);self.text('matching group',M+226,y-63,10);self.text('left over',M+407,y-63,10)
   self.text('After five extras are removed, seven cannot share equally.',M,y-97,10);return y-125
  labels={1:('6 = 6','add 2 to BOTH','8 = 8'),2:('□ = 3 + 2','rename the box','x = 3 + 2'),3:('2 + x = 3','subtract 2 on BOTH','x = 1'),4:('x − 3 = 4','add 3 to BOTH','x = 7'),6:('x = 3','replace known x','B = 2 + 3'),10:('x + 3 = 8','subtract 3 on BOTH','x = 5')}
  a,b,c=labels[ch];y=self.box('<b>'+a+'</b>   →   '+b+'   →   <b>'+c+'</b>',y,74,size=12);return y
 def qpage(self,ch,items,kind,subtitle,hints=False,columns=False):
  y=self.start(L[ch]['title'],f'Episode {ch+1} • {kind}',subtitle)
  for i,item in enumerate(items):
   if columns:row,col=divmod(i,2);x=M+270*col;top=y-row*174;width=246
   else:x=M;top=y-i*({'3':175,'4':130}.get(str(len(items)),125));width=516
   z=self.para(f'<b>{i+1}.</b> '+html.escape(item['q']),x,top,width,size=11.5)
   if hints:z=self.para('Start: '+html.escape(item.get('hint','Explain what the symbols stand for.')),x,z-7,width,size=9.5,color=self.green)
   self.lines(x,z-22,2 if len(items)==4 or hints else 3,width)
   self.keys[ch].append((self.page,i+1,item['a']))
  self.manifest.append({'page':self.page,'episode':ch+1,'type':kind,'questions':items});self.end()
 def block(self,title,body,y,size=11.5):
  y=self.para('<b>'+html.escape(title)+'</b>',M,y,size=size+1)-6
  return self.para(html.escape(body),M,y,size=size)-18
 def worked(self,ch,title,start,steps,extra):
  y=self.start(title,f'Episode {ch+1} • Worked example','Predict each step. Explain why the new equation still holds.')
  y=self.box('<b>'+html.escape(start)+'</b>',y,68,size=13)
  for n,(eq,why) in enumerate(steps):
   y=self.para(f'<b>{n+1}. {html.escape(eq)}</b>',M,y,size=12.5)-4
   y=self.para(html.escape(why),M+18,y,498,size=10.5)-13
  y=self.para('<b>Why the check matters</b><br/>'+html.escape(extra),M,y-1,size=10.5)-18
  if y>150:self.lines(M,y,2)
  self.end()
 def build(self):
  # Eight front pages, all substantive and included in the page count.
  y=self.start('The same on both sides.','Algebra Adventure',f'200-page {self.mode.lower()} edition • A course to do together',bookmark='Start here')
  self.para('Small steps.<br/><b>Big ideas.</b>',M,y-5,275,size=32,leading=41)
  self.para('Learn to explain equality, uncover mystery numbers, and turn stories into equations.',M,y-111,250,size=13)
  self.art('learning',325,310,239,330)
  self.para('<b>11 core episodes + 1 optional extension</b><br/>Detailed teaching • Worked examples<br/>Hands-on models • Practice • Complete answers',M,320,267,size=11.5)
  self.text('This adventure belongs to:',M,182,12,True);self.lines(M,153,1,360)
  self.text('Self-contained: no internet, device, or special kit required.',M,95,10);self.end()
  y=self.start('How to use this course','Start together')
  for title,body in [('A short session is enough','Try 10–15 minutes as a starting point. A twelve-page episode is not one sitting. Stop after a useful conversation or one practice page; return when attention is fresh.'),('Choose a way to explain','Counters, drawings, speech, and equations all count. Read the words aloud if reading effort hides the mathematics. Use smaller numbers when arithmetic is the obstacle.'),('Follow the teaching before the practice','Each episode opens with a purpose, a concrete model, a close look at the symbols, and two worked examples. Predict a step before uncovering it.'),('Reduce help gradually','Move through repair questions, guided practice, partly completed steps, independent practice, stories, and a checkpoint. A later revisit asks what stayed with you.'),('Check meaning as well as arithmetic','Use the original equation for a numerical check. In two-clue stories, check the total and the difference. The optional final episode asks whether the numbers fit whole-person counts.'),('Use answers as a teaching tool','Answers begin on page 177 and refer to exact page and question numbers. Explanations are examples, not scripts to memorize. Other mathematically correct reasoning is welcome.')]:y=self.block(title,body,y,11)
  self.end()
  y=self.start('Your route through the book','Contents')
  for i,l in enumerate(L):self.text(f'{i+1:02d}  '+l['title'],M,y,11);self.text(str(9+12*i),W-M-24,y,11,True);y-=30
  for title,pn in [('Mixed review: core',153),('Optional detective review',167),('Reference and grown-up support',169),('Answer key: two pages per episode',177)]:self.text(title,M,y-10,11,True);self.text(str(pn),W-M-24,y-10,11,True);y-=31
  self.para('The color and monochrome editions have identical lesson content, exercise numbers, and pagination. The 200-page count includes the cover and answers.',M,y-15,size=10);self.end()
  y=self.start('A conversation before you begin','Readiness without a score')
  for q,a in [('Is 5 = 3 + 2 true? Why?','Yes. Both sides have value five. If the child hesitates at a reversed equality, discuss what equals means before adding new symbols.'),('What belongs in 3 + 4 = □ + 5?','Two. Ask why an answer was chosen. Seven may suggest that equals is being read as “write the answer,” but one numeral alone is not a diagnosis.'),('Put out seven counters and hide three. What can you still see?','Four. Use actual objects if needed. Early algebra does not require fast arithmetic.'),('Before episode 6 only: share eight into two equal groups.','Four in each. This prepares equal groups; it is not an entry gate for equality and simple addition equations.')]:y=self.block(q,a,y,11.5)
  self.para('Write what helped, not how quickly the child answered.',M,y,size=11);self.lines(M,y-43,3);self.end()
  y=self.start('Small toolkit, many possibilities','Set up your workspace')
  for t,b in [('Counters','Use twenty buttons, coins, blocks, or paper circles. Keep all units alike when counting equal amounts. The items are models, not required equipment.'),('Two mats and a cup','Two sheets of paper can represent the two sides of an equation. A cup or folded paper can hide a starting amount. A box symbol or x names the hidden count.'),('Pencil and scrap paper','Draw bars, make a table, or show an operation on each side. Neat handwriting is not evidence of understanding; a spoken explanation can be enough.'),('A bookmark for worked steps','Cover the next step and predict it. Ask “What should the step accomplish?” before asking for the answer.'),('Printing','Both editions use US Letter pages. Print at actual size or fit to your paper. The monochrome edition uses open outlines, dark text, and labeled diagrams; no task depends on color.'),('The offline HTML','The companion HTML contains live activities and solution steps. This book teaches the same core ideas independently; no web page, link, or video is necessary to use it.')]:y=self.block(t,b,y,11)
  self.end()
  y=self.start('A helpful teaching conversation','Grown-up language')
  for t,b in [('Ask what the equation says','“What does each side stand for?” is often more useful than “What is the answer?” Let the child identify the whole quantities before acting.'),('Name the action on both sides','Say “subtract three from both sides because three was added to x.” Avoid “move the three and change its sign,” which hides why the equation remains true.'),('Treat a failed check as evidence','Ask where the values stopped matching. A wrong answer is a starting point for repair, not a reason to speed up or repeat a rule more loudly.'),('Separate help from independence','A child may solve with a hint today and without one later. Both are useful observations. A certain number of correct clicks or worksheet answers does not establish mastery.'),('Allow different routes','A bar model, a table, or an equation may all solve a story. Connect the routes after the child understands one of them. Do not require a picture from a learner who can already explain the symbols.'),('Two planned pause points','Episode 6 separates understanding 2x from dividing to solve it. Episode 10 separates solving with comparison bars from replacing a whole letter with an expression.')]:y=self.block(t,b,y,11)
  self.end()
  y=self.start('How the twelve pages fit together','Inside each episode')
  descriptions=[('1–3: Understand','Meet the idea, model it with objects or a drawing, and read the symbols carefully.'),('4–5: Watch two examples','Each step includes a reason. The second example changes a number, an orientation, or a feature so the idea is not tied to one pattern.'),('6: Explain and repair','Read another learner’s claim. Check it, explain it, or repair the incorrect step.'),('7–8: Practice with fading support','First use a starting hint. Then fill missing pieces of an argument while retaining responsibility for the reasoning.'),('9–11: Apply and check','Try independent questions, connect them to short stories, and attempt a checkpoint. Ask for support whenever necessary.'),('12: Create and revisit','Invent an example, explain a key decision, and return to a fresh question on another day. This makes remembering part of the course.')]
  for t,b in descriptions:y=self.block(t,b,y,12)
  self.end()
  y=self.start('Meet Pip: think, try, explain, check','Your robot companion')
  self.art('checking',M+326,300,190,305)
  for t,b in [('Think','Read the whole equation. What is known? What must be found?'),('Try','Choose one useful action. Preserve equality after the complete action.'),('Explain','Say why the step works. Show it with objects, a picture, or symbols.'),('Check','Test the value in the original equation. In stories, test every clue.')]:
   y=self.para('<b>'+t+'</b><br/>'+b,M,y,290,size=12)-22
  self.para('The robot illustrations are decoration, not counting diagrams. Use the labeled mathematical diagrams for exact quantities. The outline and materials were developed with AI-assisted review; classroom effectiveness has not been established.',M,177,size=10.5);self.end()
  assert self.page==8
  for ch,(l,d) in enumerate(zip(L,D)):
   # 1: deeper introduction, with decorative generated art.
   y=self.start(l['title'],f'Episode {ch+1} • Meet the idea',l['goal'],bookmark=f'{ch+1}. {l["title"]}')
   self.art('checking' if ch in [8,9,10,11] else 'learning',M+333,y-248,183,248)
   z=self.para(l['text'],M,y,309,size=12.5)-19
   z=self.para('<b>By the end</b><br/>'+html.escape(l['goal'])+' You will show a reason and check a fresh example.',M,z,309,size=11.5)
   y=min(z-25,y-273)
   y=self.box('<b>'+html.escape(l['start'])+'</b>',y,72,size=13)
   y=self.para('<b>Keep this idea:</b> '+html.escape(l['note']),M,y,size=11)-20
   self.para('<b>Talk together:</b> '+html.escape(l['ask']),M,y,size=11);self.end()
   # 2: concrete model.
   y=self.start('Build it, then say it',f'Episode {ch+1} • A hands-on model','Use real objects or point to the drawing. The representation is optional.')
   y=self.diagram(ch,y)
   for i,body in enumerate(d['hands']):y=self.para(f'<b>{i+1}.</b> '+html.escape(body),M,y,size=11)-16
   self.end()
   # 3: explicit conceptual explanations.
   y=self.start('What the symbols mean',f'Episode {ch+1} • Look closely','Read the relationship before choosing an operation.')
   for title,body in d['meaning']:y=self.block(title,body,y,12)
   if y>180:self.para('Point to one sentence above and explain it in your own words.',M,y,size=10.5);self.lines(M,y-40,2)
   self.end()
   # 4 and 5: two complete worked examples.
   self.worked(ch,'One step at a time',l['start'],l['steps'],'A successful check returns to the original statement. For a story with two clues, both clues must fit. Describe which amount each symbol represents before checking.')
   self.worked(ch,'The idea in a new example',d['start'],d['worked'],'The numbers or presentation changed, but the reason for each step still matters. Retell one step without reading its explanation. Then point to the original statement that the answer satisfies.')
   # 6–12: varied purposeful practice.
   self.qpage(ch,[{'q':q,'a':a} for q,a in EXPLAIN[ch]],'Explain and repair','Test each claim. Keep what works and repair what does not.')
   self.qpage(ch,[problem(ch,k) for k in range(4)],'Guided practice','Use the starting hint, then explain your own next step.',hints=True)
   self.qpage(ch,d['faded'],'Finish the reasoning','Fill the missing pieces. Read the whole argument afterward.')
   self.qpage(ch,[problem(ch,k) for k in range(4,10)],'Independent practice','Show a useful step and a check. Ask for help if needed.',columns=True)
   self.qpage(ch,d['stories'],'From words to mathematics','Define the count, write the relationship, then check the story.')
   self.qpage(ch,[problem(ch,k) for k in range(10,14)],'Checkpoint','Try first without a hint. An explanation matters as much as an answer.')
   self.qpage(ch,d['revisit'],'Create, explain, revisit','Save question 3 for a later session; note what you remember.')
  assert self.page==152
  # Sixteen mixed pages, the last two explicitly optional.
  for mix in range(16):
   y=self.start('Choose your own method' if mix<14 else 'Optional detective review',f'Mixed review {mix+1}','Show a useful action, explain it, and check the original statement.',bookmark='Mixed review' if mix==0 else None);items=[]
   for i in range(4):
    ch=[0,2,3,4,5,6,7,8,9,10,1][(mix*4+i)%11] if mix<14 else 11
    p=problem(ch,30+mix*4+i);items.append(p);top=y-i*130;z=self.para(f'<b>{i+1}.</b> '+html.escape(p['q']),M,top,size=12);self.lines(M,z-24,2);self.keys[ch].append((self.page,i+1,p['a']))
   self.manifest.append({'page':self.page,'type':'mixed','questions':items});self.end()
  assert self.page==168
  self.references()
  assert self.page==176
  # Two answer pages per episode, split by exercise page, not in mid-question.
  for ch,l in enumerate(L):
   split=9+ch*12+8
   groups=[[entry for entry in self.keys[ch] if entry[0]<=split],[entry for entry in self.keys[ch] if entry[0]>split]]
   for half,entries in enumerate(groups):
    y=self.start(l['title'],f'Answers • Episode {ch+1} • {half+1}/2','Example wording is offered; other correct explanations are welcome.',bookmark='Answer key' if ch==0 and half==0 else None);last=None
    for pn,n,answer in entries:
     if pn!=last:y=self.para('<b>Page '+str(pn)+'</b>',M,y,size=10)-4;last=pn
     y=self.para(str(n)+'. '+html.escape(answer),M+14,y,502,size=9.5,leading=13)-5
    self.end()
  assert self.page==200
  self.c.save();reader=PdfReader(self.out);assert len(reader.pages)==200
  for i,p in enumerate(reader.pages):assert len(p.extract_text())>100,(i+1,'nearly empty page')
  return {'edition':self.mode,'pages':self.page,'numbered_exercises':sum(len(x['questions']) for x in self.manifest),'output':str(self.out)}
 def references(self):
  y=self.start('Words and symbols','Reference • Read algebra',bookmark='Reference pages')
  for term,body in [('Equation','A statement that two expressions have the same value. Example: x + 2 = 5.'),('Expression','A way to name an amount, such as 3 + 2 or 2x + 1. An expression on its own does not make an equality claim.'),('Unknown','A number we want to find. Its letter has one fixed value within the problem.'),('Substitute','Replace a letter with a number or expression that has the same value.'),('Coefficient','The number of copies of an unknown. In 3x, the coefficient 3 means three copies of x.'),('Inverse operation','An undoing action, such as adding three to undo subtracting three.'),('≠','Does not have the same value as. Example: 3 + 2 ≠ 6.'),('Check','Use the found value in the original statement. In a story, test every clue, not only the arithmetic of a reduced equation.')]:y=self.block(term,body,y,10.5)
  self.end()
  y=self.start('Equality-preserving actions','Reference • Both complete sides')
  for t,b in [('Adding and subtracting','If two values match, adding the same number to both or subtracting the same number from both keeps them matched.'),('Multiplying and dividing','For solving, use the same nonzero multiplier or divisor on both sides. Divide every term of a complete side, not only the term containing x.'),('A whole-side example','2x + 4 = 12. Divide BOTH complete sides by two: (2x + 4) ÷ 2 = 12 ÷ 2. The result is x + 2 = 6. The four becomes two as well.'),('A legal move may be inefficient','x + 2 = 5 can become x + 3 = 6 after adding one to both sides. It remains equivalent, but does not uncover x. Subtracting two directly is more useful.'),('A note for grown-ups','Dividing by zero is undefined. Multiplying an equation by zero loses information about its solution. These exceptions belong in discussion when relevant, not at the front of a child’s first equality lesson.'),('Do not turn addition facts into subtraction rules','Reordering 2 + 5 as 5 + 2 preserves the sum. The same general claim does not hold for subtraction. Name the property or action you actually used.')]:y=self.block(t,b,y,11)
  self.end()
  y=self.start('Choose an undoing action','Reference • A decision guide')
  for t,b in [('Something added to x','x + 4 = 9. Subtract four from both sides: x = 5. Check 5 + 4 = 9.'),('Something taken from x','x − 4 = 3. Add four to both sides: x = 7. Check 7 − 4 = 3.'),('Equal copies of x','3x = 12. Divide both sides by three: x = 4. Check 3 × 4 = 12.'),('Equal groups plus extras','2x + 3 = 11. Subtract three: 2x = 8. Divide by two: x = 4. Check 2 × 4 + 3 = 11.'),('A known value in another relation','x = 3 and B = x + 2. Replace x by three: B = 3 + 2 = 5. Keep the known value visible.'),('A story gives total and difference','Translate both clues. Remove the extra amount from the total, share the remainder into two equal parts, then restore the extras to the larger count. Check both clues.')]:y=self.block(t,b,y,11.5)
  self.end()
  y=self.start('One story, two matching routes','Reference • Bars and equations')
  y=self.para('Five more adults than children. Thirteen people total. A is the adult count; C is the child count.',M,y,size=12)-19;y=self.bars(y)
  y=self.para('<b>Picture route</b><br/>Remove five extras from thirteen, leaving eight. Share eight between the two matching parts: four each. Children: four. Adults: four plus five, or nine.',M,y,size=12)-20
  y=self.para('<b>Equation route</b><br/>A = C + 5 and A + C = 13.<br/>Replace A: (C + 5) + C = 13.<br/>Combine: 2C + 5 = 13.<br/>Subtract five: 2C = 8. Divide by two: C = 4.<br/>Return to the comparison: A = 4 + 5 = 9.',M,y,size=12)-20
  self.box('<b>Both clues:</b> 4 + 9 = 13 and 9 − 4 = 5.',y,60);self.end()
  y=self.start('Repair common mistakes','Reference • What to ask next')
  for t,b in [('“The equals sign means the answer comes next.”','Try 7 = 5 + 2. Ask for the value of each side, then reverse the sides. The relationship compares equal amounts.'),('“The box must contain the left-side total.”','For 3 + 4 = □ + 5, show that the whole right side includes five already. The box is only the missing part.'),('“Always subtract the visible number.”','Compare x + 3 = 8 with x − 3 = 8. Name the action on x before choosing its inverse.'),('“2x is x + 2.”','At x = 3, draw two groups of three, then draw three plus two. The totals six and five differ.'),('“One correct story check is enough.”','Five children and eight adults give total thirteen but difference three. Return to BOTH original clues.'),('“Different letters must mean different values.”','Use x = 4 and B = x + 0. Both values are four; their names alone do not force a difference.')]:y=self.block(t,b,y,11)
  self.end()
  y=self.start('Observe growth without pressure','Reference • What the evidence means')
  for t,b in [('Explored','The learner encountered the idea, discussed an example, or tried a model. This is a start, not a score.'),('Practiced with help','A hint, revealed step, or another person’s explanation supported the solution. Record what kind of help was useful.'),('Shown independently','The learner solved a fresh example and explained or checked it without a prompt. One observation still does not prove all related skills are secure.'),('Revisited','The learner returned on another day. Notice whether the idea was retained and what support was needed this time.'),('Before the two-clue story','Look for known-number substitution, interpreting a comparison, understanding C + C = 2C, and solving a fresh two-step equation. Replacing a whole letter by an expression is taught during the story episode.'),('Scope of the course','The later topics are equations with variables on both sides, negative or fractional solutions, unknown subtrahends and divisors, general distribution, and formal elimination. They are not prerequisites here.')]:y=self.block(t,b,y,11)
  self.end()
  y=self.start('Your observation record','Reference • Use over several sessions')
  y=self.para('Write the date, episode, what the learner explained, and one next step. Compare today with the learner’s own earlier work, not with another child’s speed.',M,y,size=11)-24
  for i in range(5):
   self.text('Date / episode / observation / next helpful step',M,y,10,True);self.lines(M,y-25,2);y-=91
  self.end()
  y=self.start('Make your own practice','Reference • Build a solvable example')
  for t,b in [('Choose an answer first','To make an addition equation with x = 4, add three to get seven: x + 3 = 7. The intended answer lets you check that your invented question works.'),('Make equal groups','Choose x = 5 and three groups. Their total is fifteen, so 3x = 15. Add two extras to make 3x + 2 = 17.'),('Build a two-clue story','Choose smaller count four and larger count nine. Their difference is five and total thirteen. State these two clues without giving the counts.'),('Vary the presentation','Reverse the two sides of an equality, move x between addends, use zero as an answer, or change the context. Keep the underlying relationship correct.'),('Do not accidentally change the topic','Unknowns being subtracted from a known total, such as 8 − x = 3, introduce a new structure. Save those for a later course rather than quietly mixing them into early practice.'),('Art and edition notes','Pip’s learning and checking illustrations were generated with the built-in image tool in matching color and black-outline versions. Exact mathematical diagrams are programmatically drawn. This course was developed with AI assistance and is not a validated assessment.')]:y=self.block(t,b,y,11)
  self.end()

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--edition',choices=['color','mono','both'],default='both');args=parser.parse_args()
 books=[]
 for mode in ([False,True] if args.edition=='both' else [args.edition=='mono']):
  b=Book(mode);result=b.build();books.append(b);print(json.dumps(result))
 if len(books)==2:
  assert books[0].manifest==books[1].manifest
  assert books[0].keys==books[1].keys
  readers=[PdfReader(b.out) for b in books]
  for n,(a,b) in enumerate(zip(*[r.pages for r in readers])):
   ta=a.extract_text();tb=b.extract_text()
   if n==0:ta=ta.replace('color edition','edition');tb=tb.replace('monochrome edition','edition')
   assert ta==tb,(n+1,'edition text mismatch')
 last=books[-1]
 (ROOT/'workbook/exercise-manifest-200.json').write_text(json.dumps(last.manifest,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'workbook/answer-key-200.json').write_text(json.dumps(last.keys,ensure_ascii=False,indent=2)+'\n')
 print('PASS: exact 200-page count, matching edition content, page bounds, and nonempty text on every page.')
