import requests
import data
import helpers
#Aqui se construyen las solicitudes API que se necesitan para los tests. Asi si algo cambia no tengo que buscarlo en las pruebas
def create_delivery(body):
    return requests.post(data.UrlpruebasApi + data.postCreateDelivery,json=body, headers=data.headers)
def create_package(body):
    return requests.post(data.UrlpruebasApi + data.postCreatePackage, json=body, headers=data.headers)
def login_delivery(body):
    return requests.post(data.UrlpruebasApi + data.postLoginDelivery, json=body, headers=data.headers)
def accept_package_automated():
    return requests.put(data.UrlpruebasApi+data.putAcceptPackage+helpers.get_id_package()+"?courierId="+ helpers.getnumberdelivery())
def getpackageByNumber(packagenumber):
    return requests.get(data.UrlpruebasApi + data.getPackageByNumber + str(packagenumber))
#para casos de prueba puntuales
def accept_package_manual(packageid,deliveryid):
    return requests.put(data.UrlpruebasApi+data.putAcceptPackage+packageid+"?courierId="+ deliveryid)
def complete_package_automated():
    return requests.put(data.putCompletePackage+helpers.get_id_package())
def complete_package_manual(id):
    return requests.put(data.UrlpruebasApi+data.putCompletePackage+id)



