from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import ApiRequests
import data
import helpers
from searchers import trackers


class TestUrbanScooter:

    @classmethod
    def setup_class(cls):
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )


    #Pruebas para verificar las solicitudes API
    def test_create_package(self):
        response= ApiRequests.create_package(data.CreatePackagedata)
        assert response.status_code == 201
    def test_create_delivery(self):
        response= ApiRequests.create_delivery(data.CreateDeliverydata)
        assert response.status_code == 201
    def test_accept_package(self):
        #como por cada paquete requiero su número de paquete requiero automatizarlo para no configurarlo manualmente
        response_create_package= ApiRequests.accept_package_automated()
        assert response_create_package.status_code == 200

    #Ahora sí las pruebas, iniciare con algunas sencillas como la entrada a la pagina y visibilidad de botones
    def test_enter_package_state(self):
        helpers.screen_package_state(self.driver)
        #verifico que aparezca el contenedor de la información del paquete
        container_info_package= trackers.find_container_package_info(self.driver)
        assert container_info_package.is_displayed()
    #verifico el input para cambiar de número sea visible
    def test_visibility_tracknumber_package_state(self):
        helpers.screen_package_state(self.driver)
        track_number_input= trackers.find_package_state_number_track_input(self.driver)
        assert track_number_input.is_displayed()
    #Verificar que se pueda cambiar el pedido trackeado
    def test_change_tracked_number(self):
        helpers.screen_package_state(self.driver)
        input_track_number= trackers.find_package_state_number_track_input(self.driver)
        #el .clear() no funciono asi que tuve que seleccionar todo y borrar
        input_track_number.send_keys(Keys.CONTROL+ "a")
        input_track_number.send_keys(Keys.DELETE)

        new_track_number= helpers.get_track_number_package()
        input_track_number.send_keys(new_track_number)

        confirmation_button= trackers.find_package_confirmation_newtrack_button(self.driver)
        confirmation_button.click()

        actual_track_number= input_track_number.get_attribute("value")
        assert actual_track_number == new_track_number
    #salta el mensaje de pedido no encontrado si ingresas un número de pedido no valído
    def test_wrong_track_number(self):
        helpers.screen_package_state_manual(self.driver, data.inexistantpackagecode)
        track_not_found_message= trackers.find_package_track_not_found(self.driver)
        assert track_not_found_message.is_displayed()

    #visibilidad de la cadena de estados
    def test_state_chain_visibility(self):
        helpers.screen_package_state(self.driver)
        state_chain=trackers.find_states_chain(self.driver)
        assert state_chain.is_displayed()

    #Prueba que deberia salir positiva pero se que saldra negativa. Consiste en revisar el texto que salta al elegir un paquete con una fecha de 1 día.
    def test_1day_first_status_text(self):
        track_number = helpers.get_track_number_package_manual(data.package_1day_to_delivery)
        helpers.screen_package_state_manual(self.driver,track_number)
        first_state_text= trackers.find_package_state_first_state(self.driver).text
        assert first_state_text == data.active_first_status_first_text

    #este tambien debe de fallar en el estado que esta la pagina pero esta pensado para salir postivo basado en los diseños de figma
    def test_1daydelivery_first_status_subtext(self):
        track_number = helpers.get_track_number_package_manual(data.package_1day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_subtext= trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext== data.active_first_status_first_subtext
    #es comprobar el diseño de las otras partes de la cadena de estados sin haberlo cambiado estas 2 salen postivas, cree un index para facilitarme la vida al crear estas partes
    def test_1daydelivery_second_status_text(self):
        track_number = helpers.get_track_number_package_manual(data.package_1day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text= trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_first_status_first_text
    def test_1daydelivery_second_status_subtext(self):
        track_number = helpers.get_track_number_package_manual(data.package_1day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text= trackers.find_package_second_state_subtext(self.driver).text
        assert state_text == data.active_first_status_second_subtext
    def test_1daydelivery_third_status_text(self):
        track_number = helpers.get_track_number_package_manual(data.package_1day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_first_status_third_text
    def test_1daydelivery_third_status_subtext(self):
        track_number = helpers.get_track_number_package_manual(data.package_1day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_first_status_third_subtext
    def test_1daydelivery_fourth_status_text(self):
        track_number = helpers.get_track_number_package_manual(data.package_1day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_first_status_fourth_text
    def test_1daydelivery_fourth_status_subtext(self):
        track_number = helpers.get_track_number_package_manual(data.package_1day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text = trackers.find_package_fourth_state_subtext(self.driver).text
        assert state_text == data.active_first_status_fourth_subtext

#Utilice las solicitudes API para aceptar el pedido e hice que entrara en la pagina posteriori a aceptar el pedido para que se vea el estado deseado
    def test_accepted_package_1day_delivery_first_state_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_1day_to_delivery)
        first_state_text = trackers.find_package_state_first_state(self.driver).text
        assert first_state_text == data.active_second_status_first_text
    def test_accepted_package_1day_delivery_first_state_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_1day_to_delivery)
        state_subtext = trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext == data.active_second_status_first_subtext
    def test_accepted_package_1day_delivery_second_state_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_second_status_second_text
    def test_accepted_package_1daydelivery_second_state_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_1day_to_delivery)
        state_subtext = trackers.find_package_second_state_subtext(self.driver).text
        assert state_subtext == data.active_second_status_second_subtext
    def test_test_accepted_package_1daydelivery_third_status_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_second_status_third_text
    def test_test_accepted_package_1daydelivery_third_status_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_second_status_third_subtext
    def test_test_accepted_package_1daydelivery_fourth_status_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_second_status_fourth_text
    def test_test_accepted_package_1daydelivery_fourth_status_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_second_status_fourth_subtext


#El completar un pedido por primera vez no cambia nada asi que los resultados no se ven reflejados.
    def test_completed_package_1day_delivery_first_state_text(self):
        helpers.complete_package_manual(self.driver, data.package_1day_to_delivery)
        first_state_text = trackers.find_package_state_first_state(self.driver).text
        assert first_state_text == data.active_third_status_first_text
    def test_completed_package_1day_delivery_first_state_subtext(self):
        helpers.complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_subtext = trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext == data.active_third_status_first_subtext
    def test_completed_package_1day_delivery_second_state_text(self):
        helpers.complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_third_status_second_text
    def test_completed_package_1daydelivery_second_state_subtext(self):
        helpers.complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_subtext = trackers.find_package_second_state_subtext(self.driver).text
        assert state_subtext == data.active_third_status_second_subtext
    def test_completed_package_1daydelivery_third_status_text(self):
        helpers.complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_third_status_third_text
    def test_completed_package_1daydelivery_third_status_subtext(self):
        helpers.complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_third_status_third_subtext
    def test_completed_package_1daydelivery_fourth_status_text(self):
        helpers.complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_third_status_fourth_text
    def test_completed_package_1daydelivery_fourth_status_subtext(self):
        helpers.complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_third_status_fourth_subtext



#Para verdaderamente aceptar un pedido tienes que buscar su id nuevamente y volverlo a aceptar por segunda vez y ahora si se marca completado.
    def test_marked_completed_package_1day_delivery_first_state_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_1day_to_delivery)
        first_state_text = trackers.find_package_state_first_state(self.driver).text
        assert first_state_text == data.active_fourth_status_first_text
    def test_marked_completed_package_1day_delivery_first_state_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_subtext = trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext == data.active_fourth_status_first_subtext
    def test_marked_completed_package_1day_delivery_second_state_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_fourth_status_second_text
    def test_marked_completed_package_1daydelivery_second_state_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_subtext = trackers.find_package_second_state_subtext(self.driver).text
        assert state_subtext == data.active_fourth_status_second_subtext
    def test_marked_completed_package_1daydelivery_third_status_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_fourth_status_third_text
    def test_marked_completed_package_1daydelivery_third_status_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_fourth_status_third_subtext
    def test_marked_completed_package_1daydelivery_fourth_status_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_fourth_status_fourth_text
    def test_marked_completed_package_1daydelivery_fourth_status_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_1day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_fourth_status_fourth_subtext

 #El valor límite positivo superior son 7 días
    def test_7daydelivery_first_status_text(self):
        track_number = helpers.get_track_number_package_manual(data.package_7day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_subtext= trackers.find_package_state_first_state(self.driver).text
        assert state_subtext== data.active_first_status_first_text
    def test_7daydelivery_first_status_subtext(self):
        track_number = helpers.get_track_number_package_manual(data.package_7day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_subtext= trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext== data.active_first_status_first_subtext
    #es comprobar el diseño de las otras partes de la cadena de estados sin haberlo cambiado estas 2 salen postivas, cree un index para facilitarme la vida al crear estas partes
    def test_7daydelivery_second_status_text(self):
        track_number = helpers.get_track_number_package_manual(data.package_7day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text= trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_first_status_first_text
    def test_7daydelivery_second_status_subtext(self):
        track_number = helpers.get_track_number_package_manual(data.package_7day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text= trackers.find_package_second_state_subtext(self.driver).text
        assert state_text == data.active_first_status_second_subtext
    def test_7daydelivery_third_status_text(self):
        track_number = helpers.get_track_number_package_manual(data.package_7day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_first_status_third_text
    def test_7daydelivery_third_status_subtext(self):
        track_number = helpers.get_track_number_package_manual(data.package_7day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_first_status_third_subtext
    def test_7daydelivery_fourth_status_text(self):
        track_number = helpers.get_track_number_package_manual(data.package_7day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_first_status_fourth_text
    def test_7daydelivery_fourth_status_subtext(self):
        track_number = helpers.get_track_number_package_manual(data.package_7day_to_delivery)
        helpers.screen_package_state_manual(self.driver, track_number)
        state_text = trackers.find_package_fourth_state_subtext(self.driver).text
        assert state_text == data.active_first_status_fourth_subtext


    def test_accepted_package_7day_delivery_first_state_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_7day_to_delivery)
        first_state_text = trackers.find_package_state_first_state(self.driver).text
        assert first_state_text == data.active_second_status_first_text
    def test_accepted_package_7day_delivery_first_state_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_7day_to_delivery)
        state_subtext = trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext == data.active_second_status_first_subtext
    def test_accepted_package_7day_delivery_second_state_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_second_status_second_text
    def test_accepted_package_7daydelivery_second_state_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_7day_to_delivery)
        state_subtext = trackers.find_package_second_state_subtext(self.driver).text
        assert state_subtext == data.active_second_status_second_subtext

    def test_test_accepted_package_7daydelivery_third_status_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_second_status_third_text
    def test_test_accepted_package_7daydelivery_third_status_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_second_status_third_subtext

    def test_test_accepted_package_7daydelivery_fourth_status_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_second_status_fourth_text
    def test_test_accepted_package_7daydelivery_fourth_status_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_fourth_state_subtext(self.driver).text
        assert state_text == data.active_second_status_fourth_subtext



    def test_completed_package_7day_delivery_first_state_text(self):
        helpers.complete_package_manual(self.driver, data.package_7day_to_delivery)
        first_state_text = trackers.find_package_state_first_state(self.driver).text
        assert first_state_text == data.active_third_status_first_text
    def test_completed_package_7day_delivery_first_state_subtext(self):
        helpers.complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_subtext = trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext == data.active_third_status_first_subtext
    def test_completed_package_7day_delivery_second_state_text(self):
        helpers.complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_third_status_second_text
    def test_completed_package_7daydelivery_second_state_subtext(self):
        helpers.complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_subtext = trackers.find_package_second_state_subtext(self.driver).text
        assert state_subtext == data.active_third_status_second_subtext

    def test_completed_package_7daydelivery_third_status_text(self):
        helpers.complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_third_status_third_text
    def test_completed_package_7daydelivery_third_status_subtext(self):
        helpers.complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_third_status_third_subtext

    def test_completed_package_7daydelivery_fourth_status_text(self):
        helpers.complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_third_status_fourth_text
    def test_completed_package_7daydelivery_fourth_status_subtext(self):
        helpers.complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_fourth_status_fourth_subtext_1day_after


    def test_marked_completed_package_7day_delivery_first_state_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_7day_to_delivery)
        first_state_text = trackers.find_package_state_first_state(self.driver).text
        assert first_state_text == data.active_fourth_status_first_text
    def test_marked_completed_package_7day_delivery_first_state_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_subtext = trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext == data.active_fourth_status_first_subtext
    def test_marked_completed_package_7day_delivery_second_state_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_fourth_status_second_text
    def test_marked_completed_package_7daydelivery_second_state_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_subtext = trackers.find_package_second_state_subtext(self.driver).text
        assert state_subtext == data.active_fourth_status_second_subtext

    def test_marked_completed_package_7daydelivery_third_status_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_fourth_status_third_text
    def test_marked_completed_package_7daydelivery_third_status_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_fourth_status_third_subtext

    def test_marked_completed_package_7daydelivery_fourth_status_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_fourth_status_fourth_text
    def test_marked_completed_package_7daydelivery_fourth_status_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_7day_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_fourth_status_fourth_subtext_7day_after


#Prueba negativa considerando que se supone que solo se puede pedir a partir de un día después y solo probe cuando es aceptado el paquete por qué es el unico con diseño en figma con un paquete atrasado
    def test_accepted_package_10daysbeforedelivery_first_state_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_10daybefore_to_delivery)
        first_state_text = trackers.find_package_state_first_state(self.driver).text
        assert first_state_text == data.active_second_status_first_text
    def test_accepted_package_10daysbeforedelivery_first_state_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_10daybefore_to_delivery)
        state_subtext = trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext == data.active_second_status_first_subtext
    def test_accepted_package_10daysbeforedelivery_second_state_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_second_status_second_text
    def test_accepted_package_10daysbeforedelivery_second_state_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_10daybefore_to_delivery)
        state_subtext = trackers.find_package_second_state_subtext(self.driver).text
        assert state_subtext == data.active_second_status_second_subtext
    def test_accepted_package_10daysbeforedelivery_third_status_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_second_status_third_text
    def test_test_accepted_package_10daysbeforedelivery_third_status_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_second_status_third_subtext
    def test_accepted_package_10daysbeforedelivery_fourth_status_text(self):
        helpers.accept_package_manual_data(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_second_status_fourth_text
    def test_accepted_package_10daysbeforedelivery_fourth_status_subtext(self):
        helpers.accept_package_manual_data(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_second_status_fourth_subtext

#cuando un paquete atrasado es entregado se supone que inicia la cuenta de el tiempo de renta asi que vale la pena automatizar esto
    def test_marked_completed_package_10daysbefore_delivery_first_state_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_10daybefore_to_delivery)
        first_state_text = trackers.find_package_state_first_state(self.driver).text
        assert first_state_text == data.active_fourth_status_delivery10daysbefore_first_text
    def test_marked_completed_package_10daysbeforey_delivery_first_state_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_10daybefore_to_delivery)
        state_subtext = trackers.find_package_state_first_state_subtext(self.driver).text
        assert state_subtext == data.active_fourth_status_delivery10daysbefore_first_subtext
    def test_marked_completed_package_10daysbefore_delivery_second_state_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_second_state_text(self.driver).text
        assert state_text == data.active_fourth_status_delivery10daysbefore_second_text
    def test_marked_completed_package_10daysbeforedelivery_second_state_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_10daybefore_to_delivery)
        state_subtext = trackers.find_package_second_state_subtext(self.driver).text
        assert state_subtext == data.active_fourth_status_delivery10daysbefore_second_subtext
    def test_marked_completed_package_10daysbeforedelivery_third_status_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_third_state_text(self.driver).text
        assert state_text == data.active_fourth_status_delivery10daysbefore_third_text
    def test_marked_completed_package_10daysbeforedelivery_third_status_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_fourth_status_delivery10daysbefore_third_subtext
    def test_marked_completed_package_10daysbeforedelivery_fourth_status_text(self):
        helpers.mark_complete_package_manual(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_fourth_state_text(self.driver).text
        assert state_text == data.active_fourth_status_delivery10daysbefore_fourth_text
    def test_marked_completed_package_10daysbeforedelivery_fourth_status_subtext(self):
        helpers.mark_complete_package_manual(self.driver, data.package_10daybefore_to_delivery)
        state_text = trackers.find_package_third_state_subtext(self.driver).text
        assert state_text == data.active_fourth_status_delivery10daysbefore_fourth_subtext

#Pruebas de flujo
    #Rellena la primera parte del formulario que consiste en datos personales y lugar de entrega
    def test_fill_request_a_package_formulary(self):
        helpers.fill_request_a_package_inputs(self.driver)
        trackers.find_request_a_package_next_button(self.driver).click()
        rent_title= trackers.find_request_a_package_rent_title(self.driver)
        assert rent_title.text =="Alquiler"
    #Relleno de la segunda parte del formulario que consiste en detalles de la entrega y tiempo de renta
    def test_user_flow_happy_path_request_a_package(self):
        helpers.fill_request_a_package_inputs(self.driver)
        trackers.find_request_a_package_next_button(self.driver).click()
        helpers.fill_request_a_package_second_part(self.driver)
        confirmation_button= trackers.find_request_a_package_pedir_button(self.driver)
        confirmation_button.click()
#Pruebas de rellenar campos especificos para comprobar que se puedan rellenar individualmente
    def test_fill_request_a_package_name(self):
        helpers.enter_request_a_package(self.driver)
        name= trackers.find_request_a_package_name_input(self.driver)
        name.send_keys(data.CreatePackagedata["firstName"])
        assert name.get_attribute("value")== data.CreatePackagedata["firstName"]
    def test_fill_request_a_package_last_name(self):
        helpers.enter_request_a_package(self.driver)
        last_name= trackers.find_request_a_package_last_name_input(self.driver)
        last_name.send_keys(data.CreatePackagedata["lastName"])
        assert last_name.get_attribute("value")== data.CreatePackagedata["lastName"]
    def test_fill_request_a_package_address(self):
        helpers.enter_request_a_package(self.driver)
        address= trackers.find_request_a_package_address_input(self.driver)
        address.send_keys(data.CreatePackagedata["address"])
        assert address.get_attribute("value")== data.CreatePackagedata["address"]
    def test_fill_request_a_package_metro_station(self):
        helpers.enter_request_a_package(self.driver)
        metro_station= helpers.request_a_package_select_metro_station(self.driver)
        metro_station_number= data.CreatePackagedata["metroStation"]
        metro_station_name= data.metro_stations_number_to_name[metro_station_number]
        assert metro_station.get_attribute("value") == metro_station_name
    def test_fill_request_a_package_phone(self):
        helpers.enter_request_a_package(self.driver)
        phone= trackers.find_request_a_package_phone_input(self.driver)
        phone.send_keys(data.CreatePackagedata["phone"])
        assert phone.get_attribute("value")== data.CreatePackagedata["phone"]
    def test_fill_request_a_package_delivery_date(self):
        helpers.fill_request_a_package_inputs(self.driver)
        next_button= trackers.find_request_a_package_next_button(self.driver)
        next_button.click()
        delivery_date_input=trackers.find_request_a_package_delivery_date(self.driver)
        delivery_date_input.send_keys(data.CreatePackagedata["deliveryDate"])
        delivery_date_input.send_keys(Keys.ENTER)
        date= data.CreatePackagedata["deliveryDate"]
        date_with_format= helpers.transform_date_formato_to_daymonthyear(date)
        assert delivery_date_input.get_attribute("value") == date_with_format
    def test_fill_request_a_package_rent_time(self):
        helpers.fill_request_a_package_inputs(self.driver)
        next_button = trackers.find_request_a_package_next_button(self.driver)
        next_button.click()
        rent_time_input=trackers.find_request_a_package_rent_time_input(self.driver)
        rent_time_input.click()
        trackers.find_request_a_package_rent_time_manual(self.driver, data.CreatePackagedata["rentTime"]).click()
        get_day_text= data.rent_time_numbers_to_days[data.CreatePackagedata["rentTime"]]
        assert rent_time_input.text == get_day_text
    def test_fill_request_a_package_color(self):
        helpers.fill_request_a_package_inputs(self.driver)
        next_button = trackers.find_request_a_package_next_button(self.driver)
        next_button.click()
        color_choosed=trackers.find_request_a_package_scooter_color(self.driver)
        assert color_choosed.get_attribute("checked") == "true"

    def test_fill_request_a_package_comment(self):
        helpers.fill_request_a_package_inputs(self.driver)
        next_button = trackers.find_request_a_package_next_button(self.driver)
        next_button.click()
        comment= trackers.find_request_a_package_comment_input(self.driver)
        comment.send_keys(data.CreatePackagedata["comment"])
        assert comment.get_attribute("value")== data.CreatePackagedata["comment"]
    # Pruebas de campos del formulario pero mas centrada en clases de equivalencia considerando límites de caracteres y tipo de caracteres que se ingresan
     #Ingrese los mensajes de error y datos que se ingresaran en el apartado de data para centralizar todos los datos de pruebas.
    def test_negative_request_a_package_fill_firstName_with_1_character(self):
        helpers.enter_request_a_package(self.driver)
        first_name= trackers.find_request_a_package_name_input(self.driver)
        data_taken =data.name_limit_1_character_comprobation["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error= trackers.find_request_a_package_error_message_name_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_firstName_message_error

    def test_positive_request_a_package_fill_firstName_with_2_characters(self):
        helpers.enter_request_a_package(self.driver)
        first_name = trackers.find_request_a_package_name_input(self.driver)
        data_taken = data.name_limit_2_character_comprobation["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_positive_request_a_package_fill_firstName_with_15_characters(self):
        helpers.enter_request_a_package(self.driver)
        first_name = trackers.find_request_a_package_name_input(self.driver)
        data_taken = data.name_limit_15_character_comprobation["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_negative_request_a_package_fill_firstName_with_16_character(self):
        helpers.enter_request_a_package(self.driver)
        first_name= trackers.find_request_a_package_name_input(self.driver)
        data_taken =data.name_limit_16_character_comprobation["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error= trackers.find_request_a_package_error_message_name_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_firstName_message_error
    def test_positive_request_a_package_fill_firstName_with_latin_characters(self):
        helpers.enter_request_a_package(self.driver)
        first_name = trackers.find_request_a_package_name_input(self.driver)
        data_taken = data.name_characterType_latin_characters_comprobation["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_negative_request_a_package_fill_firstName_with_number_character(self):
        helpers.enter_request_a_package(self.driver)
        first_name = trackers.find_request_a_package_name_input(self.driver)
        data_taken = data.name_characterType_numbers_comprobation["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_name_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_firstName_message_error

    def test_positive_request_a_package_fill_firstName_with_latin_and_space_characters(self):
        helpers.enter_request_a_package(self.driver)
        first_name = trackers.find_request_a_package_name_input(self.driver)
        data_taken = data.name_characterType_latin_with_spaces_comprobation["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_positive_request_a_package_fill_firstName_with_latin_and_hyphen_characters(self):
        helpers.enter_request_a_package(self.driver)
        first_name = trackers.find_request_a_package_name_input(self.driver)
        data_taken = data.name_characterType_latin_with_hyphen_comprobation["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_negative_request_a_package_fill_firstName_with_simbols_characters(self):
        helpers.enter_request_a_package(self.driver)
        first_name = trackers.find_request_a_package_name_input(self.driver)
        data_taken = data.name_characterType_simbols_comprobation["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_name_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_firstName_message_error

    def test_negative_request_a_package_fill_firstName_void_data(self):
        helpers.enter_request_a_package(self.driver)
        first_name = trackers.find_request_a_package_name_input(self.driver)
        data_taken = data.name_comprobation_void_data["firstName"]
        first_name.send_keys(data_taken)
        first_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_name_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_firstName_message_error



    def test_negative_request_a_package_fill_lastName_with_1_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_limit_1_character_comprobation["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_lastName_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_lastName_message_error

    def test_positive_request_a_package_fill_lastName_with_2_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_limit_1_character_comprobation["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_last_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_positive_request_a_package_fill_lastName_with_15_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_limit_15_character_comprobation["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_last_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_negative_request_a_package_fill_lastName_with_16_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_limit_16_character_comprobation["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_lastName_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_lastName_message_error

    def test_positive_request_a_package_fill_lastName_with_latin_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_characterType_latin_characters_comprobation["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_last_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_negative_request_a_package_fill_lastName_with_number_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_characterType_numbers_comprobation["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_lastName_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_lastName_message_error

    def test_positive_request_a_package_fill_lastName_with_latin_and_space_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_characterType_latin_with_spaces_comprobation["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_last_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_positive_request_a_package_fill_lastName_with_latin_and_hyphen_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_characterType_latin_with_hyphen_comprobation["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_last_name_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_negative_request_a_package_fill_lastName_with_simbols_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_characterType_simbols_comprobation["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_lastName_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_lastName_message_error

    def test_negative_request_a_package_fill_lastName_void_data(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_last_name_input(self.driver)
        data_taken = data.lastName_comprobation_void_data["lastName"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_lastName_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_lastName_message_error
    def test_negative_request_a_package_fill_address_4_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_limit_4_character_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_address_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_address_message_error

    def test_positive_request_a_package_fill_address_5_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_limit_5_character_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_address_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_positive_request_a_package_fill_address_50_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_limit_50_character_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_address_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_negative_request_a_package_fill_address_51_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_limit_51_character_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_address_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_address_message_error
    def test_positive_request_a_package_fill_address_latin_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_characterType_latin_characters_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_address_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_positive_request_a_package_fill_address_number_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_characterType_number_characters_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_address_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_positive_request_a_package_fill_address_latin_with_hyphen_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_characterType_latin_and_hyphen_characters_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_address_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_positive_request_a_package_fill_address_latin_with_dot_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_characterType_latin_and_dot_characters_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_address_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_positive_request_a_package_fill_address_latin_with_comma_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_characterType_latin_and_comma_characters_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_address_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_negative_request_a_package_fill_address_simbol_characters(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_characterType_simbols_characters_comprobation["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_address_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_address_message_error
    def test_negative_request_a_package_fill_address_void_data(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_address_input(self.driver)
        data_taken = data.address_comprobation_void_data["address"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_address_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_address_message_error

    def test_negative_request_a_package_fill_phone_9_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_phone_input(self.driver)
        data_taken = data.phone_limit_9_character_comprobation["phone"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_phone_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_phone_message_error
    def test_positive_request_a_package_fill_phone_10_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_phone_input(self.driver)
        data_taken = data.phone_limit_10_character_comprobation["phone"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_phone_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_positive_request_a_package_fill_phone_12_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_phone_input(self.driver)
        data_taken = data.phone_limit_12_character_comprobation["phone"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_phone_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_positive_request_a_package_fill_phone_13_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_phone_input(self.driver)
        data_taken = data.phone_limit_13_character_comprobation["phone"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_phone_input(self.driver)
        assert not message_error_not_visible.is_displayed()

    def test_negative_request_a_package_fill_phone_13_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_phone_input(self.driver)
        data_taken = data.phone_limit_13_character_comprobation["phone"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_phone_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_phone_message_error

    def test_positive_request_a_package_fill_phone_number_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_phone_input(self.driver)
        data_taken = data.phone_characterType_number_characters_comprobation["phone"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error_not_visible = trackers.find_request_a_package_error_message_not_visible_phone_input(self.driver)
        assert not message_error_not_visible.is_displayed()
    def test_negative_request_a_package_fill_phone_simbol_plus_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_phone_input(self.driver)
        data_taken = data.phone_characterType_simbol_plus_characters_comprobation["phone"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_phone_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_phone_message_error
    def test_negative_request_a_package_fill_phone_latin_character(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_phone_input(self.driver)
        data_taken = data.phone_characterType_latin_characters_comprobation["phone"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_phone_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_phone_message_error
    def test_negative_request_a_package_fill_phone_void_datar(self):
        helpers.enter_request_a_package(self.driver)
        last_name = trackers.find_request_a_package_phone_input(self.driver)
        data_taken = data.phone_comprobation_void_data["phone"]
        last_name.send_keys(data_taken)
        last_name.send_keys(Keys.TAB)
        message_error = trackers.find_request_a_package_error_message_phone_input(self.driver)
        assert message_error.get_attribute("textContent") == data.request_a_package_phone_message_error


    def teardown_class(self):
        self.driver.quit()