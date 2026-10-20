// Guarda la app en el celular para que funcione sin conexión.
// Cambiar VERSION cada vez que se actualizan las lecturas o la página.
const VERSION = 'lecturas-v4';
const ARCHIVOS = ['./', './index.html', './lecturas.json', './manifest.json', './icono-mosaico-192.png', './icono-mosaico-512.png', './apple-touch-icon-mosaico.png'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(VERSION).then((c) => c.addAll(ARCHIVOS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((claves) => Promise.all(claves.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Primero intenta la red (para traer novedades); si no hay conexión, usa lo guardado.
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then((r) => {
        const copia = r.clone();
        caches.open(VERSION).then((c) => c.put(e.request, copia));
        return r;
      })
      .catch(() => caches.match(e.request, { ignoreSearch: true }))
  );
});
