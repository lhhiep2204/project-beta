#!/usr/bin/env python3
"""Regression gate for one owner HTML, generated docs, provenance and review helpers.

Does not certify source-language semantics, browser rendering or native behavior.
"""
import hashlib, json, re, subprocess, sys, tempfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
sys.dont_write_bytecode=True
from sync_project_review import extract
ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=[];self.links=[];self.document_links=[];self.scripts=[];self.attrs=None;self.buffer=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'):self.ids.append(a['id'])
        for field in ('href','src'):
            if a.get(field):self.links.append(a[field])
        if 'data-doc' in a:self.document_links.append(a['data-doc'])
        if tag=='script':self.attrs=a;self.buffer=[]
    def handle_data(self,data):
        if self.attrs is not None:self.buffer.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.attrs is not None:
            self.scripts.append((self.attrs,''.join(self.buffer)));self.attrs=None

def need(value,message):
    if not value:raise AssertionError(message)
def run(args):
    result=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
    need(result.returncode==0,' '.join(args)+'\n'+result.stdout+result.stderr)
    return result.stdout.strip()

def validate_audio_closure(report, native, statuses):
    """A later physical run may close an archived task without rewriting evidence."""
    need(report['task']=='T01.02' and report['taskStatus']==statuses,'Wrong recorded pre-retirement task status')
    need(report['physicalDeviceUsed'] and report['environment']['platform']=='iOS','Audio closure needs a physical device')
    need(report['nativeTests']['passed']==2 and report['nativeTests']['failed']==0 and
         report['nativeTests']['skipped']==0,'Missing physical integration results')
    cases=report['e2eCases']
    need([case['id'] for case in cases]==['T01.02-E2E-01','T01.02-E2E-02'],'Missing physical audio cases')
    for case in cases:
        need(case['status']=='passed' and case['method']=='owner_manual_on_physical_device' and
             case['ownerAnswer'] and case['protocol'],'Physical audio pass without owner observation')
    required={'networkDisabled','silentMode','allFixtureTargets','dialogueAndSolo','restartAndStop',
              'actualInterruption','activeHeadsetDisconnect','backgroundForeground','noAutomaticResume'}
    need(required<=set(report['ownerObservedConditions']) and
         all(report['ownerObservedConditions'][key] for key in required),'Incomplete physical listening scope')
    for group in ('inputHashes','implementationHashes'):
        need(report[group]==native[group],'Physical run differs from the retained native baseline')
        for path,pin in report[group].items():
            need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==pin,'Stale physical audio evidence: '+path)
    previous=report['previousEvidence']
    need(hashlib.sha256((ROOT/previous['path']).read_bytes()).hexdigest()==previous['sha256'],
         'Historical native evidence changed after physical closure')
def local_link(url,source,ids=None):
    u=urlsplit(url)
    if u.scheme or url.startswith('//'):return
    if not u.path:
        if ids is not None and u.fragment:need(unquote(u.fragment) in ids,f'{source}: missing #{u.fragment}')
        return
    path=(source.parent/unquote(u.path)).resolve()
    need(path.exists(),f'{source.relative_to(ROOT)}: broken local link {url}')

