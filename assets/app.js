'use strict';
const $ = (selector) => document.querySelector(selector);
const menu = $('#menu-toggle');
menu?.addEventListener('click', () => { const open = $('#sidebar').classList.toggle('open'); menu.setAttribute('aria-expanded', String(open)); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') { $('#sidebar').classList.remove('open'); menu?.setAttribute('aria-expanded','false'); menu?.focus(); } });
document.addEventListener('click', e => { if (!e.target.closest('#sidebar, #menu-toggle')) { $('#sidebar').classList.remove('open'); menu?.setAttribute('aria-expanded','false'); } });
$('#print')?.addEventListener('click', () => window.print());
$('#nav-search')?.addEventListener('input', e => {
 const q=e.target.value.trim().toLowerCase(); let count=0;
 document.querySelectorAll('.chapter-link').forEach(link=>{link.hidden=!link.textContent.toLowerCase().includes(q); if(!link.hidden)count++;});
 document.querySelectorAll('.nav-group').forEach(group=>{group.hidden=![...group.querySelectorAll('.chapter-link')].some(a=>!a.hidden);});
 $('#search-empty').hidden=count>0;
});
function updateKV(){
 const inputs=[$('#tokens'),$('#requests'),$('#heads')];
 if(inputs.some(e=>!e.checkValidity()||!e.value)){ $('#kv-result').textContent='请输入范围内的正整数。';return; }
 const [tokens,requests,heads]=inputs.map(e=>Number(e.value));
 if(![tokens,requests,heads].every(Number.isInteger)){ $('#kv-result').textContent='请输入范围内的正整数。';return; }
 const perToken=2*80*heads*128*2; const total=perToken*tokens*requests;
 $('#kv-result').innerHTML=`${(total/2**30).toLocaleString('zh-CN',{minimumFractionDigits:3,maximumFractionDigits:3})} GiB <small>每 Token ${perToken/1024} KiB · ${requests.toLocaleString()} 个请求的逻辑 KV 合计，不含分块余量</small>`;
}
if($('#tokens')){['tokens','requests','heads'].forEach(id=>$('#'+id).addEventListener('input',updateKV));updateKV();}
const rounds=[{slots:['A','B','C'],text:'第 1 轮：服务 A、B、C。B 在本轮结束。'},{slots:['A','C','D'],text:'第 2 轮：B 退出，D 补位；C 在本轮结束。'},{slots:['A','D','E'],text:'第 3 轮：C 退出，E 补位；A 在本轮结束。'},{slots:['D','E','F'],text:'第 4 轮：A 退出，F 补位。不同请求的进出不必同步。'}];
let round=0;
function showRound(){ $('#batch-slots').innerHTML=rounds[round].slots.map(s=>`<span class="slot">${s}</span>`).join('');$('#batch-explain').textContent=rounds[round].text;$('#next-round').disabled=round===rounds.length-1; }
if($('#batch-slots')){showRound();$('#next-round').addEventListener('click',()=>{if(round<rounds.length-1)round++;showRound();});$('#reset-round').addEventListener('click',()=>{round=0;showRound();});}
function updateBlock(){const position=Number($('#token-index').value);const i=position-1;const logical=Math.floor(i/16);$('#block-result').innerHTML=`第 ${position} 个 Token → 物理块 ${[7,2,11][logical]}<small>零基下标 ${i} → 逻辑块 ${logical} → 块内偏移 ${i%16}（Block Size = 16）</small>`;}
if($('#token-index')){$('#token-index').addEventListener('input',updateBlock);updateBlock();}
