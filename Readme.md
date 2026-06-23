# Descripción del proyecto
### Este fue un proyecto que fue pensado para ir al portafolio, originalmente iban a ser muchas menos pruebas pero entre jugar lo que tenia construido, curiosidad y practica terminarón siendo 138 tests automatizados.
### Si quieres leer lo mas importante o mas relevente te invito a que lo léas directamente desde mi portafolio de Notion, donde resumi lo que realice y agregue videos para corroborar el funciomiento. 
### 
# Como correrlo
### Aunque lamentablemente no pueda automatizar esta parte por que estoy usando el entorno de Tripleten para las pruebas. Requiero encender el server  y que me de los links, puedo crear un codigo que devuelva dichos datos para que lo corras pero la factura de la electricidad por dejar la computadora encendida todo el día no se paga sola, así que si puedes mandame mensaje y te paso ambos links.
## Primero cambia los links en data.py 
## Segundo instala pytest y selenium.
## Tercero ejecuta el test que requieras.
# Archivos
## data, Encargado de guardar los datos que se ejecutaran en los demás archivos
## searchers, encargado de los localizadores y funciones que buscan elementos dentro de la página.
## ApiRequests, Encargado de la construcción de solicitudes API 
## helpers, Usa las funciones de todos los demas archivos para construir codigo reutilizable que facilita la lectura de los test y disminuye la cantidad de líneas de los mismos. 
## Main, Archivo cuyo unico proposito es ejecutar los tests. 

