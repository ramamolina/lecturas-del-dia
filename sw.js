// Guarda la app en el celular para que funcione sin conexión.
// Cambiar VERSION cada vez que se actualizan las lecturas o la página.
const VERSION = 'lecturas-v18';
const ARCHIVOS = ['./', './index.html', './lecturas.json', './meditaciones.json', './manifest.json', './icono-mosaico-192.png', './icono-mosaico-512.png', './apple-touch-icon-mosaico.png'];
const ESPERA_RED = 3000; // ms: si la red no responde en este tiempo, se usa lo guardado

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

// Primero intenta la red (para traer novedades). Si no hay conexión, o si la red tarda
// más de ESPERA_RED (señal débil), usa lo guardado; la descarga sigue y actualiza para la próxima vez.
self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET' || new URL(e.request.url).origin !== location.origin) return;
  const red = fetch(e.request).then((r) => {
    if (r.ok) {
      const copia = r.clone();
      caches.open(VERSION).then((c) => c.put(e.request, copia));
    }
    return r;
  });
  e.waitUntil(red.catch(() => {}));
  e.respondWith(new Promise((resolver) => {
    let listo = false;
    const usarGuardado = () => caches.match(e.request, { ignoreSearch: true }).then((g) => {
      if (g && !listo) { listo = true; resolver(g); }
      return g;
    });
    const reloj = setTimeout(usarGuardado, ESPERA_RED);
    red.then((r) => { clearTimeout(reloj); if (!listo) { listo = true; resolver(r); } })
       .catch(() => { clearTimeout(reloj); usarGuardado().then((g) => { if (!listo) { listo = true; resolver(g || Response.error()); } }); });
  }));
});
