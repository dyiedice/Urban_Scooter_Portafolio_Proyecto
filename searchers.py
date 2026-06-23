from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import data
#Es mas sencillo usar .trackers en otros archivos.
class trackers:
#Coloque todos los localizadores en la parte superior
    metroStation_standar= data.CreatePackagedata["metroStation"]
    home_button_Estado_pedido = (By.CLASS_NAME, "Header_Link__1TAG7")
    home_input_track_number = (By.CSS_SELECTOR, ".Input_InputContainer__3NykH input")
    home_confirmation_track_button = (By.CSS_SELECTOR, ".Button_Button__ra12g.Header_Button__28dPO")
    state_package_divTrackcontainer= (By.XPATH, "//div[@class='Track_OrderInfo__2fpDL']")
    state_package_track_number_input= (By.XPATH, "//input[@class='Input_Input__1iN_Z Track_Input__1g7lq Input_Filled__1rDxs Input_Responsible__1jDKN']")
    state_package_confirmation_newtrack_button= (By.XPATH, "//button[@class='Button_Button__ra12g Button_Middle__1CSJM']")
    state_package_track_not_found= (By.CLASS_NAME,"Track_NotFound__6oaoY")
    state_package_container_chain_states= (By.CLASS_NAME, "Track_OrderRoadmap__3eUiE")
    status_chain_class_mother = (By.XPATH,"//div[contains(@class,'Track_OrderBrick__1qXIA')]")
    state_package_state_text= (By.CLASS_NAME,"Track_Order__1S6E9")
    state_package_state_subtext= (By.CLASS_NAME, "Track_OrderDescription__1bRk8")

    home_page_pedir_button= (By.CLASS_NAME,"Button_Button__ra12g")
    request_a_package_name_input = (By.CSS_SELECTOR, "[placeholder='* Nombre']")
    request_a_package_last_name_input = (By.CSS_SELECTOR, "[placeholder='* Apellido']")
    request_a_package_address_input = (By.CSS_SELECTOR, "[placeholder='* Dirección: a dónde llevar el scooter']")
    request_a_package_metro_station_input = (By.CSS_SELECTOR, "[placeholder='* Estación de metro']")
    request_a_package_metro_statation_index_options= (By.XPATH, "//div[@class='select-search__select']")
    request_a_package_metro_station_select_option = (By.XPATH, f"//button[@value= '{metroStation_standar}']")
    def manual_request_a_package_metro_station_select_option(value):
        return (By.XPATH, f"//button[@value='{value}']")
    request_a_package_phone_input = (By.CSS_SELECTOR, "[placeholder='* Teléfono: el repartidor o repartidora te llamará']")
    request_a_package_input_of_metro_station= (By.CLASS_NAME,"select-search__input")
    request_a_package_next_button = (By.XPATH, "//button[contains(text(),'Siguiente')]")
    request_a_package_rent_title= (By.CLASS_NAME,"Order_Header__BZXOb")

    request_a_package_delivery_date= (By.CSS_SELECTOR, "[placeholder='* Fecha de entrega']")
    request_a_package_rent_time_input = (By.CLASS_NAME, "Dropdown-control")
    request_a_package_rent_time_list = (By.CLASS_NAME, "Dropdown-menu")
    def capture_request_a_package_rent_time(days):
        return (By.XPATH, f"//div[contains(text(),'{days}')]")
    def define_color_request_a_package_scooter_color(color):
        return (By.XPATH, f"//label[contains(text(),'{color}')]")
    request_a_package_comment_input= (By.CSS_SELECTOR, "[placeholder='Comentario']")
    request_a_package_pedir_button= (By.XPATH, "//button[contains(text(),'Pedir')]")
    request_a_package_to_whom_is_the_scooter_form= (By.CLASS_NAME, "Order_Form__17u6u")
    request_a_package_list_of_container_inputs= (By.XPATH, "//div[contains(@class,'Input_InputContainer__3NykH')]")
    request_a_package_error_message= (By.XPATH, ".//div[contains(@class,'Input_ErrorMessage__3HvIb') and contains(@class,'Input_Visible___syz6')]")
    request_a_package_error_message_not_visible = (By.XPATH, ".//div[contains(@class,'Input_ErrorMessage__3HvIb') and not(contains(@class,'Input_Visible___syz6'))]")
    request_a_package_error_message_metroStation= (By.CLASS_NAME, "Order_MetroError__1BtZb")