def validate_task_plan(c):
    """Check executable children, inherited handoff scope and combined dependency DAG."""
    policy=c['task_planning']
    need(policy['status']=='approved' and policy['decision_id']=='PLAN-02','Missing owner planning decision')
    parents={t['id']:t for t in c['tasks']}
    items=dict(parents);children={}
    features={f['id'] for f in c['features']}
    statuses={'todo','ready','in_progress','blocked','done'}
    for parent in c['tasks']:
        if parent['id']!='H00':need(parent.get('stories'),'Missing decomposition for '+parent['id'])
        for child in parent.get('stories',[]):
            key=child['id']
            need(key not in items and re.fullmatch(re.escape(parent['id'])+r'\.\d{2}',key),'Duplicate or invalid child ID '+key)
            items[key]=child;children[key]=parent
            need(child['tracking'] in ('parent','independent'),'Unknown tracking mode '+key)
            need(child['tracking']!='parent' or parent['id']=='H01','Only archived runtime coverage inherits an existing handoff')
            need(child['kind'] in {'native','content','technical','locale','performance','release'},'Unknown child kind '+key)
            for field in ('area','title','need','deliverable','evidence_required','depends','features','contracts'):
                need(child.get(field),'Missing child field '+key+': '+field)
            for language in (child,child['english']):
                for field in ('title','need','deliverable','evidence_required'):
                    need(language.get(field),'Missing localized child field '+key+': '+field)
                for field in ('acceptance','checklist'):
                    need(len(language.get(field,[]))>=2,'Insufficient child '+field+': '+key)
            need(set(child['features'])<=features,'Unknown child feature '+key)
            need(set(child['contracts'])<=set(c['documents']),'Unknown child contract '+key)
            for path in child['evidence']:need((ROOT/path).is_file(),'Missing child evidence '+key)
            if child['tracking']=='parent':
                need('status' not in child and child['evidence']==['docs/audit/t01-runtime-validation.json'],'Archived runtime coverage must inherit handoff status/evidence')
            else:
                need(child.get('status') in statuses,'Unknown child status '+key)
                if child['status']=='done':need(child['evidence'],'Child done without evidence '+key)
    dev=c['development_plan']
    need(dev['decision_id']=='DEV-PLAN-01' and dev['status']=='owner_approved','Missing development story decision')
    tracked={key for key,item in items.items() if 'e2e' in item}
    need(len(dev['task_ids'])==len(set(dev['task_ids'])) and set(dev['task_ids'])==tracked,'Development E2E index differs from stories')
    for key,parent in children.items():
        child=items[key]
        active=child['phase']=='development' and child['tracking']=='independent' and child['status']!='done'
        need(not active or key in tracked,'Open development task has no E2E story '+key)
        if key not in tracked:continue
        need(child['phase']=='development' and child['tracking']=='independent','E2E attached to historical coverage '+key)
        e=child['e2e']
        need(e['surface'] in {'app','widget','localized_app_widget','physical_audio'},'Unknown E2E surface '+key)
        need(e['status'] in {'not_run','passed','failed','blocked'},'Unknown E2E status '+key)
        need(child['status']!='done' or e['status']=='passed','Development done without E2E pass '+key)
        need(e['status']!='passed' or e.get('evidence'),'E2E pass without execution evidence '+key)
        for path in e.get('evidence',[]):need((ROOT/path).is_file(),'Missing E2E evidence '+key)
        need(len(e['requires'])==len(set(e['requires'])),'Duplicate E2E prerequisite '+key)
        need(not set(e['requires'])&set(child['depends']),'Repeated execution/E2E prerequisite '+key)
        for language,details in [(child,e),(child['english'],e['english'])]:
            need(language.get('user_story') and details.get('fixture'),'Missing user story/fixture '+key)
            cases=details['scenarios']
            need(len(cases)==2 and {x['type'] for x in cases}=={'happy','edge'},'Missing success/failure E2E '+key)
            need([x['id'] for x in cases]==[key+'-E2E-01',key+'-E2E-02'],'Invalid E2E scenario IDs '+key)
            for case in cases:
                for field in ('given','when','then'):need(case.get(field),'Missing E2E '+field+' '+key)
        need([x['type'] for x in e['scenarios']]==[x['type'] for x in e['english']['scenarios']],'E2E language mismatch '+key)
    visited=set()
    def visit(key,active):
        need(key in items,'Unknown detailed dependency '+key)
        need(key not in active,'Cyclic detailed task dependencies: '+key)
        if key in visited:return
        item=items[key]
        edges=item['depends']+item.get('e2e',{}).get('requires',[])+[s['id'] for s in item.get('stories',[])]
        for dependency in edges:visit(dependency,active|{key})
        visited.add(key)
    for key in items:visit(key,set())
    def status(key):
        item=items[key]
        return children[key]['status'] if key in children and item['tracking']=='parent' else item['status']
    for key,parent in children.items():
        child=items[key]
        if child['tracking']=='independent' and child['status'] in ('ready','done'):
            need(all(status(d)=='done' for d in child['depends']),'Child ready/done with incomplete dependency '+key)
        if child['tracking']=='independent' and child['status']=='done':
            need(all(status(d)=='done' for d in child.get('e2e',{}).get('requires',[])),'Child done with incomplete E2E prerequisite '+key)
    for parent in c['tasks']:
        if parent['status']=='done':
            need(all(status(s['id'])=='done' for s in parent.get('stories',[])),'Group done with incomplete children '+parent['id'])
    return len(children)

