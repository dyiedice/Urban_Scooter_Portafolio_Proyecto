import locale
import copy
import data
from datetime import date, timedelta
#Links que se deben actualizar para hacer funcionar el codigo
UrlUrbanScooters= "https://cnt-a074221d-374b-46cf-a438-38f65546e491.containerhub.tripleten-services.com?lng=es"
UrlpruebasApi = "https://cnt-a074221d-374b-46cf-a438-38f65546e491.containerhub.tripleten-services.com"


#Variables que use para crear los distintos pedidos sin tener que cambiar los datos manualmente
tomorrow= date.today()+ timedelta(days=1)
into_7days= date.today() + timedelta(days=7)
before_10_days= date.today() - timedelta(days=10)
#Esto es para que tenga el mismo formato que debe llevar, asi tambien se pueden mandar solicitudes API y es compatible con el resto del codigo
tomorrow= tomorrow.strftime("%Y-%m-%d")
into_7days= into_7days.strftime("%Y-%m-%d")
before_10_days= before_10_days.strftime("%Y-%m-%d")

#Bases que se usan para crear y logearse
CreatePackagedata= {
    "firstName": "Yasuo",
    "lastName": "Yone",
    "address": "Ionia, mount 132",
    "metroStation": 4,
    "phone": "32323323223",
    "rentTime": 5,
    "deliveryDate": "2026-8-12",
    "comment": "Yas dont stab your brother",
    "color": [
        "BLACK"
    ]
}

CreateDeliverydata= {
    "login": "KatarinaD",
    "password": "1234",
    "firstName": "Katarina Du coteu tiene novio y se llama garen"
}
LoginDeliverydata= {
    "login": "KatarinaD",
    "password": "1234"
}
#Dato de prueba
inexistantpackagecode="333333"
#Variable dinámica
complete_package_id_data= {
    "id": None
}
#Diccionarios para traducir código
rent_time_numbers_to_days={
    1: "un día",
    2: "dos días",
    3: "tres días",
    4: "cuatro días",
    5: "cinco días",
    6: "seis días",
    7: "siete días"
}
scooter_color_english_to_spanish={
    "BLACK": "negro",
    "GREY": "gris"
}

