#!/usr/bin/env python3
"""Build the final enhanced recipe site with full recipe details."""
import json

with open("/home/heb/.hermes/recipe-site/recipes_full.json") as f:
    recipes = json.load(f)

# Build a JS-safe JSON string
js_data = json.dumps(recipes, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>🍽️ Family Meal Planner — 50 Recipes</title>
<style>
:root{--bg:#111827;--bg-card:#1f2937;--bg-card-hover:#283548;--bg-elevated:#162032;--text:#e5e7eb;--text-dim:#9ca3af;--text-bright:#f9fafb;--accent:#10b981;--accent-light:#34d399;--border:#374151;--chip-bg:#1e2d4a;--header-bg:#0c1222;--radius:14px;--radius-sm:8px;--shadow:0 4px 20px rgba(0,0,0,.35)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;line-height:1.5}
header{background:var(--header-bg);border-bottom:3px solid var(--accent);padding:14px 24px;position:sticky;top:0;z-index:100;backdrop-filter:blur(16px);background:rgba(12,18,34,.92)}
.header-inner{max-width:1280px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
.logo{font-size:1.5rem;font-weight:900;letter-spacing:-.5px}.logo em{color:var(--accent-light);font-style:normal}
.nav-tabs{display:flex;gap:4px;background:var(--bg-card);padding:4px;border-radius:12px}
.nav-tab{padding:9px 20px;border:none;background:none;color:var(--text-dim);cursor:pointer;border-radius:10px;font-size:.82rem;font-weight:600;transition:all .2s;white-space:nowrap}
.nav-tab:hover{color:var(--text);background:rgba(255,255,255,.06)}.nav-tab.active{background:var(--accent);color:#fff;font-weight:700}
.search-wrap{position:relative;flex-shrink:0}
.search-icon{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:var(--text-dim);font-size:.9rem;pointer-events:none}
.search-input{background:var(--bg-card);border:1.5px solid var(--border);color:var(--text);padding:9px 14px 9px 38px;border-radius:var(--radius-sm);width:240px;font-size:.85rem;outline:none;transition:all .2s}
.search-input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(16,185,129,.15)}::placeholder{color:#6b7280}
main{max-width:1280px;margin:0 auto;padding:28px 24px}
.page{display:none}.page.active{display:block;animation:fadeIn .2s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.category-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px}
.filter-btn{padding:8px 18px;border:2px solid transparent;border-radius:24px;cursor:pointer;font-size:.78rem;font-weight:700;background:var(--bg-card);color:var(--text);transition:all .2s;display:flex;align-items:center;gap:6px;border-color:var(--border)}
.filter-btn:hover{border-color:var(--accent);color:var(--accent-light);transform:translateY(-1px)}
.filter-btn.active{color:#fff;border-color:transparent;transform:translateY(-1px);box-shadow:0 2px 8px rgba(0,0,0,.3)}
.stats-bar{display:flex;gap:12px;margin-bottom:24px;flex-wrap:wrap}
.stat-chip{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius-sm);padding:10px 18px;font-size:.82rem;color:var(--text-dim);display:flex;align-items:center;gap:8px}
.stat-chip strong{color:var(--text-bright);font-size:1.15rem}
.recipe-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
.recipe-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:22px;cursor:pointer;transition:all .25s;position:relative;overflow:hidden}
.recipe-card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px}
.recipe-card:hover{border-color:var(--accent);transform:translateY(-3px);box-shadow:var(--shadow)}
.card-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.card-icon{font-size:1.8rem;line-height:1}
.card-number{font-size:.65rem;color:var(--text-dim);font-weight:700;letter-spacing:.5px;opacity:.7}
.card-name{font-size:.95rem;font-weight:700;line-height:1.35;margin-bottom:12px;color:var(--text-bright)}
.card-tags{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:0}
.chip{font-size:.65rem;font-weight:700;padding:3px 9px;border-radius:8px;color:#fff;text-transform:uppercase;letter-spacing:.4px}
.chip-time{background:rgba(16,185,129,.2);color:var(--accent-light);text-transform:none;font-size:.7rem;padding:3px 8px;border:1px solid rgba(16,185,129,.3)}
.chip-diff{background:rgba(251,191,36,.2);color:#fbbf24;text-transform:none;font-size:.7rem;padding:3px 8px;border:1px solid rgba(251,191,36,.3)}
.chip-easy{background:rgba(16,185,129,.2);color:var(--accent-light)}
.chip-medium{background:rgba(251,191,36,.2);color:#fbbf24}
.card-kid{margin-top:8px;font-size:.7rem;color:var(--text-dim)}
.card-kid span{color:var(--accent-light)}
.no-results{text-align:center;padding:60px 20px;color:var(--text-dim);font-size:1rem}
.no-results .emoji{font-size:3rem;margin-bottom:12px}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:200;backdrop-filter:blur(6px);overflow-y:auto;padding:20px}
.overlay.open{display:flex;justify-content:center;align-items:flex-start}
.overlay-card{background:var(--bg-card);border:1px solid var(--border);border-radius:18px;max-width:720px;width:100%;margin:24px auto;position:relative;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.5)}
.overlay-close{position:absolute;top:14px;right:14px;background:rgba(0,0,0,.5);color:#fff;border:none;width:38px;height:38px;border-radius:50%;font-size:1.1rem;cursor:pointer;z-index:10;display:flex;align-items:center;justify-content:center;transition:background .2s}
.overlay-close:hover{background:rgba(0,0,0,.8)}.overlay-banner{height:6px;width:100%}.overlay-body{padding:28px 36px 36px}
.overlay-body h2{font-size:1.6rem;font-weight:800;margin:10px 0 4px;line-height:1.2;color:var(--text-bright)}
.cat-badge{display:inline-block;font-size:.7rem;font-weight:800;padding:4px 14px;border-radius:12px;color:#fff;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
.subtitle-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-bottom:20px}
.subtitle-row .chip{transform:none}
.nutrition-bar{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:24px;background:var(--bg-elevated);padding:14px;border-radius:var(--radius-sm);border:1px solid var(--border)}
.nut-item{flex:1;text-align:center;min-width:70px}
.nut-value{font-size:1.15rem;font-weight:800;color:var(--accent-light);display:block}
.nut-label{font-size:.6rem;color:var(--text-dim);text-transform:uppercase;letter-spacing:.5px;margin-top:2px}
.nut-sub{color:#6b7280;font-size:.7rem}
.ing-list,.step-list{list-style:none}
.ing-list li{padding:8px 0;font-size:.88rem;border-bottom:1px solid rgba(255,255,255,.04);display:flex;align-items:flex-start;gap:10px;color:var(--text)}
.ing-list li::before{content:'▸';color:var(--accent);font-weight:700;flex-shrink:0;font-size:.85rem;margin-top:1px}
.step-list{counter-reset:step}
.step-list li{padding:10px 0 10px 36px;font-size:.88rem;position:relative;color:var(--text);border-bottom:1px solid rgba(255,255,255,.04)}
.step-list li::before{counter-increment:step;content:counter(step);position:absolute;left:0;top:10px;width:24px;height:24px;background:var(--accent);color:#fff;border-radius:50%;font-size:.7rem;font-weight:800;display:flex;align-items:center;justify-content:center}
.section-title{font-size:.82rem;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:var(--accent-light);margin-bottom:12px;padding-bottom:8px;border-bottom:1.5px solid var(--border)}
.detail-actions{display:flex;gap:10px;margin-top:28px;flex-wrap:wrap;align-items:center;border-top:1px solid var(--border);padding-top:20px}
.btn{padding:11px 24px;border:none;border-radius:10px;font-size:.85rem;font-weight:700;cursor:pointer;transition:all .2s;white-space:nowrap}
.btn-primary{background:var(--accent);color:#fff}.btn-primary:hover{background:var(--accent-light)}
.btn-ghost{background:transparent;color:var(--text);border:1.5px solid var(--border)}.btn-ghost:hover{background:rgba(255,255,255,.05)}
.plan-day-select{background:var(--bg);border:1.5px solid var(--border);color:var(--text);padding:10px 14px;border-radius:10px;font-size:.85rem;outline:none;cursor:pointer}
.plan-day-select:focus{border-color:var(--accent)}
.planner-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:12px}
.planner-day{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:18px;min-height:160px;transition:border-color .2s}
.planner-day:hover{border-color:var(--accent)}
.planner-day h4{font-size:.75rem;font-weight:800;text-transform:uppercase;letter-spacing:1.5px;color:var(--accent-light);margin-bottom:12px}
.planner-day .assigned{font-size:.85rem;font-weight:600;line-height.1.35;cursor:pointer;transition:color .2s}
.planner-day .assigned:hover{color:var(--accent-light)}
.planner-day .remove-btn{background:none;border:none;color:#6b7280;cursor:pointer;font-size:.68rem;padding:0;margin-top:8px;display:block;transition:color .2s}
.planner-day .remove-btn:hover{color:#ef4444}
.planner-empty{color:var(--text-dim);font-size:.78rem;font-style:italic;padding:8px 0}
.grocery-section{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:22px;margin-bottom:16px}
.grocery-section h3{font-size:1.05rem;font-weight:800;margin-bottom:14px;display:flex;align-items:center;gap:10px}
.grocery-items{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:6px}
.grocery-item{display:flex;align-items:center;gap:10px;font-size:.85rem;padding:5px 0}
.grocery-item input[type=checkbox]{accent-color:var(--accent);width:17px;height:17px;cursor:pointer;flex-shrink:0}
.grocery-item.checked label{text-decoration:line-through;color:var(--text-dim)}
.notes-area{width:100%;background:var(--bg);border:1.5px solid var(--border);color:var(--text);border-radius:10px;padding:14px;font-size:.85rem;min-height:90px;resize:vertical;font-family:inherit;outline:none;margin-top:10px}
.notes-area:focus{border-color:var(--accent)}
.action-btn{background:var(--bg-card);border:1.5px solid var(--border);color:var(--text);padding:10px 18px;border-radius:10px;font-size:.82rem;font-weight:700;cursor:pointer;display:inline-flex;align-items:center;gap:7px;transition:all .2s}
.action-btn:hover{background:rgba(255,255,255,.06);border-color:var(--text-dim)}
.top-bar{display:flex;align-items:center;gap:12px;margin-bottom:24px;flex-wrap:wrap}
.top-bar h2{font-size:1.4rem;font-weight:800}
.pagination{display:flex;gap:6px;justify-content:center;margin-top:32px;flex-wrap:wrap}
.pg-btn{padding:8px 15px;border:1px solid var(--border);background:var(--bg-card);color:var(--text);border-radius:var(--radius-sm);cursor:pointer;font-size:.82rem;font-weight:700;transition:all .2s}
.pg-btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.pg-btn:hover:not(.active){background:rgba(255,255,255,.05)}
.toast{position:fixed;bottom:28px;right:28px;background:var(--accent);color:#fff;padding:14px 28px;border-radius:12px;font-size:.85rem;font-weight:700;z-index:300;transform:translateY(100px);opacity:0;transition:all .35s;box-shadow:0 8px 30px rgba(16,185,129,.3)}
.toast.show{transform:translateY(0);opacity:1}
.empty-state{text-align:center;padding:60px 20px;color:var(--text-dim)}
.empty-state .emoji{font-size:3rem;margin-bottom:16px}
@media(max-width:640px){.header-inner{flex-direction:column;align-items:flex-start}.nav-tabs{width:100%}.nav-tab{flex:1;text-align:center;padding:8px 12px;font-size:.75rem}.search-input{width:100%}.recipe-grid{grid-template-columns:1fr}.planner-grid{grid-template-columns:1fr 1fr}.overlay-body{padding:20px}.nutrition-bar{gap:4px}.nut-item{min-width:60px}}
@media print{header,.nav-tabs,.category-bar,.search-wrap,.action-btn,.pagination,.detail-actions,.overlay-close,.toast,.remove-btn{display:none!important}body{background:#fff;color:#111}.recipe-card{break-inside:avoid}}
</style>
</head>
<body>
<header>
<div class="header-inner">
<div class="logo">🍽️ Family <em>Meal Planner</em></div>
<div class="nav-tabs">
<button id="tab-browse" class="nav-tab active" onclick="switchPage('browse')">📋 Recipes</button>
<button id="tab-planner" class="nav-tab" onclick="switchPage('planner')">📅 Meal Plan</button>
<button id="tab-grocery" class="nav-tab" onclick="switchPage('grocery')">🛒 Grocery</button>
</div>
<div class="search-wrap"><span class="search-icon">🔍</span><input class="search-input" type="text" placeholder="Search 50 recipes…" id="searchInput" oninput="renderRecipes()"></div>
</div>
</header>
<main>
<div id="page-browse" class="page active">
<div class="category-bar" id="categoryBar"></div>
<div class="stats-bar" id="statsBar"></div>
<div class="recipe-grid" id="recipeGrid"></div>
<div class="no-results" id="noResults" style="display:none"><div class="emoji">🤔</div>No recipes found. Try a different filter or search term.</div>
<div class="pagination" id="pagination"></div>
</div>
<div id="page-planner" class="page">
<div class="top-bar"><h2>📅 Weekly Meal Planner</h2><button class="action-btn" onclick="window.print()">🖨️ Print</button><button class="action-btn" onclick="clearPlan()">🗑️ Clear All</button></div>
<div class="planner-grid" id="plannerGrid"></div>
</div>
<div id="page-grocery" class="page">
<div class="top-bar"><h2>🛒 Grocery List</h2><button class="action-btn" onclick="window.print()">🖨️ Print</button><button class="action-btn" onclick="resetChecks()">☑️ Reset Checks</button></div>
<div id="groceryContent"></div>
</div>
</main>
<div class="overlay" id="recipeOverlay"><div class="overlay-card" onclick="event.stopPropagation()"><button class="overlay-close" onclick="closeOverlay()">✕</button><div class="overlay-banner" id="overlayBanner"></div><div class="overlay-body" id="overlayBody"></div></div></div>
<div class="toast" id="toast"></div>
<script>
var DATA=__DATA_PLACEHOLDER__;
var DAYS=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
var currentFilter='all',currentPage=0,perPage=18;
var mealPlan=JSON.parse(localStorage.getItem('mealPlan')||'{}');
var checkedG=JSON.parse(localStorage.getItem('checkedG')||'{}');
var notesData=localStorage.getItem('groceryNotes')||'';

function init(){
  var cats=[];DATA.forEach(function(r){if(cats.indexOf(r.category)===-1)cats.push(r.category);});
  var bar=document.getElementById('categoryBar');
  var allB=document.createElement('button');allB.className='filter-btn active';allB.dataset.cat='all';
  allB.textContent='📋 All Recipes ('+DATA.length+')';allB.style.borderColor='#10b981';allB.onclick=function(){setFilter('all');};bar.appendChild(allB);
  cats.forEach(function(cat){var c=DATA.find(function(r){return r.category===cat;});var n=DATA.filter(function(r){return r.category===cat;}).length;
  var b=document.createElement('button');b.className='filter-btn';b.dataset.cat=cat;
  b.textContent=c.icon+' '+cat+' ('+n+')';b.onclick=function(){setFilter(cat);};bar.appendChild(b);});
  renderStats();renderRecipes();
}
function renderStats(){
  var cats=[];DATA.forEach(function(r){if(cats.indexOf(r.category)===-1)cats.push(r.category);});
  var s=document.getElementById('statsBar');s.innerHTML='<div class="stat-chip">📊 <strong>'+DATA.length+'</strong> recipes</div>';
  cats.forEach(function(cat){var c=DATA.find(function(r){return r.category===cat;});var n=DATA.filter(function(r){return r.category===cat;}).length;
  s.innerHTML+='<div class="stat-chip" style="border-left:3px solid '+c.color+'">'+c.icon+' <strong>'+n+'</strong> '+cat+'</div>';});
}
function switchPage(n){document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active');});document.querySelectorAll('.nav-tab').forEach(function(t){t.classList.remove('active');});document.getElementById('page-'+n).classList.add('active');document.getElementById('tab-'+n).classList.add('active');if(n==='grocery')renderGrocery();if(n==='planner')renderPlanner();window.scrollTo({top:0,behavior:'smooth'});}
function setFilter(c){currentFilter=c;currentPage=0;document.querySelectorAll('.filter-btn').forEach(function(b){b.classList.remove('active');});var btn=document.querySelector('.filter-btn[data-cat="'+c+'"]');if(btn)btn.classList.add('active');renderRecipes();}
function getFiltered(){var q=document.getElementById('searchInput').value.toLowerCase().trim();return DATA.filter(function(r){if(currentFilter!=='all'&&r.category!==currentFilter)return false;if(q&&r.name.toLowerCase().indexOf(q)===-1&&r.category.toLowerCase().indexOf(q)===-1)return false;return true;});}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');}
function renderRecipes(){
  var f=getFiltered();var g=document.getElementById('recipeGrid');var nr=document.getElementById('noResults');var pg=document.getElementById('pagination');
  if(!f.length){g.innerHTML='';nr.style.display='block';pg.innerHTML='';return;}nr.style.display='none';
  var tp=Math.ceil(f.length/perPage);if(currentPage>=tp)currentPage=tp-1;if(currentPage<0)currentPage=0;
  var s=currentPage*perPage;var items=f.slice(s,s+perPage);g.innerHTML='';
  items.forEach(function(r){
    var d=document.createElement('div');d.className='recipe-card';d.style.setProperty('--card-color',r.color);d.onclick=function(){openRecipe(r.id);};
    var accent=document.createElement('div');accent.className='card-accent';accent.style.background=r.color;d.appendChild(accent);
    var top=document.createElement('div');top.className='card-top';
    document.writeTest=top;
    var icon=document.createElement('span');icon.className='card-icon';icon.textContent=r.icon;
    var num=document.createElement('span');num.className='card-number';num.textContent='#'+String(r.id).padStart(2,'0');
    top.appendChild(icon);top.appendChild(num);d.appendChild(top);
    var name=document.createElement('div');name.className='card-name';name.textContent=r.name;d.appendChild(name);
    var tags=document.createElement('div');card-tags';
    var timeChip=document.createElement('span');timeChip.className='chip chip-time';timeChip.textContent='⏱ '+r.prep_time+' + '+r.cook_time;
    tags.appendChild(timeChip);d.appendChild(tags);
    d.appendChild(tags2);d.appendChild(d);
    if(r.kid_friendly){var k=document.createElement('div');k.className='card-kid';k.innerHTML='👶 <span>Kid-friendly</span>';d.appendChild(k);}
    g.appendChild(d);
  });
  if(tp>1){pg.innerHTML='';for(var i=0;i<tp;i++){(function(p,idx){var b=document.createElement('button');b.className='pg-btn'+(idx===currentPage?' active':'');b.textContent=idx+1;b.onclick=function(){goPage(idx);};p.appendChild(b);})(pg,i);}}else{pg.innerHTML='';}
}
function goPage(p){currentPage=p;renderRecipes();window.scrollTo({top:320,behavior:'smooth'});}
function openRecipe(id){var r=DATA.find(function(x){return x.id===id;});if(!r)return;
  document.getElementById('overlayBanner').style.background='linear-gradient(90deg,'+r.color+','+r.color_light+')';
  var n=r.nutrition;
  var nutBar='<div class="nutrition-bar">'+
    '<div class="nut-item"><span class="nut-value">'+n.calories+'</span><span class="nut-label">Cal</span></div>'+
    '<div class="nut-item"><span class="nut-value">'+n.protein_g+'g</span><span class="nut-label">Protein</span></div>'+
    '<div class="nut-item"><span class="nut-value">'+n.carbs_g+'g</span><span class="nut-label">Carbs</span></div>'+
    '<div class="nut-item"><span class="nut-value">'+n.fat_g+'g</span><span class="nut-label">Fat</span></div>'+
    '<div class="nut-item"><span class="nut-value">'+n.fiber_g+'g</span><span class="nut-label">Fiber</span></div>'+
  '</div>';
  var dayOpts=DAYS.map(function(d){return '<option value="'+d+'">'+d+'</option>';}).join('');
  var ingHtml='<ul class="ing-list">'+r.ingredients.map(function(i){return '<li>'+i+'</li>';}).join('')+'</ul>';
  var stepHtml='<ol class="step-list">'+r.steps.map(function(s){return '<li>'+s+'</li>';}).join('')+'</ol>';
  var kidBadge=r.kid_friendly?' <span style="font-size:.75rem;color:var(--accent-light)">👶 Kid-friendly</span>':'';
  document.getElementById('overlayBody').innerHTML=
    '<div style="display:flex;align-items:center;gap:10px;margin:10px 0 4px;flex-wrap:wrap"><span class="cat-badge" style="background:'+r.color+'">'+r.icon+' '+r.category+'</span><span class="chip chip-easy">'+r.difficulty+'</span><span class="chip chip-time" style="text-transform:none">⏱ '+r.prep_time+' + '+r.cook_time+'</span></div>'+
    '<h2>'+r.name+'</h2><div style="color:var(--text-dim);font-size:.85rem;margin-bottom:16px">Serves '+r.servings+kidBadge+'</div>'+
    nutBar+
    '<div class="detail-section"><div class="section-title">📝 Ingredients</div>'+ingHtml+'</div>'+
    '<div class="detail-section"><div class="section-title">👩‍🍳 Instructions</div>'+stepHtml+'</div>'+
    '<div class="detail-actions"><select class="plan-day-select" id="planDaySelect">'+dayOpts+'</select><button class="btn btn-primary" onclick="addToPlan('+r.id+')">📅 Add to Day</button><button class="btn btn-ghost" onclick="closeOverlay()">✕ Close</button></div>';
  document.getElementById('recipeOverlay').classList.add('open');document.body.style.overflow='hidden';
  document.getElementById('recipeOverlay').onclick=function(){closeOverlay();};
}
function closeOverlay(){document.getElementById('recipeOverlay').classList.remove('open');document.body.style.overflow='';}
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeOverlay()});
function addToPlan(id){var r=DATA.find(function(x){return x.id===id;});var day=document.getElementById('planDaySelect').value;mealPlan[day]=id;localStorage.setItem('mealPlan',JSON.stringify(mealPlan));showToast(r.name+' → '+day);closeOverlay();renderPlanner();}
function removeFromPlan(day){delete mealPlan[day];localStorage.setItem('mealPlan',JSON.stringify(mealPlan));renderPlanner();showToast('Removed from '+day);}
function clearPlan(){if(!confirm('Clear entire plan?'))return;mealPlan={};localStorage.setItem('mealPlan',JSON.stringify(mealPlan));renderPlanner();showToast('Plan cleared');}
function renderPlanner(){var g=document.getElementById('plannerGrid');g.innerHTML='';
  DAYS.forEach(function(day){var rid=mealPlan[day];var r=rid?DATA.find(function(x){return x.id===rid;}):null;
  var d=document.createElement('div');d.className='planner-day';
  var h4=document.createElement('h4');h4.textContent=day;d.appendChild(h4);
  if(r){var wrap=document.createElement('div');wrap.style.fontSize='.75rem';wrap.style.marginBottom='6px';
  var tag=document.createElement('span');tag.style.cssText='display:inline-block;padding:2px 8px;border-radius:6px;color:#fff;font-weight:700;font-size:.65rem;background:'+r.color;tag.textContent=r.icon+' '+r.category;
  wrap.appendChild(tag);d.appendChild(wrap);
  var an=document.createElement('div');an.className='assigned';an.textContent=r.name;an.onclick=function(){openRecipe(r.id);};d.appendChild(an);
  var rm=document.createElement('button');rm.className='remove-btn';rm.textContent='✕ Remove';rm.onclick=function(){removeFromPlan(day);};d.appendChild(rm);
  }else{var em=document.createElement('div');em.className='planner-empty';em.textContent='Tap a recipe to assign →';d.appendChild(em);}g.appendChild(d);});}
function renderGrocery(){
  var content=document.getElementById('groceryContent');var assigned=DAYS.filter(function(d){return mealPlan[d];});
  if(!assigned.length){content.innerHTML='<div class="empty-state"><div class="emoji">📅</div><p>No meals planned yet.<br>Go to <strong>📅 Meal Plan</strong> to assign recipes first!</p></div>';return;}
  var byCat={};assigned.forEach(function(day){var r=DATA.find(function(x){return x.id===mealPlan[day];});if(!r)return;if(!byCat[r.category])byCat[r.category]=[];byCat[r.category].push({name:r.name,icon:r.icon,color:r.color,day:day,ingredients:r.ingredients});});
  var catOrder=['CHICKEN','TURKEY','SALMON & FISH','BEEF','PORK & SAUSAGE','VEGETARIAN'];
  var h='<p style="margin-bottom:16px;color:var(--text-dim);font-size:.85rem">🛒 '+assigned.length+' meals planned — ingredients grouped by category</p>';
  catOrder.forEach(function(cat){if(!byCat[cat])return;var items=byCat[cat];var color=items[0].color;
  h+='<div class="grocery-section"><h3><span class="cat-badge" style="background:'+color+'">'+items[0].icon+' '+cat+'</span><span style="font-size:.75rem;color:var(--text-dim);font-weight:400;margin-left:8px">— '+items.length+' meal(s)</span></h3><div class="grocery-items">';
  var seen={};items.forEach(function(item){item.ingredients.forEach(function(ing){var key=ing.toLowerCase();if(seen[key])return;seen[key]=1;
  var gid=cat.replace(/[^a-zA-Z0-9]/g,'_')+'_'+ing.substring(0,30).replace(/[^a-zA-Z0-9]/g,'_');var ck=checkedG[gid]?' checked':'';var cls=checkedG[gid]?'grocery-item checked':'grocery-item';
  h+='<div class="'+cls+'"><input type="checkbox"'+ck+' data-gid="'+gid+'" onchange="toggleG(\''+gid.replace(/'/g,"\\'")+'\')"><label>'+ing+'</label></div>';});});h+='</div></div>';});
  h+='<div class="grocery-section" style="border:1.5px dashed var(--border)"><h3>✏️ Extra Items / Notes</h3><textarea class="notes-area" id="groceryNotes" placeholder="Pantry staples, snacks, drinks…">'+notesData+'</textarea><button class="action-btn" style="margin-top:10px" onclick="saveNotes()">💾 Save Notes</button></div>';
  content.innerHTML=h;}
function toggleG(gid){if(checkedG[gid])delete checkedG[gid];else checkedG[gid]=1;localStorage.setItem('checkedG',JSON.stringify(checkedG));var row=document.querySelector('.grocery-item:has(input[data-gid="'+gid+'"])');if(row)row.classList.toggle('checked',!!checkedG[gid]);}
function resetChecks(){checkedG={};localStorage.removeItem('checkedG');renderGrocery();showToast('All checks reset');}
function saveNotes(){notesData=document.getElementById('groceryNotes').value;localStorage.setItem('groceryNotes',notesData);showToast('Notes saved 💾');}
function showToast(msg){var t=document.getElementById('toast');t.textContent='✅ '+msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show');},2800);}
init();
</script>
</body>
</html>"""

# Replace placeholder with actual data
HTML = HTML.replace("__DATA_PLACEHOLDER__", js_data)

with open("/home/heb/.hermes/recipe-site/index.html", "w", encoding="utf-8") as f:
    f.write(HTML)

print(f"✅ Built index.html ({len(HTML):,} bytes)")
print(f"📊 {len(recipes)} recipes with full ingredients, steps, and nutrition")
