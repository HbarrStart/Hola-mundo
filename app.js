const $=s=>document.querySelector(s);
$('#updated').textContent=MOS_DATA.reviewedAt;
$('#build').textContent=MOS_DATA.build;
$('#alerts').innerHTML=MOS_DATA.alerts.map(a=>`<article class="card"><span class="tag">${a.status}</span><h3>${a.title}</h3><p>${a.body}</p><small><b>Fuente:</b> ${a.source} · ${a.updated}</small><p><a href="${a.url}" target="_blank" rel="noopener noreferrer">Ver fuente primaria ↗</a></p></article>`).join('');
$('#sources').innerHTML=MOS_DATA.sources.map(s=>`<div class="source"><div><b>${s.name}</b><div class="muted">${s.role}</div></div><a href="${s.url}" target="_blank" rel="noopener noreferrer">Fuente ↗</a></div>`).join('');
document.querySelectorAll('.tabs button').forEach(btn=>btn.addEventListener('click',()=>{document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('active'));document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active-panel'));btn.classList.add('active');$('#'+btn.dataset.tab).classList.add('active-panel')}));