metro_stations_number_to_name = {
    1: "1st Street",
    2: "5th Street",
    3: "7th Street/Metro Center",
    4: "7th Street/Metro Center",
    5: "7th Street/Metro Center",
    6: "7th Street/Metro Center",
    7: "17th Street/Santa Monica College",
    8: "26th Street/Bergamot",
    9: "103rd Street/Watts Towers",
    10: "Allen",
    11: "Anaheim Street",
    12: "APU/Citrus College**",
    13: "Arcadia",
    14: "Artesia",
    15: "Atlantic**",
    16: "Avalon",
    17: "Aviation/LAX",
    18: "Azusa Downtown",
    19: "Chinatown",
    20: "Civic Center/Grand Park",
    21: "Civic Center/Grand Park",
    22: "Compton",
    23: "Crenshaw",
    24: "Culver City",
    25: "Del Amo",
    26: "Del Mar",
    27: "Douglas",
    28: "Downtown Inglewood",
    29: "Downtown Long Beach**",
    30: "Downtown Santa Monica**",
    31: "Duarte/City of Hope",
    32: "East LA Civic Center",
    33: "El Segundo",
    34: "Expo/Bundy",
    35: "Expo/Crenshaw",
    36: "Expo/Crenshaw",
    37: "Expo/La Brea",
    38: "Expo/Sepulveda",
    39: "Expo/Vermont",
    40: "Expo/Western",
    41: "Expo Park/USC",
    42: "Fairview Heights",
    43: "Farmdale",
    44: "Fillmore",
    45: "Firestone",
    46: "Florence",
    47: "Grand/LATTC",
    48: "Harbor Freeway",
    49: "Hawthorne/Lennox",
    50: "Heritage Square",
    51: "Highland Park",
    52: "Hollywood/Highland",
    53: "Hollywood/Vine",
    54: "Hollywood/Western",
    55: "Hyde Park",
    56: "Indiana",
    57: "Irwindale",
    58: "Jefferson/USC",
    59: "La Cienega/Jefferson",
    60: "Lake",
    61: "Lakewood Boulevard",
    62: "LATTC/Ortho Institute",
    63: "Leimert Park",
    64: "Lincoln/Cypress",
    65: "Little Tokyo/Arts District",
    66: "Long Beach Boulevard",
    67: "Maravilla",
    68: "Mariachi Plaza",
    69: "Mariposa",
    70: "Martin Luther King Jr.",
    71: "Memorial Park",
    72: "Monrovia",
    73: "North Hollywood**",
    74: "Norwalk**",
    75: "Pacific Avenue",
    76: "Pacific Coast Highway",
    77: "Palms",
    78: "Pershing Square",
    79: "Pershing Square",
    80: "Pico*",
    81: "Pico*",
    82: "Pico/Aliso",
    83: "Redondo Beach**",
    84: "San Pedro",
    85: "Sierra Madre Villa",
    86: "Slauson",
    87: "Soto",
    88: "South Pasadena",
    89: "Southwest Museum",
    90: "Union Station",
    91: "Union Station",
    92: "Union Station",
    93: "Universal City/Studio City",
    94: "Vermont/Athens",
    95: "Vermont/Beverly",
    96: "Vermont/Santa Monica",
    97: "Vermont/Sunset",
    98: "Vernon",
    99: "Wardlow",
    100: "Washington",
    101: "Westchester/Veterans**",
    102: "Westlake/MacArthur Park",
    103: "Westlake/MacArthur Park",
    104: "Westwood/Rancho Park",
    105: "Willow Street",
    106: "Willowbrook/Rosa Parks*",
    107: "Willowbrook/Rosa Parks*",
    108: "Wilshire/Normandie",
    109: "Wilshire/Vermont*",
    110: "Wilshire/Vermont*",
    111: "Wilshire/Western**",
}


#Copia la base de creación de pedidos y solo cambia cosas puntuales para crear las pruebas
package_1day_to_delivery=copy.copy(data.CreatePackagedata)
package_1day_to_delivery["deliveryDate"]= tomorrow

package_7day_to_delivery= copy.copy(data.CreatePackagedata)
package_7day_to_delivery["deliveryDate"]= into_7days

package_10daybefore_to_delivery= copy.copy(data.CreatePackagedata)
package_10daybefore_to_delivery["deliveryDate"]= before_10_days

package_manual_metroStation= copy.copy(data.CreatePackagedata)

#Paquetes de datos que usan en las pruebas de clases de equivalencia
name_limit_1_character_comprobation=copy.copy(data.CreatePackagedata)
name_limit_1_character_comprobation["firstName"]= "a"
name_limit_2_character_comprobation=copy.copy(data.CreatePackagedata)
name_limit_2_character_comprobation["firstName"]= "aa"
name_limit_15_character_comprobation=copy.copy(data.CreatePackagedata)
name_limit_15_character_comprobation["firstName"]= "Samantha Ugarte"
name_limit_16_character_comprobation=copy.copy(data.CreatePackagedata)
name_limit_16_character_comprobation["firstName"]= "Samantha Ugartes"

name_characterType_latin_characters_comprobation= copy.copy(data.CreatePackagedata)
name_characterType_latin_characters_comprobation["firstName"]= "Samsung"
name_characterType_numbers_comprobation= copy.copy(data.CreatePackagedata)
name_characterType_numbers_comprobation["firstName"]= "12334"
name_characterType_latin_with_spaces_comprobation= copy.copy(data.CreatePackagedata)
name_characterType_latin_with_spaces_comprobation["firstName"]= "Sam sung"
name_characterType_latin_with_hyphen_comprobation= copy.copy(data.CreatePackagedata)
name_characterType_latin_with_hyphen_comprobation["firstName"]= "Sam- sung"
name_characterType_simbols_comprobation= copy.copy(data.CreatePackagedata)
name_characterType_simbols_comprobation["firstName"]= "#$$#%"
name_comprobation_void_data= copy.copy(data.CreatePackagedata)
name_comprobation_void_data["firstName"]= ""

