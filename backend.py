from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from Keystone import KeystoneAuth
from Nova import NovaClient
from Neutron import NeutronClient
from Glance import GlanceClient
from Classes import VM,Network 
from TopoHandler import TopoConstructor
import os
import uuid

app = FastAPI(title = "Servidor instanciado",description=" Mini Orquestador generador de topologias",version="1.0.1")
load_dotenv()
#-- Definición de variables globales
neutron='initvalues'
nova='initvalues'
glance='initvalues'
#-----API-----
@app.post("/createTopology/")
async def createTopology(body: dict):
    if not body:
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'codigo' in body and 'tipo' in body:
            match body['tipo']:
                case 1:
                    data = createTopo1(body['codigo'],body['tipo'])
                    return JSONResponse(content=data,status_code=200)
                case 2:
                    data = createTopo2(body['codigo'],body['tipo'])
                    return JSONResponse(content=data,status_code=200)
                case 3:
                    data = createTopo3(body['codigo'],body['tipo'])
                    return JSONResponse(content=data,status_code=200)
                case 4:
                    data = createTopo4(body['codigo'],body['tipo'])
                    return JSONResponse(content=data,status_code=200)
                case _:
                    data = {"mensaje": "Se envió un formato de dato inválido o no se tiene registro de esta topologia"}
                    return JSONResponse(content=data,status_code=400)
        else:
            data = {"mensaje": "Falta parámetros para la creación de la topología"}
            return JSONResponse(content=data,status_code=400)
    
# UERANSIM-Open5GS 
def createTopo1(alumno,tipo):
    #LLamamos los servicios de neutron,glance y nova
    global neutron,glance,nova
    # Para esto se considerará la siguiente topología 
    CIDR = "192.168.0.0/24"
    Topology_ID = str(uuid.uuid4())
    listaVMs = {}
    # Posteriormente definimos las siguientes VM's que conformarán la topología
    ## Definicion de VM-UE UERANSIM
    # vm_nombre_ue = UERANSIM-UE
    # vm_ue_flavor_id =  Flavor de UE-UERANSIM
    # vm_image_id_ue = Imagen (snapshot) de la imagen de UERANSIM UE
    # vm_keypair_ue = keypair ssh (Opcional) de UERANSIM UE
    # vm_security_groups_ue = security groups base de la VM UERANSIM UE
    # Creo la VM con los parámetros indicados
    # vm_ue_ueransim = VM(vm_nombre_ue,vm_ue_flavor_id,vm_image_id_ue,vm_keypair_ue,vm_security_groups_ue)
    vm_ue_ueransim = 'VM_ueransim_ue'
    # asignación de interfaces
    interfaces_ue_ueransim = 1
    ## Definicion de VM-gNodeB UERANSIM
    # vm_nombre_gnb = UERANSIM-GNB
    # vm_gnb_flavor_id =  Flavor de gnb-UERANSIM
    # vm_image_gnb = Imagen (snapshot) de la imagen de UERANSIM gnb
    # vm_keypair_gnb = keypair ssh (Opcional) de UERANSIM gnb
    # vm_security_groups_gnb = security groups base de la VM UERANSIM gnb
    # Creo la VM con los parámetros indicados
    # vm_gnb_ueransim = VM(vm_nombre_gnb,vm_gnb_flavor_id,vm_image_gnb,vm_keypair_gnb,vm_security_groups_gnb)
    vm_gnb_ueransim = 'VM_ueransim_gnb'
    # asignación de interfaces
    interfaces_gnb_ueransim = 1
    ## Definicion de VM Open5GS Core
    # vm_nombre_o5gs = OPEN5GS-core
    # vm_o5gs_flavor_id =  Flavor de Open5GS-Core
    # vm_image_o5gs = Imagen (snapshot) de la imagen de Open5GS core
    # vm_keypair_o5gs = keypair ssh (Opcional) de Open5GS core
    # vm_security_groups_o5gs = security groups base de la Open5GS core
    # Creo la VM con los parámetros indicados
    # vm_core_open5GS = VM(vm_nombre_o5gs,vm_o5gs_flavor_id,vm_image_o5gs,vm_keypair_o5gs,vm_security_groups_o5gs)
    vm_core_open5GS = 'VM_open5gs_core'
    # asignacion de interfaces
    interfaces_Open5GS_Core = 2
    ## Definicion de VM Open5GS UPF
    # vm_nombre_o5gs_upf = OPEN5GS-UPF
    # vm_o5gs_upf_flavor_id =  Flavor de Open5GS-Core-UPF
    # vm_image_o5gs_upf = Imagen (snapshot) de la imagen de Open5GS UPF
    # vm_keypair_o5gs_upf = keypair ssh (Opcional) de Open5GS UPF
    # vm_security_groups_o5gs_upf = security groups base de la Open5GS UPF
    # Creo la VM con los parámetros indicados
    # vm_upf_open5GS = VM(vm_nombre_o5gs_upf,vm_image_o5gs_upf,vm_keypair_o5gs_upf,vm_keypair_o5gs_upf,vm_security_groups_o5gs_upf)
    vm_core_open5GS_UPF = 'VM_open5gs_upf'
    # asignacion de interfaces:
    interfaces_Open5GS_UPF = 1
    # Definicion del arreglo 
    listaVMs[vm_ue_ueransim] = interfaces_ue_ueransim
    listaVMs[vm_gnb_ueransim] = interfaces_gnb_ueransim
    listaVMs[vm_core_open5GS] = interfaces_Open5GS_Core
    listaVMs[vm_core_open5GS_UPF] = interfaces_Open5GS_UPF
    # Construyo la topologia
    bodyResponse = {}
    bodyResponse['codigo'] = alumno
    bodyResponse['tipo'] = tipo
    bodyResponse['topologyID'] = Topology_ID
    responseValue=TopoConstructor().DefaultTopologyConstructor(listaVMs,CIDR,neutron,nova)
    bodyResponse['topologyValues'] = responseValue
    return bodyResponse
