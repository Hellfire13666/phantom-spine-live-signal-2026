'use strict';
async function copyText(btn){
  const code=btn.parentElement.querySelector('pre.cmd');
  const feedback=document.querySelector('#feedback');
  if(!code || !feedback)return;
  const value=code.textContent.trim();
  let succeeded=false;
  try{if(navigator.clipboard&&navigator.clipboard.writeText){await navigator.clipboard.writeText(value);succeeded=true;}}catch(e){/* file URLs may restrict clipboard */}
  if(!succeeded){
    const t=document.createElement('textarea');t.value=value;t.setAttribute('aria-label','Command text');t.style.position='fixed';t.style.opacity='0';document.body.appendChild(t);t.select();
    try{succeeded=document.execCommand('copy');}catch(e){/* caller can select text manually */}
    document.body.removeChild(t);
  }
  feedback.textContent=succeeded?'Copied real command. Paste it into your terminal.':'Clipboard permission unavailable: select the command shown and copy it manually.';
  feedback.hidden=false;
}
document.querySelectorAll('button.copy').forEach(b=>b.addEventListener('click',()=>copyText(b)));
