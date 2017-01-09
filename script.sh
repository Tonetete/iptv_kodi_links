#!/bin/bash
if ! hash python3; then
    echo "Necesitas tener instalado python en su versión 3.0 o superior"
    exit 1
fi
echo "***IPTV KODI LINKS***"
echo "Script para crear archivos .strm de series y películas de una lista m3u"
printf '=%.0s' {1..71}
echo ""
echo "Introduce el nombre de la serie para crear los archivos .strm (vacío para obtener todos los archivos .strm de todas las series y películas)"
read value

foundFile=false
file=""
for file in *.m3u
do
    for ((i = 0; i < 1; i++))
    do
      foundFile=true
      file=${file}
    done
done

if $foundFile; then
  echo "Archivo m3u encontrado: $file"
  echo "Ejecutando script, por favor espera..."
  if [ "$value" == "" ]; then
    python3 iptv_kodi_links.py --file="$file" --all
  else
    python3 iptv_kodi_links.py --file="$file" --name="$value"
  fi
  echo "Archivos creados!"

else
  echo "Archivo m3u no encontrado."
  exit 1
fi

# Equality Comparison
