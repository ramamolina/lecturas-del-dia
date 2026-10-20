# Herramientas para actualizar las lecturas

Se usan una vez por año, cuando sale el Calendario litúrgico nuevo de la CEA.

1. `bajar_biblia.py` + `armar_biblia.py`: bajan El Libro del Pueblo de Dios de vatican.va y lo pasan a datos (una sola vez).
2. `leer_calendario.py`: lee el texto del PDF del calendario (`pdftotext -layout`).
3. `resolver_lecturas.py`: cruza cada cita del calendario con el texto bíblico.
4. `datos_app.py`: arma `lecturas.json`, que es lo que usa la app (se le pueden pasar varios años).
5. `mensaje.py`: muestra cómo queda el mensaje de una fecha.

Después de actualizar `lecturas.json`, cambiar `VERSION` en `sw.js` para que los celulares bajen la versión nueva.
