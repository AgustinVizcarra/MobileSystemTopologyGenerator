# Generador de topologías móviles 4G y 5G

Este proyecto consiste en una solución que permite el despliegue de redes minimalistas para estudio y análisis de los procedimientos internos de las redes 4G y 5G 
de forma virtualizada. Asimismo este proyecto se apoya en **Openstack** de forma que el sistema permita el despliegue de las redes de forma automatizada por medio de 
APIS gracias a un SDK. Es importante mencionar que para esta solución se tomó como referencia las herramientas de Core abierto **Open5GS**, herramientas de RAN
como **UERANSIM**,  **srsRAN** y herramientas de análisis de paquetes como es el caso de **5G Trace Visualizer** y **Wireshark**.

## Comenzando 🚀

Si en caso se quisiera replicar esta solución es importante tener en cuenta todos los requisitos y consideraciones a seguir para el **Deployment**.


### Pre-requisitos 🛠️

Para empezar se tiene que tener encuenta las siguientes dependecias:

- [Openstack Victoria](https://www.openstack.org/software/victoria/) ![release](https://img.shields.io/badge/version-22.3.0-blue)
- [Python](https://www.python.org/downloads/release/python-380/) ![version](https://img.shields.io/badge/version-3.8-blue)
- [Open5GS](https://open5gs.org/open5gs/docs/) ![release](https://img.shields.io/badge/release-2.6.6-blue)
- [UERANSIM](https://github.com/aligungr/UERANSIM) ![release](https://img.shields.io/badge/release-3.2.6-blue)
- [srsRAN](https://www.srslte.com/) ![release](https://img.shields.io/badge/release-23.10-blue)
- [5G Trace Visualizer](https://github.com/telekom/5g-trace-visualizer) ![version](https://img.shields.io/badge/latest-blue)
- [Wireshark](https://www.wireshark.org/docs/relnotes/) ![version](https://img.shields.io/badge/release-4.0.14-blue)
- [Ubuntu](https://releases.ubuntu.com/) ![version](https://img.shields.io/badge/release-20.04LTS-blue)
- [OpenVSwitch](https://docs.openvswitch.org/en/latest/faq/releases/) ![version](https://img.shields.io/badge/release-3.0-blue)

### Requisitos 📘
Para poder aplicar la solución se tuvieron nodos/máquinas virtuales con las siguientes características:
<p align="center"><b>Requerimientos de hardware</b></p>
<p align="center"><img src="https://github.com/AgustinVizcarra/MobileSystemTopologyGenerator/assets/92816809/8bd6b400-cb1b-4e8e-ae33-e9f34326755e" width="30%" height="30%" /></p>

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
> Deberá primero hacer un listado de las imágenes importadas mediante el siguiente comando
> ```
> glance image-list
> ```
> Luego, deberá seleccionar el **IMAGE_ID** correspondiente a la imagen que quiera volver público.
## Integración de OpenStack con el SDK ⚙️

_Para que pueda funcionar el despliegue automatizado vía APIS se debe considerar realizas las siguientes modificaciones en el SDK para que este funcione de forma correcta:_
1. En el archivo **Nova.py**
```
## En la declaración de parámetros del cliente Nova
def __init__(self, auth_token,username, password):
        # Cambiar URL
        self.auth_url = "http://<DIRECCIÓN_IP_CONTROLADOR>:5000/v3" ## Keystone
        self.auth_token = auth_token
        self.username = username
        self.password = password
        self.IdProject = None  # Agregar propiedad IdProject
        self.nova_url = "http://<DIRECCIÓN_IP_CONTROLADOR>:8774" ## Nova
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }
        ## cambiar<
        self.providerNetworkID = "<SELF_PROVIDER_NETWORK_ID>" ## Self Provider Network (Example:1457923c-6088-46e9-a184-5cd9b8d097d8)
....
def create_instance_with_multiple_networks(self, nombre, flavor_id, imagen_id,keypair_id, security_group_id,networks):
            ....
            ## Tener en cuenta que según la arquitectura la salida se configura vía IPTables, si en su caso no tuviera la misma arquitectura con un GW
            ## Modifique esta sección según corresponda
            print("[*] Comando para acceder desde Internet a la VM: ssh {usuario}@<DIRECCIÓN_IP_CONTROLADOR> -p "+str(puerto_libre))
            print("[*] Instancia creada de manera exitosa")
            return [nombre,'<DIRECCIÓN_IP_CONTROLADOR>',IP4,puerto_libre]
        else:
            print("Error al crear la instancia:", response.status_code)
            return None
```
2. En el archivo **Neutron.py**

```
## En la declaración de parámetros del cliente de Neutron
def __init__(self, auth_token):
        self.auth_token = auth_token
        ## Cambiar URL
        self.neutron_url = "http://<DIRECCIÓN_IP_CONTROLADOR>:9696/v2.0/"
        self.headers = {
            'Content-Type': 'application/json',
            'X-Auth-Token': self.auth_token
        }
        self.NetworkID = None
```
3. En el archivo **Keystone.py**
```
## En la declaración de parámetros del cliente de Keystone
def __init__(self,username, password):
        self.auth_url = "http://<DIRECCIÓN_IP_CONTROLADOR>:5000/v3"
        self.username = username
        self.password = password
        self.token = None
        self.headers = {'Content-Type': 'application/json'}
        self.UserID = None
        self.ProjectID = None
        self.RolName = None
```
4. En el archivo **Glance.py**
```
## En la declaración de parámetros del cliente de Keystone
def __init__(self,auth_token):
        self.auth_token = auth_token
        self.glance_url = "http://<DIRECCIÓN_IP_CONTROLADOR>:9292/v2"
        self.headers = { 'Content-Type': 'application/json','X-Auth-Token': self.auth_token }
```
5. En el archivo **backend.py**
```
## En el inicio de la instancia se usará el usuario ADMIN para crear las topologías según el proyecto asociado a cada usuario
@app.on_event('startup')
async def startup():
    # Instancio valores
    global neutron,glance,nova
    # Autenticando con Openstack
    username = <ADMIN_USERNAME>
    password = <ADMIN_PASSWORD>
    keystone = KeystoneAuth(username,password)
    token = keystone.get_token()
    token = keystone.updateToken()
    # ADMIN Project ID (cambiar posteriormente)
    project_admin_id = <USER_PROJECT_ID>
    token = keystone.get_token_project(project_admin_id)
    # Instancio los servicios de OpenStack
    nova = NovaClient(token,username,password)
    glance = GlanceClient(token)
    neutron = NeutronClient(token)
...
# Instanciación del servicio de APIs
if __name__ == "__main__":
    import uvicorn
    # Es opcional el uso de certificado SSL en caso desee puede consultar certificados SSL autofirmados con certbot (https://certbot.eff.org/)
    # En este caso el puerto lo puede configurar según corresponda, para nuestro caso se usó el 8888
    # Inicalizando servicio de API
uvicorn.run("backend:app",host="<DIRECCIÓN_IP_CONTROLADOR>",ssl_keyfile=os.environ.get('SSL_KEYFILE'),ssl_certfile=os.environ.get('SSL_CERTFILE'),port=8888,reload=True)
```
> [!NOTE]
> En nuestro caso el servicio fue desplegado en una instancia de uvicorn para su operación, el servicio puede ser operado desde instancias corriendo en contenedores como **Docker** o **Podman**.

> [!WARNING]
> Para evitar problemas de ejecución, verifique que los servicios de Openstack y el orquestador (backend) tenga asignados los privilegios respectivos.
### Realizando Pruebas 🔩

_Para poder ejecutar las pruebas puede hacer uso de clientes HTTPs como el caso de Postman. Para ello puede tomar el siguiente ejemplo de ejecución y la respuesta obtenida del servicio al momento de crear una topología_

<p align="center"><b>Ejemplo de solicitud</b></p>
<p align="center"><img src="https://github.com/AgustinVizcarra/MobileSystemTopologyGenerator/assets/92816809/da8c3471-c5a5-4e79-857f-215acdde119f" width="50%" height="50%" /></p> 

<p align="center"><b>Ejemplo de respuesta</b></p>
<p align="center"><img src="https://github.com/AgustinVizcarra/MobileSystemTopologyGenerator/assets/92816809/6de20655-bad1-4acc-afc2-14fd46bcd336" width="50%" height="50%" /></p> 

_Podrá también validar la creación de la topología ingresando al Dashboard Horizon_

<p align="center"><b>Vista de Horizon</b></p>
<p align="center"><img src="https://github.com/AgustinVizcarra/MobileSystemTopologyGenerator/assets/92816809/c1dbf6ec-ab48-4e00-8475-eef915be6e7b" width="50%" height="50%" /></p> 

## Contacto y/o preguntas 🖇️

Si en caso necesitarás las imágenes usadas para poder desplegar las topologías, dudas o comentarios de mejora sientete libre en escribirnos a **a.vizcarra@pucp.edu.pe** o **ronny.pastor@pucp.edu.pe**. Adicionalmente, si quieres entender como se encuentran configuradas por dentro cada una de las imágenes puedes visitar el **[repositorio de configuraciones](https://github.com/AgustinVizcarra/Gira_4G_5G_Tools)**

## Autores ✒️

_El personal detrás de la formulación, elaboración y ejecución de este proyecto:_

* **[Agustin Vizcarra Lizarbe](https://www.linkedin.com/in/agustin-vizcarra-lizarbe-14275b20b/)**
* **[Ronny Pastor Kolmakov](https://www.linkedin.com/in/ronny-eduardo-pastor-kolmakov-1888211b5/)**

## Licencia 📄

Este proyecto está bajo la licencia GNU GPL v2.0 para más detalles remitase al archivo **LICENSE.GPL**

## Reconocimientos🎁

* Expresamos nuestra más sincero reconocimiento a nuestros asesores **Cesar Santivañez** y **José Rodriguez** ya que sin ellos este proyecto no hubiera sido posible.
* Agradecemos de sobremanera al Grupo de Investigación de Redes Avanzadas (GIRA) por todo el apoyo brindado y por siempre mostrar la mejor disposición para ayudar.
* Agradecemos al equipo de NOKIA USA por la orientación profesional y por el soporte brindado.
* Agradecemos a todos los desarrolladores detrás de las herramientas usadas ya que sin el desarrollo de sus herramientas y la disponibilidad de uso abierto, no hubieramos podido concretar este proyecto.
* Agradecemos y dedicamos este trabajo a toda la especialidad de Ingeniería de las Telecomunicaciones de la Pontifica Universidad Católica del Perú.
