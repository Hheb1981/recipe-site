import json, os

os.makedirs("/home/heb/.hermes/recipe-site", exist_ok=True)

with open("/home/heb/.hermes/recipe-site/recipes.json", "r") as f:
    recipes_json = f.read()

# Build the complete HTML as a proper Python string
html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🍽️ Family Meal Planner — 50 Recipes</title>
<style>
:root{--bg:#1a1a2e;--bg-card:#16213e;--bg-card-hover:#1a2744;--text:#e0e0e0;--text-dim:#8892a4;--accent:#388E3C;--accent-light:#4CAF50;--border:#2a3a5c;--chip-bg:#1e2d4a;--header-bg:#0f1923;--shadow:0 2px 12px rgba(0,0,0,.3);--radius:12px}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
header{background:var(--header-bg);border-bottom:2px solid var(--accent);padding:16px 24px;position:sticky;top:0;z-index:100}
.header-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}
.logo{font-size:1.4rem;font-weight:800;letter-spacing:-.5px}.logo span{color:var(--accent-light)}
.nav-tabs{display:flex;gap:4px;background:var(--bg-card);padding:4px;border-radius:10px}
.nav-tab{padding:8px 18px;border:none;background:none;color:var(--text-dim);cursor:pointer;border-radius:8px;font-size:.85rem;font-weight:600;transition:all .2s}
.nav-tab:hover{color:var(--text);background:rgba(255,255,255,.05)}.nav-tab.active{background:var(--accent);color:#fff}
.search-wrap{position:relative}
.search-input{background:var(--bg-card);border:1px solid var(--border);color:var(--text);padding:8px 14px 8px 36px;border-radius:8px;width:220px;font-size:.85rem;outline:none;transition:border-color .2s}
.search-input:focus{border-color:var(--accent-light)}
.search-icon{position:absolute;left:10px;top:50%;transform:translateY(-50%);color:var(--text-dim);font-size:.9rem;pointer-events:none}
main{max-width:1200px;margin:0 auto;padding:24px}
.page{display:none}.page.active{display:block}
.category-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px}
.filter-btn{padding:8px 16px;border:2px solid transparent;border-radius:20px;cursor:pointer;font-size:.8rem;font-weight:700;background:var(--chip-bg);color:var(--text);transition:all .2s;display:flex;align-items:center;gap:6px}
.filter-btn:hover{transform:translateY(-1px)}.filter-btn.active{color:#fff}
.filter-btn[data-cat="all"]{border-color:var(--accent)}.filter-btn[data-cat="all"].active{background:var(--accent)}
.stats-bar{display:flex;gap:16px;margin-bottom:24px;flex-wrap:wrap}
.stat-chip{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:8px 16px;font-size:.8rem;color:var(--text-dim)}.stat-chip strong{color:var(--text);font-size:1.1rem}
.recipe-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.recipe-card{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;cursor:pointer;transition:all .2s;position:relative;overflow:hidden}
.recipe-card:hover{background:var(--bg-card-hover);transform:translateY(-2px);box-shadow:var(--shadow);border-color:var(--accent)}
.recipe-card .card-accent{position:absolute;top:0;left:0;right:0;height:4px}
.recipe-card .card-top{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:8px}
.recipe-card .card-icon{font-size:1.6rem;line-height:1}
.recipe-card .card-number{font-size:.7rem;color:var(--text-dim);font-weight:600}
.recipe-card .card-name{font-size:.95rem;font-weight:700;line-height:1.3;margin-bottom:10px}
.card-tag{font-size:.7rem;font-weight:700;padding:3px 10px;border-radius:10px;color:#fff;text-transform:uppercase;letter-spacing:.5px}
.no-results{text-align:center;padding:60px 20px;color:var(--text-dim);font-size:1rem}
.no-results .emoji{font-size:2.5rem;margin-bottom:12px}
.overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.7);z-index:200;backdrop-filter:blur(4px);overflow-y:auto;padding:24px}
.overlay.open{display:flex;justify-content:center;align-items:flex-start}
.overlay-card{background:var(--bg-card);border:1px solid var(--border);border-radius:16px;max-width:700px;width:100%;margin:24px auto;position:relative;overflow:hidden}
.overlay-close{position:absolute;top:16px;right:16px;background:rgba(0,0,0,.4);color:#fff;border:none;width:36px;height:36px;border-radius:50%;font-size:1.2rem;cursor:pointer;z-index:10;display:flex;align-items:center;justify-content:center}
.overlay-close:hover{background:rgba(0,0,0,.7)}.overlay-banner{height:8px;width:100%}.overlay-body{padding:28px 32px 32px}
.overlay-body .cat-badge{display:inline-block;font-size:.72rem;font-weight:800;padding:4px 14px;border-radius:12px;color:#fff;text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px}
.overlay-body h2{font-size:1.5rem;font-weight:800;margin-bottom:6px;line-height:1.2}
.overlay-body .subtitle{color:var(--text-dim);font-size:.85rem;margin-bottom:24px}
.detail-section{margin-bottom:20px}.detail-section h3{font-size:.85rem;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--accent-light);margin-bottom:10px;padding-bottom:6px;border-bottom:1px solid var(--border)}
.detail-section ul{list-style:none}.detail-section ul li{padding:6px 0;font-size:.9rem;border-bottom:1px solid rgba(255,255,255,.03)}
.detail-actions{display:flex;gap:10px;margin-top:24px;flex-wrap:wrap;align-items:center}
.btn{padding:10px 22px;border:none;border-radius:8px;font-size:.85rem;font-weight:700;cursor:pointer;transition:all .2s}
.btn-primary{background:var(--accent);color:#fff}.btn-primary:hover{background:var(--accent-light)}
.btn-ghost{background:transparent;color:var(--text);border:1px solid var(--border)}.btn-ghost:hover{background:rgba(255,255,255,.05)}
.plan-day-select{background:var(--bg);border:1px solid var(--border);color:var(--text);padding:8px 12px;border-radius:8px;font-size:.85rem;outline:none}
.plan-day-select:focus{border-color:var(--accent-light)}
.planner-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.planner-day{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:16px;min-height:140px}
.planner-day h4{font-size:.8rem;font-weight:800;text-transform:uppercase;letter-spacing:1px;color:var(--accent-light);margin-bottom:10px}
.planner-day .assigned{font-size:.85rem;font-weight:600;line-height:1.3}
.planner-day .remove-btn{background:none;border:none;color:var(--text-dim);cursor:pointer;font-size:.7rem;padding:0;margin-top:6px;display:block}
.planner-day .remove-btn:hover{color:#ff5252}
.planner-empty{color:var(--text-dim);font-size:.8rem;font-style:italic}
.grocery-section{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin-bottom:16px}
.grocery-section h3{font-size:1rem;font-weight:800;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.grocery-items{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:6px}
.grocery-item{display:flex;align-items:center;gap:8px;font-size:.85rem;padding:4px 0}
.grocery-item input[type=checkbox]{accent-color:var(--accent);width:16px;height:16px;cursor:pointer}
.grocery-item.checked label{text-decoration:line-through;color:var(--text-dim)}
.notes-area{width:100%;background:var(--bg);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:12px;font-size:.85rem;min-height:80px;resize:vertical;font-family:inherit;outline:none;margin-top:8px}
.notes-area:focus{border-color:var(--accent-light)}
.toast{position:fixed;bottom:24px;right:24px;background:var(--accent);color:#fff;padding:12px 24px;border-radius:10px;font-size:.85rem;font-weight:700;z-index:300;transform:translateY(80px);opacity:0;transition:all .3s;box-shadow:0 4px 16px rgba(0,0,0,.4)}
.toast.show{transform:translateY(0);opacity:1}
.top-actions{display:flex;align-items:center;gap:10px;margin-left:auto}
.action-btn{background:var(--bg-card);border:1px solid var(--border);color:var(--text);padding:10px 16px;border-radius:8px;font-size:.8rem;font-weight:700;cursor:pointer;display:flex;align-items:center;gap:6px;transition:all .2s}
.action-btn:hover{background:rgba(255,255,255,.05)}
.pagination{display:flex;gap:6px;justify-content:center;margin-top:32px}
.pg-btn{padding:8px 14px;border:1px solid var(--border);background:var(--bg-card);color:var(--text);border-radius:8px;cursor:pointer;font-size:.8rem;font-weight:700}
.pg-btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.pg-btn:hover:not(.active){background:rgba(255,255,255,.05)}
@media(max-width:640px){.header-inner{flex-direction:column;align-items:flex-start}.recipe-grid{grid-template-columns:1fr}.planner-grid{grid-template-columns:1fr 1fr}.overlay-body{padding:20px}}
</style>
</head>
<body>
<header>
  <div class="header-inner">
    <div class="logo">🍽️ Family <span>Meal Planner</span></div>
    <div class="nav-tabs">
      <button class="nav-tab active" onclick="switchPage('browse',this)">📋 Recipes</button>
      <button class="nav-tab" onclick="switchPage('planner',this)">📅 Meal Plan</button>
      <button class="nav-tab" onclick="switchPage('grocery',this)">🛒 Grocery</button>
    </div>
    <div class="search-wrap">
      <span class="search-icon">🔍</span>
      <input class="search-input" type="text" placeholder="Search recipes…" id="searchInput" oninput="renderRecipes()">
    </div>
  </div>
</header>
<main>
<div id="page-browse" class="page active">
  <div class="category-bar" id="categoryBar"></div>
  <div class="stats-bar" id="statsBar"></div>
  <div class="recipe-grid" id="recipeGrid"></div>
  <div class="no-results" id="noResults" style="display:none"><div class="emoji">🤔</div>No recipes found. Try a different filter or search.</div>
  <div class="pagination" id="pagination"></div>
</div>
<div id="page-planner" class="page">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;flex-wrap:wrap">
    <h2 style="font-size:1.3rem;font-weight:800">📅 Weekly Meal Planner</h2>
    <button class="action-btn" onclick="window.print()">🖨️ Print</button>
    <button class="action-btn" onclick="clearPlan()">🗑️ Clear All</button>
  </div>
  <div class="planner-grid" id="plannerGrid"></div>
</div>
<div id="page-grocery" class="page">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;flex-wrap:wrap">
    <h2 style="font-size:1.3rem;font-weight:800">🛒 Grocery List</h2>
    <button class="action-btn" onclick="window.print()">🖨️ Print</button>
    <button class="action-btn" onclick="resetChecks()">☑️ Reset Checks</button>
  </div>
  <div id="groceryContent"></div>
</div>
</main>
<div class="overlay" id="recipeOverlay" onclick="if(event.target===this)closeOverlay()">
  <div class="overlay-card">
    <button class="overlay-close" onclick="closeOverlay()">✕</button>
    <div class="overlay-banner" id="overlayBanner"></div>
    <div class="overlay-body" id="overlayBody"></div>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
var RECIPES=""" + recipes_json + """;
var DAYS=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
var currentFilter='all', currentPage=0, perPage=18;
var mealPlan=JSON.parse(localStorage.getItem('mealPlan')||'{}');
var checkedG=JSON.parse(localStorage.getItem('checkedG')||'{}');

function init(){
  var cats=[];RECIPES.forEach(r){if(cats.indexOf(r.category)<0)cats.push(r.category);};
  var bar=document.getElementById('categoryBar');
  bar.innerHTML='<button class="filter-btn active" data-cat="all" style="border-color:#388E3C" onclick="setFilter(\\'all\\',this)">📋 All ('+RECIPES.length+')</button>';
  cats.forEach(function(cat){
    var c=RECIPES.find(function(r){return r.category===cat;});
    var n=RECIPES.filter(function(r){return r.category===cat;}).length;
    var b=document.createElement('button');
    b.className='filter-btn';b.dataset.cat=cat;
    b.innerHTML=c.icon+' '+cat+' ('+n+')';b.onclick=function(){setFilter(cat,null);};
    bar.appendChild(b);
  });
  buildStats();
}
function buildStats(){
  var cats=[];RECIPES.forEach(function(r){if(cats.indexOf(r.category)<0)cats.push(r.category);});
  var sb=document.getElementById('statsBar');
  sb.innerHTML='<div class="stat-chip"><strong>'+RECIPES.length+'</strong> total recipes</div>';
  cats.forEach(function(cat){
    var c=RECIPES.find(function(r){return r.category===cat;});
    var n=RECIPES.filter(function(r){return r.category===cat;}).length;
    sb.innerHTML+='<div class="stat-chip" style="border-left:3px solid '+c.color+'">'+c.icon+' <strong>'+n+'</strong> '+cat+'</div>';
  });
}
function switchPage(name,btn){
  document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active');});
  document.querySelectorAll('.nav-tab').forEach(function(t){t.classList.remove('active');});
  document.getElementById('page-'+name).classList.add('active');
  if(btn)btn.classList.add('active');
  if(name==='grocery')renderGrocery();
  if(name==='planner')renderPlanner();
}
function setFilter(cat,btn){
  currentFilter=cat;currentPage=0;
  document.querySelectorAll('.filter-btn').forEach(function(b){b.classList.remove('active');});
  if(btn){btn.classList.add('active');}
  else{document.querySelectorAll('.filter-btn').forEach(function(b){if(b.dataset.cat===cat)b.classList.add('active');});}
  renderRecipes();
}
function escapeJs(s){return s.replace(/'/g,"\\\\'").replace(/"/g,'\\\\"').replace(/\\n/g,'\\\\n');}
function getFiltered(){
  var q=document.getElementById('searchInput').value.toLowerCase().trim();
  return RECIPES.filter(function(r){
    if(currentFilter!=='all'&&r.category!==currentFilter)return false;
    if(q&&r.name.toLowerCase().indexOf(q)<0&&r.category.toLowerCase().indexOf(q)<0)return false;
    return true;
  });
}
function renderRecipes(){
  var f=getFiltered();
  var grid=document.getElementById('recipeGrid');
  var nr=document.getElementById('noResults');
  var pg=document.getElementById('pagination');
  if(!f.length){grid.innerHTML='';nr.style.display='block';pg.innerHTML='';return;}
  nr.style.display='none';
  var totalPages=Math.ceil(f.length/perPage);
  if(currentPage>=totalPages)currentPage=totalPages-1;
  var start=currentPage*perPage;
  var pageItems=f.slice(start,start+perPage);
  grid.innerHTML=pageItems.map(function(r){
    return '<div class="recipe-card" onclick="openRecipe('+r.id+')">'+
      '<div class="card-accent" style="background:'+r.color+'"></div>'+
      '<div class="card-top"><span class="card-icon">'+r.icon+'</span><span class="card-number">#'+String(r.id).padStart(2,'0')+'</span></div>'+
      '<div class="card-name">'+r.name+'</div>'+
      '<div style="margin-top:8px"><span class="card-tag" style="background:'+r.color+'">'+r.category+'</span></div>'+
    '</div>';
  }).join('');
  if(totalPages>1){
    var btns='';
    for(var i=0;i<totalPages;i++){
      btns+='<button class="pg-btn'+(i===currentPage?' active':'')+'" onclick="goPage('+i+')">'+(i+1)+'</button>';
    }
    pg.innerHTML=btns;
  }else{pg.innerHTML='';}
}
function goPage(p){currentPage=p;renderRecipes();window.scrollTo({top:300,behavior:'smooth'});}
function openRecipe(id){
  var r=RECIPES.find(function(x){return x.id===id;});if(!r)return;
  document.getElementById('overlayBanner').style.background='linear-gradient(90deg,'+r.color+','+r.color_light+')';
  var dayOpts=DAYS.map(function(d){return '<option value="'+d+'">'+d+'</option>';}).join('');
  document.getElementById('overlayBody').innerHTML=
    '<span class="cat-badge" style="background:'+r.color+'">'+r.icon+' '+r.category+'</span>'+
    '<h2>'+r.name+'</h2>'+
    '<div class="subtitle">#'+String(r.id).padStart(2,'0')+' · '+r.category+'</div>'+
    '<div class="detail-section"><h3>📝 Ingredients</h3><ul><li style="color:var(--text-dim)">Full ingredient list available in the PDF recipe card for this meal.</li></ul></div>'+
    '<div class="detail-section"><h3>👩‍🍳 Instructions</h3><ul><li style="color:var(--text-dim)">Step-by-step instructions available in the PDF recipe card.</li></ul></div>'+
    '<div class="detail-section"><h3>📊 Nutrition</h3><ul><li style="color:var(--text-dim)">Nutrition information available in the PDF recipe card.</li></ul></div>'+
    '<div class="detail-actions">'+
      '<select class="plan-day-select" id="planDaySelect">'+dayOpts+'</select>'+
      '<button class="btn btn-primary" onclick="addToPlan('+r.id+')">📅 Add to Day</button>'+
      '<button class="btn btn-ghost" onclick="closeOverlay()">✕ Close</button>'+
    '</div>';
  document.getElementById('recipeOverlay').classList.add('open');
  document.body.style.overflow='hidden';
}
function closeOverlay(){
  document.getElementById('recipeOverlay').classList.remove('open');
  document.body.style.overflow='';
}
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeOverlay()});
function addToPlan(id){
  var r=RECIPES.find(function(x){return x.id===id;});
  var day=document.getElementById('planDaySelect').value;
  mealPlan[day]=id;localStorage.setItem('mealPlan',JSON.stringify(mealPlan));
  showToast('✅ \"'+r.name+'\" added to '+day);closeOverlay();renderPlanner();
}
function removeFromPlan(day){
  delete mealPlan[day];localStorage.setItem('mealPlan',JSON.stringify(mealPlan));
  renderPlanner();showToast('🗑️ Removed from '+day);
}
function clearPlan(){
  if(!confirm('Clear entire meal plan?'))return;
  mealPlan={};localStorage.setItem('mealPlan',JSON.stringify(mealPlan));
  renderPlanner();showToast('🗑️ Plan cleared');
}
function renderPlanner(){
  document.getElementById('plannerGrid').innerHTML=DAYS.map(function(day){
    var rid=mealPlan[day];var r=rid?RECIPES.find(function(x){return x.id===rid;}):null;
    return '<div class="planner-day"><h4>'+day+'</h4>'+
      (r?'<div style="font-size:.75rem;margin-bottom:4px"><span style="display:inline-block;padding:2px 8px;border-radius:6px;color:#fff;font-weight:700;font-size:.65rem;background:'+r.color+'">'+r.icon+' '+r.category+'</span></div>'+
      '<div class="assigned" style="cursor:pointer" onclick="openRecipe('+r.id+')">'+r.name+'</div>'+
      '<button class="remove-btn" onclick="removeFromPlan(\\''+day.replace(/'/g,"\\\\'")+'\\')">✕ Remove</button>'
      :'<div class="planner-empty">Tap a recipe to assign</div>')+
    '</div>';
  }).join('');
}
function renderGrocery(){
  var content=document.getElementById('groceryContent');
  var assigned=DAYS.filter(function(d){return mealPlan[d];});
  if(!assigned.length){
    content.innerHTML='<p style="color:var(--text-dim);padding:40px;text-align:center">No meals planned yet. Go to 📅 Meal Plan to assign recipes first!</p>';
    return;
  }
  var byCat={};
  assigned.forEach(function(day){
    var r=RECIPES.find(function(x){return x.id===mealPlan[day];});
    if(!r)return;
    if(!byCat[r.category])byCat[r.category]=[];
    byCat[r.category].push({name:r.name,icon:r.icon,color:r.color,day:day});
  });
  var catOrder=['CHICKEN','TURKEY','SALMON & FISH','BEEF','PORK & SAUSAGE','VEGETARIAN'];
  var h='<p style="margin-bottom:16px;color:var(--text-dim);font-size:.85rem">📅 '+assigned.length+' meal(s) planned for the week</p>';
  catOrder.forEach(function(cat){
    if(!byCat[cat])return;
    var items=byCat[cat];var color=items[0].color;
    h+='<div class="grocery-section"><h3><span style="color:'+color+'">'+items[0].icon+'</span> '+cat+' <span style="font-size:.75rem;color:var(--text-dim);font-weight:400">— '+items.length+' meal(s)</span></h3><div class="grocery-items">';
    items.forEach(function(item,i){
      var gid=cat.replace(/[^a-z]/gi,'_')+'-'+i;
      var checked=checkedG[gid]?' checked':'';
      var cls=checkedG[gid]?'grocery-item checked':'grocery-item';
      h+='<div class="'+cls+'"><input type="checkbox"'+checked+' onchange="toggleG(\\''+gid.replace(/'/g,"\\\\'")+'\\')"><label><strong>'+item.name+'</strong> <span style="color:var(--text-dim)">('+item.day+')</span></label></div>';
    });
    h+='</div></div>';
  });
  h+='<div class="grocery-section" style="border:1px dashed var(--border)"><h3>✏️ Extra Items / Notes</h3><textarea class="notes-area" id="groceryNotes" placeholder="Add items that don\'t need a recipe (milk, bread, fruit, snacks…)">';
  h+=notesData||'';
  h+='<'+'/textarea><button class="btn btn-ghost" style="margin-top:8px" onclick="saveNotes()">💾 Save Notes</button></div>';
  content.innerHTML=h;
  if(notesData)document.getElementById('groceryNotes').value=notesData;
}
function toggleG(gid){
  if(checkedG[gid])delete checkedG[gid];else checkedG[gid]=1;
  localStorage.setItem('checkedG',JSON.stringify(checkedG));
  var el=document.querySelector('input[onchange*="'+gid+'"]');
  if(el){var row=el.closest('.grocery-item');if(row)row.classList.toggle('checked',checkedG[gid]);}
}
function resetChecks(){
  checkedG={};localStorage.removeItem('checkedG');renderGrocery();showToast('☑️ All checks reset');
}
function saveNotes(){
  notesData=document.getElementById('groceryNotes').value;
  localStorage.setItem('groceryNotes',notesData);
  showToast('💾 Notes saved');
}
function showToast(msg){
  var t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');
  setTimeout(function(){t.classList.remove('show');},2500);
}
init();renderRecipes();
</script>
</body>
</html>"""

with open("/home/heb/.hermes/recipe-site/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done! File size:", len(html), "chars")
print("Pages: Browse (grid+pagination), Meal Plan (7-day), Grocery List (grouped by category)")
