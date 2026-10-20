(function(){
  var d=document,root=d.documentElement,L=root.lang==='en';
  try{var t=localStorage.getItem('theme');if(t)root.dataset.theme=t}catch(e){}
  var tb=d.getElementById('theme');
  if(tb)tb.onclick=function(){var n=root.dataset.theme==='light'?'dark':'light';root.dataset.theme=n;try{localStorage.setItem('theme',n)}catch(e){}};
  /* reveal */
  var r=d.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.08});r.forEach(function(e){io.observe(e)})}else r.forEach(function(e){e.classList.add('in')});
  /* spotlight cards */
  d.addEventListener('pointermove',function(e){var c=e.target.closest&&e.target.closest('.card');if(!c)return;var b=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-b.left)+'px');c.style.setProperty('--my',(e.clientY-b.top)+'px')});
  /* typing */
  var el=d.getElementById('typed');
  if(el){var w=JSON.parse(el.dataset.words),i=0,j=0,del=false,still=matchMedia('(prefers-reduced-motion:reduce)').matches;
    if(still){el.innerHTML='<em>'+w[0]+'</em>'}else(function tick(){var s=w[i];j+=del?-1:1;el.innerHTML='<em>'+s.slice(0,j)+'</em>';var ms=del?35:70;if(!del&&j===s.length){del=true;ms=1600}else if(del&&j===0){del=false;i=(i+1)%w.length;ms=350}setTimeout(tick,ms)})()}
  /* counters */
  d.querySelectorAll('[data-count]').forEach(function(n){var to=+n.dataset.count,suf=n.dataset.suf||'',done=false;
    var o=new IntersectionObserver(function(es){if(es[0].isIntersecting&&!done){done=true;var t0=performance.now();(function f(t){var p=Math.min((t-t0)/1200,1);n.textContent=Math.round(to*(1-Math.pow(1-p,3))).toLocaleString(L?'en-US':'tr-TR')+suf;if(p<1)requestAnimationFrame(f)})(t0)}});o.observe(n)});
  /* live github repos */
  var box=d.getElementById('repos');
  if(box){fetch('https://api.github.com/users/yigitbuyukeren/repos?per_page=30&sort=pushed').then(function(r){return r.ok?r.json():Promise.reject()}).then(function(a){
    var h=a.filter(function(x){return !x.fork&&x.name!=='yigitbuyukeren'&&x.name!=='yigitbuyukeren.github.io'}).slice(0,6).map(function(x){
      var s=d.createElement('a');s.className='card repo reveal in';s.href=x.html_url;s.rel='noopener';
      var h3=d.createElement('h3');h3.textContent=x.name;var p=d.createElement('p');p.textContent=x.description||'';
      var m=d.createElement('div');m.className='meta';
      if(x.language){var l=d.createElement('span');l.innerHTML='<i class="dot"></i>';l.append(x.language);m.append(l)}
      var u=d.createElement('span');u.textContent=(L?'updated ':'güncellendi ')+new Date(x.pushed_at).toLocaleDateString(L?'en-GB':'tr-TR',{month:'short',year:'numeric'});m.append(u);
      s.append(h3,p,m);return s});
    if(h.length)box.replaceChildren.apply(box,h)}).catch(function(){})}
  var y=d.getElementById('y');if(y)y.textContent=new Date().getFullYear();
})();
