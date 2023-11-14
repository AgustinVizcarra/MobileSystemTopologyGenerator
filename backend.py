from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from Keystone import KeystoneAuth
from Nova import NovaClient
from Neutron import NeutronClient
from Glance import GlanceClient
from Classes.VM import VM 
from TopoHandler import TopoConstructor
import os
import uuid

app = FastAPI(title = "Servidor instanciado",description=" Mini Orquestador generador de topologias",version="1.0.1")
load_dotenv()

@app.on_event('startup')
async def startup():
    # Instancio valores
    global neutron,glance,nova
    # Autenticando con Openstack
    username = 'admin'
    password = 'ADMIN_PASS'
    keystone = KeystoneAuth(username,password)
    token = keystone.get_token()
    token = keystone.updateToken()
    # ADMIN Project ID (cambiar posteriormente)
    project_admin_id = '9c599a37763940acb61124467d9e423e'
    token = keystone.get_token_project(project_admin_id)
    # Instancio los servicios de OpenStack
    nova = NovaClient(token,username,password)
    glance = GlanceClient(token)
    neutron = NeutronClient(token)
    
#-----API-----#
@app.post("/createTopology/")
async def createTopology(body: dict):
    if not body:
        data = {"mensaje": "no se envió datos en el body"}
        return JSONResponse(content=data,status_code=400)
    else:
        if 'codigo' in body and 'tipo' in body:
            ## Para versiones de python superiores en adelante (3.10)
            #match body['tipo']:
                #case 1:
                    #data = createTopo1(body['codigo'],body['tipo'])
                    #return JSONResponse(content=data,status_code=200)
                #case 2:
                    #data = createTopo2(body['codigo'],body['tipo'])
                    #return JSONResponse(content=data,status_code=200)
                #case 3:
                    #data = createTopo3(body['codigo'],body['tipo'])
                    #return JSONResponse(content=data,status_code=200)
                #case 4:
                    #data = createTopo4(body['codigo'],body['tipo'])
                    #return JSONResponse(content=data,status_code=200)
                #case 5:
                    #data = createTopo5(body['codigo'],body['tipo'])
                    #return JSONResponse(content=data,status_code=200)
                #case _:
                    #data = {"mensaje": "Se envió un formato de dato inválido o no se tiene registro de esta topologia"}
                    #return JSONResponse(content=data,status_code=400)
            if body['tipo'] == 1:
                data = createTopo1(body['codigo'],body['tipo'])
                return JSONResponse(content=data,status_code=200)                
            elif body['tipo'] == 2:
                data = createTopo2(body['codigo'],body['tipo'])
                return JSONResponse(content=data,status_code=200)
            elif body['tipo'] == 3:
                data = createTopo3(body['codigo'],body['tipo'])
                return JSONResponse(content=data,status_code=200)                            
            elif body['tipo'] == 4:
                data = createTopo4(body['codigo'],body['tipo'])
                return JSONResponse(content=data,status_code=200)
            elif body['tipo'] == 5:
                data = createTopo5(body['codigo'],body['tipo'])
                return JSONResponse(content=data,status_code=200)
            else:
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
    # UERANSIM-Open5GS
    interfaz_UE_UERANSIM = ['192.168.0.132']
    interfaz_GNB_UERANSIM = ['192.168.0.131']
    interfaz_5GC_CPLANE_OPEN5GS = ['192.168.0.111']
    interfaz_5GC_UPLANE_OPEN5GS = ['192.168.0.112']
    listado = nova.list_flavors()
    listado_imagenes = glance.listar_imagenes()
    ## Definicion de VM-UE UERANSIM
    vm_nombre_ue = "UERANSIM-UE-"+alumno
    vm_ue_flavor_id =  listado['2/2/10'][0]
    vm_image_id_ue = listado_imagenes['UERANSIM-UE']
    vm_keypair_ue = None
    vm_security_groups_ue = None
    # Creo la VM con los parámetros indicados
    vm_ue_ueransim = VM(vm_nombre_ue,vm_ue_flavor_id,vm_image_id_ue,vm_keypair_ue,vm_security_groups_ue)
    # asignación de interfaces
    listaVMs[vm_ue_ueransim] = interfaz_UE_UERANSIM
    ## Definicion de VM-gNodeB UERANSIM
    vm_nombre_gnb = "UERANSIM-GNB-"+alumno
    vm_gnb_flavor_id =  listado['2/2/10'][0]
    vm_image_gnb = listado_imagenes['UERANSIM-GNB']
    vm_keypair_gnb = None
    vm_security_groups_gnb = None
    # Creo la VM con los parámetros indicados
    vm_gnb_ueransim = VM(vm_nombre_gnb,vm_gnb_flavor_id,vm_image_gnb,vm_keypair_gnb,vm_security_groups_gnb)
    # asignación de interfaces
    listaVMs[vm_gnb_ueransim] = interfaz_GNB_UERANSIM
    ## Definicion de VM Open5GS Core
    vm_nombre_o5gs = 'Open5GS-5GC-'+alumno
    vm_o5gs_flavor_id =  listado['ubuntu'][0]
    vm_image_o5gs = listado_imagenes['Open5GS-5GC']
    vm_keypair_o5gs = None
    vm_security_groups_o5gs = None
    # Creo la VM con los parámetros indicados
    vm_core_open5GS = VM(vm_nombre_o5gs,vm_o5gs_flavor_id,vm_image_o5gs,vm_keypair_o5gs,vm_security_groups_o5gs)
    # asignacion de interfaces
    listaVMs[vm_core_open5GS] = interfaz_5GC_CPLANE_OPEN5GS
    ## Definicion de VM Open5GS UPF
    vm_nombre_o5gs_upf = 'Open5GS-UPF-'+alumno
    vm_o5gs_upf_flavor_id =  listado['ubuntu'][0]
    vm_image_o5gs_upf = listado_imagenes['Open5GS-UPF-Corp']
    vm_keypair_o5gs_upf = None
    vm_security_groups_o5gs_upf = None
    # Creo la VM con los parámetros indicados
    vm_upf_open5GS = VM(vm_nombre_o5gs_upf,vm_o5gs_upf_flavor_id,vm_image_o5gs_upf,vm_keypair_o5gs_upf,vm_security_groups_o5gs_upf)
    # asignacion de interfaces:
    listaVMs[vm_upf_open5GS] = interfaz_5GC_UPLANE_OPEN5GS
    # Definicion del arreglo 
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
    # srsRAN LTE + Open5GS
    interfaz_UE_srsRAN = ['192.168.0.122']
    interfaz_ENB_srsRAN = ['192.168.0.121']
    interfaz_EPC_CPLANE_OPEN5GS = ['192.168.0.111']
    listado = nova.list_flavors()
    listado_imagenes = glance.listar_imagenes()
    ## Definicion de VM-UE srsRAN
    vm_nombre_ue = "srsRAN-UE-"+alumno
    vm_ue_flavor_id =  listado['ubuntu'][0]
    vm_image_id_ue = listado_imagenes['SRSRAN-LTE']
    vm_keypair_ue = None
    vm_security_groups_ue = None
    # Creo la VM con los parámetros indicados
    vm_ue_srsran = VM(vm_nombre_ue,vm_ue_flavor_id,vm_image_id_ue,vm_keypair_ue,vm_security_groups_ue)
    # asignación de interfaces
    listaVMs[vm_ue_srsran] = interfaz_UE_srsRAN
    ## Definicion de VM-eNodeB srsRAN
    vm_nombre_enb = 'srsRAN-eNb-'+alumno
    vm_enb_flavor_id =  listado['ubuntu'][0]
    vm_image_enb = listado_imagenes['SRSRAN-LTE']
    vm_keypair_enb = None
    vm_security_groups_enb = None
    # Creo la VM con los parámetros indicados
    vm_enb_srsRAN = VM(vm_nombre_enb,vm_enb_flavor_id,vm_image_enb,vm_keypair_enb,vm_security_groups_enb)
    # asignación de interfaces
    listaVMs[vm_enb_srsRAN] = interfaz_ENB_srsRAN 
    ## Definicion de VM Open5GS Core EPC
    vm_nombre_o5gs = 'Open5GS-EPC-'+alumno
    vm_o5gs_flavor_id = listado['ubuntu'][0]
    vm_image_o5gs = listado_imagenes['Open5GS-EPC']
    vm_keypair_o5gs = None
    vm_security_groups_o5gs = None
    # Creo la VM con los parámetros indicados
    vm_core_open5GS = VM(vm_nombre_o5gs,vm_o5gs_flavor_id,vm_image_o5gs,vm_keypair_o5gs,vm_security_groups_o5gs)
    # asignacion de interfaces
    listaVMs[vm_core_open5GS] = interfaz_EPC_CPLANE_OPEN5GS
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
    # srsRAN NR   + FlexRic
    interfaz_UE_srsRAN = ['192.168.0.122']
    interfaz_GNB_srsRAN = ['192.168.0.121']
    interfaz_5GC_UCPLANE_OPEN5GS = ['192.168.0.111']
    interfaz_flex_RIC = ['192.168.0.123']
    listado = nova.list_flavors()
    listado_imagenes = glance.listar_imagenes()
    ## Definicion de VM-UE srsRAN
    vm_nombre_ue = 'srsRAN-UE-'+alumno
    vm_ue_flavor_id =  listado['ubuntu'][0]
    vm_image_id_ue = listado_imagenes['SRSRAN-LTE']
    vm_keypair_ue = None
    vm_security_groups_ue = None
    # Creo la VM con los parámetros indicados
    vm_ue_srsran = VM(vm_nombre_ue,vm_ue_flavor_id,vm_image_id_ue,vm_keypair_ue,vm_security_groups_ue)
    # asignación de interfaces
    listaVMs[vm_ue_srsran] = interfaz_UE_srsRAN
    ## Definicion de VM-gNodeB srsRAN
    vm_nombre_gnb = 'srsRAN-gNb-E2-'+alumno
    vm_gnb_flavor_id = listado['ubuntu'][0]
    vm_image_gnb = listado_imagenes['SRSRAN-E2']
    vm_keypair_gnb = None
    vm_security_groups_gnb = None
    # Creo la VM con los parámetros indicados
    vm_gnb_srsRAN = VM(vm_nombre_gnb,vm_gnb_flavor_id,vm_image_gnb,vm_keypair_gnb,vm_security_groups_gnb)
    # asignación de interfaces
    listaVMs[vm_gnb_srsRAN] = interfaz_GNB_srsRAN
    ## Definicion de VM Open5GS Core
    vm_nombre_o5gs = 'Open5GS-Core-'+alumno
    vm_o5gs_flavor_id =  listado['ubuntu'][0]
    vm_image_o5gs = listado_imagenes['Open5GS-Monolithic']
    vm_keypair_o5gs = None
    vm_security_groups_o5gs = None
    # Creo la VM con los parámetros indicados
    vm_core_open5GS = VM(vm_nombre_o5gs,vm_o5gs_flavor_id,vm_image_o5gs,vm_keypair_o5gs,vm_security_groups_o5gs)
    # asignacion de interfaces
    listaVMs[vm_core_open5GS] = interfaz_5GC_UCPLANE_OPEN5GS
    ## Definicion de FLEX RIC (Radio Interface Controller)
    vm_nombre_flex_ric = 'flex-RIC-'+alumno
    vm_flex_ric_flavor_id = listado['ubuntu'][0]
    vm_image_flex_ric = listado_imagenes['FlexRIC']
    vm_keypair_flex_ric = None
    vm_security_groups_flex_ric = None
    # Creo la VM con los parámetros indicados
    vm_flex_ric = VM(vm_nombre_flex_ric,vm_flex_ric_flavor_id,vm_image_flex_ric,vm_keypair_flex_ric,vm_security_groups_flex_ric)
    # asignacion de interfaces:
    listaVMs[vm_flex_ric] = interfaz_flex_RIC
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
    # srsRAN NR + Open5GS
    interfaz_UE_srsRAN = ['192.168.0.122']
    interfaz_GNB_srsRAN = ['192.168.0.121']
    interfaz_5GC_CPLANE_OPEN5GS = ['192.168.0.111']
    interfaz_5GC_UPLANE_OPEN5GS = ['192.168.0.112']
    listado = nova.list_flavors()
    listado_imagenes = glance.listar_imagenes()
    ## Definicion de VM-UE srsRAN
    vm_nombre_ue = 'srsRAN-UE-'+alumno
    vm_ue_flavor_id = listado['ubuntu'][0]
    vm_image_id_ue = listado_imagenes['SRSRAN-LTE']
    vm_keypair_ue = None
    vm_security_groups_ue = None
    # Creo la VM con los parámetros indicados
    vm_ue_srsran = VM(vm_nombre_ue,vm_ue_flavor_id,vm_image_id_ue,vm_keypair_ue,vm_security_groups_ue)
    # asignación de interfaces
    listaVMs[vm_ue_srsran] = interfaz_UE_srsRAN
    ## Definicion de VM-gNodeB srsRAN
    vm_nombre_gnb = 'srsRAN-gNb-'+alumno
    vm_gnb_flavor_id =  listado['ubuntu'][0]
    vm_image_gnb = listado_imagenes['SRSRAN-NR']
    vm_keypair_gnb = None
    vm_security_groups_gnb = None
    # Creo la VM con los parámetros indicados
    vm_gnb_srsRAN = VM(vm_nombre_gnb,vm_gnb_flavor_id,vm_image_gnb,vm_keypair_gnb,vm_security_groups_gnb)
    # asignación de interfaces
    listaVMs[vm_gnb_srsRAN] = interfaz_GNB_srsRAN 
    ## Definicion de VM Open5GS Core
    vm_nombre_o5gs = 'Open5GS-5GC-'+alumno
    vm_o5gs_flavor_id =  listado['ubuntu'][0]
    vm_image_o5gs = listado_imagenes['Open5GS-5GC']
    vm_keypair_o5gs = None
    vm_security_groups_o5gs = None
    # Creo la VM con los parámetros indicados
    vm_core_open5GS = VM(vm_nombre_o5gs,vm_o5gs_flavor_id,vm_image_o5gs,vm_keypair_o5gs,vm_security_groups_o5gs)
    # asignacion de interfaces
    listaVMs[vm_core_open5GS] = interfaz_5GC_CPLANE_OPEN5GS
    ## Definicion de VM Open5GS Core
    vm_nombre_o5gs_upf = 'Open5GS-UPF-'+alumno
    vm_o5gs_upf_flavor_id =  listado['ubuntu'][0]
    vm_image_o5gs_upf = listado_imagenes['Open5GS-UPF']
    vm_keypair_o5gs_upf = None
    vm_security_groups_o5gs_upf = None
    # Creo la VM con los parámetros indicados
    vm_upf_open5GS = VM(vm_nombre_o5gs_upf,vm_o5gs_upf_flavor_id,vm_image_o5gs_upf,vm_keypair_o5gs_upf,vm_security_groups_o5gs_upf)
    # asignacion de interfaces:
    listaVMs[vm_upf_open5GS] = interfaz_5GC_UPLANE_OPEN5GS
    # Construyo la topologia
    bodyResponse = {}
    bodyResponse['codigo'] = alumno
    bodyResponse['tipo'] = tipo
    bodyResponse['topologyID'] = Topology_ID
    responseValue=TopoConstructor().DefaultTopologyConstructor(listaVMs,CIDR,neutron,nova)
    bodyResponse['topologyValues'] = responseValue
    return bodyResponse
