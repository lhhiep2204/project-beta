#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Export agent docs and refresh owner review from the canonical contract in docs/index.html.

Edit project-contract in that HTML for product/flow/task changes. Editorial JSON and
PDF catalog remain data authorities; generated views are checked, never separately edited.
Standard library only. --check is read-only and fails on any stale generated output.
"""
from __future__ import annotations
import argparse, hashlib, html, json, re, subprocess
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'docs/index.html'
A = ROOT / 'docs/content-authoring'
S = ROOT / 'docs/design-system'

def read(p): return json.loads(p.read_text())
def encode(v): return json.dumps(v,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
def sha(b): return hashlib.sha256(b).hexdigest()
def esc(v): return html.escape(str(v),quote=True)
def anchor_id(source, fragment): return 'doc-'+sha((source+'#'+fragment).encode())[:16]
def extract(text): return json.loads(re.search(r'<script id="project-contract" type="application/json">(.*?)</script>',text,re.S)[1])
def inline(s, source='docs/index.html'):
    s=esc(s)
    def link(m):
        label,url=m[1],html.unescape(m[2]); parts=urlsplit(url)
        if url.startswith('#'):
            return f'<a href="#document" data-doc="{esc(source)}" data-fragment="{esc(unquote(parts.fragment))}">{label}</a>'
        if not parts.scheme and not url.startswith('#'):
            target=(ROOT/source).parent/unquote(parts.path)
            try: rel=str(target.resolve().relative_to(ROOT))
            except ValueError: return label
            if target.suffix=='.md':return f'<a href="#document" data-doc="{esc(rel)}" data-fragment="{esc(unquote(parts.fragment))}">{label}</a>'
            if target.resolve()==PAGE:return f'<a href="#{esc(parts.fragment or "overview")}">{label}</a>'
            url='../'+quote(rel,safe='/')+('#'+parts.fragment if parts.fragment else '')
        if parts.scheme and parts.scheme not in ('http','https'):return label
        return f'<a href="{esc(url)}">{label}</a>'
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    return s

def markdown(text,source):
    """Small safe renderer for repository headings/tables/lists/code/paragraphs."""
    result=[]; lines=text.splitlines(); i=0
    while i<len(lines):
        line=lines[i]; i+=1
        if not line.strip():continue
        anchor=re.fullmatch(r'<a id="([a-zA-Z0-9_-]+)"></a>',line.strip())
        if anchor:
            result.append(f'<span id="{anchor_id(source,anchor[1])}" data-source-anchor="{esc(anchor[1])}"></span>');continue
        if line.startswith('```'):
            block=[]
            while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
            i+=1;result.append('<pre><code>'+esc('\n'.join(block))+'</code></pre>');continue
        if line.startswith('|'):
            rows=[line]
            while i<len(lines) and lines[i].startswith('|'):rows.append(lines[i]);i+=1
            body=[]
            for n,row in enumerate(rows):
                cells=re.split(r'(?<!\\)\|',row.strip().strip('|'))
                if all(re.fullmatch(r'\s*:?-+:?\s*',c) for c in cells):continue
                tag='th' if n==0 else 'td'
                body.append('<tr>'+''.join(f'<{tag}>'+inline(c.strip().replace('\\|','|'),source)+f'</{tag}>' for c in cells)+'</tr>')
            result.append('<div class="table-wrap"><table>'+''.join(body)+'</table></div>');continue
        h=re.match(r'^(#{1,6}) (.*)',line)
        if h:
            level=min(6,len(h[1])+1);result.append(f'<h{level}>'+inline(h[2],source)+f'</h{level}>');continue
        if line.startswith('- ') or re.match(r'^\d+\. ',line):
            items=[line]
            while i<len(lines) and (lines[i].startswith('- ') or re.match(r'^\d+\. ',lines[i])):items.append(lines[i]);i+=1
            result.append('<ul>'+''.join('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',v),source)+'</li>' for v in items)+'</ul>');continue
        result.append('<p>'+inline(line,source)+'</p>')
    return '\n'.join(result)

def evidence():
    reconciliation=read(A/'source-reconciliation/validation-report.json')
    stale_evidence=[]
    for path,pin in {**reconciliation['input_sha256'],**reconciliation['implementation_sha256']}.items():
        current=sha((ROOT/path).read_bytes())
        if current!=pin:stale_evidence.append(dict(task='legacy T02 → H02',path=path,reviewed_sha256=pin,current_sha256=current))
    runtime=read(ROOT/'docs/audit/t01-runtime-validation.json')
    for path,pin in {**runtime['inputHashes'],**runtime['implementationHashes']}.items():
        current=sha((ROOT/path).read_bytes())
        if current!=pin:stale_evidence.append(dict(task='legacy T01 → H01',path=path,reviewed_sha256=pin,current_sha256=current))
    # A review generator must expose stale historical handoffs, not recertify or
    # rewrite them merely to publish an unrelated task. The audit still rejects
    # their drift through the original validators and runtime hash checks.
    kana=read(A/'kana/validation-report.json')
    for path,pin in kana['input_and_validator_sha256'].items():
        if sha((ROOT/path).read_bytes())!=pin:raise ValueError('Stale H03 authoring evidence (legacy T03): '+path)
    catalog=read(ROOT/'docs/reference-inventory/catalog.json')
    candidates=read(A/'sentence-bank/validation-report.json')
    for path,pin in candidates['input_and_validator_sha256'].items():
        current=sha((ROOT/path).read_bytes())
        if current!=pin:stale_evidence.append(dict(task='legacy T04 → H04',path=path,reviewed_sha256=pin,current_sha256=current))
    native_path=ROOT/'docs/audit/t05-native-validation.json'
    native=read(native_path) if native_path.exists() else None
    if native:
        for path,pin in {**native['inputHashes'],**native['implementationHashes']}.items():
            current=sha((ROOT/path).read_bytes())
            if current!=pin:stale_evidence.append(dict(task='legacy T05 → T01',path=path,reviewed_sha256=pin,current_sha256=current))
    closure_path=extract(PAGE.read_text()).get('native_proof',{}).get('closure_report')
    closure=read(ROOT/closure_path) if closure_path else None
    if closure:
        for path,pin in {**closure['inputHashes'],**closure['implementationHashes']}.items():
            current=sha((ROOT/path).read_bytes())
            if current!=pin:stale_evidence.append(dict(task='T01.02 physical audio',path=path,reviewed_sha256=pin,current_sha256=current))
    localization_path=ROOT/'docs/audit/t09-01-localization-validation.json'
    if localization_path.exists():
        localization=read(localization_path)
        for path,pin in {**localization['inputHashes'],**localization['implementationHashes']}.items():
            current=sha((ROOT/path).read_bytes())
            if current!=pin:stale_evidence.append(dict(task='legacy T09.01 → T05.01',path=path,reviewed_sha256=pin,current_sha256=current))
    lessons=[read(p) for p in sorted(A.glob('lesson-*.json'))]
    units=[read(p) for p in sorted((A/'kanji').glob('unit-*.json'))]
    chars=[e for p in sorted((A/'kanji').glob('characters-*.json')) for e in read(p)['entries']]
    coverage=read(A/'batch-source-coverage.json')
    source_rows=[]
    for s in catalog['sources']:
        b=(ROOT/s['relative_path']).read_bytes()
        info=subprocess.run(['pdfinfo',str(ROOT/s['relative_path'])],check=True,capture_output=True,text=True).stdout
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1])
        if pages!=s['page_count'] or sha(b)!=s['sha256']:raise ValueError('Source changed: '+s['id'])
        source_rows.append(dict(id=s['id'],pages=pages,sha256=sha(b),path=s['relative_path'],verified='hash_and_page_count'))
    current=[]
    for l in lessons:
        cov=next(x for x in coverage['lessons'] if x['lesson']==l['reference_lesson_number'])
        groups={str(g['source_topic_group']).split(':',1)[0].strip() for g in l['grammar_points']}
        if groups!=set(cov['source_grammar_groups_accounted_for']):raise ValueError('Grammar coverage drift')
        current.append(dict(number=l['reference_lesson_number'],level=l['source_level_label'],title=l['title']['vi'],vocabulary=len(l['vocabulary']),grammar=len(l['grammar_points']),patterns=len(l['sentence_patterns']),examples=len(l['examples']),dialogues=len(l['dialogues']),source=cov['vocabulary_source_id'],pages=cov['vocabulary_pdf_pages'],source_groups=len(groups),path=f"docs/content-authoring/lesson-{l['reference_lesson_number']:02}.md"))
    counts={k:sum(len(l[k]) for l in lessons) for k in ['vocabulary','grammar_points','sentence_patterns','examples','dialogues']}
    counts.update(lessons=len(lessons),units=len(units),characters=len(chars),source_pages=sum(s['pages'] for s in source_rows),source_grammar_groups=sum(x['source_groups'] for x in current),bound_entries=sum(any(re.search('[〜～]', ''.join(s['base'] for s in f['japanese']['segments'])) for f in w['forms']) for l in lessons for w in l['vocabulary']),kanji_word_occurrences=sum(len(u['word_examples']) for u in units))
    files=list(A.glob('lesson-*.json'))+list((A/'kanji').glob('unit-*.json'))+list((A/'kanji').glob('characters-*.json'))+[A/'kana'/n for n in ['inventory.json','source-inventory.json','kana.schema.json','review.json']]
    files += [A/'sentence-bank'/n for n in ['identities.json','bank.json','bank.schema.json','bound-contexts.json','speech.json','review.json']]
    counts['editorial_bytes']=sum(p.stat().st_size for p in files)
    counts['unit_word_occurrences']=counts['kanji_word_occurrences']
    counts['character_example_occurrences']=sum(len(char['examples']) for char in chars)
    counts['kanji_word_occurrences']+=counts['character_example_occurrences']
    no_example=[p['id'] for l in lessons for p in l['sentence_patterns'] if not any(e['pattern_id']==p['id'] for e in l['examples'])]
    no_variant=[(p['id'],t['key']) for l in lessons for p in l['sentence_patterns'] for t in p['templates'] if not any(e['pattern_id']==p['id'] and e['pattern_variant_key']==t['key'] for e in l['examples'])]
    if no_example or no_variant:raise ValueError('Missing example coverage')
    unit_rows=[dict(number=u['reference_unit_number'],level=u['source_level_label'],characters=len(u['character_glyphs']),words=len(u['word_examples']),milestone=u['publisher_lesson_milestone']['global_lesson_number'],milestone_level='N5' if u['publisher_lesson_milestone']['global_lesson_number']<=25 else 'N4',path=f"docs/content-authoring/kanji/unit-{u['reference_unit_number']:02}.md") for u in units]
    return dict(date=native['date'] if native else '2026-11-08',stale_evidence=stale_evidence,native_proof=native,native_audio_closure=closure,candidate_authoring=candidates,kana_authoring=kana,source_reconciliation=reconciliation,proper_name_review=dict(path='docs/content-authoring/source-reconciliation/proper-name-review.json',decision='B-U-59',source_rows=38,new_entries=41,visual_pages=19),scope='All canonical files checked structurally. H02 (legacy T02) records primary assigned-scope source/VI/EN/reading review; its revision-bound report is included separately. B-U-59 and the earlier seven-page audit remain historical evidence.',counts=counts,sources=source_rows,canonical_content_sha256={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted(files)},lessons=current,units=unit_rows,missing_pattern_examples=no_example,missing_variant_examples=no_variant,visual_rechecks=[dict(source=s,page=p,scope=scope) for s,p,scope in [('N5_GRAMMAR',29,'Lesson 1 lexical forms/annotations'),('N5_GRAMMAR',30,'Lesson 1 phrases, countries and names (historical pre-B-U-59 check)'),('N5_GRAMMAR',171,'Lesson 24 giving viewpoint and topic 1 example correction'),('N4_GRAMMAR',95,'SRC-05 printed translation discrepancy'),('N4_GRAMMAR',137,'SRC-06/07 printed translation ambiguity'),('N4_KANJI',8,'Units 21–25 previous-volume review/supplement relationship'),('N4_KANJI',188,'SRC-02 printed Han-Viet discrepancy')]],limitations=['No independent full re-transcription of 1451 source pages.',('Assigned-scope primary source/VI/EN/reading review completed under B-U-51; independent human full-corpus certification is not claimed.' if reconciliation['task_acceptance_complete'] else 'Assigned-scope H02 source/content acceptance remains open.'),'Kana and sentence-bank authoring have separate revision-bound primary reviews; native playback/integration remains open.','Other 17 languages and independent linguistic/release review pending.','Current browser visual/interaction QA was blocked by the URL policy rejecting local file:// access; no bypass attempted.',('T01 physical audio closure uses two real-driver iPhone tests and explicit owner manual listening/actual-event confirmation. Physical UI automation did not execute; exact voice identifier and headset model were not recorded. Full application/performance/release acceptance remains separate.' if closure else 'Legacy P0-T05 evidence records a bounded native Simulator proof now tracked as T01. Offline listening/real-audio verification is scheduled in development under DOC-PLAN-02 and does not block documentation; full application/performance acceptance also remains separate.' if native else 'No iOS application build, playback or device/performance acceptance; H01 separately verifies its macOS runtime library.'),*(['Historical task evidence has stale input fingerprints; see stale_evidence. No review pins were refreshed.'] if stale_evidence else [])])

def badge(text):return f'<span class="badge">{esc(text)}</span>'

TASK_STATUS = {'todo':'Chưa bắt đầu','ready':'Có thể bắt đầu','in_progress':'Đang thực hiện','blocked':'Có trở ngại','done':'Đã hoàn tất'}
TASK_KIND = {'native':'App / widget native','content':'Nội dung','technical':'Kỹ thuật dùng chung','locale':'Bản dịch','performance':'Đo hiệu năng','release':'Nghiệm thu / phát hành'}
PHASE_LABEL = {'documentation':'Documentation','development':'Development / implement','acceptance':'Nghiệm thu','release':'Phát hành'}

def roadmap_tasks(c):
    """Keep completed documentation/foundations in the handoff, not the queue."""
    completed_priorities=c['delivery_phases']['review_focus']['completed_task_priorities']
    return [t for t in c['tasks'] if not (t['status']=='done' and
            (t['phase']=='documentation' or t['priority'] in completed_priorities))]

def review_findings(c):
    """Do not duplicate scheduled P1 work as current documentation issues."""
    focus=c['delivery_phases']['review_focus']
    tasks={t['id']:t for t in c['tasks']}
    return [f for f in c['findings'] if f['status']!='resolved' and not
            (f['phase'] in focus['planned_finding_phases'] and
             tasks[f['task']]['priority']==focus['planned_priority'])]

def documentation_blockers(c, e):
    """Derive the phase gate; never store a second editable readiness flag."""
    blockers=[s['id'] for s in c['delivery_phases']['tasks'] if s['status']!='done']
    blockers += [t['id'] for t in c['tasks'] if t['phase']=='documentation' and t['status']!='done']
    blockers += [f['id'] for f in c['findings'] if f['status']!='resolved' and f['phase']=='documentation']
    blockers += [q['id'] for q in c['questions']]
    blockers += [x['task']+' · '+x['path'] for x in e['stale_evidence']]
    return blockers

def render_documentation(c,e):
    phase=c['delivery_phases'];tasks=phase['tasks'];blockers=documentation_blockers(c,e)
    ready=not blockers
    view='<section id="documentation"><p class="eyebrow">Documentation / Final handoff</p><h2>'+('Documentation hoàn tất · Ready for development' if ready else 'Documentation chưa hoàn tất · Chưa chuyển development')+'</h2>'
    view+='<p>'+esc(phase['documentation_scope'])+'</p><div class="notice"><strong>Tài liệu bàn giao</strong><p>'+esc(phase['gate_rule'])+'</p>'
    if blockers:view+='<p>Còn chặn: '+esc(', '.join(blockers))+'.</p>'
    else:view+='<p>Checklist documentation đã đóng. Nghe offline và kiểm chứng audio thực hiện trong development theo DOC-PLAN-02, không yêu cầu trong phase documentation. Bản final chỉ hợp lệ cùng kết quả sync/audit hiện tại; thay đổi contract hoặc dữ liệu phải kiểm tra lại trước khi bắt đầu task mới.</p>'
    view+='</div>'
    handoff=phase['completed_documentation']
    view+='<p>'+esc(handoff['summary'])+'</p><p>'+', '.join('<a href="#document" data-doc="'+esc(path)+'">'+esc(Path(path).name)+'</a>' for path in handoff['documents'])+'</p>'
    # Preserve incoming historical links without rendering completed task rows.
    archived=[t for t in c['tasks'] if t not in roadmap_tasks(c)]
    aliases=[s['id'] for s in tasks if s['status']=='done']
    aliases += [key for t in archived for key in [t['id']]+[s['id'] for s in t.get('stories',[])]]
    view+=''.join('<span id="'+esc(key)+'"></span>' for key in aliases)
    focus=phase['review_focus']
    view+='<p>'+esc(focus['summary'])+'</p><p>'+', '.join('<a href="#document" data-doc="'+esc(path)+'">'+esc(Path(path).parent.name+'/'+Path(path).name)+'</a>' for path in focus['handoff_documents'])+'</p>'
    pending=[s for s in tasks if s['status']!='done']
    if pending:view+='<div class="table-wrap"><table><thead><tr><th>Task documentation còn mở</th><th>Trạng thái</th><th>Phạm vi và bằng chứng</th></tr></thead><tbody>'
    for s in pending:
        view+='<tr id="'+s['id']+'"><td><strong>'+esc(s['id'])+'</strong><br>'+esc(s['title'])+'</td><td>'+badge(TASK_STATUS[s['status']])+'</td><td>'+esc(s['scope'])+'<br>'+', '.join('<a href="../'+esc(path)+'">'+esc(Path(path).name)+'</a>' for path in s['evidence'])+'</td></tr>'
    if pending:view+='</tbody></table></div>'
    view+='<p>'+esc(phase['implementation_scope'])+'</p><p class="muted">'+esc(phase['review_scope'])+'</p><h3>Task có thể thực hiện sau gate documentation</h3>'
    items={t['id']:t for t in c['tasks']}
    for t in c['tasks']:
        for s in t.get('stories',[]):items[s['id']]=dict(s,status=t['status'] if s['tracking']=='parent' else s['status'])
    view+='<ul>'
    for t in c['tasks']:
        for s in t.get('stories',[]):
            if s['tracking']=='parent' or s['phase']!='development':continue
            status=s['status']
            if status=='done':continue
            missing=[d for d in s['depends'] if items[d]['status']!='done']
            if status not in ('ready','in_progress') and missing:continue
            label=TASK_STATUS[status] if status in ('ready','in_progress') else 'Đủ phụ thuộc; chưa bắt đầu'
            view+='<li>'+task_links([s['id']])+' · '+esc(s['title'])+' · '+esc(label)+'.'
            if missing:view+=' Còn phụ thuộc: '+task_links(missing)+'.'
            view+='</li>'
    return view+'</ul><p>Danh sách này đối chiếu phụ thuộc, không đổi trạng thái thực hiện hoặc đóng nghiệm thu. Các task tiếp theo mở theo DAG trong roadmap.</p></section>'

def task_links(ids):
    return ', '.join(f'<a href="#{esc(key)}">{esc(key)}</a>' for key in ids) or 'Không'

def render_e2e(s, policy):
    e=s.get('e2e')
    if not e:return ''
    status={'not_run':'Chưa chạy','passed':'Đã đạt','failed':'Có lỗi','blocked':'Bị chặn'}[e['status']]
    view='<div class="task-e2e"><h4>Kịch bản E2E · '+status+'</h4><p><strong>Fixture:</strong> '+esc(e['fixture'])+'</p>'
    view+='<p><strong>Môi trường:</strong> '+esc(e['surface'])+' · <strong>Phụ thuộc bổ sung để đóng E2E:</strong> '+task_links(e['requires'])+'</p>'
    for case in e['scenarios']:
        view+='<h5>'+esc(case['id'])+' · '+('Luồng thành công' if case['type']=='happy' else 'Biên / lỗi / phục hồi')+'</h5><dl>'
        for field,label in [('given','Given · Điều kiện'),('when','When · Thao tác'),('then','Then · Kết quả mong đợi')]:
            view+='<dt>'+label+'</dt><dd>'+esc(case[field])+'</dd>'
        view+='</dl>'
    return view+'<p><strong>Bằng chứng để đóng:</strong> '+esc(policy['evidence_required'])+'</p></div>'

def render_roadmap(c):
    policy=c['task_planning']
    tasks=roadmap_tasks(c)
    children=[s for t in tasks for s in t.get('stories',[])]
    inherited=sum(s['tracking']=='parent' for s in children)
    view='<section id="roadmap"><p class="eyebrow">07 / Kế hoạch phát triển</p><h2>Trạng thái từng nhóm và task thực hiện.</h2>'
    view+=f'<p>{esc(policy["summary"])}</p><p><strong>{len(tasks)} nhóm · {len(children)-inherited} task triển khai/nghiệm thu.</strong> P0/P1 là mức ưu tiên; phase thực hiện được ghi riêng. N5 + N4 vẫn cùng phạm vi bàn giao. Trạng thái nhóm và task con được ghi riêng, không suy phần trăm hoàn thành.</p>'
    view+=f'<details class="planning-rules"><summary>{esc(policy["decision_id"])} · Cách chia task đã được owner xác nhận ({esc(policy["date"])})</summary><p>{esc(policy["owner_instruction"])}</p><ul>'+''.join(f'<li>{esc(rule)}</li>' for rule in policy['rules'])+'</ul></details>'
    dev=c['development_plan']
    view+='<div id="development" class="notice"><h3>Development theo user story · '+str(len(dev['task_ids']))+' task / '+str(2*len(dev['task_ids']))+' kịch bản E2E</h3><p>'+esc(dev['summary'])+'</p><p>Mặc định chỉ hiện development. Mở từng task để xem user story, fixture, Given/When/Then và điều kiện đóng. Các kịch bản mới đều chưa chạy.</p><details class="planning-rules"><summary>'+esc(dev['decision_id'])+' · Quy tắc thực hiện và Definition of Done</summary><p>'+esc(dev['owner_instruction'])+'</p><ul>'+''.join('<li>'+esc(rule)+'</li>' for rule in dev['rules'])+'</ul></details></div>'
    migration=c['task_id_migration']
    view+='<details class="planning-rules"><summary>'+esc(migration['decision_id'])+' · Tra cứu mã task cũ</summary><p>'+esc(migration['summary'])+'</p><div class="table-wrap"><table><thead><tr><th>Mã trước đây</th><th>Mã hiện tại</th></tr></thead><tbody>'
    for old,new in migration['legacy_to_current'].items():view+='<tr><td>'+esc(old)+'</td><td>'+esc(new)+'</td></tr>'
    view+='</tbody></table></div>'
    current_map=migration.get('previous_current_to_current',{})
    if current_map:
        view+='<p>ID nhóm còn hoạt động, từ roadmap trước sang hiện tại:</p><div class="table-wrap"><table><thead><tr><th>Nhóm trước</th><th>Nhóm hiện tại</th></tr></thead><tbody>'
        for old,new in current_map.items():view+='<tr><td>'+esc(old)+'</td><td>'+esc(new)+'</td></tr>'
        view+='</tbody></table></div>'
    for title,key in [('ID ở roadmap ngay trước lần đổi này','retired_previous_current_to_document'),('ID theo crosswalk lịch sử trước DOC-PLAN-05','retired_legacy_to_document')]:
        retired=migration.get(key,{})
        if retired:
            view+='<p>'+esc(title)+':</p><div class="table-wrap"><table><thead><tr><th>Mã đã chuyển khỏi roadmap</th><th>Tài liệu bàn giao</th></tr></thead><tbody>'
            for old,path in retired.items():view+='<tr><td>'+esc(old)+'</td><td>'+inline('['+Path(path).name+']('+path.removeprefix('docs/')+')')+'</td></tr>'
            view+='</tbody></table></div>'
    view+='</details>'
    view+='<div class="table-wrap"><table><thead><tr><th>Nhóm</th><th>Phase</th><th>Trạng thái</th><th>Task con hoàn tất</th></tr></thead><tbody>'
    for t in tasks:
        items=t.get('stories',[])
        done=sum((t['status'] if s['tracking']=='parent' else s['status'])=='done' for s in items)
        view+='<tr><td>'+task_links([t['id']])+' · '+esc(t.get('planning_title',t['title']))+'</td><td>'+esc(PHASE_LABEL[t['phase']])+'</td><td>'+badge(TASK_STATUS[t['status']])+'</td><td>'+(str(done)+'/'+str(len(items)) if items else '—')+'</td></tr>'
    priorities=sorted({t['priority'] for t in tasks})
    priority_labels={'P0':'P0 · Nền tảng','P1':'P1 · Tính năng và nghiệm thu'}
    view+='</tbody></table></div><div class="task-controls"><label>Phase <select id="task-phase"><option value="development">Development</option><option value="all">Tất cả phase</option><option value="documentation">Documentation</option><option value="acceptance">Nghiệm thu</option><option value="release">Phát hành</option></select></label><label>Lọc trạng thái / ưu tiên <select id="task-filter"><option value="all">Tất cả</option>'+''.join(f'<option value="{p}">{priority_labels[p]}</option>' for p in priorities)+''.join(f'<option value="{key}">{label}</option>' for key,label in TASK_STATUS.items())+'</select></label><label>Tìm task <input id="task-query" type="search" placeholder="Tên tính năng, màn hình, ID, E2E…"></label></div><p id="task-results" class="muted" aria-live="polite"></p><div class="task-jumps" aria-label="Nhóm công việc">'
    view+=''.join(f'<a href="#{t["id"]}">{t["id"]} · {esc(t.get("planning_title",t["title"]))}</a>' for t in tasks)+'</div><div class="task-list">'
    for t in tasks:
        items=t.get('stories',[])
        title=t.get('planning_title',t['title'])
        view+=f'<article id="{t["id"]}" class="task-group" data-phase="{esc(t["phase"])}" data-priority="{t["priority"]}" data-status="{t["status"]}" data-task-search="{esc(t["id"]+" "+title)}"><div class="task-top">{badge(t["priority"])} {badge(TASK_STATUS.get(t["status"],t["status"]))}<span>{t["id"]} · Vai trò: {esc(t["owner"])}</span></div><h3>{esc(title)}</h3>'
        if t['id']=='H01':
            view+='<p class="task-handoff"><strong>Giữ nguyên bàn giao H01 (mã cũ T01).</strong> Các mục bên dưới kế thừa trạng thái/bằng chứng của H01, không giao lại như task mới. Bằng chứng hiện có là kiểm thử package/thư viện trên macOS, chưa phải nghiệm thu app iOS.</p>'
        view+=f'<p class="meta">Phase: {esc(PHASE_LABEL[t["phase"]])}</p><details class="task-baseline"><summary>Mốc bàn giao và phụ thuộc của nhóm</summary><p><strong>Đầu ra:</strong> {esc(t["deliverable"])}</p><p><strong>Hoàn tất khi:</strong> {esc(t["acceptance"])}</p><p>Phụ thuộc nhóm (tra cứu): {task_links(t["depends"])}</p></details>'
        if not items:view+='<p class="muted">Mốc tài liệu đã hoàn tất; giữ nguyên lịch sử, không mở lại thành task mới.</p>'
        previous_area=None
        for s in items:
            if s['area']!=previous_area:
                view+=f'<h4 class="task-area">{esc(s["area"])}</h4>';previous_area=s['area']
            status=t['status'] if s['tracking']=='parent' else s['status']
            label='Theo H01 · '+TASK_STATUS.get(status,status) if s['tracking']=='parent' else TASK_STATUS.get(status,status)
            search=' '.join([s['id'],s['title'],s['area'],s['need'],s['deliverable'],s['english']['title']])
            if 'e2e' in s:
                search+=' '+s['user_story']+' '+s['english']['user_story']+' E2E '+s['e2e']['fixture']+' '+' '.join(case['id'] for case in s['e2e']['scenarios'])
            view+=f'<details id="{s["id"]}" class="task-story" data-status="{esc(status)}" data-task-search="{esc(search)}"><summary><span class="task-story-id">{s["id"]}</span> {esc(s["title"])} <span class="task-story-status">{badge(label)}</span></summary><p class="task-need">{("<strong>User story:</strong> " if "user_story" in s else "")+esc(s.get("user_story",s["need"]))}</p><p class="meta">{TASK_KIND[s["kind"]]} · {esc(s["area"])}</p><p><strong>Đầu ra:</strong> {esc(s["deliverable"])}</p><p><strong>Điều kiện nghiệm thu:</strong></p><ul>'+''.join('<li>'+esc(x)+'</li>' for x in s['acceptance'])+'</ul><p><strong>Checklist triển khai / đối chiếu:</strong></p><ul>'+''.join('<li>'+esc(x)+'</li>' for x in s['checklist'])+'</ul>'
            if 'user_story' in s:view+=render_e2e(s,dev)
            view+=f'<p><strong>Phụ thuộc để bắt đầu:</strong> {task_links(s["depends"])}</p><p><strong>Phạm vi đã chốt:</strong> {task_links(s["features"])}</p><p><strong>Hợp đồng:</strong> '+', '.join(f'<a href="#document" data-doc="{esc(path)}">{esc(Path(path).name)}</a>' for path in s['contracts'])+f'</p><p><strong>Bằng chứng cần có:</strong> {esc(s["evidence_required"])}</p>'
            if s['evidence']:
                view+='<p><strong>Bằng chứng đã ghi nhận'+(' (kế thừa H01)' if s['tracking']=='parent' else '')+':</strong> '+', '.join(f'<a href="../{esc(path)}">{esc(path)}</a>' for path in s['evidence'])+'</p>'
            else:view+='<p class="muted">Chưa ghi nhận bằng chứng hoàn tất cho task này.</p>'
            view+='</details>'
        view+='</article>'
    return view+'</div></section>'

def render_view(c,e,version_hash):
    counts=e['counts']
    findings=review_findings(c)
    nav=[('overview','Tổng quan'),('documentation','Gate documentation'),('scope','Tính năng'),('flows','Luồng màn hình'),('prototype','Thử giao diện'),('sources','Audit nguồn'),('curriculum','Đọc giáo trình')]
    if findings:nav.append(('findings','Vấn đề documentation'))
    nav += [('development','Development / E2E'),('roadmap','Roadmap thực hiện')]
    if c['questions']:nav.append(('decisions','Xác nhận'))
    nav.append(('agents','Agent & hợp đồng'))
    view='<a class="skip" href="#overview">Đến nội dung</a><aside class="navigation"><div class="brand">Project<span>Beta</span></div><p>FINAL DOCUMENTATION / 2.2</p><nav>'+''.join(f'<a href="#{i}">{t}</a>' for i,t in nav)+'</nav><small>'+'.'.join(reversed(c['date'].split('-'))) +'<br>Offline · Một tài liệu duy nhất<br>Phiên bản '+version_hash[:12]+'</small></aside><main class="review-main">'
    blockers=documentation_blockers(c,e)
    headline='Ready for development' if not blockers else 'Chưa ready for development'
    view+='<section id="overview" class="hero"><p class="eyebrow">Final documentation · '+esc(c['date'])+'</p><h1>ProjectBeta<br>Tài liệu bàn giao dev.</h1><p class="lead">Một bản HTML cho phạm vi, thiết kế, flow, hợp đồng và trạng thái công việc. Điều kiện chuyển phase: hoàn tất tất cả task documentation.</p><div class="notice"><strong>'+headline+'</strong><p>'+('Documentation đã đủ điều kiện bàn giao. Bản dịch và kiểm chứng nghe offline/audio thực hiện trong development theo xác nhận owner; không yêu cầu nghe/audio trong phase hiện tại. Từng task implement vẫn phải đủ phụ thuộc riêng.' if not blockers else 'Các task documentation hoặc bằng chứng còn thiếu được liệt kê tại gate bên dưới; chưa chuyển sang development.')+'</p><a href="#documentation">Xem gate và checklist documentation →</a></div>'
    view+='<div class="stats">'+''.join(f'<div><strong>{v}</strong><span>{t}</span></div>' for v,t in [(counts['lessons'],'bài có nội dung'),(counts['units'],'Kanji unit'),(counts['characters'],'chữ Kanji'),('2 / 19','ngôn ngữ nội dung hiện có')])+'</div></section>'
    view+=render_documentation(c,e)
    view+='<section id="scope"><p class="eyebrow">01 / Phạm vi đã chốt</p><h2>Mọi tính năng cùng một bộ quy tắc.</h2><div class="feature-grid">'
    for f in c['features']:view+=f'<article id="{f["id"]}"><span class="meta">{f["id"]} · Đã chốt</span><h3>{esc(f["title"])}</h3><p>{esc(f["description"])}</p><small>{esc(f["authority"])}</small></article>'
    view+='</div></section><section id="flows"><p class="eyebrow">02 / Flow & trạng thái</p><h2>Đường đi và điểm trở về.</h2><div class="flow-list">'
    for i,f in enumerate(c['flows'],1):view+=f'<article><b>{i:02}</b><div><h3>{esc(f["title"])}</h3><p>{esc(f["description"])}</p></div></article>'
    view+='''</div><div class="notice"><strong>Nguyên tắc UX chung</strong><p>Lưu thành công mới cập nhật trạng thái; lỗi giữ ngữ cảnh và có thử lại. Không đổi nguồn widget khi rỗng; không hiển thị “không có kết quả” khi index chưa sẵn sàng. Native text size/RTL vẫn thuộc phạm vi. Browser demo chỉ minh họa, không thay thế hợp đồng.</p></div></section>
<section id="prototype"><p class="eyebrow">03 / Prototype hợp nhất</p><h2>Thử luồng chính và các cỡ widget.</h2><p>Mở một bản mô phỏng bên dưới. Bản app dùng trích đoạn bài 1/26, unit 1/21/26 và 57 ô kana; loa chỉ mô phỏng trạng thái. Ngân hàng câu theo kiến thức chưa được triển khai. Hai mô phỏng độc lập; nút đặt lại chỉ xóa dữ liệu demo.</p><div class="actions"><button data-prototype="app">Mở mô phỏng app</button><button data-prototype="widgets">Mở typography & widgets</button><button id="close-prototype" class="secondary">Đóng mô phỏng</button></div><div id="prototype-host"></div><p class="muted">Chưa kiểm tra trực quan/tương tác HTML: browser URL policy từ chối đường dẫn file://. Static/helper checks không chứng minh Liquid Glass, TTS hay WidgetKit native.</p></section>'''
    view+='<section id="sources"><p class="eyebrow">04 / Nguồn & mức độ tin cậy</p><h2>Đủ bản nháp chưa có nghĩa là đủ bằng chứng.</h2><p>Sáu PDF tham khảo, ấn bản Elementary I/II thứ hai theo catalog; tổng '+str(counts['source_pages'])+' trang. N5/N4 là nhãn chương trình nguồn, không phải danh sách chính thức bảo đảm bao phủ kỳ thi. Không đóng gói PDF/OCR vào app.</p><div class="table-wrap"><table><thead><tr><th>Nguồn</th><th>Trang</th><th>Kiểm tra lại</th><th>SHA-256</th></tr></thead><tbody>'
    for s in e['sources']:view+=f'<tr><td>{s["id"]}</td><td>{s["pages"]}</td><td>Hash & số trang khớp</td><td><code class="hash">{s["sha256"]}</code></td></tr>'
    view+='</tbody></table></div><div class="feature-grid"><article><h3>Đã kiểm tra toàn bộ bằng máy</h3><p>50 bài, 50 unit, 536 master; IDs, references, ruby/kana, nghĩa VI/EN bắt buộc, source bounds, mốc lesson/unit. '+str(counts['vocabulary'])+' mục từ, 255 điểm ngữ pháp, 278 mẫu, '+str(counts['examples'])+' ví dụ, 50 hội thoại; 253 nhóm ngữ pháp nguồn. Mọi mẫu và mọi biến thể khai báo hiện có câu ví dụ liên kết.</p></article><article><h3>Đã đối chiếu ảnh có giới hạn</h3><p>Audit ngày 07.11 xem lại 7 trang nguồn: N5 grammar 29/30/171; N4 grammar 95/137; N4 Kanji 8/188. Ngày 08.11 đối chiếu thêm 19 trang có tên bị loại (xem bằng chứng B-U-59 trong lịch sử). Các báo cáo cũ ghi tác giả đã đối soát trang/nhóm và cross-check giới hạn; không gọi đó là lần kiểm chứng độc lập mới toàn bộ.</p></article><article><h3>Còn thiếu để chứng nhận đầy đủ</h3><p>T02 đã hoàn tất primary review phạm vi nguồn, VI/EN và ruby; T03 có review kana riêng. T04 có báo cáo riêng về ngân hàng câu và dependency. Chưa có chứng nhận ngôn ngữ độc lập, 17 ngôn ngữ còn lại, phát âm thực tế hoặc quyền phát hành. T09/T12 và tích hợp native vẫn là các gate riêng.</p></article><article><h3>Phạm vi loại trừ</h3><p>Không sao chép nguyên hội thoại, bài đọc, bài tập/đáp án. Giữ tên riêng theo nguồn, kể cả tên hư cấu (B-U-59). Các bảng bổ sung ngoài hai trang từ vựng mỗi bài và mọi minh họa phụ lục từ điển Kanji không được tuyên bố đã bao phủ hết; số từ hiện có không chứng minh mọi từ phổ biến ngoài phạm vi đó đã được biên soạn.</p></article></div>'
    if e['stale_evidence']:
        view+='<article class="notice"><h3>Bằng chứng bàn giao cũ đang lệch dữ liệu</h3><p>Các hash legacy của H01/H02 dưới đây không khớp file hiện tại. Giữ nguyên báo cáo lịch sử; sinh lại HTML không phải review lại nội dung. Audit toàn kho vẫn phải báo lỗi cho phần lệch này.</p><ul>'+''.join('<li>'+esc(x['task']+' · '+x['path'])+'</li>' for x in e['stale_evidence'])+'</ul></article>'
    view+='<details><summary>Độ phủ từng bài: đủ 50 hàng, đếm trực tiếp dữ liệu hiện tại</summary><div class="table-wrap"><table><tr><th>Bài</th><th>Chủ đề</th><th>Trang từ nguồn</th><th>Từ</th><th>Ngữ pháp / nhóm nguồn</th><th>Mẫu / ví dụ</th></tr>'
    for l in e['lessons']:view+=f'<tr><td>{l["level"]} {l["number"]}</td><td><a href="#document" data-doc="{l["path"]}">{esc(l["title"])}</a></td><td>{l["source"]} {l["pages"]}</td><td>{l["vocabulary"]}</td><td>{l["grammar"]} / {l["source_groups"]}</td><td>{l["patterns"]} / {l["examples"]}</td></tr>'
    view+='</table></div></details><details><summary>Độ phủ 50 Kanji unit và mốc đã học</summary><div class="table-wrap"><table><tr><th>Unit</th><th>Nhãn tập</th><th>Liên kết chữ</th><th>Từ xuất hiện</th><th>Mốc học cho widget</th></tr>'
    for u in e['units']:view+=f'<tr><td><a href="#document" data-doc="{u["path"]}">{u["number"]}</a></td><td>{u["level"]}</td><td>{u["characters"]}</td><td>{u["words"]}</td><td>{u["milestone_level"]} bài {u["milestone"]}</td></tr>'
    view+='</table></div></details></section><section id="curriculum"><p class="eyebrow">05 / Đọc toàn bộ nội dung hiện có</p><h2>Giáo trình ngay trong HTML này.</h2><p>Đọc đầy đủ các bản nháp VI/EN: từ vựng, dạng từ, ngữ pháp, công thức, ví dụ, hội thoại, Kanji và nguồn liên quan. Phần này sinh từ dữ liệu chuẩn; không bị giới hạn như prototype. Cách ghi 漢字【かな】 biểu thị furigana để soát nội dung.</p><label>Tìm tài liệu/bài học <input id="document-filter" type="search" placeholder="Ví dụ: 24, Kanji, grammar…"></label><p id="document-match-status" class="muted" role="status">Gõ tên bài hoặc tài liệu để hiện kết quả có thể bấm mở; bạn cũng có thể chọn trong danh sách bên dưới.</p><div id="document-matches" class="document-matches"></div><label>Chọn tài liệu <select id="document-picker"><option value="">Chọn bài hoặc tài liệu…</option></select></label><div id="document" class="document-reader" tabindex="-1"><p>Chọn một bài hoặc một hàng trong bảng nguồn để đọc.</p></div></section>'
    if findings:
        view+='<section id="findings"><p class="eyebrow">06 / Vấn đề documentation</p><h2>Vấn đề cần giải quyết trong bản review hiện tại.</h2><div class="finding-list">'
        for f in findings:
            view+=f'<article id="{f["id"]}" class="finding {f["status"]}"><span class="meta">{f["id"]} · Còn mở · {esc(PHASE_LABEL[f["phase"]])}</span><h3>{esc(f["title"])}</h3><p>{esc(f["description"])}</p><a href="#{f["task"]}">{f["task"]} →</a></article>'
        view+='</div></section>'
    view+=render_roadmap(c)
    if c['questions']:
        view+='<section id="decisions"><p class="eyebrow">08 / Xác nhận có phiên bản</p><h2>Đề xuất cần bạn xác nhận.</h2><p>Lựa chọn ở đây chỉ lưu ghi chú review trong trình duyệt, chưa cập nhật repository hoặc thay thế xác nhận của bạn. Dùng “Xuất phản hồi”, rồi gửi nội dung đó cho agent. Ghi chú gắn với phiên bản '+version_hash[:12]+'; thay đổi đặc tả sẽ tạo phiên bản mới.</p>'
        for q in c['questions']:view+=f'<article class="decision"><span class="meta">{q["id"]} · Đề xuất, chưa duyệt</span><h3>{esc(q["title"])}</h3><p>{esc(q["proposal"])}</p><p class="muted">{esc(q["reason"])}</p><label>Phản hồi <select data-decision="{q["id"]}"><option value="unreviewed">Chưa xem</option><option value="agree">Đồng ý đề xuất</option><option value="change">Cần điều chỉnh</option></select></label><label>Ghi chú <textarea data-note="{q["id"]}" rows="2"></textarea></label></article>'
        view+='''<label>Nhận xét về toàn bộ phạm vi, ưu tiên và giới hạn audit <textarea id="overall-note" rows="3" placeholder="Ghi rõ feature/task/bài học cần sửa…"></textarea></label><p id="review-storage" class="muted"></p><button id="export-review">Xuất phản hồi</button><textarea id="review-export" rows="9" readonly hidden aria-label="Phản hồi để gửi agent"></textarea></section>'''
    view+='<section id="agents"><p class="eyebrow">09 / Handoff cho agent</p><h2>Tài liệu đủ rõ trước khi tăng số agent.</h2><p><strong>Khuyến nghị hiện tại: AGENTS.md gọn + hợp đồng + kiểm tra tự động; chưa cần cài custom agent.</strong> Vấn đề hiện nay là thiếu dữ liệu/bằng chứng, không phải thiếu vai trò. Khi công việc lặp lại đủ lớn, có thể dùng hai vai trò review có phạm vi rõ: nội dung Nhật/nguồn và tích hợp iOS. Một người/agent chịu trách nhiệm tổng hợp cuối; người viết không tự gọi self-review là review độc lập.</p><p>OpenAI mô tả AGENTS.md là hướng dẫn bền vững theo repository; các file quy trình khác là quy ước có thể điều chỉnh. Đây là cơ sở cho cách tổ chức gọn, còn quyết định chưa cài custom agent là đánh giá riêng cho Beta. <a href="'+c['agent_recommendation']['source']+'">OpenAI Docs</a>.</p><p>HTML này chứa contract chuẩn. Tài liệu English cho agent được xuất từ cùng contract; dữ liệu bài học JSON/PDF catalog vẫn là nguồn dữ liệu riêng, có hash và được nhúng lại bằng script. Không sửa hai bản độc lập.</p><details><summary>Đọc hợp đồng kỹ thuật và tài liệu chi tiết trong trang này</summary><div id="agent-document-links"></div></details><details><summary>Lịch sử quyết định B-U / DS-U (chỉ bằng chứng lịch sử)</summary><p>Đọc bảng quyết định mới nhất và mục superseded. Trạng thái “open/pending” trong các đoạn cũ không phải hàng đợi hiện hành; task/đề xuất ở trên mới là hiện trạng.</p><button data-history="discovery" class="secondary">Xem B-U và discovery</button> <button data-history="design" class="secondary">Xem DS-U và design</button><div id="history-reader"></div></details></section><footer><p>ProjectBeta · Final documentation 2.2 · '+version_hash[:12]+' · Nội dung draft, không phải build đã nghiệm thu.</p></footer></main><noscript><p>JavaScript đang tắt. Các phần đặc tả, flow, audit và task phía trên vẫn đọc được; bật JavaScript để dùng corpus reader, prototype và xuất phản hồi.</p></noscript>'
    return view

def embed_app(c):
    s=c['prototype_app']
    s=s.replace('<link rel="stylesheet" href="review.css">','<style>'+ (S/'review.css').read_text()+'</style>')
    for file in ['review-data.js','review-logic.js','review.js']:
        s=s.replace(f'<script defer src="{file}"></script>','')
        s=s.replace('</body>','<script>'+ (S/file).read_text()+'</script></body>')
    # The outer review contains all destinations; no nested link may replace the artifact.
    s=re.sub(r'<a href="[^"]+">.*?</a>','',s)
    s=s.replace('id="app-shell"','id="app-shell"')
    return s

def embed_widgets(c):
    s=c['prototype_widgets']
    def replace_link(m):
        if 'widget-link' in m[1]:
            return '<button type="button" class="widget-link" style="width:100%;text-align:left;border:0;font:inherit" onclick="parent.postMessage({projectBetaOpenApp:true},\'*\')">'+m[4]+'</button>'
        return '<span>'+m[4]+'</span>'
    s=re.sub(r'<a\b([^>]*)href="([^"]+)"([^>]*)>(.*?)</a>',replace_link,s,flags=re.S)
    s=s.replace('nếu đã dùng bản app mẫu, ngôn ngữ/Furigana/giao diện ban đầu lấy từ bản đó.', 'mô phỏng này độc lập với bản app mẫu và không lưu dữ liệu app.')
    m=re.search(r'(<script id="review-data" type="application/json">)(.*?)(</script>)',s,re.S)
    if m:
        data=json.loads(m[2]);data['tokens']=c['tokens'];s=s[:m.start(2)]+encode(data)+s[m.end(2):]
    return s

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    text=PAGE.read_text();c=extract(text);e=evidence();outputs={}
    text=re.sub(r'<title>.*?</title>',lambda m:'<title>'+esc(c['title'])+'</title>',text,count=1,flags=re.S)
    # Owner notes must be invalidated by curriculum/presentation changes too, not
    # just requirement edits. Exclude generated reports to avoid a hash cycle.
    excluded=set(c['documents'])|{'docs/audit/report.md','docs/delivery-plan.md'}
    review_inputs=[p for p in (ROOT/'docs').rglob('*.md') if str(p.relative_to(ROOT)) not in excluded]
    review_inputs += [S/name for name in ['review-data.js','review-logic.js','review.js','review.css']]
    review_inputs += [ROOT/'scripts'/name for name in ['project_review.js','project_review.css','sync_project_review.py']]
    input_hashes={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted(review_inputs)}
    version_hash=sha((encode(c)+encode(e)+encode(input_hashes)).encode())
    header='> GENERATED from [the owner HTML](../index.html) project-contract. Do not edit this export; update that contract and run `python3 scripts/sync_project_review.py`.\n\n'
    for path,body in c['documents'].items():
        link='../index.html' if path.startswith('docs/design-system/') else 'index.html'
        outputs[ROOT/path]=header.replace('../index.html',link)+body
    outputs[ROOT/'docs/01-discovery-and-open-questions.md']='> HISTORICAL DECISION EVIDENCE. Current scope, readiness, task order and proposals are maintained in [the single owner review](index.html). Approved B-U/DS-U rows remain evidence; old open-question/status paragraphs are not the current backlog. Later decisions supersede earlier rows.\n\n'+c['decision_history']['discovery']
    outputs[S/'tokens.json']=json.dumps(c['tokens'],ensure_ascii=False,indent=2)+'\n'
    outputs[ROOT/'docs/audit/source-audit.json']=json.dumps(e,ensure_ascii=False,indent=2)+'\n'
    counts=e['counts']; report=['# Documentation and source audit','',f'Current review revision: `{version_hash}`. Date: {c["date"]}. Generated; edit docs/index.html contract for product/status changes.','','## Scope and evidence','','All 279 pre-consolidation files are enumerated with hashes in baseline-manifest.json. Lesson/Kanji structural checks and the separate kana authoring validator define their own evidence scopes; generated readable content is checked. All six PDF hashes and page counts match the catalog. The 2026-11-07 audit visually rechecked seven source pages; the 2026-11-08 proper-name review checks 38 rows on 19 pages. Prior author/cross-agent evidence is historical, not a new independent full-corpus review.','','Current counts: `'+json.dumps(counts,ensure_ascii=False)+'`.','','H02 (legacy T02) records 2189 vocabulary rows,253 grammar groups,536 definitions,1498 unit words and826 master examples with primary VI/EN/reading review of102 files; see its revision-bound evidence below. This is not independent human certification. Kana authoring has a separate 301-item primary review. Native kana/candidate integration and remaining locales stay open; H04 authoring evidence is reported separately.','','## Findings','']
    report+=[c['delivery_phases']['review_focus']['english'],'']
    for f in review_findings(c):
        report += [f'### {f["id"]} / {f["status"]} / {f["task"]}',f['english'],'']
    report+=['## Proper names — B-U-59, 2026-11-08','','Restored 41 names from 38 rows on 19 visually checked source pages. The source spelling, contextual reading, VI/EN entity description and stable identity are recorded in [the item-level review](../content-authoring/source-reconciliation/proper-name-review.json). All 2189 vocabulary ledger row targets resolve to the correct lesson/form. This focused check does not certify every source row or sentence.','']
    report+=['## Validation limits','']+['- '+x for x in e['limitations']]+['','The same conclusions, priority tasks and owner proposals are readable in [the only owner HTML](../index.html).','']
    t04=e['candidate_authoring']
    report+=['## H04 authoring handoff (legacy T04)','',f"{t04['reviewed_candidates']} dependency-complete candidates cover {t04['reviewed_target_coverage']}/{t04['targets']} targets; {t04['missing_targets']} remain in the gap ledger. {t04['speech_targets']} speech authoring records include {t04['dictionary_forms']} dictionary forms and {t04['bound_contexts']} bound contexts. Authoring completion: {t04['task_authoring_acceptance_complete']}. See [the inventory](../content-authoring/sentence-bank/inventory.md) and [revision-bound validation](../content-authoring/sentence-bank/validation-report.json). Python reference fixtures and primary reading review are not native voice/application acceptance.",'']
    report+=['## H03 kana authoring (legacy T03)','','301 entries with VI/EN contexts, source-table denominator and revision-bound primary self-review; 29 remain in a separate reference group. See [kana authoring](../content-authoring/kana/README.md) and its [validation report](../content-authoring/kana/validation-report.json). No native voice or release pass.','']
    if e.get('native_audio_closure'):
        report+=['## T01 physical audio closure — 2026-11-09','','Two real-driver integration tests passed on physical iPhone 18 Pro / iOS 27.2. The owner explicitly confirmed the complete offline/silent and real interruption/headset/background cases. See [the physical audio report](t01-02-physical-audio-validation.json) for exact prompts, owner replies and revision-bound native results. Manual audio is owner-observed; there is no agent recording or physical screenshot review. Physical UI automation was blocked before execution by the free-profile app limit. Historical Simulator reports remain unchanged; no full-app or release acceptance is implied.','']
    if e['stale_evidence']:
        report+=['## Historical evidence drift','','The following prior handoff fingerprints differ from current canonical files. They remain historical; regeneration does not renew their review. The repository audit must continue to reject this drift.','']+['- '+x['task']+': '+x['path'] for x in e['stale_evidence']]+['']
    if c.get('source_reconciliation'):
        report+=['## H02 source/content review (legacy T02)','',c['source_reconciliation']['english_summary'],'',
                 'The primary review compares100 vocabulary pages,100 grammar explanation pages,104 Kanji unit reading pages,82 definition pages and12 milestone/header pages. '
                 'Inspect [the detailed review boundary](../content-authoring/source-reconciliation/review.json) and '
                 '[the ledger validation](../content-authoring/source-reconciliation/validation-report.json). '
                 'Recorded primary source/VI/EN/contextual-reading acceptance is distinct from machine integrity checks. Optional dictionary illustrations are not exhaustive. No independent human, native voice/device or release certification is implied.','']
    outputs[ROOT/'docs/audit/report.md']='\n'.join(report)
    policy=c['task_planning'];en_policy=policy['english']
    plan=['# Delivery plan (generated)','','Source: [owner HTML](index.html#roadmap). Edit its project-contract, never this export. P0 foundations and P1 delivery remain in the same N5+N4 product scope. The documentation gate applies before new development; task readiness also requires its own dependencies. Ready does not mean completed.','',f'## {policy["decision_id"]}: owner-approved decomposition ({policy["date"]})','',en_policy['owner_instruction'],'',en_policy['summary'],'']+['- '+rule for rule in en_policy['rules']]+['','## Group and task index','','| Group | Scope | Recorded status | Children |','| --- | --- | --- | --- |']
    phase=c['delivery_phases']
    handoff=phase['completed_documentation']
    gate=['## Documentation handoff — '+handoff['decision_id'],'',handoff['english'],'',phase['english']['documentation_scope'],'',phase['english']['gate_rule'],'','Current documentation gate: '+('ready for development' if not documentation_blockers(c,e) else 'not ready; '+', '.join(documentation_blockers(c,e)))+'.','', 'Read: '+', '.join('['+Path(path).name+']('+path.removeprefix('docs/')+')' for path in handoff['documents'])+'.','']
    focus=phase['review_focus']
    gate += ['## '+focus['decision_id']+': current review and P1 execution','',focus['english'],'','Foundation handoff: '+', '.join('['+Path(path).parent.name+'/'+Path(path).name+']('+path.removeprefix('docs/')+')' for path in focus['handoff_documents'])+'.','']
    migration=c['task_id_migration']
    gate += ['## '+migration['decision_id']+': task ID migration','',migration['english'],'','| Previous ID | Current ID |','| --- | --- |']
    gate += ['| '+old+' | '+new+' |' for old,new in migration['legacy_to_current'].items()]
    gate += ['']
    previous_map=migration.get('previous_current_to_current',{})
    if previous_map:
        gate+=['Active group renumbering (previous current roadmap → current):','| Previous group | Current group |','| --- | --- |']
        gate += ['| '+old+' | '+new+' |' for old,new in previous_map.items()]
        gate+=['']
    for title,key in [('Retired IDs from the previous current roadmap','retired_previous_current_to_document'),('Earlier retired IDs','retired_legacy_to_document')]:
        if migration.get(key):
            gate += [title+':']
            gate += ['- '+old+': ['+Path(path).name+']('+path.removeprefix('docs/')+')' for old,path in migration[key].items()]
            gate+=['']
    pending=[entry for entry in phase['tasks'] if entry['status']!='done']
    if pending:gate+=['| Open documentation task | Status | Reviewed scope |','| --- | --- | --- |']
    for entry in pending:gate.append('| '+entry['id']+' · '+entry['english']['title']+' | '+entry['status']+' | '+entry['english']['scope']+' |')
    plan[4:4]=gate+['']
    dev=c['development_plan'];en_dev=dev['english']
    plan[4:4]=['## '+dev['decision_id']+': development user stories and E2E','',en_dev['owner_instruction'],'',en_dev['summary'],'']+['- '+rule for rule in en_dev['rules']]+['']
    for t in roadmap_tasks(c):
        plan.append(f'| [{t["id"]}](index.html#{t["id"]}) | {t.get("planning_title_english",t["english"]["title"])} | {t["status"]} | '+', '.join(f'[{s["id"]}](index.html#{s["id"]})' for s in t.get('stories',[]))+' |')
    plan+=['']
    for t in roadmap_tasks(c):
        en=t['english'];plan += [f'## {t["id"]} / {t["priority"]} / {t["status"]}: {t.get("planning_title_english",en["title"])}',f'Phase: {t["phase"]}. Owner role: {t["owner"]}. Parent dependency traceability: {", ".join(t["depends"]) or "none"}.',f'Existing integration output: {en["deliverable"]}',f'Existing integration acceptance: {en["acceptance"]}','']
        if t['id']=='H01':plan+=['H01 children are coverage views of the existing delivery, inherit its status/evidence, and must not be assigned again. Existing evidence is macOS library/package testing, not iOS app acceptance.','']
        for s in t.get('stories',[]):
            en=s['english'];status='inherited from '+t['id']+' ('+t['status']+')' if s['tracking']=='parent' else s['status']
            plan += [f'### {s["id"]} / {status}: {en["title"]}','',f'Need: {en["need"]}',f'Type: {s["kind"]}. Role: {t["owner"]}. Priority: {t["priority"]}.',f'Output: {en["deliverable"]}',f'Execution dependencies: {", ".join(s["depends"]) or "none"}.',f'Feature contracts: {", ".join(s["features"])}.', 'Read: '+', '.join(f'[{Path(p).name}]({p.removeprefix("docs/")})' for p in s['contracts'])+'.','','Acceptance:','']+['- '+x for x in en['acceptance']]+['','Implementation / handoff checklist:','']+['- '+x for x in en['checklist']]+['',f'Required evidence: {en["evidence_required"]}', 'Recorded evidence: '+(', '.join(f'[{Path(p).name}]({p.removeprefix("docs/")})' for p in s['evidence']) if s['evidence'] else 'none; completion not established.') ,'']
            if 'e2e' in s:
                e2e=s['e2e'];ee=e2e['english']
                plan+=['User story: '+en['user_story'],'','E2E status: '+e2e['status']+'. Surface: '+e2e['surface']+'.','Additional E2E closure prerequisites: '+(', '.join(e2e['requires']) or 'none')+'.','Fixture: '+ee['fixture'],'']
                for case in ee['scenarios']:
                    plan+=['#### '+case['id']+' / '+case['type'],'','Given: '+case['given'],'When: '+case['when'],'Then: '+case['then'],'']
                plan+=['E2E completion evidence: '+dev['evidence_required_english'],'']
    outputs[ROOT/'docs/delivery-plan.md']='\n'.join(plan)
    # All Markdown is readable from the owner artifact without navigating to a separate file.
    docs={}
    for p in sorted((ROOT/'docs').rglob('*.md')):
        if p.name=='report.md' and p.parent.name=='audit':continue
        body=outputs.get(p,p.read_text());rel=str(p.relative_to(ROOT));docs[rel]={'title':next((l.lstrip('# ') for l in body.splitlines() if l.startswith('# ')),p.stem),'html':markdown(body,rel)}
    for p,body in outputs.items():
        if p.suffix=='.md':docs[str(p.relative_to(ROOT))]={'title':next((l.lstrip('# ') for l in body.splitlines() if l.startswith('# ')),p.stem),'html':markdown(body,str(p.relative_to(ROOT)))}
    data=dict(version=version_hash,documents=docs,prototypes={'app':embed_app(c),'widgets':embed_widgets(c)},history={k:markdown(v,'docs/01-discovery-and-open-questions.md' if k=='discovery' else 'docs/design-system/decisions.md') for k,v in c['decision_history'].items()})
    replacements={'STYLE':'<style>'+ (ROOT/'scripts/project_review.css').read_text()+'</style>','VIEW':render_view(c,e,version_hash),'DATA':'<script id="review-payload" type="application/json">'+encode(data)+'</script>','SCRIPT':'<script>'+ (ROOT/'scripts/project_review.js').read_text()+'</script>'}
    for name,value in replacements.items():text=re.sub(rf'<!-- {name}:START -->.*?<!-- {name}:END -->',lambda m:f'<!-- {name}:START -->\n{value}\n<!-- {name}:END -->',text,flags=re.S)
    outputs[PAGE]=text
    stale=[]
    for p,value in outputs.items():
        if args.check:
            if not p.exists() or p.read_text()!=value:stale.append(str(p.relative_to(ROOT)))
        else:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(value)
    if stale:raise SystemExit('Stale generated outputs: '+', '.join(stale))
    print(('Checked' if args.check else 'Wrote')+f' {len(outputs)} outputs; {len(docs)} embedded documents; contract {version_hash[:12]}.')

if __name__=='__main__':main()
