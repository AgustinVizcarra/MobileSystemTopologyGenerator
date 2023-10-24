#!/bin/bash
# Verificamos que el script se esté ejecutando con permisos de root
if [ "$(id -u)" != "0" ]; then
    echo "Este script debe ejecutarse con privilegios de root."
    exit 1
fi
# Obtenemos la lista de puertos utilizados por iptables
PUERTOS_UTILIZADOS=$(sudo iptables -t nat -L PREROUTING | grep -E 'dpt' | awk '{print$7}' | tr -d "dpt: ")
maximo=$(echo "${PUERTOS_UTILIZADOS[@]}" | sort -n | tail -1)
PUERTO_DISPONIBLE=$(($maximo + 1))
# Imprimimos el puerto disponible
echo "$PUERTO_DISPONIBLE"