lastName_limit_1_character_comprobation=copy.copy(data.CreatePackagedata)
lastName_limit_1_character_comprobation["lastName"]= "a"
lastName_limit_2_character_comprobation=copy.copy(data.CreatePackagedata)
lastName_limit_2_character_comprobation["lastName"]= "aa"
lastName_limit_15_character_comprobation=copy.copy(data.CreatePackagedata)
lastName_limit_15_character_comprobation["lastName"]= "Samantha Ugarte"
lastName_limit_16_character_comprobation=copy.copy(data.CreatePackagedata)
lastName_limit_16_character_comprobation["lastName"]= "Samantha Ugartes"

lastName_characterType_latin_characters_comprobation= copy.copy(data.CreatePackagedata)
lastName_characterType_latin_characters_comprobation["lastName"]= "Samsung"
lastName_characterType_numbers_comprobation= copy.copy(data.CreatePackagedata)
lastName_characterType_numbers_comprobation["lastName"]= "12334"
lastName_characterType_latin_with_spaces_comprobation= copy.copy(data.CreatePackagedata)
lastName_characterType_latin_with_spaces_comprobation["lastName"]= "Sam sung"
lastName_characterType_latin_with_hyphen_comprobation= copy.copy(data.CreatePackagedata)
lastName_characterType_latin_with_hyphen_comprobation["lastName"]= "Sam- sung"
lastName_characterType_simbols_comprobation= copy.copy(data.CreatePackagedata)
lastName_characterType_simbols_comprobation["lastName"]= "#$$#%"
lastName_comprobation_void_data= copy.copy(data.CreatePackagedata)
lastName_comprobation_void_data["lastName"]= ""

address_limit_4_character_comprobation= copy.copy(data.CreatePackagedata)
address_limit_4_character_comprobation["address"]= "Lisa"
address_limit_5_character_comprobation= copy.copy(data.CreatePackagedata)
address_limit_5_character_comprobation["address"]= "Lissa"
address_limit_50_character_comprobation= copy.copy(data.CreatePackagedata)
address_limit_50_character_comprobation["address"]= "Polish your writing with suggestions that help you"
address_limit_51_character_comprobation= copy.copy(data.CreatePackagedata)
address_limit_51_character_comprobation["address"]= "Polish your writing with suggestions that helps you"

address_characterType_latin_characters_comprobation= copy.copy(data.CreatePackagedata)
address_characterType_latin_characters_comprobation["address"]= "Ecatepec"
address_characterType_number_characters_comprobation= copy.copy(data.CreatePackagedata)
address_characterType_number_characters_comprobation["address"]= "90889"
address_characterType_latin_and_space_characters_comprobation= copy.copy(data.CreatePackagedata)
address_characterType_latin_and_space_characters_comprobation["address"]= "Ecate peor"
address_characterType_latin_and_hyphen_characters_comprobation= copy.copy(data.CreatePackagedata)
address_characterType_latin_and_hyphen_characters_comprobation["address"]= "Ecate-peor"
address_characterType_latin_and_dot_characters_comprobation= copy.copy(data.CreatePackagedata)
address_characterType_latin_and_dot_characters_comprobation["address"]= "Ecatepec.Assault"
address_characterType_latin_and_comma_characters_comprobation= copy.copy(data.CreatePackagedata)
address_characterType_latin_and_comma_characters_comprobation["address"]= "Ecatepec, Vecindario"
address_characterType_simbols_characters_comprobation= copy.copy(data.CreatePackagedata)
address_characterType_simbols_characters_comprobation["address"]= "#$$#%"
address_comprobation_void_data= copy.copy(data.CreatePackagedata)
address_comprobation_void_data["address"]= ""

