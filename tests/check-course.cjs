const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const html=fs.readFileSync(path.join(__dirname,'..','Algebra_Adventure.html'),'utf8');
const code=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes=new Map();function node(id){if(!nodes.has(id))nodes.set(id,{value:({xRange:'3',children:'4',extra:'5',total:'12',amount:'2',op:'sub',target:'both'})[id]||'',innerHTML:'',textContent:'',disabled:false,dataset:{},setAttribute(k,v){this[k]=v},style:{},classList:{add(){},remove(){},toggle(){}},insertAdjacentHTML(_,s){this.innerHTML+=s}});return nodes.get(id)}
const stored={};const ctx=vm.createContext({document:{getElementById:node},localStorage:{getItem:k=>stored[k]||null,setItem:(k,v)=>stored[k]=v},window:{print(){}},console});
vm.runInContext(code,ctx);const run=c=>vm.runInContext(c,ctx);
for(let ch=0;ch<8;ch++){
 run(`go(${ch})`);
 for(let i=0;i<100;i++){
 const p=run(`makeProblem(${ch})`);const n=p.q.match(/\d+/g).map(Number),v=p.answers[0];
 if(ch===0)assert.equal(n[0]+n[1],v+n[2]);
 if(ch===1)assert.equal(v,n[0]-n[2]);
 if(ch===2)assert.equal(v,n[0]+n[1]);
 if(ch===3)assert.equal(n[0]+v,n[1]);
 if(ch===4)assert.equal(p.q.includes('−')?v-n[0]:v*n[0],n[1]);
 if(ch===5)assert.equal(v,n[0]+n[1]);
 if(ch===6){assert.equal(p.answers[1]-v,n[0]);assert.equal(p.answers[1]+v,n[1])}
 if(ch===7)assert.equal(v,((n[1]-n[0])%2===0)?'yes':'no');
 }
 const p=run('practice');p.answers.forEach((v,i)=>node('answer'+i).value=String(v));run('checkAnswer()');assert.match(node('answerFeedback').textContent,/That works/);const count=run(`profile().counts[${ch}]`);run('checkAnswer()');assert.equal(run(`profile().counts[${ch}]`),count);run('newPractice()');node('answer0').value='-999';run('checkAnswer()');assert.match(node('answerFeedback').textContent,/Not/);
}
run('go(0)');node('amount').value='5';node('op').value='add';node('target').value='both';run('balanceMove()');assert.equal(run('lab.left'),7);assert.equal(run('lab.right'),7);node('target').value='left';run('balanceMove()');assert.equal(run('lab.left'),12);assert.equal(run('lab.right'),7);
run('go(3)');node('amount').value='2';node('op').value='sub';run('solveMove()');assert.equal(run('lab.b'),0);assert.equal(run('lab.c'),1);assert.match(node('labFeedback').textContent,/Solved/);
run('go(4)');node('op').value='div';run('solveMove()');assert.equal(run('lab.a'),1);assert.equal(run('lab.c'),4);node('amount').value='0';run('solveMove()');assert.match(node('labFeedback').textContent,/1 to 20/);
run('go(6)');run('drawStory()');assert.match(node('storyView').innerHTML,/2C \+ 5 = 13/);
run('go(7)');run('drawDetect()');assert.match(node('detectView').innerHTML,/3.5/);node('total').value='13';run('drawDetect()');assert.match(node('detectView').innerHTML,/4 children and 9 adults/);
run("state.person='Reagan';go(0)");assert.equal(run('profile().counts[0]'),0);run("state.person='Quinn';go(0)");assert.equal(run('profile().counts[0]'),1);
assert(!/<(?:script|link|img)[^>]+(?:src|href)=["']https?:/i.test(html));assert(!/\bfetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon/.test(code));assert(html.includes("connect-src 'none'"));
console.log('PASS: 800 generated problems independently checked; all eight lesson render paths; answer feedback and duplicate-credit guard; balance and equation operations; zero rejection; story/detective calculations; separate learner progress; offline resource audit. DOM-stub checks only, not browser visual QA.');
