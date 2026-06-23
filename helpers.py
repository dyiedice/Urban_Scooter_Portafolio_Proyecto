import requests
import data
import ApiRequests
from searchers import trackers
import helpers
from selenium.webdriver import Keys
from datetime import datetime

#Pagina centrada en realizar el codigo que sera reutilizable durante los tests para facilitar la lectura y no crear mil líneas innecesariamente
def enterpage(driver):
    driver.get(data.UrlUrbanScooters)
#Algo que se vera alrededor de todo este archivo es que cuando hago algo automatizado también hago una version donde ingreso datos manualmente incluso si no le doy uso.
def get_track_number_package():
    response = ApiRequests.create_package(data.CreatePackagedata)
    response = response.json()
    return str(response["track"])
def get_track_number_package_manual(data):
    response = ApiRequests.create_package(data)
    response = response.json()
    return str(response["track"])

def get_id_package():
    response = ApiRequests.create_package(data.CreatePackagedata)
    response = response.json()
    trackvalue= response["track"]
    getidresponse= ApiRequests.getpackageByNumber(trackvalue)
    getidresponse = getidresponse.json()
    return str(getidresponse["order"]["id"])
def get_id_package_manual(tracknumber):
    getidresponse= ApiRequests.getpackageByNumber(tracknumber)
    getidresponse = getidresponse.json()
    return str(getidresponse["order"]["id"])
def get_number_package_configurable(data):
    response = ApiRequests.create_package(data)
    response = response.json()
    trackvalue = response["track"]
    getidresponse = ApiRequests.getpackageByNumber(trackvalue)
    getidresponse = getidresponse.json()
    return str(getidresponse["order"]["id"])
# Crea un repartidor, incia sesión y guarda la respuesta para conseguir el campo "id". No encontré razon para hacer manual este ya qué no hay documentación sobre repartidores que no sea en la app.
def getnumberdelivery():
    ApiRequests.create_delivery(data.CreateDeliverydata)
    response=ApiRequests.login_delivery(data.LoginDeliverydata)
    response= response.json()
    value= response["id"]
    return str(value)
#Entrala pantalla de estado del pedido con un número track creado en el momento
def screen_package_state(driver):
    driver.get(data.UrlUrbanScooters)
    trackers.find_button_Estado_pedido(driver)
    track_number = helpers.get_track_number_package()
    trackers.find_input_enter_track_number(driver).send_keys(track_number)
    trackers.find_confirmation_track_button(driver)
#Entra la pantalla de estado del pedido con un número de pedido espécifico
def screen_package_state_manual(driver, track_number):
    driver.get(data.UrlUrbanScooters)
    trackers.find_button_Estado_pedido(driver)
    trackers.find_input_enter_track_number(driver).send_keys(track_number)
    trackers.find_confirmation_track_button(driver)
#Crea y consigue el "id" del repartidor, "id" del paquete y acepta el paquete para luego ingresar a la página
def accept_package(driver):
    deliveryid = helpers.getnumberdelivery()
    package_tracknumber= helpers.get_track_number_package()
    get_package_id= helpers.get_id_package_manual(package_tracknumber)
    ApiRequests.accept_package_manual(get_package_id,deliveryid)
    screen_package_state_manual(driver, package_tracknumber)
def accept_package_manual_data(driver, data):
    track_number = helpers.get_track_number_package_manual(data)
    deliveryid = helpers.getnumberdelivery()
    get_package_id = helpers.get_id_package_manual(track_number)
    ApiRequests.accept_package_manual(get_package_id, deliveryid)
    helpers.screen_package_state_manual(driver, track_number)
#Crea un paquete y lo completa automáticamente
def complete_package(driver):
    track_number = helpers.get_track_number_package()
    get_package_id = helpers.get_id_package_manual(track_number)
    ApiRequests.complete_package_manual(get_package_id)
    helpers.screen_package_state_manual(driver, track_number)
#Le das un número de pedido que completa
def complete_package_manual(driver,data):
    track_number = helpers.get_track_number_package_manual(data)
    get_package_id = helpers.get_id_package_manual(track_number)
    ApiRequests.complete_package_manual(get_package_id)
    helpers.screen_package_state_manual(driver, track_number)
#Crea un pedido, acepta el pedido y consigue su número de trackeo y le consigue la "id", completa el pedido péro como se cambia de id lo busca nuevamente para completarlo por segunda vez y que ahora si se refleje en la página.
def mark_complete_package(driver):
    track_number = helpers.get_track_number_package()
    get_package_id = helpers.get_id_package_manual(track_number)
    ApiRequests.complete_package_manual(get_package_id)
    get_package_id = helpers.get_id_package_manual(track_number)
    ApiRequests.complete_package_manual(get_package_id)
    helpers.screen_package_state_manual(driver, track_number)
