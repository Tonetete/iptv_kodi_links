# iptv_kodi_links


Proyecto creado para extraer los enlaces de una lista m3u para series y películas y convertirlos en archivos `.strm`

En el caso de las series, se crearán carpetas con el nombre de las mismas y se guardarán los enlaces con el formato SXXEXX, 01x01, SEXXEPXX, etc...

El script acepta los siguientes parámetros: `--all`, `--file` y `--name`

Como usarlo:

- Si queremos obtener todas las series y películas, ejecutaremos el script mediante el comando `python iptv_kodi_links.py file="<nombre_archivo_m3u>" --all`

- Si queremos obtener los enlaces de una serie en concreto, ejecutaremos el script mediante el comando `python iptv_kodi_links.py file="<nombre_archivo_m3u>" --name="<nombre_serie>"`

En todos los casos el archivo `.m3u` debe estar ubicado en la misma carpeta que el script para poder ejecutarlo.

Para su correcto funcionamiento es necesario tener instalado Python 3 o superior en tu ordenador.
Puedes encontrarlo en este enlace: https://www.python.org/downloads/
