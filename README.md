# Generador de topologías móviles 4G y 5G

Este proyecto consiste en una solución que permite el despliegue de redes minimalistas para estudio y análisis de los procedimientos internos de las redes 4G y 5G 
de forma virtualizada. Asimismo este proyecto se apoya en **Openstack** de forma que el sistema permita el despliegue de las redes de forma automatizada por medio de 
APIS gracias a un SDK. Es importante mencionar que para esta solución se tomó como referencia las herramientas de Core abierto **Open5GS**, herramientas de RAN
como **UERANSIM**,  **srsRAN** y herramientas de análisis de paquetes como es el caso de **5G Trace Visualizer** y **Wireshark**

## Comenzando 🚀

Si en caso se quisiera replicar esta solución es importante tener en cuenta todos los requisitos y consideraciones a seguir para el **Deployment**.


### Pre-requisitos 📋

Para empezar se tiene que tener encuenta las siguientes dependecias:

- [Openstack Victoria](https://www.openstack.org/software/victoria/) ![release](https://img.shields.io/badge/version-22.3.0%25-blue)
- [Python](https://www.python.org/downloads/release/python-380/) ![version](https://img.shields.io/badge/version-3.8-blue)
- [Open5GS](https://open5gs.org/open5gs/docs/) ![release](https://img.shields.io/badge/release-2.6.6-blue)
- [UERANSIM](https://github.com/aligungr/UERANSIM) ![release](https://img.shields.io/badge/release-3.2.6-blue)
- [srsRAN](https://www.srslte.com/) ![release](https://img.shields.io/badge/release-23.10-blue)
- [5G Trace Visualizer](https://github.com/telekom/5g-trace-visualizer) ![version](https://img.shields.io/badge/latest-blue)
- [Wireshark](https://www.wireshark.org/docs/relnotes/) ![version](https://img.shields.io/badge/release-4.0.14-blue)
- [Ubuntu](https://releases.ubuntu.com/) ![version](https://img.shields.io/badge/release-20.04LTS-blue)
- [OpenVSwitch](https://docs.openvswitch.org/en/latest/faq/releases/) ![version](https://img.shields.io/badge/release-3.0-blue)

### Instalación 🔧

Para la instalación, primero debemos considerar el despliegue de OpenStack por lo que para eso debemos remitirnos a la siguiente topología utilizada:
<p align="center"><b>Arquitectura de despliegue</b></p>
<p align="center"><img src="https://github.com/AgustinVizcarra/MobileSystemTopologyGenerator/assets/92816809/978c089c-886f-45a2-bbd0-72a828a56a68" width="50%" height="50%" /></p> 

Para seguir con la instalación de esta topología puede apoyarse en la [documentación oficial de Openstack](https://docs.openstack.org/install-guide/) o haciendo consulta al siguiente
a los siguientes pasos en resumido:

- Anadir el repositorio correspondiente a la version usada en el curso ([ref](https://docs.openstack.org/install-guide/environment-packages-ubuntu.html)) e instalar el
cliente openstack de la siguiente forma:
  ```
  # add-apt-repository cloud-archive:victoria
  # apt install python3-openstackclient
  ```
- Base de datos - [MariaDB](https://docs.openstack.org/install-guide/environment-sql-database-ubuntu.html).
- Message Queue - [RabbitMQ](https://docs.openstack.org/install-guide/environment-messaging-ubuntu.html).
- Cache - [Memcached](https://docs.openstack.org/install-guide/environment-memcached-ubuntu.html).
- Key-value Store - [Etcd](https://docs.openstack.org/install-guide/environment-etcd-ubuntu.html).
- Identity - [Keystone](https://docs.openstack.org/keystone/victoria/install/). 
- Image - [Glance](https://docs.openstack.org/glance/victoria/install/).
- Compute - [Nova](https://docs.openstack.org/nova/victoria/install/).
- Networking - [Neutron](https://docs.openstack.org/neutron/victoria/install/), uso de OvS para redes [provider](https://docs.openstack.org/neutron/victoria/admin/deploy-ovs-provider.html#deploy-ovs-provider).
- Dashboard - [Horizon](https://docs.openstack.org/horizon/victoria/install/).

_Teniendo una topología como la siguiente:_

<p align="center"><img src="https://github.com/AgustinVizcarra/MobileSystemTopologyGenerator/assets/92816809/045d25c0-4f79-4c8b-9eef-060d770e8faf" width="50%" height="50%" /></p> 

_Con la topología ya funcional deberá considerar importar las imágenes (de Core y RAN) usando glance y guardarlas en el repositorio para que Openstack pueda acceder a ellas_

```
openstack image create --public \
--disk-format qcow2 --container-format bare \
--file <IMAGE_FILE> --property <IMAGE_METADATA> <NAME>
```
_Ahora para que esta imagen se encuentre disponible y la solución pueda acceder a ellas deberá realizar lo siguiente_
```
openstack image set --public IMAGE_ID

```
> [!IMPORTANT]
> Deberá primero hacer un listado de las imágenes importadas y luego deberá seleccionar el **IMAGE_ID** correspondiente a la imagen que quiera seleccionar
## Ejecutando las pruebas ⚙️

_Explica como ejecutar las pruebas automatizadas para este sistema_

### Analice las pruebas end-to-end 🔩

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

### Y las pruebas de estilo de codificación ⌨️

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

## Despliegue 📦

_Agrega notas adicionales sobre como hacer deploy_

## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - El framework web usado
* [Maven](https://maven.apache.org/) - Manejador de dependencias
* [ROME](https://rometools.github.io/rome/) - Usado para generar RSS

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

## Autores ✒️

_Menciona a todos aquellos que ayudaron a levantar el proyecto desde sus inicios_

* **Andrés Villanueva** - *Trabajo Inicial* - [villanuevand](https://github.com/villanuevand)
* **Fulanito Detal** - *Documentación* - [fulanitodetal](#fulanito-de-tal)

También puedes mirar la lista de todos los [contribuyentes](https://github.com/your/project/contributors) quíenes han participado en este proyecto. 

## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* Dona con cripto a esta dirección: `0xf253fc233333078436d111175e5a76a649890000`
* etc.