#Aqui coloque todas las funciones que solo devuelven los elementos Web que buscan los localizadores
    def find_button_Estado_pedido(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.home_button_Estado_pedido))
        driver.find_element(*trackers.home_button_Estado_pedido).click()

    def find_input_enter_track_number(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.home_input_track_number))
        return driver.find_element(*trackers.home_input_track_number)

    def find_confirmation_track_button(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.home_confirmation_track_button))
        driver.find_element(*trackers.home_confirmation_track_button).click()
    def find_container_package_info(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.state_package_divTrackcontainer))
        return driver.find_element(*trackers.state_package_divTrackcontainer)
    def find_package_state_number_track_input(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.state_package_track_number_input))
        return driver.find_element(*trackers.state_package_track_number_input)
    def find_package_confirmation_newtrack_button(driver):
        return driver.find_element(*trackers.state_package_confirmation_newtrack_button)
    def find_package_track_not_found(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.state_package_track_not_found))
        return driver.find_element(*trackers.state_package_track_not_found)
    def find_states_chain(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.state_package_container_chain_states))
        return driver.find_element(*trackers.state_package_container_chain_states)
#Si un nombre se repíte en toda una lista como en este caso de la cadena de estados. En vez de buscarlos por texto me parecio mejor crear un array y buscar por elementos encontrados en vez de por texto que además puede fallar si no está el texto esperado.
    def getchain_status(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.status_chain_class_mother))
        status = driver.find_elements(*trackers.status_chain_class_mother)
        return status

    def find_package_state_first_state(driver):
        state_chain = trackers.getchain_status(driver)
        state_chain = state_chain[0]
        texto = state_chain.find_element(*trackers.state_package_state_text)
        WebDriverWait(driver, 10).until(EC.visibility_of(texto))
        return texto
    def find_package_state_first_state_subtext(driver):
        state_chain = trackers.getchain_status(driver)
        state_chain = state_chain[0]
        texto = state_chain.find_element(*trackers.state_package_state_subtext)
        WebDriverWait(driver, 10).until(EC.visibility_of(texto))
        return texto
    def find_package_second_state_text(driver):
        state_chain = trackers.getchain_status(driver)
        state_chain = state_chain[1]
        texto = state_chain.find_element(*trackers.state_package_state_text)
        WebDriverWait(driver, 10).until(EC.visibility_of(texto))
        return texto
    def find_package_second_state_subtext(driver):
        state_chain = trackers.getchain_status(driver)
        state_chain = state_chain[1]
        texto = state_chain.find_element(*trackers.state_package_state_subtext)
        WebDriverWait(driver, 10).until(EC.visibility_of(texto))
        return texto
    def find_package_third_state_text(driver):
        state_chain = trackers.getchain_status(driver)
        state_chain = state_chain[2]
        texto = state_chain.find_element(*trackers.state_package_state_text)
        WebDriverWait(driver, 10).until(EC.visibility_of(texto))
        return texto
    def find_package_third_state_subtext(driver):
        state_chain = trackers.getchain_status(driver)
        state_chain = state_chain[2]
        texto = state_chain.find_element(*trackers.state_package_state_subtext)
        WebDriverWait(driver, 10).until(EC.visibility_of(texto))
        return texto
    def find_package_fourth_state_text(driver):
        state_chain = trackers.getchain_status(driver)
        state_chain = state_chain[3]
        texto = state_chain.find_element(*trackers.state_package_state_text)
        WebDriverWait(driver, 10).until(EC.visibility_of(texto))
        return texto
    def find_package_fourth_state_subtext(driver):
        state_chain = trackers.getchain_status(driver)
        state_chain = state_chain[3]
        texto = state_chain.find_element(*trackers.state_package_state_subtext)
        WebDriverWait(driver, 10).until(EC.visibility_of(texto))
        return texto
    def find_pedir_button(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.home_page_pedir_button))
        pedir_button= driver.find_element(*trackers.home_page_pedir_button)
        return pedir_button

    def get_input_array(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_array_inputs))
        list_inputs= driver.find_elements(*trackers.request_a_package_array_inputs)
        return list_inputs
    def find_request_a_package_name_input(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_name_input))
        name_input= driver.find_element(*trackers.request_a_package_name_input)
        return name_input
    def find_request_a_package_last_name_input(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_last_name_input))
        last_name_input = driver.find_element(*trackers.request_a_package_last_name_input)
        return last_name_input
    def find_request_a_package_address_input(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_address_input))
        address_input = driver.find_element(*trackers.request_a_package_address_input)
        return address_input
    def find_request_a_package_metro_station_input(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_metro_station_input))
        metro_searcher = driver.find_element(*trackers.request_a_package_metro_station_input)
        return metro_searcher
    def find_request_a_package_metro_station_list_options(driver):
        WebDriverWait(driver,10).until(EC.presence_of_element_located(trackers.request_a_package_metro_statation_index_options))
        list_stations= driver.find_element(*trackers.request_a_package_metro_statation_index_options)
        return list_stations
    def find_request_a_package_select_metro_from_list(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_metro_station_select_option))
        selected_station = driver.find_element(*trackers.request_a_package_metro_station_select_option)
        return selected_station
    def find_request_a_package_select_metro_from_list_manual(driver,metrovalue):
        locator= trackers.manual_request_a_package_metro_station_select_option(metrovalue)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
        selected_station = driver.find_element(*locator)
        return selected_station
    def find_request_a_package_phone_input(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_phone_input))
        phone = driver.find_element(*trackers.request_a_package_phone_input)
        return phone
    def find_request_a_package_next_button(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_next_button))
        next_button= driver.find_element(*trackers.request_a_package_next_button)
        return next_button
    def find_request_a_package_rent_title(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_rent_title))
        rent_title= driver.find_element(*trackers.request_a_package_rent_title)
        return rent_title
    def find_request_a_package_delivery_date(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_delivery_date))
        delivery_date= driver.find_element(*trackers.request_a_package_delivery_date)
        return delivery_date
    def find_request_a_package_rent_time_input(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_rent_time_input))
        rent_time_input= driver.find_element(*trackers.request_a_package_rent_time_input)
        return rent_time_input

    def find_request_a_package_rent_time(driver):
        rent_time= data.CreatePackagedata["rentTime"]
        text_days_rented = data.rent_time_numbers_to_days[rent_time]
        locator = trackers.capture_request_a_package_rent_time(text_days_rented)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
        rent_option= driver.find_element(*locator)
        return rent_option
    def find_request_a_package_rent_time_manual(driver, rent_time):
        days_rent_time = data.rent_time_numbers_to_days[rent_time]
        locator = trackers.capture_request_a_package_rent_time(days_rent_time)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
        rent_option= driver.find_element(*locator)
        return rent_option
  #El color no solo puede ser uno u otro si no que puede ser ambos asi que para cubrirlo en vez de crear un localizador especifico para cada uno y un if, preferi crear un localizador dínamico y un ciclo que ocupa menos lineas y es mas escalable ya que no ocupa actualizar el if si se agregan más colores
    def find_request_a_package_scooter_color(driver):
        for color in data.CreatePackagedata["color"]:
            color_selected = data.scooter_color_english_to_spanish[color]
            locator = trackers.define_color_request_a_package_scooter_color(color_selected)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
            driver.find_element(*locator).click()
            last_input = driver.find_element(By.ID, color.lower())
        return last_input
