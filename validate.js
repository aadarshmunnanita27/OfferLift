const fs=require('fs'),vm=require('vm'),assert=require('assert');
const path=require('path');const root=__dirname;
const d=JSON.parse(fs.readFileSync(path.join(root,'dist/data.json'),'utf8'));
const credit=d.name==='CreditPulse';let els={};
const vals={budget:'20',margin:'20',cost:'0.05',threshold:'30'};
for(const [k,v]of Object.entries(d.rows[0].x))vals['f_'+k]=v;
const doc={getElementById:id=>els[id]||(els[id]={innerHTML:'',textContent:'',value:vals[id]??'',classList:{toggle(){}},setAttribute(){}}),querySelectorAll:()=>[],createElement:()=>({click(){}})};
const ctx=vm.createContext({document:doc,console,Math,Number,Object,Array,JSON,Error,Blob,URL,setTimeout,fetch:()=>new Promise(()=>{})});
vm.runInContext(fs.readFileSync(path.join(root,'dist/app.js'),'utf8'),ctx);ctx.payload=d;vm.runInContext('D=payload',ctx);
let err=0;for(const r of d.rows){ctx.row=r;const e=vm.runInContext(credit?'Math.abs(predict(vector(row.x))-row.p)':'Math.max(Math.abs(gb(D.models[0],vector(row.x))-row.p0),Math.abs(gb(D.models[1],vector(row.x))-row.p1))',ctx);err=Math.max(err,e)}
assert(err<1e-10,'Browser model differs from Python');
for(const tab of ['overview','explore','evaluate','method']){vm.runInContext(`switchTab('${tab}')`,ctx);assert(els.content.innerHTML.length>300,tab+' did not render')}
ctx.input=fs.readFileSync(path.join(root,'dist/sample.csv'),'utf8');let rows=vm.runInContext('csv(input)',ctx);assert(rows.length===10);ctx.batchRows=rows;let results=vm.runInContext('batchRows.map(scoreRow)',ctx);assert(results.every(x=>!x.includes('NaN')));
assert.throws(()=>vm.runInContext('vector({})',ctx));
assert.deepEqual(JSON.parse(JSON.stringify(vm.runInContext('csv(\'a,b\\n"x,y",2\\n\')',ctx))),[{a:'x,y',b:'2'}]);
console.log(JSON.stringify({test_rows:d.rows.length,max_inference_error:err,render_functions:4,sample_csv_rows:rows.length,invalid_input_rejected:true,visual_browser_test:false},null,2));
