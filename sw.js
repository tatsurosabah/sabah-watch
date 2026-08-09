/* Sabah Watch service worker
   アプリ更新時は CACHE の版番号を必ず上げること（古いキャッシュを確実に破棄するため） */
const CACHE = 'sabah-watch-v1';
const SHELL = ['./', './index.html', './manifest.json', './icon-180.png', './icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;

  // news.json はネットワーク優先（最新を見せたい）／失敗時は前回分を返す
  if (url.pathname.endsWith('news.json')) {
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put('news.json', copy));
        return res;
      }).catch(() => caches.match('news.json'))
    );
    return;
  }

  // それ以外（アプリ本体）はキャッシュ優先＝オフラインでも開ける
  e.respondWith(
    caches.match(req).then(hit => hit || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(req, copy));
      return res;
    }))
  );
});
