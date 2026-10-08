// Service Worker for TrailGemma & FloraCast
const CACHE_NAME = 'trailgemma-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/css/style.css',
  '/js/app.js',
  '/js/tabpfn_ui.js',
  '/js/audio_guide.js',
  '/assets/fall_trail.jpg',
  '/assets/garden_planner.jpg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Pre-caching offline trail assets');
      return cache.addAll(ASSETS_TO_CACHE).catch(err => console.log('Cache add warning:', err));
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keyList) => {
      return Promise.all(keyList.map((key) => {
        if (key !== CACHE_NAME) {
          return caches.delete(key);
        }
      }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Offline-first strategy for static assets
  if (event.request.method === 'GET') {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request).then((networkResponse) => {
          return networkResponse;
        }).catch(() => {
          // If offline and requesting page, return cached index
          if (event.request.destination === 'document') {
            return caches.match('/index.html');
          }
        });
      })
    );
  }
});