def main():
    htmls=sorted(p for p in ROOT.rglob('*.html') if '.git' not in p.parts)
    need(htmls==[ROOT/'docs/index.html'],'Expected exactly docs/index.html; found '+str(htmls))
    text=htmls[0].read_text();parsed=Page(text);c=extract(text)
    duplicates=[i for i,n in Counter(parsed.ids).items() if n>1];need(not duplicates,'Duplicate HTML IDs '+str(duplicates))
    blocks={a.get('id'):s for a,s in parsed.scripts if a.get('type')=='application/json'}
    payload=json.loads(blocks['review-payload'])
    need(len(c['features'])==15,'Unexpected feature inventory')
    for collection in ['features','tasks','findings','questions']:
        ids=[x['id'] for x in c[collection]];need(len(ids)==len(set(ids)),f'Duplicate {collection} IDs')
    tasks={t['id']:t for t in c['tasks']};done=set()
    def visit(key,active):
        need(key in tasks,'Unknown task dependency '+key);need(key not in active,'Cyclic task dependencies')
        if key in done:return
        for dependency in tasks[key]['depends']:visit(dependency,active|{key})
        done.add(key)
    for key in tasks:visit(key,set())
    child_count=validate_task_plan(c)
    rendered=re.search(r'<!-- VIEW:START -->(.*?)<!-- VIEW:END -->',text,re.S)[1]
    for task in c['tasks']:
        for story in task.get('stories',[]):
            if 'e2e' not in story:continue
            import html
            need(html.escape(story['user_story'],quote=True) in rendered,'User story omitted from owner view '+story['id'])
            for case in story['e2e']['scenarios']:
                need('<h5>'+case['id']+' · ' in rendered,'E2E scenario omitted from owner view '+case['id'])
    # Guard the story completion boundary, including cycles hidden in E2E handoffs.
    import copy
    sample=next(s['id'] for t in c['tasks'] for s in t.get('stories',[])
                if s.get('e2e',{}).get('status')=='not_run')
    for mutation in ('missing_case','missing_then','closure_cycle','unknown_prerequisite','false_pass'):
        altered=copy.deepcopy(c)
        entry=next(s for t in altered['tasks'] for s in t.get('stories',[]) if s['id']==sample)
        if mutation=='missing_case':entry['e2e']['scenarios'].pop()
        elif mutation=='missing_then':entry['e2e']['english']['scenarios'][0]['then']=''
        elif mutation=='closure_cycle':entry['e2e']['requires'].append(sample)
        elif mutation=='unknown_prerequisite':entry['e2e']['requires'].append('T99.99')
        else:entry['e2e']['status']='passed'
        try:validate_task_plan(altered)
        except AssertionError:pass
        else:raise AssertionError('Development plan accepted invalid fixture '+mutation)
    # The final-documentation gate is derived from current canonical state.
    from sync_project_review import documentation_blockers, roadmap_tasks, review_findings
    phase=c['delivery_phases']
    doc_tasks=phase['tasks']
    need(phase['decision_id']=='DOC-PLAN-01' and doc_tasks,'Missing owner documentation gate')
    handoff=phase['completed_documentation']
    need(handoff['decision_id']=='DOC-PLAN-03' and handoff['status']=='owner_approved','Missing documentation handoff decision')
    need(handoff['summary'] and handoff['english'] and handoff['documents'],'Missing documentation handoff material')
    need(set(handoff['documents'])<=set(c['documents']),'Unknown documentation handoff contract')
    focus=phase['review_focus']
    need(focus['decision_id']=='DOC-PLAN-04' and focus['status']=='owner_approved','Missing current review decision')
    need(focus['completed_task_priorities']==['P0'] and focus['planned_priority']=='P1','Wrong priority disposition')
    need(set(focus['planned_finding_phases'])=={'development','acceptance','release'},'Wrong planned finding phases')
    for path in focus['handoff_documents']:need(path in payload['documents'],'Missing foundation handoff '+path)
    migration=c['task_id_migration']
    need(migration['decision_id']=='DOC-PLAN-06' and migration['status']=='owner_approved','Missing task ID migration decision')
    mapping=migration['legacy_to_current']
    current_ids={key for task in c['tasks'] for key in [task['id']]+[s['id'] for s in task.get('stories',[])]}
    need(set(mapping.values())==current_ids and len(mapping)==len(current_ids),'Task ID migration is not one-to-one')
    need(mapping['T06']=='T01' and mapping['T11']=='T06' and mapping['T12']=='T07','Wrong renumbered execution groups')
    retired=migration['retired_current_task']
    need(retired['group_id']=='T01' and retired['story_ids']==['T01.01','T01.02'] and retired['status']=='done',
         'Completed T01 is not recorded as a retired handoff')
    need(retired['document'] in c['documents'] and set(migration['retired_legacy_to_document'])=={'T05','T05.01','T05.02'},
         'Retired T01 crosswalk is incomplete')
    need(set(migration['retired_previous_current_to_document'])=={'T01','T01.01','T01.02'} and
         set(migration['retired_previous_current_to_document'].values())=={retired['document']},
         'Removed completed group is not linked to its handoff document')
    need(set(migration['previous_current_to_current'])=={f'T{i:02}' for i in range(2,9)} and
         set(migration['previous_current_to_current'].values())=={f'T{i:02}' for i in range(1,8)},
         'Previous current IDs do not map to the renumbered roadmap')
    need(tasks['T01']['priority']=='P1','Current T01 must inherit P1')
    visible_tasks={t['id'] for t in roadmap_tasks(c)}
    need(len({s['id'] for s in doc_tasks})==len(doc_tasks),'Duplicate documentation task')
    for entry in doc_tasks:
        need(entry['status'] in {'todo','ready','in_progress','blocked','done'},'Invalid documentation status')
        need(entry['scope'] and entry['english']['scope'] and entry['evidence'],'Missing documentation review scope/evidence')
        for path in entry['evidence']:need((ROOT/path).is_file(),'Missing documentation evidence '+path)
        need(entry['id'] in parsed.ids,'Documentation task missing from HTML '+entry['id'])
        need(('<tr id="'+entry['id']+'">' in rendered)==(entry['status']!='done'),'Completed documentation task listed '+entry['id'])
    for task in c['tasks']:
        expected='documentation' if task['id']=='H00' else 'acceptance' if task['id']=='T06' else 'release' if task['id']=='T07' else 'development'
        need(task['phase']==expected,'Wrong phase classification '+task['id'])
        need(all(s['phase']==expected for s in task.get('stories',[])),'Child phase mismatch '+task['id'])
        need(('<article id="'+task['id']+'"' in rendered)==(task['id'] in visible_tasks),'Execution roadmap disposition mismatch '+task['id'])
        if task['id'] not in visible_tasks:
            for key in [task['id']]+[s['id'] for s in task.get('stories',[])]:
                need(key in parsed.ids,'Missing historical handoff anchor '+key)
                need(not re.search(r'<(?:article|details) id="'+re.escape(key)+'"',rendered),'Completed foundation rendered as task '+key)
    visible_findings={f['id'] for f in review_findings(c)}
    for finding in c['findings']:
        need((finding['id'] in parsed.ids)==(finding['id'] in visible_findings),'Current finding disposition mismatch '+finding['id'])
    need(('findings' in parsed.ids)==bool(visible_findings),'Empty current issue section rendered')
    # Scheduled P1 findings remain open; actual documentation defects must surface.
    scheduled=next(f for f in c['findings'] if f['status']=='open' and f['phase']=='development')
    need(scheduled['id'] not in visible_findings,'Scheduled P1 finding duplicated')
    altered=copy.deepcopy(c)
    moved=next(f for f in altered['findings'] if f['id']==scheduled['id']);moved['phase']='documentation'
    need(moved['id'] in {f['id'] for f in review_findings(altered)} and moved['id'] in documentation_blockers(altered,{'stale_evidence':[]}),'Documentation finding hidden by P1 priority')
    altered=copy.deepcopy(c);next(t for t in altered['tasks'] if t['id']==scheduled['task'])['priority']='P0'
    need(scheduled['id'] in {f['id'] for f in review_findings(altered)},'Unscheduled foundation issue hidden')
    current_evidence=json.loads((ROOT/'docs/audit/source-audit.json').read_text())
    blockers=documentation_blockers(c,current_evidence)
    need(('Documentation hoàn tất · Ready for development' in text)==(not blockers),'HTML gate contradicts documentation state')
    # Regression: each required input independently closes the gate.
    import copy
    for mutate in ('task','T00','proposal','finding','drift'):
        altered=copy.deepcopy(c);evidence_copy=copy.deepcopy(current_evidence)
        if mutate=='task':altered['delivery_phases']['tasks'][0]['status']='todo'
        elif mutate=='T00':altered['tasks'][0]['status']='todo'
        elif mutate=='proposal':altered['questions'].append({'id':'gate-regression'})
        elif mutate=='finding':altered['findings'].append({'id':'gate-regression','status':'open','phase':'documentation'})
        else:evidence_copy['stale_evidence'].append({'task':'gate-regression','path':'fixture'})
        need(documentation_blockers(altered,evidence_copy),'Documentation gate failed negative fixture '+mutate)
    run(['python3','scripts/validate_kana.py','--complete','--self-test','--check'])
    kana_report=json.loads((ROOT/'docs/content-authoring/kana/validation-report.json').read_text())
    if tasks['H03']['status']=='done':
        need(kana_report['task_authoring_acceptance_complete'],'Kana handoff marked done without reviewed authoring evidence')
    run(['python3','scripts/validate_sentence_bank.py','--self-test','--check'])
    candidate_report=json.loads((ROOT/'docs/content-authoring/sentence-bank/validation-report.json').read_text())
    if tasks['H04']['status']=='done':
        need(candidate_report['task_authoring_acceptance_complete'],'Candidate handoff closure without complete target/dependency evidence')
    for child in tasks['H04']['stories']:
        if child['status']!='done':continue
        if child['id']=='H04.01':
            need(candidate_report['alignment_only_or_reviewed_coverage']==candidate_report['targets'],'H04.01 missing target/form/sense alignment')
        elif child['id']=='H04.02':
            need(candidate_report['reviewed_candidates']==candidate_report['candidates'],'H04.02 missing candidate dependency review')
        elif child['id']=='H04.03':
            need(candidate_report['speech_authoring_complete'],'H04.03 missing speech/context review')
    owner_audit=json.loads((ROOT/'docs/audit/source-audit.json').read_text())
    need(owner_audit['counts']['bound_entries']==candidate_report['vocabulary_bound_entries'],
         'Bound vocabulary census differs between owner review and T04')
    # An H02 ledger pass checks integrity, not linguistic or release acceptance.
    run(['python3','scripts/validate_source_reconciliation.py','--self-test','--check'])
    t02_report=json.loads((ROOT/'docs/content-authoring/source-reconciliation/validation-report.json').read_text())
    if tasks['H02']['status']=='done':
        need(t02_report['task_acceptance_complete'],'H02 marked done without complete source/content acceptance')
    if tasks['H01']['status']=='done':
        runtime=json.loads((ROOT/'docs/audit/t01-runtime-validation.json').read_text())
        need(runtime['task']=='P0-T01' and runtime['swiftTestsPassed']>0,'Missing T01 execution evidence')
        for group in ('inputHashes','implementationHashes'):
            for path,pin in runtime[group].items():
                need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==pin,'Stale T01 runtime evidence: '+path)
    if c.get('native_proof'):
        native=json.loads((ROOT/c['native_proof']['report']).read_text())
        need(native['task']=='P0-T05' and native['nativeTestsPassed']>0,'Missing bounded T05 execution evidence')
        for group in ('inputHashes','implementationHashes'):
            for path,pin in native[group].items():
                need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==pin,'Stale T05 native evidence: '+path)
        run(['python3','scripts/build_native_proof.py','--check'])
        def restore_task_id(task_id):
            for old,new in sorted(mapping.items(),key=lambda pair:len(pair[1]),reverse=True):
                if task_id==new:return old
            return task_id
        statuses={restore_task_id(t['id']):t['status'] for t in [tasks['T01'],*tasks['T01']['stories']]}
        closure_path=c['native_proof'].get('closure_report')
        if closure_path:
            closure=json.loads((ROOT/closure_path).read_text())
            prior=retired['recorded_task_status']
            validate_audio_closure(closure,native,prior)
            need(prior==closure['taskStatus'] and all(s=='done' for s in prior.values()),
                 'Retired audio task lacks completed recorded status')
            # These fixtures ensure that a status edit or synthetic event cannot
            # replace the actual owner-observed physical evidence.
            for mutation in ('simulator','unobserved','missing_case','stale_input'):
                altered=copy.deepcopy(closure)
                if mutation=='simulator':altered['physicalDeviceUsed']=False
                elif mutation=='unobserved':altered['ownerObservedConditions']['actualInterruption']=False
                elif mutation=='missing_case':altered['e2eCases'].pop()
                else:altered['inputHashes'][next(iter(altered['inputHashes']))]='0'*64
                try:validate_audio_closure(altered,native,prior)
                except AssertionError:pass
                else:raise AssertionError('Audio closure accepted invalid fixture '+mutation)
        else:
            need(statuses==native['taskStatus'],'Current T01 status differs from bounded historical T05 execution evidence')
            if tasks['T01']['status']=='done':
                need(not native['missingEvidence'],'T05 closed with missing native/physical evidence')
    if c.get('localization_infrastructure'):
        localization=json.loads((ROOT/c['localization_infrastructure']['report']).read_text())
        need(localization['task']=='T09.01' and mapping['T09.01']=='T04.01' and localization['runtimeTestsPassed']>=24
             and localization['nativeTestsPassed']>=1,'Missing T09.01 execution evidence')
        for group in ('inputHashes','implementationHashes'):
            for path,pin in localization[group].items():
                need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==pin,'Stale T09.01 localization evidence: '+path)
        run(['python3','scripts/validate_localization.py','--self-test','--check'])
        story=next(s for s in tasks['T04']['stories'] if s['id']=='T04.01')
        need(story['status']==localization['taskStatus'],'T09.01 status differs from execution evidence')
    for f in c['findings']:need(f['task'] in tasks,'Unknown finding task')
    for t in c['tasks'].copy():
        if t['status'] in ('ready','done'):need(all(tasks[p]['status']=='done' for p in t['depends']),'Task marked ready with unfinished dependency: '+t['id'])
    need(all(q['status']=='proposed' for q in c['questions']),'Do not silently promote owner proposals')
    for url in parsed.links:local_link(url,htmls[0],set(parsed.ids))
    for key in parsed.document_links:need(key in payload['documents'],'Missing embedded doc '+key)
    for key,doc in payload['documents'].items():
        need((ROOT/key).is_file(),'Unknown embedded doc '+key)
        p=Page(doc['html'])
        for target in p.document_links:need(target in payload['documents'],'Missing nested embedded doc '+target)
    files=[p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and '__pycache__' not in p.parts]
    json_count=0
    for p in files:
        if p.suffix=='.json':json.loads(p.read_text());json_count+=1
        elif p.suffix=='.jsonl':
            for line in p.read_text().splitlines():
                if line.strip():json.loads(line)
        elif p.suffix=='.md':
            for url in re.findall(r'\[[^\]]*\]\(([^)\n]+)\)',p.read_text()):local_link(url,p)
        elif p.suffix=='.py':compile(p.read_bytes(),str(p),'exec')
    review=json.loads((ROOT/'docs/content-authoring/batch-review.json').read_text())
    for m in review['canonical_content_manifest']:
        b=(ROOT/m['path']).read_bytes();need(hashlib.sha256(b).hexdigest()==m['sha256'] and len(b)==m['bytes'],'Stale current content pin '+m['path'])
    lesson_data=[json.loads(p.read_text()) for p in sorted((ROOT/'docs/content-authoring').glob('lesson-*.json'))]
    coverage=json.loads((ROOT/'docs/content-authoring/batch-source-coverage.json').read_text())
    for lesson,row in zip(lesson_data,coverage['lessons']):
        need(lesson['reference_lesson_number']==row['lesson'],'Coverage lesson order')
        for field,key in [('vocabulary','vocabulary_entries'),('grammar_points','grammar_points'),('sentence_patterns','sentence_patterns'),('examples','original_examples')]:need(len(lesson[field])==row[key],'Coverage count drift')
    need(sum(len(l['examples']) for l in lesson_data)==review['counts']['examples'],'Stale review counts')
    source_counts=json.loads((ROOT/'docs/audit/source-audit.json').read_text())['counts']
    # B-U-59: source names are content, with their own stable identities.
    names=json.loads((ROOT/'docs/content-authoring/source-reconciliation/proper-name-review.json').read_text())
    by_lesson={l['reference_lesson_number']:l for l in lesson_data}
    for item in names['items']:
        lesson=by_lesson[item['lesson']]
        matches=[w for w in lesson['vocabulary'] if w['id']==item['item_id']]
        need(len(matches)==1,'Restored proper-name identity missing: '+item['name'])
        form=matches[0]['forms'][0]
        need(''.join(s['base'] for s in form['japanese']['segments'])==item['name'], 'Proper-name spelling drift: '+item['name'])
        need(form['kana_reading']==item['reading'],'Proper-name reading drift: '+item['name'])
    for lesson in lesson_data:
        need(not any('fictional' in x.lower() for x in lesson['coverage']['omitted']), 'Revoked name omission in lesson coverage')
    inventory=json.loads((ROOT/'docs/content-authoring/source-reconciliation/source-inventory.json').read_text())
    ledger=json.loads((ROOT/'docs/content-authoring/source-reconciliation/vocabulary-ledger.json').read_text())['vocabulary']
    mapped={r['source_row']:r for r in ledger}
    need(len(mapped)==len(ledger),'Duplicate vocabulary source row')
    for page in inventory['vocabulary_pages']:
        words={w['id']:w for w in by_lesson[page['lesson']]['vocabulary']}
        for row in page['rows']:
            key=f"{page['source_id']}:{page['pdf_page']}:{row['ordinal']}"
            need(row['scope']=='included','Revoked fictional-name source exclusion: '+key)
            record=mapped.get(key,{})
            need(record.get('disposition')=='mapped' and record.get('targets'), 'Unresolved vocabulary source row: '+key)
            for target in record['targets']:
                word=words.get(target['id'])
                need(word is not None,'Source row points outside its lesson: '+key)
                need(set(target['form_keys']) <= {f['key'] for f in word['forms']},'Source row form missing: '+key)
    for key in ['vocabulary','grammar_points','sentence_patterns','examples','dialogues','kanji_word_occurrences']:
        need(source_counts[key]==review['counts'][key],'Audit and content review count mismatch: '+key)
    need(source_counts['unit_word_occurrences']+source_counts['character_example_occurrences']==source_counts['kanji_word_occurrences'],'Inconsistent Kanji word subtotals')
    # Parse every executable JS block, including both embedded prototype documents.
    scripts=[s for a,s in parsed.scripts if a.get('type')!='application/json']
    for name,source in payload['prototypes'].items():
        p=Page(source);need(len(p.ids)==len(set(p.ids)),'Prototype duplicate IDs '+name)
        need(not any(not x.startswith('#') for x in p.links),'Prototype external navigation/dependency '+name)
        for attrs,script in p.scripts:
            if attrs.get('type')=='application/json':json.loads(script)
            else:scripts.append(script)
    with tempfile.TemporaryDirectory(prefix='beta-js-') as temp:
        for n,script in enumerate(scripts):
            path=Path(temp)/f'block-{n}.js';path.write_text(script);run(['node','--check',str(path)])
    for p in files:
        if p.suffix=='.js':run(['node','--check',str(p)])
    helper=r'''
const assert=require('node:assert/strict');
const vm=require('node:vm'),fs=require('node:fs');
const x=require('./docs/design-system/review-logic.js');
assert.equal(x.normalize('ĐIỆN THOẠI'),'dien thoai');
assert.equal(x.normalize('ガッコウ'),x.normalize('がっこう'));
assert.notEqual(x.normalize('が'),x.normalize('か'));
assert.equal(x.matchRank(['学校'],'がっこう'),Infinity);
assert.equal(x.matchRank(['がっこう'],'ガッコウ'),0);
assert.equal(x.matchRank(['abc'],'ab'),1);assert.equal(x.matchRank(['abc'],'bc'),2);
assert.equal(x.matchRank(['abc'],''),Infinity);
const n5=Array.from({length:25},(_,i)=>i+1),n4=Array.from({length:25},(_,i)=>i+26);
assert.deepEqual(x.planPrefix(n5,3,6,true).changed,[4,5,6]);
assert.deepEqual(x.planPrefix(n5,6,5,false).changed,[5,6]);
assert.deepEqual(x.planPrefix(n4,25,30,true).changed,[26,27,28,29,30]);
assert.equal(x.planPrefix(n4,30,28,false).next,27);
assert.deepEqual(x.planPrefix(n4,30,28,true).changed,[]);
assert.throws(()=>x.planPrefix(n4,25,3,true));
const context={window:{}};vm.runInNewContext(fs.readFileSync('./docs/design-system/review-data.js','utf8'),context);
const d=context.window.PROJECT_BETA_REVIEW;
assert.equal(d.lessons.length,2);assert.equal(d.units.length,3);assert.equal(d.kana.length,57);
assert.equal(new Set(d.targets.map(t=>t.key)).size,d.targets.length);
for(const l of d.lessons){const source=JSON.parse(fs.readFileSync(`docs/content-authoring/lesson-${String(l.reference_lesson_number).padStart(2,'0')}.json`));for(const v of l.vocabulary)assert.equal(JSON.stringify(v),JSON.stringify(source.vocabulary.find(w=>w.id===v.id)));for(const dia of l.dialogues)assert.equal(JSON.stringify(dia),JSON.stringify(source.dialogues.find(w=>w.id===dia.id)));}
console.log('Review helper assertions passed; not browser/native tests.');
// Exercise the actual roadmap filtering code with a DOM model, not a browser.
const owner=JSON.parse(fs.readFileSync('./docs/index.html','utf8').match(/<script id="project-contract" type="application\/json">(.*?)<\/script>/s)[1]);
const nodes=new Map(),events={},windowEvents={};
const groups=owner.tasks.filter(task=>!(task.status==='done'&&(task.phase==='documentation'||owner.delivery_phases.review_focus.completed_task_priorities.includes(task.priority)))).map(task=>{
  const group={id:task.id,hidden:false,dataset:{phase:task.phase,priority:task.priority,status:task.status,taskSearch:task.id+' '+(task.planning_title||task.title)},matches:selector=>selector.includes('.task-group'),closest:()=>group,scrollIntoView(){}};
  nodes.set(group.id,group);
  const children=(task.stories||[]).map(story=>{
    const child={id:story.id,hidden:false,open:false,dataset:{status:story.tracking==='parent'?task.status:story.status,taskSearch:[story.id,story.title,story.area,story.need,story.deliverable,story.english.title,story.user_story||'',...(story.e2e?.scenarios||[]).map(c=>c.id)].join(' ')},matches:selector=>selector.includes('.task-story'),closest:()=>group,scrollIntoView(){}};
    nodes.set(child.id,child);return child;
  });
  group.querySelectorAll=selector=>selector==='.task-story'?children:[];
  return group;
});
for(const id of ['task-phase','task-filter','task-query','task-results'])nodes.set(id,{value:id==='task-phase'?'development':id==='task-filter'?'all':'',addEventListener(event,handler){events[id+':'+event]=handler;}});
const state={hash:''};
const taskContext={byId:id=>nodes.get(id),location:state,window:{addEventListener:(event,handler)=>windowEvents[event]=handler},document:{querySelectorAll:()=>groups,addEventListener:(event,handler)=>events[event]=handler}};
const source=fs.readFileSync('./scripts/project_review.js','utf8');
vm.runInNewContext(source.slice(source.indexOf('  const taskGroups='),source.indexOf("  document.querySelectorAll('[data-history]')")),taskContext);
for(const id of ['H00','H01','H02','H03','H04','H01.01'])assert.equal(nodes.has(id),false);
assert.equal(nodes.get('T06').hidden,true);assert.equal(nodes.get('T01').hidden,false);
assert.equal(nodes.get('T01.02').hidden,false);assert.equal(nodes.get('T01').dataset.phase,'development');assert.equal(nodes.get('T01').dataset.priority,'P1');
nodes.get('task-phase').value='all';events['task-phase:change']();
function filter(status,query=''){
  nodes.get('task-filter').value=status;nodes.get('task-query').value=query;events['task-filter:change']();
}
filter('ready');
assert.equal(nodes.get('T04').hidden,false);assert.equal(nodes.get('T04.02').hidden,false);
assert.equal(nodes.get('T04.01').hidden,true);
filter('done');
assert.equal(nodes.get('T01.01').hidden,true);assert.equal(nodes.get('T01.02').hidden,true);assert.equal(nodes.get('T04.01').hidden,false);assert.equal(nodes.get('T01').hidden,true);
filter('P1');assert.equal(nodes.get('T01.02').hidden,false);
filter('P0');assert(groups.every(group=>group.hidden));
filter('P1','chon n5/n4 lan dau');
assert.equal(nodes.get('T01.02').hidden,false);assert.equal(nodes.get('T01.03').hidden,true);assert.equal(nodes.get('T02').hidden,true);
filter('all','danh dau/bo da hoc');assert.equal(nodes.get('T01.06').hidden,false);
filter('all','T01.06-E2E-02');assert.equal(nodes.get('T01.06').hidden,false);assert.equal(nodes.get('T01.05').hidden,true);
nodes.get('task-phase').value='release';events['task-phase:change']();
filter('all');assert.equal(nodes.get('T07').hidden,false);assert.equal(nodes.get('T01').hidden,true);
state.hash='#T01.02';windowEvents.hashchange();assert.equal(nodes.get('task-phase').value,'all');
filter('all','no-such-task');assert(groups.every(group=>group.hidden));
state.hash='#T01.02';windowEvents.hashchange();
assert.equal(nodes.get('task-filter').value,'all');assert.equal(nodes.get('task-query').value,'');
assert.equal(nodes.get('T01.02').open,true);assert.equal(nodes.get('T01').hidden,false);
filter('done');events.click({target:{closest:()=>({hash:state.hash})}});
assert.equal(nodes.get('T02').hidden,false);
console.log('Roadmap filter/deep-link model assertions passed; not browser visual/interaction tests.');
'''
    print(run(['node','-e',helper]))
    for command in [
        ['python3','scripts/validate_authoring_samples.py','--self-test'],
        ['python3','scripts/validate_authoring_batch.py','--complete','--self-test'],
        ['python3','scripts/render_authoring_content.py','--check'],
        ['python3','scripts/build_design_review.py','--check'],
        ['python3','scripts/sync_project_review.py','--check']]:
        output=run(command);print(output.splitlines()[0] if not output.startswith('{') else 'Complete batch structural validation passed.')
    print(f'PASS: one HTML; {len(payload["documents"])} embedded docs; {json_count} JSON files; {child_count} detailed tasks/coverage views; local links, manifest, combined task DAG, all JS blocks and generated outputs checked.')
    print('LIMITS: source semantics/completeness, browser visual/interactions and native/device/performance/release acceptance are not certified.')
if __name__=='__main__':main()
