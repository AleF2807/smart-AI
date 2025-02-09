self.addEventListener('install', (event) => {
    console.log('Service Worker installato!');
    event.waitUntil(
      caches.open('smartlife-cache').then((cache) => {
        return cache.addAll([
          './index.html',
          './AI.html',
          './home.html',
          './static/style_home.css',
          './icon-192x192.png',
          './icon-512x512.png'
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', (event) => {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  });
  