/* Review-only helpers. Native implementation follows the domain contracts. */
(function (root) {
  function normalize(value) {
    const widthFolded = String(value).normalize('NFKC').replace(/[Đđ]/g, 'd');
    let base = '', folded = '';
    for (const char of widthFolded.normalize('NFD')) {
      if (/\p{Mark}/u.test(char)) {
        if (!/[A-Za-z]/.test(base)) folded += char;
      } else {
        base = char;
        const code = char.codePointAt(0);
        folded += code >= 0x30a1 && code <= 0x30f6 ? String.fromCodePoint(code - 0x60) : char;
      }
    }
    return folded.normalize('NFC').toLowerCase().trim().replace(/\s+/g, ' ');
  }
  function matchRank(fields, query) {
    const q = normalize(query);
    if (!q) return Infinity;
    return Math.min(...fields.map(value => {
      const f = normalize(value);
      return f === q ? 0 : f.startsWith(q) ? 1 : f.includes(q) ? 2 : Infinity;
    }));
  }
  function planPrefix(order, current, target, desiredLearned) {
    const index = order.indexOf(target);
    if (index < 0) throw new Error('Unknown lesson');
    const empty = order[0] - 1;
    const next = desiredLearned ? Math.max(current, target) : current >= target ? (index ? order[index - 1] : empty) : current;
    const changed = order.filter(number => (number <= current) !== (number <= next));
    return { next, changed, desiredLearned };
  }
  const api = { normalize, matchRank, planPrefix };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.ProjectBetaReviewLogic = api;
})(typeof window !== 'undefined' ? window : globalThis);
