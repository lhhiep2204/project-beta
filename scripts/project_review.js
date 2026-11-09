/* Owner review UI only. Never writes approval or production state to the repository. */
(() => {
  'use strict';
  const payload = JSON.parse(document.getElementById('review-payload').textContent);
  const contract = JSON.parse(document.getElementById('project-contract').textContent);
  const byId = id => document.getElementById(id);
  const picker = byId('document-picker');
  function populateDocuments(query = '') {
    const term = query.trim();
    const normalized = term.normalize('NFD').replace(/\p{Mark}/gu,'').toLowerCase();
    picker.replaceChildren(new Option('Chọn bài hoặc tài liệu…',''));
    const matches = Object.entries(payload.documents).filter(([path,doc]) =>
      (path+' '+doc.title).normalize('NFD').replace(/\p{Mark}/gu,'').toLowerCase().includes(normalized)
    );
    matches.forEach(([path,doc]) => picker.add(new Option(doc.title+' · '+path.replace('docs/',''), path)));

    const status = byId('document-match-status');
    const results = byId('document-matches');
    results.replaceChildren();
    if (!term) {
      status.textContent = 'Gõ tên bài hoặc tài liệu để hiện kết quả có thể bấm mở; bạn cũng có thể chọn trong danh sách bên dưới.';
      return;
    }
    if (!matches.length) {
      status.textContent = 'Không tìm thấy tài liệu phù hợp. Thử số bài, N5/N4 hoặc Kanji.';
      return;
    }
    const visibleMatches = matches.slice(0, 12);
    status.textContent = matches.length > visibleMatches.length
      ? `Tìm thấy ${matches.length} tài liệu; hiện ${visibleMatches.length} kết quả đầu. Dùng danh sách chọn bên dưới để mở kết quả khác.`
      : `Tìm thấy ${matches.length} tài liệu. Bấm tên tài liệu để mở.`;
    visibleMatches.forEach(([path,doc]) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'secondary';
      button.dataset.documentPath = path;
      button.textContent = doc.title+' · '+path.replace('docs/','');
      results.append(button);
    });
  }
  function openDocument(path, fragment = '') {
    const doc = payload.documents[path];
    byId('document').innerHTML = doc ? doc.html : '<p>Tài liệu này chưa có trong snapshot. Không coi đây là nội dung đã duyệt.</p>';
    byId('document').scrollTop = 0;
    byId('document').scrollIntoView({block:'start'});
    byId('document').focus({preventScroll:true});
    if(fragment){
      const anchor=[...byId('document').querySelectorAll('[data-source-anchor]')].find(node=>node.dataset.sourceAnchor===fragment);
      if(anchor)anchor.scrollIntoView({block:'start'});
    }
    if ([...picker.options].some(o=>o.value===path)) picker.value=path;
  }
  populateDocuments();
  byId('document-filter').addEventListener('input',e=>populateDocuments(e.target.value));
  picker.addEventListener('change',()=> { if(picker.value)openDocument(picker.value); });
  byId('document-matches').addEventListener('click',event=>{
    const button=event.target.closest('button[data-document-path]');
    if(button)openDocument(button.dataset.documentPath);
  });
  document.addEventListener('click',event=>{
    const link=event.target.closest('[data-doc]');
    if(link){event.preventDefault();openDocument(link.dataset.doc,link.dataset.fragment);}
  });
  const links=byId('agent-document-links');
  Object.keys(contract.documents).forEach(path=>{
    const a=document.createElement('a');a.href='#document';a.dataset.doc=path;a.textContent=payload.documents[path]?.title||path;links.append(a);
  });
  function showPrototype(kind){
    const frame=document.createElement('iframe');
    frame.title=kind==='app'?'ProjectBeta app review simulation':'ProjectBeta typography and widget simulation';
    frame.setAttribute('sandbox','allow-scripts');
    frame.srcdoc=payload.prototypes[kind];
    byId('prototype-host').replaceChildren(frame);
  }
  document.querySelectorAll('[data-prototype]').forEach(button=>button.addEventListener('click',()=>showPrototype(button.dataset.prototype)));
  window.addEventListener('message',event=>{
    const frame=byId('prototype-host').querySelector('iframe');
    if(frame && event.source===frame.contentWindow && event.data?.projectBetaOpenApp===true)showPrototype('app');
  });
  byId('close-prototype').addEventListener('click',()=>byId('prototype-host').replaceChildren());
  const taskGroups=[...document.querySelectorAll('.task-group')];
  const normalizeTask=value=>value.normalize('NFD').replace(/\p{Mark}/gu,'').replace(/[đĐ]/g,'d').toLowerCase();
  function filterTasks(){
    const filter=byId('task-filter').value, phase=byId('task-phase').value, query=normalizeTask(byId('task-query').value.trim());
    let visibleGroups=0, visibleStories=0;
    taskGroups.forEach(group=>{
      const children=[...group.querySelectorAll('.task-story')];
      const groupMatch=normalizeTask(group.dataset.taskSearch).includes(query);
      const phaseMatch=phase==='all'||phase===group.dataset.phase;
      const priorityMatch=filter==='all'||filter===group.dataset.priority;
      children.forEach(story=>{
        story.hidden=!phaseMatch||!(priorityMatch||filter===story.dataset.status)||!(groupMatch||normalizeTask(story.dataset.taskSearch).includes(query));
        if(!story.hidden)visibleStories++;
      });
      group.querySelectorAll('.task-area').forEach(heading=>{
        let next=heading.nextElementSibling, hasVisible=false;
        while(next?.classList.contains('task-story')){
          hasVisible ||= !next.hidden;next=next.nextElementSibling;
        }
        heading.hidden=!hasVisible;
      });
      group.hidden=!phaseMatch||(children.length?!children.some(story=>!story.hidden):!(priorityMatch||filter===group.dataset.status)||!groupMatch);
      if(!group.hidden)visibleGroups++;
    });
    byId('task-results').textContent=visibleGroups?`Đang hiển thị ${visibleGroups} nhóm, ${visibleStories} mục chi tiết (gồm ánh xạ T01 nếu khớp bộ lọc).`:'Không có task khớp bộ lọc. Thử tên tính năng, màn hình hoặc ID khác.';
  }
  byId('task-filter').addEventListener('change',filterTasks);
  byId('task-phase').addEventListener('change',filterTasks);
  byId('task-query').addEventListener('input',filterTasks);
  function revealTask(){
    const id=location.hash.slice(1),target=byId(id);
    if(!target?.matches('.task-story,.task-group'))return;
    if(target.hidden||target.closest('.task-group')?.hidden){
      byId('task-phase').value='all';byId('task-filter').value='all';byId('task-query').value='';filterTasks();
    }
    if(target.matches('.task-story'))target.open=true;
    target.scrollIntoView({block:'start'});
  }
  window.addEventListener('hashchange',revealTask);
  // Clicking the current hash must also recover a task hidden by a later filter.
  document.addEventListener('click',event=>{
    const anchor=event.target.closest('a[href^="#T"]');
    if(anchor?.hash===location.hash)revealTask();
  });
  filterTasks();revealTask();
  document.querySelectorAll('[data-history]').forEach(button=>button.addEventListener('click',()=>{byId('history-reader').innerHTML=payload.history[button.dataset.history];byId('history-reader').scrollTop=0;}));
  // A final document can have no open decision form.
  if (byId('export-review')) {
  const key='projectbeta-owner-review-'+payload.version;
  let notes={};let storage=true;
  try{notes=JSON.parse(localStorage.getItem(key)||'{}');if(!notes||typeof notes!=='object')notes={};}catch{storage=false;}
  const inputs=[...document.querySelectorAll('[data-decision],[data-note],#overall-note')];
  const name=input=>input.dataset.decision?'decision-'+input.dataset.decision:input.dataset.note?'note-'+input.dataset.note:'overall';
  function storageMessage(){byId('review-storage').textContent=storage?'Ghi chú chỉ lưu cục bộ cho phiên bản này. Chưa gửi, chưa duyệt repository.':'Trình duyệt không cho lưu: ghi chú chỉ còn trong phiên này. Hãy xuất/copy trước khi đóng.';}
  inputs.forEach(input=>{
    if(typeof notes[name(input)]==='string')input.value=notes[name(input)];
    input.addEventListener('input',()=>{
      notes[name(input)]=input.value;
      try{localStorage.setItem(key,JSON.stringify(notes));}catch{storage=false;}
      storageMessage();
    });
  });storageMessage();
  byId('export-review').addEventListener('click',()=>{
    inputs.forEach(input=>notes[name(input)]=input.value);
    const lines=['ProjectBeta owner review','Review SHA-256 (contract + curriculum + presentation): '+payload.version,'Exported: '+new Date().toISOString(),'These are user review selections, not automatically recorded repository approvals.',''];
    const labels={unreviewed:'Chưa xem',agree:'Đồng ý đề xuất',change:'Cần điều chỉnh'};
    contract.questions.forEach(q=>lines.push(q.id+' — '+q.title,labels[notes['decision-'+q.id]]||'Chưa xem','Ghi chú: '+(notes['note-'+q.id]||''),''));
    lines.push('Nhận xét chung: '+(notes.overall||''));
    byId('review-export').value=lines.join('\n');byId('review-export').hidden=false;byId('review-export').focus();byId('review-export').select();
  });
  }
  if('IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>{
      for(const entry of entries)if(entry.isIntersecting){document.querySelectorAll('.navigation nav a').forEach(a=>{if(a.hash==='#'+entry.target.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});}
    },{rootMargin:'-5% 0px -70% 0px'});
    document.querySelectorAll('.review-main>section').forEach(section=>observer.observe(section));
  }
})();