phone_limit_9_character_comprobation= copy.copy(data.CreatePackagedata)
phone_limit_9_character_comprobation["phone"]= "263738383"
phone_limit_10_character_comprobation= copy.copy(data.CreatePackagedata)
phone_limit_10_character_comprobation["phone"]= "2637383838"
phone_limit_12_character_comprobation= copy.copy(data.CreatePackagedata)
phone_limit_12_character_comprobation["phone"]= "263738383343"
phone_limit_13_character_comprobation= copy.copy(data.CreatePackagedata)
phone_limit_13_character_comprobation["phone"]= "2637383833433"
phone_characterType_number_characters_comprobation= copy.copy(data.CreatePackagedata)
phone_characterType_number_characters_comprobation["phone"]= "26373838384"
phone_characterType_simbol_plus_characters_comprobation= copy.copy(data.CreatePackagedata)
phone_characterType_simbol_plus_characters_comprobation["phone"]= "++++++++++"
phone_characterType_latin_characters_comprobation= copy.copy(data.CreatePackagedata)
phone_characterType_latin_characters_comprobation["phone"]= "Katarinaisa"
phone_comprobation_void_data= copy.copy(data.CreatePackagedata)
phone_comprobation_void_data["phone"]= ""

#Mensajes de error
request_a_package_firstName_message_error= "Introduce un nombre correcto"
request_a_package_lastName_message_error= "Introduce un apellido correcto"
request_a_package_address_message_error= "Introduce una dirección válida"
request_a_package_phone_message_error= "Introduce un número válido"

#Creo un tiempo local en español para que los meses se pasen a español para verificar que salga asi cuando se completa un pedido
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
renttime_generic=data.CreatePackagedata["rentTime"]

#Texto que debe concordar con la fecha del paquete se creo
fecha_renta= date.today()+ timedelta(days=renttime_generic)
fecha_renta= fecha_renta.strftime(" %d de %B")
renttime_1dayafter=data.package_1day_to_delivery["rentTime"]
rent_date_1dayafter= date.today()+ timedelta(days=renttime_1dayafter)
rent_date_1dayafter= rent_date_1dayafter.strftime(" %d de %B")

renttime_7dayafter=data.package_7day_to_delivery["rentTime"]
rent_date_7dayafter= date.today()+ timedelta(days=renttime_7dayafter)
rent_date_7dayafter= rent_date_7dayafter.strftime(" %d de %B")

renttime_10daybefore=data.package_7day_to_delivery["rentTime"]
rent_date_10daybefore= date.today()+ timedelta(days=renttime_10daybefore)
rent_date_10daybefore= rent_date_10daybefore.strftime(" %d de %B")



#Rutas de solicitudes API
postCreateDelivery= "/api/v1/courier"
postCreatePackage= "/api/v1/orders"
postLoginDelivery= "/api/v1/courier/login"
DeleteDelivery= "/api/v1/courier/:id"
putAcceptPackage= "/api/v1/orders/accept/"
putCancelPackage= "/api/v1/orders/cancel"
putCompletePackage= "/api/v1/orders/finish/"
getPackageByNumber="/api/v1/orders/track?t="
getListPackagesByDelivery="/api/v1/orders?courierId=1"
getListPackagesByNearMetro="/api/v1/orders?courierId=1&nearestStation=[1, 2]"
getListPackagesAvailable="/api/v1/orders?courierId=1"
getListAvailablePackagesByNearMetro="/api/v1/orders?limit=10&page=0&nearestStation=[110]"
headers={ "Content-Type": "application/json", }

#Datos usados para validar que se muestren asi en las pruebas
active_first_status_first_text= "El scooter está en el almacén"
active_first_status_first_subtext= "El servicio de entrega lo recogerá pronto"
active_first_status_second_text= "El repartidor o repartidora está en camino"
active_first_status_second_subtext= "Llama al número: 0101"
active_first_status_third_text= "El servicio de entrega llegó"
active_first_status_third_subtext= "Recoge el scooter y paga la cuota de alquiler"
active_first_status_fourth_text= "Bien, vamos a dar un paseo"
active_first_status_fourth_subtext= "Hasta que termine el periodo de alquiler"

