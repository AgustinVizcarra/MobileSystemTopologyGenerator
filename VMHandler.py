from Nova import NovaClient
from Neutron import NeutronClient
from Classes.VM import VM
from Classes.Network import Network

class VMConstructor:
    def createVM(VM: VM,networks,neutron: NeutronClient,nova: NovaClient):
        ##Networks es una listas con los nombres de las redes a las cuales se deben crear
        net_id = {}
        for n in networks:
            aux = []
            for ips in networks.values():
                aux.append(ips)
            net_id[neutron.getNetworkIDbyName(n)] = ips 
        puerto_asignado=nova.create_instance_with_multiple_networks(nombre=VM.name,flavor_id = VM.flavorID, imagen_id = VM.imageID, keypair_id = VM.keyPairID, security_group_id = VM.securitygroupID, networks = net_id)
        return puerto_asignado
        
    def editVM(VM: VM,network: Network,neutron: NeutronClient,nova: NovaClient):
        vm_id = nova.get_instance_id(vm_name=VM.name)
        network_id = neutron.getNetworkIDbyName(network)
        nova.agregar_interfaz_to_VM(network_id=network_id,vm_id=vm_id)