#Saca los colores de un paquete de datos que se le entregue
    def find_request_a_package_scooter_color_manual(driver, color_given):
        for color in color_given:
            color_selected = data.scooter_color_english_to_spanish[color]
            locator = trackers.define_color_request_a_package_scooter_color(color_selected)
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
            color_checked=driver.find_element(*locator)
            color_checked.click()

        return color_checked

    def find_request_a_package_comment_input(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_comment_input))
        comment_input= driver.find_element(*trackers.request_a_package_comment_input)
        return comment_input
    def find_request_a_package_pedir_button(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_pedir_button))
        pedir_button=driver.find_element(*trackers.request_a_package_pedir_button)
        return pedir_button
#Lo mismo crea una lista donde se buscan los inputs y dentro de ellos están los errores apartir de aqui es mas sencillo verificar si son visibles o no por sus atributos y textos de clase
    def get_request_a_package_error_message_list(driver):
        WebDriverWait(driver,10 ).until(EC.visibility_of_element_located(trackers.request_a_package_to_whom_is_the_scooter_form))
        list_of_message_errors = driver.find_elements(*trackers.request_a_package_list_of_container_inputs)
        return list_of_message_errors

    def find_request_a_package_error_message_name_input(driver):
        list_of_message_errors = trackers.get_request_a_package_error_message_list(driver)
        list_of_message_errors = list_of_message_errors[1]
        error_element = list_of_message_errors.find_element(*trackers.request_a_package_error_message)
        return error_element
    def find_request_a_package_error_message_not_visible_name_input(driver):
        list_of_message_errors = trackers.get_request_a_package_error_message_list(driver)
        list_of_message_errors = list_of_message_errors[1]
        error_element = list_of_message_errors.find_element(*trackers.request_a_package_error_message_not_visible)
        return error_element

    def find_request_a_package_error_message_lastName_input(driver):
        list_of_message_errors = trackers.get_request_a_package_error_message_list(driver)
        list_of_message_errors = list_of_message_errors[2]
        error_element = list_of_message_errors.find_element(*trackers.request_a_package_error_message)
        return error_element

    def find_request_a_package_error_message_not_visible_last_name_input(driver):
        list_of_message_errors = trackers.get_request_a_package_error_message_list(driver)
        list_of_message_errors = list_of_message_errors[2]
        error_element = list_of_message_errors.find_element(*trackers.request_a_package_error_message_not_visible)
        return error_element
    def find_request_a_package_error_message_address_input(driver):
        list_of_message_errors = trackers.get_request_a_package_error_message_list(driver)
        list_of_message_errors = list_of_message_errors[3]
        error_element = list_of_message_errors.find_element(*trackers.request_a_package_error_message_not_visible)
        return error_element

    def find_request_a_package_error_message_not_visible_address_input(driver):
        list_of_message_errors = trackers.get_request_a_package_error_message_list(driver)
        list_of_message_errors = list_of_message_errors[3]
        error_element = list_of_message_errors.find_element(*trackers.request_a_package_error_message_not_visible)
        return error_element
    def find_request_a_package_error_metroStation_input(driver):
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(trackers.request_a_package_error_message_metroStation))
        metro_error= driver.find_element(*trackers.request_a_package_error_message_metroStation)
        return metro_error
    def find_request_a_package_error_message_phone_input(driver):
        list_of_message_errors = trackers.get_request_a_package_error_message_list(driver)
        list_of_message_errors = list_of_message_errors[4]
        error_element = list_of_message_errors.find_element(*trackers.request_a_package_error_message)
        return error_element

    def find_request_a_package_error_message_not_visible_phone_input(driver):
        list_of_message_errors = trackers.get_request_a_package_error_message_list(driver)
        list_of_message_errors = list_of_message_errors[4]
        error_element = list_of_message_errors.find_element(*trackers.request_a_package_error_message_not_visible)
        return error_element








