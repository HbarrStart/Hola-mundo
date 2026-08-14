const incident={event:'Sismo M7,4 — 10 ago 2026',status:'EMERGENCIA ACTIVA',cutoff:'Verificar cada actualización',note:'Las cifras de víctimas, heridos, desaparecidos y daños son dinámicas. MOS no fija una cifra sin fuente primaria y hora de corte.'};
const sources=[
{name:'Servicio Geológico Colombiano',url:'https://www.sgc.gov.co/',role:'Sismicidad, magnitud, epicentro y réplicas.'},
{name:'UNGRD',url:'https://www.gestiondelriesgo.gov.co/',role:'Daños, afectaciones, respuesta y coordinación nacional.'},
{name:'Cruz Roja Colombiana',url:'https://www.cruzrojacolombiana.org/',role:'Respuesta humanitaria y asistencia.'},
{name:'Defensa Civil Colombiana',url:'https://www.defensacivil.gov.co/',role:'Respuesta y apoyo operativo.'},
{name:'IDEAM',url:'https://www.ideam.gov.co/',role:'Información meteorológica e hidrológica relevante.'}
];
document.querySelector('#updated').textContent=new Date().toLocaleString('es-CO',{dateStyle:'short',timeStyle:'short'});
document.querySelector('#cards').innerHTML=[
['Evento','Sismo M7,4','CONFIRMADO','SGC'],
['Epicentro','San José del Palmar, Chocó','CONFIRMADO','SGC'],
['Cifras humanas','DINÁMICAS','VERIFICAR','UNGRD'],
['Daños','DINÁMICOS','VERIFICAR','UNGRD']
].map(([a,b,c,d])=>`<article class="card"><span class="badge">${c}</span><div class="meta">${a}</div><div class="value">${b}</div><div class="meta">Fuente primaria: ${d}</div></article>`).join('');
document.querySelector('#sources').innerHTML=sources.map(s=>`<article class="source"><a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.name} ↗</a><p>${s.role}</p></article>`).join('');