# Network Slicing Open5GS-UERANSIM 
def createTopo5(alumno,tipo):
    #LLamamos los servicios de neutron,glance y nova
    global neutron,glance,nova
    # Para esto se considerará la siguiente topología 
    CIDR = "192.168.0.0/24"
    Topology_ID = str(uuid.uuid4())
    listaVMs = {}
    # Posteriormente definimos las siguientes VM's que conformarán la topología
    # UERANSIM + Open5GS
    interfaz_UE_UERANSIM = ['192.168.0.132']
    interfaz_GNB_UERANSIM = ['192.168.0.131']
    interfaz_5GC_CPLANE_OPEN5GS = ['192.168.0.111']
    interfaz_5GC_UPLANE_1_OPEN5GS = ['192.168.0.114']
    interfaz_5GC_UPLANE_2_OPEN5GS = ['192.168.0.115']
    listado = nova.list_flavors()
    listado_imagenes = glance.listar_imagenes()
    ## Definicion de VM-UE srsRAN
    vm_nombre_ue = 'ueransim-ue-'+alumno
    vm_ue_flavor_id = listado['2/2/10'][0]
    vm_image_id_ue = listado_imagenes['UERANSIM-NS-UE']
    vm_keypair_ue = None
    vm_security_groups_ue = None
    # Creo la VM con los parámetros indicados
    vm_ue_ueransim = VM(vm_nombre_ue,vm_ue_flavor_id,vm_image_id_ue,vm_keypair_ue,vm_security_groups_ue)
    # asignación de interfaces
    listaVMs[vm_ue_ueransim] = interfaz_UE_UERANSIM
    ## Definicion de VM-gNodeB srsRAN
    vm_nombre_gnb = 'ueransim-gnb-'+alumno
    vm_gnb_flavor_id =  listado['2/2/10'][0]
    vm_image_gnb = listado_imagenes['UERANSIM-NS-GNB']
    vm_keypair_gnb = None
    vm_security_groups_gnb = None
    # Creo la VM con los parámetros indicados
    vm_gnb_ueransim = VM(vm_nombre_gnb,vm_gnb_flavor_id,vm_image_gnb,vm_keypair_gnb,vm_security_groups_gnb)
    # asignación de interfaces
    listaVMs[vm_gnb_ueransim] = interfaz_GNB_UERANSIM 
    ## Definicion de VM Open5GS Core
    vm_nombre_o5gs = 'Open5GS-5GC-'+alumno
    vm_o5gs_flavor_id =  listado['ubuntu'][0]
    vm_image_o5gs = listado_imagenes['Open5GS-NS-5GC']
    vm_keypair_o5gs = None
    vm_security_groups_o5gs = None
    # Creo la VM con los parámetros indicados
    vm_core_open5GS = VM(vm_nombre_o5gs,vm_o5gs_flavor_id,vm_image_o5gs,vm_keypair_o5gs,vm_security_groups_o5gs)
    # asignacion de interfaces
    listaVMs[vm_core_open5GS] = interfaz_5GC_CPLANE_OPEN5GS
    ## Definicion de VM Open5GS UPF-1
    vm_nombre_o5gs_upf = 'Open5GS-UPF1-'+alumno
    vm_o5gs_upf_flavor_id =  listado['2/2/10'][0]
    vm_image_o5gs_upf = listado_imagenes['Open5GS-NS-UPF1']
    vm_keypair_o5gs_upf = None
    vm_security_groups_o5gs_upf = None
    # Creo la VM con los parámetros indicados
    vm_upf_1_open5GS = VM(vm_nombre_o5gs_upf,vm_o5gs_upf_flavor_id,vm_image_o5gs_upf,vm_keypair_o5gs_upf,vm_security_groups_o5gs_upf)
    # asignacion de interfaces:
    listaVMs[vm_upf_1_open5GS] = interfaz_5GC_UPLANE_1_OPEN5GS
    ## Definicion de VM Open5GS UPF-2
    vm_nombre_o5gs_upf = 'Open5GS-UPF2-'+alumno
    vm_o5gs_upf_flavor_id =  listado['2/2/10'][0]
    vm_image_o5gs_upf = listado_imagenes['Open5GS-NS-UPF2']
    vm_keypair_o5gs_upf = None
    vm_security_groups_o5gs_upf = None
    # Creo la VM con los parámetros indicados
    vm_upf_2_open5GS = VM(vm_nombre_o5gs_upf,vm_o5gs_upf_flavor_id,vm_image_o5gs_upf,vm_keypair_o5gs_upf,vm_security_groups_o5gs_upf)
    # asignacion de interfaces:
    listaVMs[vm_upf_2_open5GS] = interfaz_5GC_UPLANE_2_OPEN5GS
    # Construyo la topologia
    bodyResponse = {}
    bodyResponse['codigo'] = alumno
    bodyResponse['tipo'] = tipo
    bodyResponse['topologyID'] = Topology_ID
    responseValue=TopoConstructor().DefaultTopologyConstructor(listaVMs,CIDR,neutron,nova)
    bodyResponse['topologyValues'] = responseValue
    return bodyResponse
if __name__ == "__main__":
    import uvicorn
    #Inicalizando servicio de API
    uvicorn.run("backend:app",host="10.20.12.178",ssl_keyfile=os.environ.get('SSL_KEYFILE'),ssl_certfile=os.environ.get('SSL_CERTFILE'),port=8888,reload=True)
    