# LTE srsRAN-Open5GS 
def createTopo2(alumno,tipo):
    #LLamamos los servicios de neutron,glance y nova
    global neutron,glance,nova
    # Para esto se considerará la siguiente topología 
    CIDR = "192.168.0.0/24"
    Topology_ID = str(uuid.uuid4())
    listaVMs = {}
    # Posteriormente definimos las siguientes VM's que conformarán la topología
    ## Definicion de VM-UE srsRAN
    # vm_nombre_ue = srsRAN-UE
    # vm_ue_flavor_id =  Flavor de UE-srsRAN
    # vm_image_id_ue = Imagen (snapshot) de la imagen de srsRAN UE
    # vm_keypair_ue = keypair ssh (Opcional) de srsRAN UE
    # vm_security_groups_ue = security groups base de la VM srsRANS UE
    # Creo la VM con los parámetros indicados
    # vm_ue_srsran = VM(vm_nombre_ue,vm_ue_flavor_id,vm_image_id_ue,vm_keypair_ue,vm_security_groups_ue)
    vm_ue_srsran = 'VM_srsran_ue'
    # asignación de interfaces
    interfaces_ue_ueransim = 1
    ## Definicion de VM-eNodeB srsRAN
    # vm_nombre_enb = srsRAN-enb
    # vm_enb_flavor_id =  Flavor de enb-srsRAN
    # vm_image_enb = Imagen (snapshot) de la imagen de srsRAN enb
    # vm_keypair_enb = keypair ssh (Opcional) de srsRAN enb
    # vm_security_groups_enb = security groups base de la VM srsRAN gnb
    # Creo la VM con los parámetros indicados
    # vm_enb_srsRAN = VM(vm_nombre_enb,vm_enb_flavor_id,vm_image_enb,vm_keypair_enb,vm_security_groups_enb)
    vm_enb_srsRAN = 'vm_enb_srsRAN'
    # asignación de interfaces
    interfaces_enb_srsRAN = 1
    ## Definicion de VM Open5GS Core
    # vm_nombre_o5gs = OPEN5GS-core
    # vm_o5gs_flavor_id =  Flavor de Open5GS-Core
    # vm_image_o5gs = Imagen (snapshot) de la imagen de Open5GS core
    # vm_keypair_o5gs = keypair ssh (Opcional) de Open5GS core
    # vm_security_groups_o5gs = security groups base de la Open5GS core
    # Creo la VM con los parámetros indicados
    # vm_core_open5GS = VM(vm_nombre_o5gs,vm_o5gs_flavor_id,vm_image_o5gs,vm_keypair_o5gs,vm_security_groups_o5gs)
    vm_core_open5GS = 'VM_open5gs_core'
    # asignacion de interfaces
    interfaces_Open5GS_Core = 2
    ## Definicion de VM Open5GS SGWU
    # vm_nombre_o5gs_SGWU = OPEN5GS-SGWU
    # vm_o5gs_sgwu_flavor_id =  Flavor de Open5GS-Core-SGWU
    # vm_image_o5gs_sgwu = Imagen (snapshot) de la imagen de Open5GS SGWU
    # vm_keypair_o5gs_sgwu = keypair ssh (Opcional) de Open5GS SGWU
    # vm_security_groups_o5gs_sgwu = security groups base de la Open5GS SGWU
    # Creo la VM con los parámetros indicados
    # vm_sgwu_open5GS = VM(vm_nombre_o5gs_sgwu,vm_image_o5gs_sgwu,vm_keypair_o5gs_sgwu,vm_keypair_o5gs_sgwu,vm_security_groups_o5gs_upf)
    vm_core_open5GS_SGWU = 'VM_open5gs_sgwu'
    # asignacion de interfaces:
    interfaces_Open5GS_SGWU = 1
    # Definicion del arreglo 
    listaVMs[vm_ue_srsran] = interfaces_ue_ueransim
    listaVMs[vm_enb_srsRAN] = interfaces_enb_srsRAN 
    listaVMs[vm_core_open5GS] = interfaces_Open5GS_Core
    listaVMs[vm_core_open5GS_SGWU] = interfaces_Open5GS_SGWU
    # Construyo la topologia
    bodyResponse = {}
    bodyResponse['codigo'] = alumno
    bodyResponse['tipo'] = tipo
    bodyResponse['topologyID'] = Topology_ID
    responseValue=TopoConstructor().DefaultTopologyConstructor(listaVMs,CIDR,neutron,nova)
    bodyResponse['topologyValues'] = responseValue
    return bodyResponse
