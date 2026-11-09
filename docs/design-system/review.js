/* Interactive HTML sketch; not production app code or a runtime-content schema. */
(function () {
  'use strict';
  const D = window.PROJECT_BETA_REVIEW;
  const L = window.ProjectBetaReviewLogic;
  const storageKey = 'projectbeta-design-system-review-v1';
  const defaults = { level: null, language: 'system', appearance: 'system', furigana: true, learned: { N5: 0, N4: 25 }, favorites: [] };
  let saved, storageAvailable = true;
  try { saved = JSON.parse(localStorage.getItem(storageKey) || 'null'); } catch { saved = null; storageAvailable = false; }
  const S = { ...defaults, ...(saved || {}), learned: { ...defaults.learned, ...(saved?.learned || {}) }, favorites: Array.isArray(saved?.favorites) ? saved.favorites : [] };
  if (!['N5', 'N4'].includes(S.level)) S.level = null;
  let route = { kind: 'lessons' }, tab = 'lessons', pendingRetry = null, pendingConfirm = null, menuTarget = null;
  let audio = null, audioTimer = null, audioRevision = 0, holdTimer = null, holdOrigin = null;
  let searchQuery = '', searchScope = null, searchOrigin = null, searchTimer = null, searchRevision = 0, searchHits = [];
  let favoriteType = 'all', favoriteLevel = 'all', kanaScript = 'hiragana', kanaGroup = 'basic', selectedKana = null;
  const shell = document.getElementById('app-shell');
  const main = document.getElementById('app-main');
  const contextDialog = document.getElementById('context-dialog');
  const confirmDialog = document.getElementById('confirm-dialog');
  const media = matchMedia('(prefers-color-scheme: dark)');
  const words = {
    lessons: ['Bài học', 'Lessons'], kanji: ['Kanji', 'Kanji'], favorites: ['Yêu thích', 'Favorites'], settings: ['Cài đặt', 'Settings'],
    choose: ['Bạn muốn bắt đầu với cấp độ nào?', 'Which level would you like to start with?'], free: ['Cả hai cấp độ đều có thể truy cập tự do.', 'Both levels are freely accessible.'],
    vocabulary: ['Từ vựng', 'Vocabulary'], grammar: ['Ngữ pháp', 'Grammar'], patterns: ['Mẫu câu', 'Sentence patterns'], dialogues: ['Hội thoại', 'Dialogues'],
    alphabet: ['Hiragana / Katakana', 'Hiragana / Katakana'], learned: ['Đã học', 'Learned'], mark: ['Đánh dấu đã học', 'Mark as learned'], unmark: ['Bỏ dấu đã học', 'Mark as not learned'],
    add: ['Thêm vào yêu thích', 'Add to favorites'], remove: ['Bỏ yêu thích', 'Remove from favorites'], close: ['Đóng', 'Close'], cancel: ['Hủy', 'Cancel'], confirm: ['Xác nhận', 'Confirm'],
    stop: ['Dừng', 'Stop'], search: ['Tìm kiếm', 'Search'], global: ['Toàn app', 'All content'], within: ['Trong bài này', 'This lesson'], jump: ['Tới mục', 'Jump to'],
    all: ['Tất cả', 'All'], noFavorites: ['Chưa có mục yêu thích', 'No favorites yet'], favoriteHelp: ['Nhấn giữ nội dung để thêm vào yêu thích.', 'Touch and hold content to add a favorite.'],
    noFiltered: ['Không có mục phù hợp bộ lọc', 'No matching favorites'], noResults: ['Không tìm thấy kết quả', 'No results'], queryHelp: ['Nhập từ hoặc nội dung bạn muốn tìm.', 'Enter a word or phrase to search.'],
    waiting: ['Đang chờ truy vấn ổn định…', 'Waiting for input…'], searching: ['Đang tìm…', 'Searching…'], language: ['Ngôn ngữ', 'Language'], appearance: ['Giao diện', 'Appearance'],
    system: ['Theo hệ thống', 'System'], light: ['Sáng', 'Light'], dark: ['Tối', 'Dark'], level: ['Cấp độ', 'Level'], unit: ['Unit', 'Unit'], lesson: ['Bài', 'Lesson'],
    saved: ['Đã lưu thay đổi.', 'Change saved.'], failed: ['Không lưu được thay đổi. Trạng thái cũ được giữ lại.', 'Could not save. The previous state is preserved.'],
    retry: ['Thử lại', 'Retry'], empty: ['Nội dung chưa sẵn sàng', 'Content unavailable'], basic: ['Cơ bản', 'Basic'], voiced: ['Âm đục / bán đục', 'Voiced / semi-voiced'],
    combined: ['Âm ghép / mở rộng', 'Combined / extended'], special: ['Cách dùng đặc biệt', 'Special uses'], reference: ['Tham khảo cổ / hiếm', 'Historical / rare reference'], examples: ['Ví dụ', 'Examples']
  };
  const paths = {
    lessons: '<path d="M3 4h7a3 3 0 0 1 2 1 3 3 0 0 1 2-1h7v15h-7a3 3 0 0 0-2 1 3 3 0 0 0-2-1H3z"/><path d="M12 5v15"/>',
    kanji: '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M7 8h10m-5-2v12m-4-5 8 4m0-4-8 4"/>',
    favorites: '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3l-5.6 2.9 1.1-6.2L3 9.6l6.2-.9z"/>',
    settings: '<circle cx="12" cy="12" r="3"/><path d="m10 3-1 3-3 1-3 3 2 2-1 3 3 3 3-1 2 4 3-2 2-2 3-3-1-3-2-2-2-3-3 1z"/>',
    search: '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6"/>', back: '<path d="m14 5-7 7 7 7"/>',
    speaker: '<path d="m11 5-6 4H2v6h3l6 4z"/>', waves: '<path d="m11 5-6 4H2v6h3l6 4z"/><path d="M15 8a6 6 0 0 1 0 8m3-11a10 10 0 0 1 0 14"/>',
    stop: '<rect x="6" y="6" width="12" height="12" rx="1" fill="currentColor" stroke="none"/>', check: '<path d="m5 12 4 4L20 5"/>'
  };
  function esc(value) { return String(value ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
  function icon(name) { return `<svg viewBox="0 0 24 24" aria-hidden="true">${paths[name] || paths.lessons}</svg>`; }
  function language() {
    if (S.language !== 'system') return S.language;
    const code = (navigator.language || 'en').toLowerCase();
    if (code.startsWith('zh')) return 'zh-Hans';
    return D.languages.includes(code.split('-')[0]) ? code.split('-')[0] : 'en';
  }
  function t(key) { return words[key]?.[language() === 'vi' ? 0 : 1] || key; }
  function text(value) { return typeof value === 'string' ? value : value?.[language()] ?? value?.en ?? ''; }
  function meaning(value) { return `<p class="meaning" dir="auto">${esc(text(value))}${language() !== 'en' && !value?.[language()] ? '<span class="fallback-label">English</span>' : ''}</p>`; }
  function jp(value) { return (value?.segments || []).map(s => s.ruby ? `<ruby>${esc(s.base)}<rt>${esc(s.ruby)}</rt></ruby>` : esc(s.base)).join(''); }
  function plain(value) { return (value?.segments || []).map(s => s.base).join(''); }
  function lesson() { return D.lessons.find(item => item.id === route.id); }
  function unit() { return D.units.find(item => item.id === route.unitId || item.id === route.id); }
  function info(key) { return D.targets.find(item => item.key === key); }
  function targetRoute(target) { return target.routes?.find(r => r.level === (favoriteLevel === 'all' ? S.level : favoriteLevel)) || target.route; }
  function favoriteAttrs(key) { return `data-favorite="${esc(key)}" tabindex="0"`; }
  function feedback(message, retry) { document.getElementById('feedback').textContent = message; pendingRetry = retry || null; document.getElementById('retry').hidden = !pendingRetry; document.getElementById('retry').textContent = t('retry'); }
  function persisted() { return { level: S.level, language: S.language, appearance: S.appearance, furigana: S.furigana, learned: { ...S.learned }, favorites: S.favorites.map(item => ({ ...item })) }; }
  function commit(transform, message, retry) {
    const next = persisted(); transform(next);
    try {
      if (document.getElementById('review-failure').checked) throw new Error('Review save failure');
      try { localStorage.setItem(storageKey, JSON.stringify(next)); } catch { storageAvailable = false; }
      Object.assign(S, next);
      feedback(`${message || t('saved')}${storageAvailable ? '' : (language() === 'vi' ? ' · Chỉ phiên duyệt; trình duyệt không cho lưu lại.' : ' · Review session only; browser storage is unavailable.')}`);
      render(); return true;
    } catch { feedback(t('failed'), retry || (() => commit(transform, message))); render(); return false; }
  }
  function appearance() {
    const theme = S.appearance === 'system' ? (media.matches ? 'dark' : 'light') : S.appearance;
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.setProperty('--accent', D.tokens.colors.accent[theme]);
    document.documentElement.style.setProperty('--on-accent', D.tokens.colors.on_accent[theme]);
    shell.dir = ['ar', 'he'].includes(language()) ? 'rtl' : 'ltr';
    shell.classList.toggle('no-ruby', !S.furigana);
  }
  function owner(r) { return `${r.kind}:${r.id || r.unitId || ''}`; }
  function navigate(next, nextTab) { if (owner(next) !== owner(route)) stopAudio(false); cancelHold(); route = next; if (nextTab) tab = nextTab; render(); }
  function rootRoute(name) { return { kind: name }; }
  function back() {
    if (route.fromSearch) { navigate({ kind: 'search' }); return; }
    if (route.kind === 'search') { cancelSearch(); searchQuery = ''; searchHits = []; navigate(searchOrigin || rootRoute(tab)); return; }
    if (route.kind === 'character') { navigate({ kind: 'unit', id: route.unitId }); return; }
    navigate(rootRoute(tab));
  }
  function row(title, subtitle, destination, key, mark = false) {
    return `<button class="list-row" type="button" data-route='${esc(JSON.stringify(destination))}' ${key ? favoriteAttrs(key) : ''}><span class="row-body">${subtitle ? `<span class="meta">${esc(subtitle)}</span>` : ''}<span class="row-title" dir="auto">${esc(title)}</span></span>${mark ? `<span class="learned-mark">${icon('check')}</span>` : ''}<span class="chevron" aria-hidden="true">›</span></button>`;
  }
  function audioButton(target, label) { return `<button type="button" class="icon-button speaker" data-audio="${esc(target)}" data-audio-label="${esc(label)}" aria-label="${esc(label)}">${icon('speaker')}</button>`; }
  function contentRow(japanese, translation, target, label, favoriteKey, unavailableReason = '') {
    const action = unavailableReason
      ? `<span class="speech-unavailable" role="status">${language() === 'vi' ? 'Chưa có ngữ cảnh phát âm' : 'Speech context unavailable'}</span>`
      : audioButton(target, label);
    return `<div class="content-row" ${favoriteKey ? favoriteAttrs(favoriteKey) : ''}><div><div class="jp" lang="ja">${jp(japanese)}</div>${translation ? meaning(translation) : ''}</div>${action}</div>`;
  }
  function plan(lessonData, desired) { return L.planPrefix(D.lessonOrder[lessonData.source_level_label], S.learned[lessonData.source_level_label], lessonData.reference_lesson_number, desired); }
  function setLearned(lessonData, desired) {
    const level = lessonData.source_level_label, before = S.learned[level], change = plan(lessonData, desired);
    if (!change.changed.length) { feedback(t('saved')); return; }
    const apply = () => {
      if (S.learned[level] !== before) { setLearned(lessonData, desired); return; }
      commit(next => { next.learned[level] = change.next; }, t('saved'), () => setLearned(lessonData, desired));
    };
    if (change.changed.length > 1) {
      const range = `${change.changed[0]}–${change.changed.at(-1)}`;
      document.getElementById('confirm-title').textContent = `${desired ? t('mark') : t('unmark')}: ${level} ${range}?`;
      document.getElementById('confirm-copy').textContent = language() === 'vi' ? 'Chỉ thay đổi các bài trong phạm vi này. Cấp độ còn lại giữ nguyên.' : 'Only the lessons in this range change. The other level is unchanged.';
      pendingConfirm = apply; confirmDialog.showModal();
    } else apply();
  }
  function navHTML() { return ['lessons', 'kanji', 'favorites', 'settings'].map(name => `<button type="button" class="${name === tab ? 'selected ' : ''}nav-button" data-nav="${name}">${icon(name)}<span>${t(name)}</span></button>`).join(''); }
  function collectionHTML() {
    if (!S.level || !['lessons', 'kanji'].includes(tab) || route.kind === 'search') return '';
    const entries = tab === 'lessons' ? D.lessons.filter(item => item.source_level_label === S.level) : D.units.filter(item => item.source_level_label === S.level);
    return `<h2>${t(tab)}</h2><p class="meta" style="margin:0 8px 15px">${S.level}</p>${entries.map(item => `<button class="collection-button ${route.id === item.id || route.unitId === item.id ? 'selected' : ''}" type="button" data-route='${esc(JSON.stringify({ kind: tab === 'lessons' ? 'lesson' : 'unit', id: item.id }))}'><small>${t(tab === 'lessons' ? 'lesson' : 'unit')} ${item.reference_lesson_number || item.reference_unit_number}</small>${esc(text(item.title))}</button>`).join('')}`;
  }
  function toolbarHTML() {
    if (!S.level) return '<span class="toolbar-title">ProjectBeta</span>';
    const detail = ['lesson', 'unit', 'character', 'alphabet', 'search'].includes(route.kind);
    let value = `${detail ? `<button type="button" class="icon-button" data-back aria-label="${t('close')}">${icon('back')}</button>` : ''}<span class="toolbar-title">${route.kind === 'lesson' ? `${lesson().source_level_label} · ${t('lesson')} ${lesson().reference_lesson_number}` : t(tab)}</span><span class="toolbar-spacer"></span>`;
    if (['lessons', 'kanji'].includes(route.kind)) value += `<select class="toolbar-select" data-level aria-label="${t('level')}"><option ${S.level === 'N5' ? 'selected' : ''}>N5</option><option ${S.level === 'N4' ? 'selected' : ''}>N4</option></select>`;
    if (route.kind === 'lesson') value += `<select class="toolbar-select" data-jump aria-label="${t('jump')}"><option value="topic">${t('jump')}</option><option value="vocabulary">${t('vocabulary')}</option><option value="grammar">${t('grammar')}</option><option value="patterns">${t('patterns')}</option><option value="dialogues">${t('dialogues')}</option></select><button type="button" class="icon-button ${S.furigana ? 'selected' : ''}" data-ruby aria-label="Furigana">ふ</button>`;
    if (route.kind !== 'search') value += `<button type="button" class="icon-button" data-search aria-label="${t('search')}">${icon('search')}</button>`;
    value += `<button type="button" class="stop-button" data-stop style="display:${audio ? 'inline-flex' : 'none'}">${icon('stop')}${t('stop')}</button>`;
    return value;
  }
  function choiceHTML() { return `<div class="choice"><p class="meta">ProjectBeta</p><h1>${t('choose')}</h1><p class="guidance">${t('free')}</p>${['N5', 'N4'].map(level => `<button class="level-choice" type="button" data-choose="${level}"><span><strong>${level}</strong><small>${t('lesson')} ${level === 'N5' ? '1–25' : '26–50'}</small></span><span class="chevron">›</span></button>`).join('')}</div>`; }
  function lessonsHTML() { return `<p class="meta level-label">${S.level}</p><h1>${t('lessons')}</h1>${row(t('alphabet'), '', { kind: 'alphabet' })}${D.lessons.filter(l => l.source_level_label === S.level).map(l => row(text(l.title), `${l.source_level_label} · ${t('lesson')} ${l.reference_lesson_number}`, { kind: 'lesson', id: l.id }, `lesson:${l.id}`, l.reference_lesson_number <= S.learned[l.source_level_label])).join('')}`; }
  function lessonHTML(l) {
    const isLearned = l.reference_lesson_number <= S.learned[l.source_level_label];
    const vocabulary = l.vocabulary.map(v => `<div id="item-${v.id}" ${favoriteAttrs(`vocabulary:${v.id}`)}>${v.forms.map(form => {
      const bound = form.kana_reading.includes('〜') || plain(form.japanese).includes('〜');
      return contentRow(form.japanese, v.meanings.find(m => m.form_keys.includes(form.key))?.text || v.meanings[0].text,
        `word:${v.id}:${form.key}`, form.kana_reading, null, bound ? 'context' : '');
    }).join('')}${text(v.usage) ? `<p class="guidance">${esc(text(v.usage))}</p>` : ''}</div>`).join('');
    const grammar = l.grammar_points.map(g => `<div id="item-${g.id}" ${favoriteAttrs(`grammar:${g.id}`)}><h3>${esc(text(g.title))}</h3><p class="body-copy" dir="auto">${esc(text(g.explanation))}</p>${text(g.notes) ? `<p class="guidance">${esc(text(g.notes))}</p>` : ''}</div>`).join('');
    const patterns = l.sentence_patterns.map(p => {
      const formula = p.templates[0].pieces.map(piece => piece.kind === 'slot' ? `[${text(p.slots.find(slot => slot.key === piece.value)?.label)}]` : piece.value).join('');
      const examples = l.examples.filter(e => e.pattern_id === p.id).slice(0, 3);
      return `<div id="item-${p.id}" ${favoriteAttrs(`patterns:${p.id}`)}><p class="formula" dir="auto">${esc(formula)}</p>${examples.map(e => `<div id="item-${e.id}">${contentRow(e.japanese, e.translation, `example:${e.id}`, plain(e.japanese))}</div>`).join('')}</div>`;
    }).join('');
    const dialogues = l.dialogues.map(d => `<div ${favoriteAttrs(`dialogues:${d.id}`)} id="item-${d.id}"><div class="section-heading"><h3>${esc(text(d.title))}</h3>${audioButton(`dialogue:${d.id}`, text(d.title))}</div><p class="guidance">${esc(text(d.scenario))}</p>${d.turns.map((turn, index) => `<div class="turn" data-turn="${d.id}:${index}"><div class="turn-name" lang="ja">${jp(d.characters.find(c => c.key === turn.speaker_key).display_name)}<span class="playing-marker" hidden>●</span></div>${contentRow(turn.japanese, turn.translation, `turn:${d.id}:${index}`, plain(turn.japanese))}</div>`).join('')}</div>`).join('');
    return `<header class="topic" id="topic" ${favoriteAttrs(`lesson:${l.id}`)}><p class="meta level-label">${l.source_level_label} · ${t('lesson')} ${l.reference_lesson_number}</p><h1 dir="auto">${esc(text(l.title))}</h1><button type="button" class="learned-button" data-learned="${l.id}">${icon('check')}${isLearned ? t('unmark') : t('mark')}</button></header><section class="section" id="vocabulary"><h2>${t('vocabulary')}</h2>${vocabulary}</section><section class="section" id="grammar"><h2>${t('grammar')}</h2>${grammar}</section><section class="section" id="patterns"><h2>${t('patterns')}</h2>${patterns}</section><section class="section" id="dialogues"><h2>${t('dialogues')}</h2>${dialogues}</section>`;
  }
  function unitsHTML() { return `<p class="meta level-label">${S.level}</p><h1>${t('kanji')}</h1>${D.units.filter(u => u.source_level_label === S.level).map(u => row(text(u.title), `${u.source_level_label} · ${t('unit')} ${u.reference_unit_number}`, { kind: 'unit', id: u.id }, `unit:${u.id}`)).join('')}`; }
  function unitHTML(u) { return `<header ${favoriteAttrs(`unit:${u.id}`)}><p class="meta level-label">${u.source_level_label} · ${t('unit')} ${u.reference_unit_number}</p><h1>${esc(text(u.title))}</h1></header><div class="glyph-grid">${u.characters.map(k => `<button type="button" class="glyph-cell" lang="ja" data-route='${esc(JSON.stringify({ kind: 'character', id: k.id, unitId: u.id }))}'>${esc(k.character)}</button>`).join('')}</div>`; }
  function characterHTML(u, k) {
    const sentences = D.characterSentences[k.id] || [];
    return `<header ${favoriteAttrs(`kanji:${k.id}`)}><p class="meta level-label">${u.source_level_label} · ${t('unit')} ${u.reference_unit_number}</p><div class="kanji-hero" lang="ja">${esc(k.character)}</div>${meaning(k.meanings)}</header><section class="section">${language() === 'vi' ? `<p class="reading-line"><span>Hán-Việt</span>${esc(k.han_viet.join(', '))}</p>` : ''}<p class="reading-line"><span>On</span><bdi lang="ja">${esc(k.on_readings.join('・') || '—')}</bdi></p><p class="reading-line"><span>Kun</span><bdi lang="ja">${esc(k.kun_readings.join('・') || '—')}</bdi></p></section><section class="section"><h2>${t('vocabulary')}</h2>${k.examples.map(e => contentRow(e.japanese, e.meanings, `kanji-word:${e.id}`, e.kana_reading)).join('')}</section><section class="section"><h2>${t('examples')}</h2>${sentences.slice(0, 3).map(e => contentRow(e.japanese, e.translation, `example:${e.id}`, plain(e.japanese))).join('')}</section>`;
  }
  function favoritesHTML() {
    let rows = S.favorites.map(f => ({ saved: f, target: info(f.key) || { key: f.key, type: 'unavailable', level: '', levels: [], label: { vi: 'Nội dung không còn khả dụng', en: 'Content unavailable' } } }));
    if (favoriteType !== 'all') rows = rows.filter(f => f.target.type === favoriteType);
    if (favoriteLevel !== 'all') rows = rows.filter(f => (f.target.levels || [f.target.level]).includes(favoriteLevel));
    rows.sort((a, b) => b.saved.savedAt - a.saved.savedAt || a.saved.key.localeCompare(b.saved.key));
    return `<h1>${t('favorites')}</h1><div class="filters"><select id="favorite-type"><option value="all">${t('all')}</option>${['vocabulary', 'grammar', 'patterns', 'dialogues', 'kanji', 'lesson', 'unit'].map(type => `<option value="${type}" ${favoriteType === type ? 'selected' : ''}>${t(type)}</option>`).join('')}</select><select id="favorite-level"><option value="all">N5 + N4</option>${['N5', 'N4'].map(level => `<option ${favoriteLevel === level ? 'selected' : ''}>${level}</option>`).join('')}</select></div>${rows.length ? rows.map(({ target }) => target.type === 'unavailable' ? `<div class="list-row" ${favoriteAttrs(target.key)}><span class="row-title">${esc(text(target.label))}</span></div>` : row(text(target.label), `${target.levels.join('/')} · ${t(target.type)}`, targetRoute(target), target.key)).join('') : `<div class="empty"><h2>${t(S.favorites.length ? 'noFiltered' : 'noFavorites')}</h2><p>${t('favoriteHelp')}</p></div>`}`;
  }
  function settingsHTML() {
    const languageOptions = [['system', t('system')], ...D.languages.map(code => [code, new Intl.DisplayNames(['en'], { type: 'language' }).of(code)])];
    return `<h1>${t('settings')}</h1><div class="settings-section"><label class="setting-row"><span>${t('language')}</span><select data-pref="language">${languageOptions.map(([code, name]) => `<option value="${code}" ${S.language === code ? 'selected' : ''}>${esc(name)}</option>`).join('')}</select></label><label class="setting-row"><span>${t('appearance')}</span><select data-pref="appearance">${['system', 'light', 'dark'].map(value => `<option value="${value}" ${S.appearance === value ? 'selected' : ''}>${t(value)}</option>`).join('')}</select></label><label class="setting-row"><span>Furigana</span><input type="checkbox" data-pref="furigana" ${S.furigana ? 'checked' : ''}></label><label class="setting-row"><span>${t('level')}</span><select data-pref="level"><option ${S.level === 'N5' ? 'selected' : ''}>N5</option><option ${S.level === 'N4' ? 'selected' : ''}>N4</option></select></label></div>`;
  }
  function alphabetHTML() {
    const cells = D.kana.filter(c => c.script === kanaScript && c.group === kanaGroup);
    if (!selectedKana || !cells.some(c => c.id === selectedKana)) selectedKana = cells[0]?.id || null;
    const selected = cells.find(c => c.id === selectedKana);
    const bound = selected?.word && selected.word.reading.includes('〜');
    return `<h1>${t('alphabet')}</h1><div class="filters"><select id="kana-script"><option value="hiragana" ${kanaScript === 'hiragana' ? 'selected' : ''}>Hiragana</option><option value="katakana" ${kanaScript === 'katakana' ? 'selected' : ''}>Katakana</option></select></div><div class="kana-groups">${['basic', 'voiced', 'combined', 'special', 'reference'].map(group => `<button type="button" class="${kanaGroup === group ? 'selected' : ''}" data-kana-group="${group}">${t(group)}</button>`).join('')}</div><div class="glyph-grid">${cells.map(c => `<button class="glyph-cell ${c.id === selectedKana ? 'selected' : ''}" type="button" lang="ja" data-kana="${c.id}">${esc(c.glyph)}</button>`).join('')}</div>${selected ? `<section class="kana-detail"><div class="kanji-hero" lang="ja">${esc(selected.glyph)}</div>${selected.word ? contentRow(selected.word.japanese, selected.word.meanings, `kana-word:${selected.id}`, selected.word.reading, null, bound ? 'context' : '') : ''}${selected.sentence ? contentRow(selected.sentence.japanese, selected.sentence.translation, `kana-sentence:${selected.id}`, plain(selected.sentence.japanese)) : ''}</section>` : `<div class="jp">${kanaScript === 'hiragana' ? 'ゐ　ゑ' : 'ヰ　ヱ'}</div>`}`;
  }
  function searchHTML() { return `<h1>${t('search')}</h1><p class="meta">${t(searchScope ? 'within' : 'global')}</p><label class="search-box">${icon('search')}<input id="query" type="search" value="${esc(searchQuery)}" placeholder="${t('search')}" autocomplete="off"></label><p class="search-status" id="search-status">${searchQuery ? '' : t('queryHelp')}</p><div id="search-results">${searchResultsHTML()}</div>`; }
  function searchResultsHTML() {
    if (!searchQuery.trim()) return '';
    if (!searchHits.length) return `<div class="empty"><h2>${t('noResults')}</h2></div>`;
    return ['vocabulary', 'grammar', 'patterns', 'dialogues', 'kanji'].map(type => {
      const group = searchHits.filter(e => e.type === type);
      return group.length ? `<section class="search-group"><h2>${t(type)}</h2>${group.map(e => `<button type="button" class="list-row" data-result="${esc(e.key)}"><span class="row-body"><span class="meta">${e.level}</span><span class="row-title" dir="auto">${esc(text(e.label))}</span></span><span class="chevron">›</span></button>`).join('')}</section>` : '';
    }).join('');
  }
  function cancelSearch() { searchRevision++; if (searchTimer !== null) clearTimeout(searchTimer); searchTimer = null; }
  function runSearch() {
    cancelSearch(); const token = searchRevision, query = searchQuery;
    if (!query.trim()) { searchHits = []; document.getElementById('search-status').textContent = t('queryHelp'); document.getElementById('search-results').innerHTML = ''; return; }
    document.getElementById('search-status').textContent = t('waiting'); document.getElementById('search-results').innerHTML = '';
    searchTimer = setTimeout(() => {
      if (token !== searchRevision || route.kind !== 'search') return;
      searchHits = D.targets.filter(e => ['vocabulary', 'grammar', 'patterns', 'dialogues', 'kanji'].includes(e.type) && (!searchScope || e.lessonId === searchScope || e.lessonIds?.includes(searchScope))).map(e => ({ ...e, rank: L.matchRank([...(e.fields || []), text(e.searchText), text(e.label)], query) })).filter(e => Number.isFinite(e.rank)).sort((a, b) => a.rank - b.rank || a.order - b.order || a.key.localeCompare(b.key));
      document.getElementById('search-status').textContent = `${searchHits.length} ${language() === 'vi' ? 'kết quả trong dữ liệu mẫu' : 'results in sample data'}`;
      document.getElementById('search-results').innerHTML = searchResultsHTML(); searchTimer = null;
    }, 500);
  }
  function render() {
    appearance();
    document.getElementById('confirm-cancel').textContent = t('cancel'); document.getElementById('confirm-apply').textContent = t('confirm');
    shell.classList.toggle('no-level', !S.level);
    document.getElementById('app-navigation').innerHTML = `<div class="brand">ProjectBeta</div>${navHTML()}`;
    document.getElementById('app-tabs').innerHTML = navHTML();
    const collection = collectionHTML(); shell.classList.toggle('no-collection', !collection); document.getElementById('app-collection').innerHTML = collection;
    document.getElementById('app-toolbar').innerHTML = toolbarHTML();
    if (!S.level) main.innerHTML = choiceHTML();
    else if (route.kind === 'lessons') main.innerHTML = lessonsHTML();
    else if (route.kind === 'lesson') main.innerHTML = lessonHTML(lesson());
    else if (route.kind === 'kanji') main.innerHTML = unitsHTML();
    else if (route.kind === 'unit') main.innerHTML = unitHTML(unit());
    else if (route.kind === 'character') main.innerHTML = characterHTML(unit(), unit().characters.find(k => k.id === route.id));
    else if (route.kind === 'favorites') main.innerHTML = favoritesHTML();
    else if (route.kind === 'settings') main.innerHTML = settingsHTML();
    else if (route.kind === 'alphabet') main.innerHTML = alphabetHTML();
    else if (route.kind === 'search') main.innerHTML = searchHTML();
    updateAudioDOM();
  }
  function updateAudioDOM() {
    shell.querySelectorAll('[data-audio]').forEach(button => {
      const target = button.dataset.audio, playing = audio && (audio.target === target || (audio.dialogueId && target === `turn:${audio.dialogueId}:${audio.turn}`));
      button.classList.toggle('playing', Boolean(playing)); button.innerHTML = icon(playing ? 'waves' : 'speaker');
      button.setAttribute('aria-label', `${button.dataset.audioLabel}${playing ? (language() === 'vi' ? ' · đọc lại từ đầu' : ' · restart from beginning') : ''}`);
    });
    shell.querySelectorAll('[data-turn]').forEach(turn => { const playing = Boolean(audio?.dialogueId && turn.dataset.turn === `${audio.dialogueId}:${audio.turn}`); turn.classList.toggle('playing', playing); const marker = turn.querySelector('.playing-marker'); if (marker) marker.hidden = !playing; });
    shell.querySelectorAll('[data-stop]').forEach(button => { button.style.display = audio ? 'inline-flex' : 'none'; });
  }
  function stopAudio(announce = true) { audioRevision++; if (audioTimer !== null) clearTimeout(audioTimer); audioTimer = null; audio = null; updateAudioDOM(); if (announce) feedback(t('stop')); }
  function play(target) {
    stopAudio(false); const token = audioRevision;
    const pieces = target.split(':');
    audio = { target, dialogueId: ['dialogue', 'turn'].includes(pieces[0]) ? pieces[1] : null, turn: pieces[0] === 'turn' ? Number(pieces[2]) : 0 };
    const d = audio.dialogueId ? D.lessons.flatMap(l => l.dialogues).find(item => item.id === audio.dialogueId) : null;
    function next() {
      if (token !== audioRevision || !audio) return;
      updateAudioDOM();
      audioTimer = setTimeout(() => {
        if (token !== audioRevision || !audio) return;
        if (pieces[0] === 'dialogue' && audio.turn + 1 < d.turns.length) { audio.turn++; next(); } else stopAudio(false);
      }, 2200);
    }
    next(); feedback(language() === 'vi' ? 'Mô phỏng đọc từ đầu · không âm thanh.' : 'Playback state simulation · no sound.');
  }
  function showContext(key) {
    const target = info(key) || (S.favorites.some(f => f.key === key) ? { label: { vi: 'Nội dung không còn khả dụng', en: 'Content unavailable' } } : null); if (!target) return;
    menuTarget = key; document.getElementById('context-label').textContent = text(target.label);
    document.getElementById('context-action').textContent = S.favorites.some(f => f.key === key) ? t('remove') : t('add');
    document.getElementById('context-close').textContent = t('close'); if (!contextDialog.open) contextDialog.showModal();
  }
  function setFavorite(key, desired) { commit(next => { next.favorites = next.favorites.filter(f => f.key !== key); if (desired) next.favorites.push({ key, savedAt: Date.now() }); }, desired ? t('add') : t('remove'), () => setFavorite(key, desired)); }
  function cancelHold() { if (holdTimer !== null) clearTimeout(holdTimer); holdTimer = null; holdOrigin = null; }
  shell.addEventListener('click', event => {
    if (contextDialog.open || confirmDialog.open) { event.preventDefault(); return; }
    const button = event.target.closest('button'); if (!button) return;
    if (button.dataset.nav) { cancelSearch(); navigate(rootRoute(button.dataset.nav), button.dataset.nav); }
    else if (button.dataset.route) navigate(JSON.parse(button.dataset.route));
    else if (button.hasAttribute('data-back')) back();
    else if (button.dataset.choose) commit(next => { next.level = button.dataset.choose; }, t('saved'));
    else if (button.dataset.audio) play(button.dataset.audio);
    else if (button.hasAttribute('data-stop')) stopAudio();
    else if (button.hasAttribute('data-ruby')) commit(next => { next.furigana = !S.furigana; });
    else if (button.dataset.learned) { const l = D.lessons.find(item => item.id === button.dataset.learned); setLearned(l, l.reference_lesson_number > S.learned[l.source_level_label]); }
    else if (button.hasAttribute('data-search')) { searchOrigin = { ...route }; searchScope = route.kind === 'lesson' ? route.id : null; searchQuery = ''; searchHits = []; cancelSearch(); navigate({ kind: 'search' }); document.getElementById('query')?.focus(); }
    else if (button.dataset.result) { const target = info(button.dataset.result); navigate({ ...targetRoute(target), fromSearch: true }); if (target.anchor) requestAnimationFrame(() => document.getElementById(target.anchor)?.scrollIntoView({ block: 'center', behavior: 'auto' })); }
    else if (button.dataset.kanaGroup) { kanaGroup = button.dataset.kanaGroup; selectedKana = null; render(); }
    else if (button.dataset.kana) { selectedKana = button.dataset.kana; render(); play(`kana:${selectedKana}`); }
  });
  shell.addEventListener('change', event => {
    const element = event.target;
    if (element.hasAttribute('data-level')) { const level = element.value; if (commit(next => { next.level = level; })) navigate(rootRoute(tab)); }
    else if (element.dataset.pref) { const key = element.dataset.pref, value = element.type === 'checkbox' ? element.checked : element.value; commit(next => { next[key] = value; }); }
    else if (element.hasAttribute('data-jump')) document.getElementById(element.value)?.scrollIntoView({ block: 'start', behavior: 'auto' });
    else if (element.id === 'favorite-type') { favoriteType = element.value; render(); }
    else if (element.id === 'favorite-level') { favoriteLevel = element.value; render(); }
    else if (element.id === 'kana-script') { kanaScript = element.value; selectedKana = null; render(); }
  });
  shell.addEventListener('input', event => { if (event.target.id === 'query' && !event.isComposing) { searchQuery = event.target.value; runSearch(); } });
  shell.addEventListener('compositionstart', event => { if (event.target.id === 'query') { cancelSearch(); document.getElementById('search-status').textContent = t('waiting'); document.getElementById('search-results').innerHTML = ''; } });
  shell.addEventListener('compositionend', event => { if (event.target.id === 'query') { searchQuery = event.target.value; runSearch(); } });
  shell.addEventListener('contextmenu', event => { if (event.target.closest('[data-audio],input,select')) return; const target = event.target.closest('[data-favorite]'); if (!target) return; event.preventDefault(); cancelHold(); showContext(target.dataset.favorite); });
  shell.addEventListener('pointerdown', event => { cancelHold(); if (event.button !== 0 || event.target.closest('[data-audio],input,select,[data-learned]')) return; const target = event.target.closest('[data-favorite]'); if (!target) return; holdOrigin = { x: event.clientX, y: event.clientY }; holdTimer = setTimeout(() => { holdTimer = null; showContext(target.dataset.favorite); }, 550); });
  document.addEventListener('pointermove', event => { if (holdOrigin && Math.hypot(event.clientX - holdOrigin.x, event.clientY - holdOrigin.y) > 10) cancelHold(); });
  document.addEventListener('pointerup', cancelHold); document.addEventListener('pointercancel', cancelHold); window.addEventListener('scroll', cancelHold, { passive: true });
  shell.addEventListener('keydown', event => { if (event.key === 'ContextMenu' || (event.shiftKey && event.key === 'F10')) { const target = event.target.closest('[data-favorite]'); if (target) { event.preventDefault(); showContext(target.dataset.favorite); } } });
  document.getElementById('context-action').addEventListener('click', () => { const key = menuTarget; contextDialog.close(); setFavorite(key, !S.favorites.some(f => f.key === key)); });
  document.getElementById('context-close').addEventListener('click', () => contextDialog.close());
  document.getElementById('confirm-cancel').addEventListener('click', () => { pendingConfirm = null; confirmDialog.close(); });
  document.getElementById('confirm-apply').addEventListener('click', () => { const apply = pendingConfirm; pendingConfirm = null; confirmDialog.close(); apply?.(); });
  confirmDialog.addEventListener('cancel', () => { pendingConfirm = null; });
  document.getElementById('retry').addEventListener('click', () => pendingRetry?.());
  document.getElementById('review-size').addEventListener('change', event => { shell.dataset.size = event.target.value; });
  document.getElementById('review-scale').addEventListener('change', event => { document.documentElement.style.setProperty('--scale', event.target.value); });
  document.getElementById('review-first').addEventListener('click', () => { stopAudio(false); cancelSearch(); S.level = null; route = { kind: 'lessons' }; tab = 'lessons'; try { localStorage.setItem(storageKey, JSON.stringify(persisted())); } catch { /* browser review only */ } render(); });
  document.getElementById('review-learned').addEventListener('click', () => { S.learned = { N5: 6, N4: 30 }; try { localStorage.setItem(storageKey, JSON.stringify(persisted())); } catch { /* browser review only */ } render(); feedback('Mẫu dữ liệu đã học: N5 đến bài 6; N4 đến bài 30. Không thay đổi dữ liệu app.'); });
  media.addEventListener('change', appearance);
  document.addEventListener('visibilitychange', () => { if (document.hidden) { stopAudio(false); cancelHold(); } });
  window.addEventListener('pagehide', () => { stopAudio(false); cancelSearch(); cancelHold(); });
  render();
})();
