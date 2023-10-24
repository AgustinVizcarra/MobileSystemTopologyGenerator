import uuid
from Classes.Network import Network
from NetworkHandler import NetworkConstructor
from VMHandler import VMConstructor

class TopoConstructor:
    def DefaultTopologyConstructor(self,VMs,CIDR,neutron,nova):
        # Una sola red
        nameNetwork= str(uuid.uuid4())
        nameSubnet = str(uuid.uuid4())
        network = Network(nameNetwork=nameNetwork,CIDR=CIDR,nameSubnet=nameSubnet)
        NetworkConstructor.createNetwork(network,neutron,nova)
        #Asignacion de la cantidad de interfaces para el segmento de red
        mapVM_network={}
        mapVM_response={}
        for vm,interfaces in VMs.items():
            aux = []
            for interface in interfaces:
                aux.append(interface)
            mapVM_network[vm]={nameNetwork:aux}
            #mapVM_response[vm.name]={nameNetwork:aux}
        for vm,network_interfaces in mapVM_network.items():
            outputdata=VMConstructor.createVM(vm,network_interfaces,neutron,nova)
            data={}
            data['network']=network_interfaces
            data['IPAccess']=outputdata[1]+":"+outputdata[3]
            data['IPMgmt']=outputdata[2]
            mapVM_response[vm.name]=data
        return mapVM_response