# RIC srsRAN-Open5GS
def createTopo3(alumno,tipo):
    #LLamamos los servicios de neutron,glance y nova
    global neutron,glance,nova
    # Para esto se considerará la siguiente topología 
    CIDR = "192.168.0.0/24"
    Topology_ID = str(uuid.uuid4())
    listaVMs = {}
    # Posteriormente definimos las siguientes VM's que conformarán la topología
    ## Definicion de VM-UE srsRAN
    # vm_nombre_ue = srsRAN-UE
    # vm_ue_flavor_id =  Flavor de UE-srsRAN
    # vm_image_id_ue = Imagen (snapshot) de la imagen de srsRAN UE
    # vm_keypair_ue = keypair ssh (Opcional) de srsRAN UE
    # vm_security_groups_ue = security groups base de la VM srsRANS UE
    # Creo la VM con los parámetros indicados
    # vm_ue_srsran = VM(vm_nombre_ue,vm_ue_flavor_id,vm_image_id_ue,vm_keypair_ue,vm_security_groups_ue)
    vm_ue_srsran = 'VM_srsran_ue'
    # asignación de interfaces
    interfaces_ue_ueransim = 1
    ## Definicion de VM-gNodeB srsRAN
    # vm_nombre_gnb = srsRAN-gnb
    # vm_gnb_flavor_id =  Flavor de gnb-srsRAN
    # vm_image_gnb = Imagen (snapshot) de la imagen de srsRAN gnb
    # vm_keypair_gnb = keypair ssh (Opcional) de srsRAN gnb
    # vm_security_groups_gnb = security groups base de la VM srsRAN gnb
    # Creo la VM con los parámetros indicados
    # vm_gnb_srsRAN = VM(vm_nombre_gnb,vm_gnb_flavor_id,vm_image_gnb,vm_keypair_gnb,vm_security_groups_gnb)
    vm_gnb_srsRAN = 'vm_gnb_srsRAN'
    # asignación de interfaces
    interfaces_gnb_srsRAN = 1
    ## Definicion de VM Open5GS Core
    # vm_nombre_o5gs = OPEN5GS-core
    # vm_o5gs_flavor_id =  Flavor de Open5GS-Core
    # vm_image_o5gs = Imagen (snapshot) de la imagen de Open5GS core
    # vm_keypair_o5gs = keypair ssh (Opcional) de Open5GS core
    # vm_security_groups_o5gs = security groups base de la Open5GS core
    # Creo la VM con los parámetros indicados
    # vm_core_open5GS = VM(vm_nombre_o5gs,vm_o5gs_flavor_id,vm_image_o5gs,vm_keypair_o5gs,vm_security_groups_o5gs)
    vm_core_open5GS = 'VM_open5gs_core'
    # asignacion de interfaces
    interfaces_Open5GS_Core = 3
    ## Definicion de FLEX RIC (Radio Interface Controller)
    # vm_nombre_flex_ric = flex-ric
    # vm_flex_ric_flavor_id =  Flavor de flex_ric
    # vm_image_flex_ric = Imagen (snapshot) de la imagen de flex_ric
    # vm_keypair_flex_ric = keypair ssh (Opcional) de flex_ric
    # vm_security_groups_flex_ric = security groups base de la flex_ric
    # Creo la VM con los parámetros indicados
    # vm_flex_ric = VM(vm_nombre_flex_ric,vm_flex_ric_flavor_id,vm_image_flex_ric,vm_keypair_flex_ric,vm_security_groups_flex_ric)
    vm_flex_ric = 'VM_flex_ric'
    # asignacion de interfaces:
    interfaces_Flex_Ric = 1
    # Definicion del arreglo 
    listaVMs[vm_ue_srsran] = interfaces_ue_ueransim
    listaVMs[vm_gnb_srsRAN] = interfaces_gnb_srsRAN 
    listaVMs[vm_core_open5GS] = interfaces_Open5GS_Core
    listaVMs[vm_flex_ric] = interfaces_Flex_Ric
    # Construyo la topologia
    bodyResponse = {}
    bodyResponse['codigo'] = alumno
    bodyResponse['tipo'] = tipo
    bodyResponse['topologyID'] = Topology_ID
    responseValue=TopoConstructor().DefaultTopologyConstructor(listaVMs,CIDR,neutron,nova)
    bodyResponse['topologyValues'] = responseValue
    return bodyResponse
