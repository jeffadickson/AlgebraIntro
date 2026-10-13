"""Core exercise generators, shared by both print editions."""
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
  a=2+(k*5)%8;b=1+(k*3)%7
  total=a+b; c=1+k%total
  if k%3==0:q=f'{a} + {b} = □ + {c}';v=total-c;ans=f'□ = {v}; both sides are {total}.';assert a+b==v+c
  elif k%3==1:q=f'Is {total} = {a} + {b} true? Explain.';ans=f'Yes. Both sides are {total}.'
  else:q=f'Is {a} + {b} = {total+1} true? Repair the right side.';ans=f'No. The left is {total}; replace {total+1} with {total}.'
  hint='Work out each side separately.'
 elif ch==1:
  start=x+b;add=k%2==0;v=start+b if add else start-b;assert v==(start+b if add else start-b)
  q=f'Start with {start} = {start}. {"Add" if add else "Subtract"} {b} on BOTH sides. Write the new equality.';ans=f'{v} = {v}.';hint='Use the same operation and amount twice.'
 elif ch==2:
  a=2+(k*3)%8;b=1+(k*5)%7
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

