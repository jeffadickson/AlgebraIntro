"""Reproducible 100-page workbook. Run with Python + reportlab + pypdf."""
from pathlib import Path
import json, random, html
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'workbook/Algebra_Adventure_Workbook.pdf'
FONT=Path('/usr/share/fonts/truetype/dejavu')
# Set ALGEBRA_FONT_DIR on systems where DejaVu is installed elsewhere.
import os
FONT=Path(os.environ.get('ALGEBRA_FONT_DIR',str(FONT)))
pdfmetrics.registerFont(TTFont('Body',str(FONT/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('Bold',str(FONT/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold')
L=json.loads((ROOT/'course/lessons.json').read_text())
W,H=612,792; M=48; INK=HexColor('#193b40'); GREEN=HexColor('#176b59'); PALE=HexColor('#edf5ef'); LINE=HexColor('#cbd8d1'); GOLD=HexColor('#edb65b')
C=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
C.setTitle('Algebra Adventure | The Same on Both Sides | 100-page workbook')
C.setAuthor('AlgebraIntro')
PAGE=0; KEYS=[[] for _ in L]; MANIFEST=[]
def text(s,x,y,size=11,font='Body',color=INK):
 C.setFillColor(color);C.setFont(font,size);C.drawString(x,y,s)
def para(s,x,y,width=516,size=11,leading=None,color=INK):
 p=Paragraph(s,ParagraphStyle('p',fontName='Body',fontSize=size,leading=leading or size*1.5,textColor=color,spaceAfter=0))
 _,h=p.wrap(width,1000)
 assert y-h>=42,(PAGE,'overflow',s[:70],y,h)
 p.drawOn(C,x,y-h);return y-h

def robot(x,y,scale=1):
 C.saveState();C.translate(x,y);C.scale(scale,scale);C.setStrokeColor(INK);C.setLineWidth(2)
 C.setFillColor(PALE);C.roundRect(8,18,44,35,9,fill=1);C.setFillColor(white);C.roundRect(0,50,60,36,10,fill=1)
 C.setFillColor(INK);C.roundRect(7,61,46,18,6,fill=1);C.setFillColor(PALE);C.circle(19,70,3,fill=1,stroke=0);C.circle(41,70,3,fill=1,stroke=0)
 C.line(23,65,37,65);C.line(30,86,30,95);C.setFillColor(GOLD);C.circle(30,98,4,fill=1)
 C.line(21,40,39,40);C.line(21,32,39,32);C.line(8,44,-3,29);C.line(52,44,67,59);C.line(20,18,20,7);C.line(40,18,40,7);C.restoreState()

def page(title,section,subtitle=''):
 global PAGE
 PAGE+=1;C.setFillColor(white);C.rect(0,0,W,H,fill=1,stroke=0)
 C.setFillColor(GREEN);C.rect(M,H-50,32,4,fill=1,stroke=0)
 text(section.upper(),M+42,H-51,9,'Bold',GREEN)
 y=para('<b>'+html.escape(title)+'</b>',M,H-75,size=25,leading=30)
 if subtitle:y=para(html.escape(subtitle),M,y-9,size=10,color=GREEN)
 C.setStrokeColor(LINE);C.line(M,42,W-M,42)
 text('ALGEBRA ADVENTURE  •  Think · Try · Explain · Check',M,26,8)
 C.setFont('Bold',9);C.drawRightString(W-M,26,str(PAGE))
 C.bookmarkPage('p'+str(PAGE))
 return y-24

def end():C.showPage()
def lines(x,y,n=3,width=516,gap=23):
 C.setStrokeColor(LINE);C.setLineWidth(.6)
 for i in range(n):C.line(x,y-i*gap,x+width,y-i*gap)
 return y-n*gap

def box(s,y,height=70):
 C.setFillColor(PALE);C.roundRect(M,y-height,516,height,12,fill=1,stroke=0)
 para(s,M+16,y-12,484,size=12);return y-height-18

def equation(s,y):
 return box('<b>'+html.escape(s)+'</b>',y,58)

def bars(y,extra=5,base='C = ?',larger='Adults',smaller='Children'):
 text(smaller,M,y-17,10);text(larger,M,y-65,10)
 for dy in [0,-48]:
  C.setFillColor(PALE);C.setStrokeColor(GREEN);C.rect(M+85,y+dy-30,210,32,fill=1);text(base,M+150,y+dy-18,13,'Bold')
 C.setFillColor(HexColor('#fff1d9'));C.rect(M+295,y-78,95,32,fill=1);text('+ '+str(extra),M+325,y-66,13,'Bold')
 return y-108

# Explicit reasoning questions: answers are examples, not mandated wording.
EXPLAIN=[
 [('Milo says the equals sign means “write the answer next.” Use 7 = 5 + 2 to help him.', 'It means same value. The left is 7 and the right is 7, even with the sum after the sign.'),('Is 3 + 2 = 4 + 1 true? Explain without changing either side.','Yes. Each side has value 5.'),('Someone puts 7 in 3 + 4 = □ + 5. Explain the mistake and repair it.','The left is 7, but 7 + 5 is 12. Put 2 in the box so the right is 7.')],
 [('From 6 = 6, subtract 1 on the left and 2 on the right. What happens?','You get 5 and 4. Equality is broken because the amounts removed differ.'),('Starting from 8 = 8, the left becomes 10. Repair the right.','Add 2 to the right too: 10 = 10.'),('Does adding 1 to BOTH sides of x + 2 = 5 preserve equality? Does it uncover x?','Yes, it gives x + 3 = 6, an equivalent equation. It does not leave x alone.')],
 [('What does x mean in x = 3 + 2? Is it a multiplication sign?','x names the number 5 in this problem. The multiplication sign is ×.'),('Test x = 1 in 2 + x = 3. What do you replace?','Replace x with 1. Then 2 + 1 = 3, so the check works.'),('One problem has x = 5 and a new problem has x = 2. Is that allowed?','Yes. x keeps one value within a problem; a new problem can use another value.')],
 [('Are x + 2 = 3 and 3 = x + 2 asking for the same x? Explain.','Yes. Reversing the two sides keeps the equality true. Both give x = 1.'),('Why is x = 0 a valid answer to 2 + x = 2?','Because 2 + 0 = 2. Zero adds nothing and both sides match.'),('A friend solves x + 3 = 8 as x = 11. Check and repair the answer.','11 + 3 = 14, not 8. Subtract 3 from both sides to get x = 5.')],
 [('Why add 3 to BOTH sides of x − 3 = 4?','It undoes subtracting 3 on the left and preserves equality. x = 7.'),('A bag loses 2 counters and has 5 left. Is the starting count more or less than 5?','More. It started with 7 because 7 − 2 = 5.'),('A friend subtracts 3 from 4 and says x = 1 in x − 3 = 4. Repair the method.','Undo taking away by adding 3 to BOTH sides. x = 7; check 7 − 3 = 4. Taking 3 away from 1 cannot leave 4.')],
 [('At x = 3, compare 2x and x + 2.','2x = 6. x + 2 = 5. Two copies of x are not the same as adding two.'),('Two bags look the same. May we assume their counter counts are equal?','No. We need information that the contents have equal counts, not just equal-looking bags.'),('Explain 3x = 12 using counters or a drawing.','Three equal groups total 12. Share 12 into three groups of 4, so x = 4.')],
 [('In x = 4 and B = x + 3, which is known and which must be found?','x is known to be 4; B is the new unknown. B = 7.'),('Does B = x + 3 by itself choose one pair? Give two pairs.','No. For example x = 1, B = 4 and x = 2, B = 5 both work.'),('Could different letters name equal numbers? Use x = 4 and B = x + 0.','Yes. B = 4 and x = 4. Different names do not require different values.')],
 [('Why remove the 3 in 2x + 3 = 11 before sharing into two groups?','The 3 loose counters are not part of the two equal groups. Removing them leaves 8 to share.'),('Someone divides 2x + 4 = 12 by 2 and writes x + 4 = 6. Repair the step.','Divide the WHOLE side: (2x + 4) ÷ 2 = 12 ÷ 2 gives x + 2 = 6.'),('Check x = 4 in 3x + 2 = 14.','3 × 4 + 2 = 12 + 2 = 14. It works.')],
 [('There are 2 more blue beads than red. Repair R = B + 2.','B = R + 2. Blue is the larger count, so add the extras to red.'),('Five more adults than children: is A = C + 5 enough to find just one pair?','No. C = 3, A = 8 and C = 4, A = 9 both fit. A total would provide another clue.'),('In A = C + 5, what do A and C stand for?','A is the number of adults and C is the number of children. The letters represent counts.')],
 [('Why replace A by the WHOLE expression (C + 5) in A + C = 13?','Because A and C + 5 are equal counts. Replacing all of A gives (C + 5) + C = 13.'),('A child proposes 5 children and 8 adults for total 13, difference 5. Check both clues.','The total is 13, but the difference is 3. The correct counts are 4 children and 9 adults.'),('Why does the bar picture have two C-sized parts? Are both groups children?','One is the child count; the other is an equal number of adults. Two equal amounts remain after the extras.')],
 [('Choose a first move for x + 4 = 9 and for x − 4 = 3. Why do they differ?','Subtract 4 in the first; add 4 in the second. Each undoes the operation on x.'),('A friend gets x = 5 from 2x = 10. Show a check, not just a repeat of the answer.','Replace x: 2 × 5 = 10. Both sides match.'),('Explain a useful first move for 2x + 1 = 9, then finish.','Subtract 1 from both sides: 2x = 8. Divide both sides by 2: x = 4. Check 2 × 4 + 1 = 9.')],
 [('Five extras and twelve people: what remains after removing the extras? Can it share equally?','Seven remain. Two equal whole-number groups leave one over, so no whole-person solution.'),('Four extras and twelve people: find both counts and check.','4 children and 8 adults. Total 12 and difference 4.'),('Could 3.5 be an amount of juice but not a count of whole children? Explain.','Yes. We can measure 3.5 cups of juice, but not count 3.5 whole children in the room.')]
]

def problem(ch,k):
 """Each generated answer is verified by substituting into its defining relation."""
 x=(k*3+ch)%10;a=2+k%3;b=1+(k*2+ch)%6
 if ch==10:return problem([3,4,5,7,0,8,9][k%7],k+11)
 if ch==0:
  total=a+b; c=1+k%total
  if k%3==0:q=f'{a} + {b} = □ + {c}';v=total-c;ans=f'□ = {v}; both sides are {total}.';assert a+b==v+c
  elif k%3==1:q=f'Is {total} = {a} + {b} true? Explain.';ans=f'Yes. Both sides are {total}.'
  else:q=f'Is {a} + {b} = {total+1} true? Repair the right side.';ans=f'No. The left is {total}; replace {total+1} with {total}.'
  hint='Work out each side separately.'
 elif ch==1:
  start=x+b;add=k%2==0;v=start+b if add else start-b;assert v==(start+b if add else start-b)
  q=f'Start with {start} = {start}. {"Add" if add else "Subtract"} {b} on BOTH sides. Write the new equality.';ans=f'{v} = {v}.';hint='Use the same operation and amount twice.'
 elif ch==2:
  v=a+b;q=f'{"□" if k%2==0 else "x"} = {a} + {b}. Find the missing number and check.';ans=f'{v}; check {v} = {a} + {b}.';hint='Find the value of the whole sum.';assert v==a+b
 elif ch in [3,4,5,7]:
  coef=a if ch in [5,7] else 1;constant=-b if ch==4 else 0 if ch==5 else b
  if ch==4:x+=b
  total=coef*x+constant;expr=('x' if coef==1 else str(coef)+'x')+(' + '+str(constant) if constant>0 else ' − '+str(-constant) if constant<0 else '')
  q=f'{total} = {expr}' if ch==3 and k%3==0 else f'{b} + x = {total}' if ch==3 and k%3==1 else f'{expr} = {total}'
  ans=f'x = {x}; check {coef} × {x} {"− "+str(-constant) if constant<0 else "+ "+str(constant)} = {total}.'
  hint=f'{"Add "+str(-constant) if constant<0 else "Subtract "+str(constant) if constant>0 else "Divide by "+str(coef)} on both sides.'
  assert coef*x+constant==total
 elif ch==6:
  q=f'Known: x = {x}. Find B when B = x + {b}.';ans=f'B = {x+b}; replace x: {x} + {b} = {x+b}.';hint='Write the known number in place of x.'
 elif ch==8:
  if k%2:q=f'Blue has {b} more beads than red. Write a relation using B and R.';ans=f'B = R + {b}. Blue is the larger count.'
  else:q=f'Blue has {b} more beads than red. There are {x} red. Find blue and write the relation.';ans=f'B = R + {b}; B = {x+b}.'
  hint='Start with the smaller count, then add the extras.'
 elif ch==9:
  larger,smaller,place=[('blue beads','red beads','a box'),('adults','children','a room'),('long sticks','short sticks','a rack')][k%3]
  total=2*x+b;q=f'In {place}, there are {b} more {larger} than {smaller}. There are {total} altogether. Find both counts.'
  ans=f'{smaller}: {x}; {larger}: {x+b}. Checks: {x} + {x+b} = {total}; {x+b} − {x} = {b}.';hint=f'Remove {b} extras from {total}, then share equally.';assert x+(x+b)==total and (x+b)-x==b
 elif ch==11:
  total=2*x+b+k%2;remain=total-b;possible=remain%2==0;q=f'{total} people, with {b} more adults than children. Is a whole-person answer possible? Explain.'
  ans=f'Yes: {remain//2} children, {remain//2+b} adults; total {total}, difference {b}.' if possible else f'No. Removing {b} leaves the odd number {remain}, which cannot share into two equal whole-number counts.';hint='Remove the extras; test whether the rest shares equally.'
 return {'q':q,'a':ans,'hint':hint}

def questions(ch,items,kind,subtitle):
 y=page(L[ch]['title'],f'Episode {ch+1} • {kind}',subtitle);pageno=PAGE
 if kind=='Independent practice':
  for i,item in enumerate(items):
   row,col=divmod(i,2);x=M+col*270;top=y-row*173
   z=para(f'<b>{i+1}.</b> '+html.escape(item['q']),x,top,246,size=12)
   lines(x,z-24,3,246)
   KEYS[ch].append((pageno,i+1,item['a']))
 else:
  gap=132 if len(items)==4 else 178
  for i,item in enumerate(items):
   top=y-i*gap;z=para(f'<b>{i+1}.</b> '+html.escape(item['q']),M,top,size=12)
   if kind=='Guided practice':z=para('Start: '+html.escape(item['hint']),M,z-7,size=10,color=GREEN)
   lines(M,z-24,2 if len(items)==4 else 3)
   KEYS[ch].append((pageno,i+1,item['a']))
 MANIFEST.append({'page':pageno,'episode':ch+1,'type':kind,'questions':items})
 end()

# Front matter: four useful pages, counted in the exact 100-page total.
y=page('The same on both sides.','Algebra Adventure','A self-contained course and workbook • Ages around 9')
y=para('Small steps.<br/><b>Big ideas.</b>',M,y-18,size=34,leading=43)
y=para('Learn to explain equality, uncover a mystery number, and turn a story into equations.',M,y-24,350,size=15)
robot(449,535,1.0)
y=equation('2 + x = 3     →     x = 1',y-32)
y=para('<b>11 core episodes + 1 optional extension</b><br/>Teaching explanations • Worked examples • Space to think<br/>Mixed practice • Reference pages • Full answer key',M,y-12,size=12)
text('This adventure belongs to:',M,181,12,'Bold');lines(M,152,1,340)
text('No internet, device, or special equipment required.',M,96,10)
end()
y=page('A course to do together','Start here')
for title,body in [('Use short sessions','Try 10–15 minutes, then stop when attention fades. An episode may take several sessions. This is a sequence of ideas, not a race or a daily timetable.'),('Choose your way to think','Use counters, draw a picture, talk aloud, or write equations. Read questions aloud when needed. A learner who can explain with symbols does not have to draw every picture.'),('Use the six-page rhythm','Each episode has a teaching page, worked example, guided practice, independent practice, reasoning page, and checkpoint. Cover hints when ready. Use the answer key after a real attempt.'),('Watch the evidence','Record explored, practiced with help, shown independently, or revisited. A correct answer alone does not show understanding. Ask for an explanation and check a fresh example later.'),('Pause at two bridges','In episode 6, explain 2x before solving by division. In episode 10, solve with bars first if helpful, then connect the bars to replacing A with (C + 5). Episode 12 is optional.'),('Keep it kind and precise','Ask “What did you try?” Say “subtract two from both sides,” not “move the two.” These materials reflect an AI-assisted design review, not classroom validation or a human teacher endorsement.')]:
 y=para('<b>'+title+'</b><br/>'+body,M,y,size=11)-18
end()
y=page('Your route through the book','Contents')
for i,l in enumerate(L):
 text(f'{i+1:02d}',M,y,11,'Bold',GREEN);text(l['title'],M+36,y,11);C.setFont('Body',11);C.drawRightString(W-M,y,str(5+6*i));y-=29
for title,pn in [('Mixed practice (core)',77),('Optional detective mix',84),('Reference and grown-up notes',85),('Answer key by episode',89)]:
 text(title,M,y-10,11,'Bold');C.drawRightString(W-M,y-10,str(pn));y-=29
para('All 100 pages are included in this count. Every numbered exercise has an answer or an example explanation in the key. Different correct explanations are welcome.',M,y-17,size=10)
end()
y=page('Before you begin','A conversation, not an exam')
for q,a in [('Is 5 = 3 + 2 true? Why?','Both sides have value five. Reversing the sides is allowed.'),('What belongs in 3 + 4 = □ + 5?','Two. Ask the child why; seven may mean the equals sign is being read as an answer cue.'),('Put out seven counters. Hide three. How many can you see?','Four. Use real objects if the arithmetic gets in the way.'),('Before episode 6: share eight counters into two equal groups.','Four in each group. This is preparation for sharing, not an entry gate for the early lessons.')]:
 y=para('<b>'+q+'</b>',M,y,size=13)-8;y=para('Grown-up note: '+a,M,y,size=10)-20
para('Notice what helps: counters, a smaller number, reading aloud, or another example. Write observations, not a score.',M,y,size=11);lines(M,y-65,4)
end()

for ch,l in enumerate(L):
 # Teaching page.
 y=page(l['title'],f'Episode {ch+1} • Learn',l['goal'])
 y=para(l['text'],M,y,size=13)-22;y=equation(l['start'],y)
 if ch in [8,9]:y=bars(y,5)
 elif ch==5:
  y=box('<b>x + x = 2 × x = 2x</b><br/>Two copies of the SAME number.',y,86)
 elif ch==7:y=box('<b>Two equal bags + three loose counters</b><br/>Remove the loose counters before sharing the rest.',y,86)
 elif ch==0:y=box('<b>5 = 3 + 2</b> and <b>3 + 2 = 5</b><br/>Both promise the same value on each side.',y,86)
 y=para('<b>Keep this idea:</b> '+l['note'],M,y,size=11)-20
 y=para('<b>Talk together:</b> '+l['ask'],M,y,size=12)-25
 if y>145:lines(M,y,3)
 end()
 # Fully worked teaching page with all required steps.
 y=page('Watch the reasoning',f'Episode {ch+1} • Worked example','Cover the next step. Predict it before you read it.')
 for n,(eq,why) in enumerate(l['steps']):
  y=para(f'<b>{n+1}. {html.escape(eq)}</b>',M,y,size=13)-4
  y=para(html.escape(why),M+18,y,498,size=10.5)-15
 y=para('<b>One more example</b><br/>'+html.escape(l['check']['q']),M,y-3,size=11)-8
 y=para('<b>Answer:</b> '+html.escape(', '.join(map(str,l['check']['answers'])))+'. '+html.escape(l['check']['hint']),M,y,size=11)-14
 if y>180:
  y=para('Retell a step in your own words or sketch what changed.',M,y,size=11)-25;lines(M,y,2)
 end()
 questions(ch,[problem(ch,k) for k in range(4)],'Guided practice','A starting hint is provided. Explain why it helps.')
 questions(ch,[problem(ch,k) for k in range(4,10)],'Independent practice','Show a useful step, then check. Ask for help whenever you need it.')
 questions(ch,[{'q':q,'a':a,'hint':''} for q,a in EXPLAIN[ch]],'Explain and repair','Words, pictures, counters, and spoken explanations all count.')
 questions(ch,[problem(ch,k) for k in range(10,14)],'Checkpoint','Try without hints first. Return later with different numbers.')

# Eight mixed pages: seven core-only, one explicitly optional.
for mix in range(8):
 y=page('Choose your own method' if mix<7 else 'Optional detective mix','Mixed practice '+str(mix+1),'Name a useful action. Check the equation or BOTH story clues.')
 items=[]
 for i in range(6):
  ch=([0,2,3,4,5,6,7,8,9,10,1][(mix*6+i)%11] if mix<7 else 11)
  p=problem(ch,30+mix*6+i);items.append(p);top=y-i*86
  z=para(f'<b>{i+1}.</b> '+html.escape(p['q']),M,top,size=11)
  lines(M,z-17,1);KEYS[ch].append((PAGE,i+1,p['a']))
 MANIFEST.append({'page':PAGE,'type':'mixed','questions':items});end()

# Four reference pages.
y=page('Your algebra toolkit','Reference • Words and symbols')
for term,meaning,example in [('Equality','Both sides have the same value.','5 = 3 + 2'),('Unknown','A number we are trying to find.','x + 2 = 5'),('Substitute','Replace a letter by an equal number or expression.','x = 3; B = x + 2 → B = 3 + 2'),('Inverse operation','An operation that undoes another.','Add 3 to undo subtracting 3.'),('Coefficient','How many copies of the unknown are being added.','3x means x + x + x.'),('Check','Replace the unknown in the original equation.','For x = 4 in 2x + 1 = 9: 2 × 4 + 1 = 9.'),('Comparison','A statement about how two amounts differ.','B = R + 2 says blue has two more.'),('≠','Does not have the same value as.','3 + 2 ≠ 6')]:
 y=para('<b>'+term+'</b> — '+meaning+'<br/><font color="#176b59">'+example+'</font>',M,y,size=11)-16
end()
y=page('A method you can explain','Reference • Solving')
for title,body in [('1. Read the equation','What happened to x? Was something added, taken away, or multiplied?'),('2. Choose a useful undoing action','x + 3 = 8: subtract 3 from both sides.<br/>x − 3 = 4: add 3 to both sides.<br/>2x = 8: divide both sides by 2.'),('3. Undo two actions when needed','2x + 3 = 11 → 2x = 8 → x = 4.<br/>First remove the extra three; then share eight into two equal groups.'),('4. Keep the whole side together','Dividing 2x + 4 = 12 by two gives x + 2 = 6.<br/>Every term is divided, including the four.'),('5. Check where you started','Put the value into the original equation: 2 × 4 + 3 = 11. A number that fails this check cannot be the solution.'),('A legal move versus a useful move','Adding one to both sides of x + 2 = 5 gives x + 3 = 6. Equality is preserved, but x is not alone. Prefer the action that uncovers x.')]:
 y=para('<b>'+title+'</b><br/>'+body,M,y,size=12)-20
end()
y=page('From a story to two clues','Reference • Comparison bars')
y=para('Five more adults than children. Thirteen people altogether. Let A be the adult count and C the child count.',M,y,size=12)-20
y=bars(y)
y=para('<b>Comparison:</b> A = C + 5<br/><b>Total:</b> A + C = 13<br/><b>Replace A:</b> (C + 5) + C = 13<br/><b>Combine equal amounts:</b> 2C + 5 = 13<br/><b>Remove extras:</b> 2C = 8<br/><b>Share:</b> C = 4<br/><b>Return to the comparison:</b> A = 9',M,y,size=13,leading=27)-20
y=box('<b>Check BOTH clues</b><br/>9 + 4 = 13 and 9 − 4 = 5.',y,82)
para('The matching bar in the adult row represents an adult count equal to the child count. It is not a second actual group of children.',M,y,size=11)
end()
y=page('Notice progress, then revisit','Reference • Grown-up record')
y=para('Use these observations after hearing an explanation and checking a fresh example. They are not a validated assessment scale. The optional detective does not determine completion.',M,y,size=11)-20
for term,body in [('Explored','Met the idea; tried examples or discussed a picture.'),('Practiced with help','Used hints, a worked step, counters with guidance, or another person’s explanation.'),('Shown independently','Solved a fresh example and explained or checked it without a prompt.'),('Revisited','Returned later and showed which parts were remembered.')]:
 y=para('<b>'+term+':</b> '+body,M,y,size=11)-13
text('Date / episode / observation / next helpful step',M,y-10,10,'Bold');lines(M,y-39,7,gap=28)
para('Later topics: negative and fractional solutions, unknowns on both sides, unknown subtrahends, and formal elimination. They are not prerequisites for this course.',M,111,size=10)
end()
assert PAGE==88,PAGE
for ch,l in enumerate(L):
 y=page(l['title'],f'Answer key • Episode {ch+1}','Example explanations are offered. Other correct reasoning is welcome.')
 last=None
 for pn,n,answer in KEYS[ch]:
  if last!=pn:
   y=para('<b>Page '+str(pn)+'</b>',M,y,size=9.5)-3;last=pn
  y=para(str(n)+'. '+html.escape(answer),M+14,y,502,size=9,leading=12)-4
 end()
assert PAGE==100,PAGE
C.save()
reader=PdfReader(OUT);assert len(reader.pages)==100
for i,p in enumerate(reader.pages):
 txt=p.extract_text();assert txt and len(txt)>100,(i+1,'empty')
(ROOT/'workbook/exercise-manifest.json').write_text(json.dumps(MANIFEST,ensure_ascii=False,indent=2)+'\n')
(ROOT/'workbook/answer-key.json').write_text(json.dumps(KEYS,ensure_ascii=False,indent=2)+'\n')
print(f'Built {OUT}: exactly 100 pages; {sum(len(x["questions"]) for x in MANIFEST)} numbered exercises; all generated numeric relations checked.')