# NR srsRAN-Open5GS 
def createTopo4(alumno,tipo):
    #LLamamos los servicios de neutron,glance y nova
    global neutron,glance,nova
    # Para esto se considerará la siguiente topología 
    CIDR = "192.168.0.0/24"
    Topology_ID = str(uuid.uuid4())
    listaVMs = {}
    # Posteriormente definimos las siguientes VM's que conformarán la topología
    ## Definicion de VM-UE srsRAN
    # vm_nombre_ue = srsRAN-UE
    # vm_ue_flavor_id =  Flavor de UE-srsRAN
    # vm_image_id_ue = Imagen (snapshot) de la imagen de srsRAN UE
    # vm_keypair_ue = keypair ssh (Opcional) de srsRAN UE
    # vm_security_groups_ue = security groups base de la VM srsRANS UE
    # Creo la VM con los parámetros indicados
    # vm_ue_srsran = VM(vm_nombre_ue,vm_ue_flavor_id,vm_image_id_ue,vm_keypair_ue,vm_security_groups_ue)
    vm_ue_srsran = 'VM_srsran_ue'
    # asignación de interfaces
    interfaces_ue_ueransim = 1
    ## Definicion de VM-gNodeB srsRAN
    # vm_nombre_gnb = srsRAN-gnb
    # vm_gnb_flavor_id =  Flavor de gnb-srsRAN
    # vm_image_gnb = Imagen (snapshot) de la imagen de srsRAN gnb
    # vm_keypair_gnb = keypair ssh (Opcional) de srsRAN gnb
    # vm_security_groups_gnb = security groups base de la VM srsRAN gnb
    # Creo la VM con los parámetros indicados
    # vm_gnb_srsRAN = VM(vm_nombre_gnb,vm_gnb_flavor_id,vm_image_gnb,vm_keypair_gnb,vm_security_groups_gnb)
    vm_gnb_srsRAN = 'vm_gnb_srsRAN'
    # asignación de interfaces
    interfaces_gnb_srsRAN = 1
    ## Definicion de VM Open5GS Core
    # vm_nombre_o5gs = OPEN5GS-core
    # vm_o5gs_flavor_id =  Flavor de Open5GS-Core
    # vm_image_o5gs = Imagen (snapshot) de la imagen de Open5GS core
    # vm_keypair_o5gs = keypair ssh (Opcional) de Open5GS core
    # vm_security_groups_o5gs = security groups base de la Open5GS core
    # Creo la VM con los parámetros indicados
    # vm_core_open5GS = VM(vm_nombre_o5gs,vm_o5gs_flavor_id,vm_image_o5gs,vm_keypair_o5gs,vm_security_groups_o5gs)
    vm_core_open5GS = 'VM_open5gs_core'
    # asignacion de interfaces
    interfaces_Open5GS_Core = 2
    ## Definicion de VM Open5GS Core
    # vm_nombre_o5gs_upf = OPEN5GS-UPF
    # vm_o5gs_upf_flavor_id =  Flavor de Open5GS-Core-UPF
    # vm_image_o5gs_upf = Imagen (snapshot) de la imagen de Open5GS UPF
    # vm_keypair_o5gs_upf = keypair ssh (Opcional) de Open5GS UPF
    # vm_security_groups_o5gs_upf = security groups base de la Open5GS UPF
    # Creo la VM con los parámetros indicados
    # vm_upf_open5GS = VM(vm_nombre_o5gs_upf,vm_o5gs_upf_flavor_id,vm_image_o5gs_upf,vm_keypair_o5gs_upf,vm_security_groups_o5gs_upf)
    vm_core_open5GS_UPF = 'VM_open5gs_upf'
    # asignacion de interfaces:
    interfaces_Open5GS_UPF = 1
    # Definicion del arreglo 
    listaVMs[vm_ue_srsran] = interfaces_ue_ueransim
    listaVMs[vm_gnb_srsRAN] = interfaces_gnb_srsRAN 
    listaVMs[vm_core_open5GS] = interfaces_Open5GS_Core
    listaVMs[vm_core_open5GS_UPF] = interfaces_Open5GS_UPF
    # Construyo la topologia
    bodyResponse = {}
    bodyResponse['codigo'] = alumno
    bodyResponse['tipo'] = tipo
    bodyResponse['topologyID'] = Topology_ID
    responseValue=TopoConstructor().DefaultTopologyConstructor(listaVMs,CIDR,neutron,nova)
    bodyResponse['topologyValues'] = responseValue
    return bodyResponse

if __name__ == "__main__":
    # Autenticando con Openstack
    # username = Defino nombre de usuario
    # password = Defino contraseña
    # keystone = KeystoneAuth(username,password)
    # token = keystone.get_token()
    # Si en caso hubiera un superusuario
    # token = keystone.updateToken()
    # Instancio los servicios de OpenStack
    # nova = NovaClient(token,username,password)
    # neutron = NeutronClient(token)
    # glance = GlanceClient(token)
    import uvicorn
    #Inicalizando servicio de API
    uvicorn.run("backend:app",host="192.168.1.35",ssl_keyfile=os.environ.get('SSL_KEYFILE'),ssl_certfile=os.environ.get('SSL_CERTFILE'),port=8888,reload=True)
    