#Lo mismo que el automatico peró con un número de pedido que quieras
def mark_complete_package_manual(driver,data):
    deliveryid = helpers.getnumberdelivery()
    track_number = helpers.get_track_number_package_manual(data)
    get_package_id = helpers.get_id_package_manual(track_number)
    ApiRequests.accept_package_manual(get_package_id, deliveryid)
    get_package_id = helpers.get_id_package_manual(track_number)
    ApiRequests.complete_package_manual(get_package_id)
    get_package_id = helpers.get_id_package_manual(track_number)
    ApiRequests.complete_package_manual(get_package_id)
    helpers.screen_package_state_manual(driver, track_number)

#Pagina del formulario
def enter_request_a_package(driver):
    enterpage(driver)
    trackers.find_pedir_button(driver).click()
#Hace click en el input y agarra la estación de metro del paquete de creación de pedidos para buscarla de la lista dinamica y seleccionarla
def request_a_package_select_metro_station(driver):
    trackers.find_request_a_package_metro_station_input(driver).click()
    trackers.find_request_a_package_metro_station_list_options(driver)
    select_station= trackers.find_request_a_package_select_metro_from_list(driver)
    select_station.click()
    return trackers.find_request_a_package_metro_station_input(driver)
def request_a_package_select_metro_station_manual(driver, data):
    trackers.find_request_a_package_metro_station_input(driver).click()
    list_of_stations= trackers.find_request_a_package_metro_station_list_options(driver)
    select_station= list_of_stations.find_element(*trackers.find_request_a_package_select_metro_from_list_manual(driver, data))
    select_station.click()
    return trackers.find_request_a_package_metro_station_input(driver)
#Rellena toda la primera parte del formulario
def fill_request_a_package_inputs(driver):
    enter_request_a_package(driver)
    trackers.find_request_a_package_name_input(driver).send_keys(data.CreatePackagedata["firstName"])
    trackers.find_request_a_package_last_name_input(driver).send_keys(data.CreatePackagedata["lastName"])
    trackers.find_request_a_package_address_input(driver).send_keys(data.CreatePackagedata["address"])
    helpers.request_a_package_select_metro_station(driver)
    trackers.find_request_a_package_phone_input(driver).send_keys(data.CreatePackagedata["phone"])

#Rellena pero con un paquete de datos que se le otorgue
def fill_request_a_package_manual(driver, package_data):
    enter_request_a_package(driver)
    trackers.find_request_a_package_name_input(driver).send_keys(package_data["firstName"])
    trackers.find_request_a_package_last_name_input(driver).send_keys(package_data["lastName"])
    trackers.find_request_a_package_address_input(driver).send_keys(package_data["address"])
    trackers.find_request_a_package_metro_station_input(driver).send_keys(package_data["metroStation"])
    trackers.find_request_a_package_phone_input(driver).send_keys(package_data["phone"])
#Rellena la segunda parte del formulario
def fill_request_a_package_second_part(driver):
    trackers.find_request_a_package_delivery_date(driver).send_keys(data.CreatePackagedata["deliveryDate"])
    trackers.find_request_a_package_delivery_date(driver).send_keys(Keys.ENTER)
    trackers.find_request_a_package_rent_time_input(driver).click()
    trackers.find_request_a_package_rent_time(driver).click()
    trackers.find_request_a_package_scooter_color(driver)
    trackers.find_request_a_package_comment_input(driver).send_keys(data.CreatePackagedata["comment"])
def fill_request_a_package_second_part_manual(driver,package_data):
    trackers.find_request_a_package_delivery_date(driver).send_keys(package_data["deliveryDate"])
    trackers.find_request_a_package_delivery_date(driver).send_keys(Keys.ENTER)
    trackers.find_request_a_package_rent_time_input(driver).click()
    trackers.find_request_a_package_rent_time_manual(driver, package_data["rentTime"]).click()
    trackers.find_request_a_package_scooter_color_manual(driver, package_data["color"])
    trackers.find_request_a_package_comment_input(driver).send_keys(package_data["comment"])
#Cambia el formato de la fecha que des
def transform_date_formato_to_daymonthyear(date_got):
    date_get_format= datetime.strptime(date_got, "%Y-%m-%d")
    date_with_new_format= date_get_format.strftime("%d.%m.%Y")
    return date_with_new_format










