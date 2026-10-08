function toggleSidebar(){
  document.getElementById('sidebar').classList.toggle('open');
}
function openModal(){ document.getElementById('modal').classList.add('show'); }
function closeModal(){ document.getElementById('modal').classList.remove('show'); }
window.addEventListener('click', e => {
  const modal=document.getElementById('modal');
  if(e.target===modal) closeModal();
});
let activeStatus='all';
function filterStatus(status, btn){
  activeStatus=status;
  document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  filterRows();
}
function filterRows(){
  const query=(document.getElementById('searchInput')?.value || '').toLowerCase();
  document.querySelectorAll('#appointmentTable tbody tr').forEach(row=>{
    const text=row.innerText.toLowerCase();
    const status=row.dataset.status;
    const statusMatch=activeStatus==='all' || status===activeStatus;
    row.style.display=(statusMatch && text.includes(query)) ? '' : 'none';
  });
}
setTimeout(()=>document.querySelectorAll('.toast').forEach(x=>x.remove()), 3600);