active_second_status_first_text= "El scooter está en el almacén"
active_second_status_first_subtext= "El servicio de entrega lo recogerá pronto"
active_second_status_second_text=  "El repartidor o repartidora "+ data.CreateDeliverydata["firstName"]+ " esta en camino"
active_second_status_second_subtext= "Llama al número: 0101"
active_second_status_third_text= "El servicio de entrega llegó"
active_second_status_third_subtext= "Recoge el scooter y paga la cuota de alquiler"
active_second_status_fourth_text= "Bien, vamos a dar un paseo"
active_second_status_fourth_subtext=  "Hasta que termine el periodo de alquiler"

active_third_status_first_text= "El scooter está en el almacén"
active_third_status_first_subtext= "El servicio de entrega lo recogerá pronto"
active_third_status_second_text=  "El repartidor o repartidora "+ data.CreateDeliverydata["firstName"]+ " esta en camino"
active_third_status_second_subtext= "Llama al número: 0101"
active_third_status_third_text= "El servicio de entrega llegó"
active_third_status_third_subtext= "Recoge el scooter y paga la cuota de alquiler"
active_third_status_fourth_text= "Bien, vamos a dar un paseo"
active_third_status_fourth_subtext=  "Hasta que termine el periodo de alquiler"

active_fourth_status_first_text= "El scooter está en el almacén"
active_fourth_status_first_subtext= "El servicio de entrega lo recogerá pronto"
active_fourth_status_second_text=  "El repartidor o repartidora "+ data.CreateDeliverydata["firstName"]+ " esta en camino"
active_fourth_status_second_subtext= "Llama al número: 0101"
active_fourth_status_third_text= "El servicio de entrega llegó"
active_fourth_status_third_subtext= "Recoge el scooter y paga la cuota de alquiler"
active_fourth_status_fourth_text= "Bien, vamos a dar un paseo"
active_fourth_status_fourth_subtext=  "Hasta que termine el periodo de alquiler" + fecha_renta +" a las 20:30"

#Por si quiero probar el cambiar el tiempo de renta que lo tome del paquete que se está tomando para la prueba y no uno génerico
active_fourth_status_fourth_subtext_1day_after=  "Hasta que termine el periodo de alquiler" + rent_date_1dayafter+" a las 20:30"
active_fourth_status_fourth_subtext_7day_after=  "Hasta que termine el periodo de alquiler" + rent_date_7dayafter+" a las 20:30"


active_second_status_delivery10daysbefore_first_text= "El scooter está en el almacén"
active_second_status_delivery10daysbefore_first_subtext= "El servicio de entrega lo recogerá pronto"
active_second_status_delivery10daysbefore_second_text=  "El repartidor o repartidora se demoró"
active_second_status_delivery10daysbefore_second_subtext= "No podremos entregar el scooter a tiempo. Para aclarar el estado de su pedido, llame a soporte: 0101"
active_second_status_delivery10daysbefore_third_text= "El servicio de entrega llegó"
active_second_status_delivery10daysbefore_third_subtext= "Recoge el scooter y paga la cuota de alquiler"
active_second_status_delivery10daysbefore_fourth_text= "Bien, vamos a dar un paseo"
active_second_status_delivery10daysbefore_fourth_subtext=  "Hasta que termine el periodo de alquiler"

active_fourth_status_delivery10daysbefore_first_text= "El scooter está en el almacén"
active_fourth_status_delivery10daysbefore_first_subtext= "El servicio de entrega lo recogerá pronto"
active_fourth_status_delivery10daysbefore_second_text=  "El repartidor o repartidora "+ data.CreateDeliverydata["firstName"]+ " esta en camino"
active_fourth_status_delivery10daysbefore_second_subtext= "Llama al número: 0101"
active_fourth_status_delivery10daysbefore_third_text= "El servicio de entrega llegó"
active_fourth_status_delivery10daysbefore_third_subtext= "Recoge el scooter y paga la cuota de alquiler"
active_fourth_status_delivery10daysbefore_fourth_text= "Bien, vamos a dar un paseo"
active_fourth_status_delivery10daysbefore_fourth_subtext=  "Hasta que termine el periodo de alquiler" + rent_date_10daybefore +" a las 20:30"