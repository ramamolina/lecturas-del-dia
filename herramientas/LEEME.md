# Herramientas para actualizar las lecturas

Se usan una vez por año, cuando sale el Calendario litúrgico nuevo de la CEA.

1. `bajar_biblia.py` + `armar_biblia.py`: bajan El Libro del Pueblo de Dios de vatican.va y lo pasan a datos (una sola vez).
2. `leer_calendario.py`: lee el texto del PDF del calendario (`pdftotext -layout`).
3. `resolver_lecturas.py`: cruza cada cita del calendario con el texto bíblico.
4. `datos_app.py`: arma `lecturas.json`, que es lo que usa la app (se le pueden pasar varios años).
5. `mensaje.py`: muestra cómo queda el mensaje de una fecha.

Después de actualizar `lecturas.json`, cambiar `VERSION` en `sw.js` para que los celulares bajen la versión nueva.

## Calendario 2027 (cargado el 01/11/2026)
- PDF: https://curas.com.ar/Calendario/Calendario_lit%C3%BArgico_2027_para_la_Argentina.pdf (67 páginas).
- El formato cambió un poco respecto de 2026 (color después de un guion: "Feria - Verde"; misa de la vigilia como "Misa vespertina:" con sus lecturas; Pascua con "Desde la mañana:"). Los scripts ya contemplan los dos formatos.
- Erratas del PDF corregidas a mano en el texto antes de leerlo (`pdftotext -layout` y después estos cambios):
  - Cánticos marcados como salmo: "S.R. Isaías 12" y "S.R. Tobías 13" → "C.R." (10/1, 4/6, 5/6, 12/12).
  - Falta el número hebreo del salmo: "S.R. 97, 1.7-9" → "S.R. 97 (98)" (4/1); "S.R. 18, " → "S.R. 18 (19), " (16/1, 30/9).
  - Falta los dos puntos: "Lecturas Éxodo 32" → "Lecturas: Éxodo 32" (11/3).
- Para armar los datos: `datos_app.py lecturas2026.json lecturas2027.json ../lecturas.json`.

## Meditaciones (Adviento y Navidad)

- Textos en `meditaciones/en/` (originales de dominio público, de Standard Ebooks) y `meditaciones/es/` (traducción libre de Claude).
- Después de cambiar alguno, correr `python3 herramientas/armar_meditaciones.py` para regenerar `meditaciones.json`, y subir la versión de `sw.js`.
- Fechas fijas: *A Christmas Carol* (Dickens) del 1 al 24 de diciembre; *The Everlasting Man*, cap. «The God in the Cave» (Chesterton), del 25/12 al 8/1. Se repiten todos los años.
- Homilías de San Josemaría (*Es Cristo que pasa*): solo links a escriva.org, según la celebración del día (tabla `HOMILIAS` en `index.html`).

## Meditaciones de Cuaresma y Semana Santa (Newman)

- Fuente: *Meditations and Devotions* (1893), texto OCR de Internet Archive (`MeditationsAndDevotionsOf`), limpiado con los scripts de `herramientas/newman/` (`sacar.py` → `limpiar.py` → `pulir.py` → `spec.py`, que arma cada trozo y corrige errores de OCR).
- Se ubican por días respecto de la Pascua (se calcula sola cada año): Ceniza a sábado, «Hope in God — Creator»; 14 días de Vía Crucis; 7 días de Vía Crucis breve (dos estaciones por día); 14 días de «Hope in God — Redeemer»; Domingo de Ramos a Viernes Santo, las meditaciones para el Viernes Santo (de a dos); Sábado Santo, «It is Consummated».
- De las doce meditaciones para el Viernes Santo se dejaron afuera la 2 (sobre el pueblo judío) y la 3 (oración por Inglaterra).

## Meditaciones: mayo, tiempo pascual y tiempo ordinario (Newman)

- Mayo (fechas `05-01`…`05-31`): *Meditations and Devotions*, Parte I, un título de la Letanía lauretana por día (`nw-may-NN`).
- Parte III, «Meditations on Christian Doctrine» (`nw-dNN`, en el orden del libro). Se reparten con **series** (`series` en `meditaciones.json`):
  - Cada serie tiene `tramos` (extremos = número de días respecto de la Pascua, o `'MM-DD'`) y una lista de `textos`.
  - La app asigna los textos en orden, uno por cada día del tramo que no tenga ya una meditación fija (por `pascua` o por `fechas`). Si la lista se termina, ese día queda sin meditación.
  - `pascua`: domingo de Pascua → Pentecostés (Resurrección, Dios con nosotros, los cuarenta días, Ascensión, Paráclito…).
  - `ordinario-enero`: 9 de enero → martes antes de Ceniza (Dios y el alma, el pecado, la Cruz, atributos de Dios, Conclusión).
- Fijas por la Pascua: Corpus Christi (+63, domingo en Argentina, y los dos días siguientes) y Sagrado Corazón (+68).
- `ordinario`: lunes después de Pentecostés → 30 de noviembre. Empieza con *Ortodoxia* de Chesterton (1908, Standard Ebooks), 56 partes `orto-NN` (unos 56 días libres: junio-julio). El título del capítulo se saca del texto porque ya va en el título de la meditación.
- Para agregar otra obra al final de una serie: textos en `meditaciones/en` y `meditaciones/es`, y sumarla a la lista de la serie en `armar_meditaciones.py`.
- Pendiente: fines de enero → Ceniza, y agosto → noviembre (candidatos: resto de *El hombre eterno*, *San Francisco de Asís* de Chesterton).
