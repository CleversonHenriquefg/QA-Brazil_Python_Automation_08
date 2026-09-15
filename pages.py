from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class UrbanRoutesPage:
    # Localizadores da rota e da tarifa.
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    CALL_TAXI_BUTTON = (
        By.XPATH,
        "//button[contains(., 'Chamar um táxi')]"
    )
    COMFORT_TARIFF = (
        By.XPATH,
        "//div[contains(@class, 'tcard')]"
        "[.//div[normalize-space()='Comfort']]"
    )

    # Localizadores do telefone.
    PHONE_BUTTON = (By.CLASS_NAME, "np-button")
    PHONE_FIELD = (By.ID, "phone")
    NEXT_PHONE_BUTTON = (By.XPATH, "//button[normalize-space()='Próximo']")
    PHONE_CODE_FIELD = (
        By.XPATH,
        "//input[@id='code' and not(contains(@class, 'card-input'))]"
    )
    CONFIRM_PHONE_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Confirmar']"
    )

    # Localizadores do cartão.
    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-button")
    ADD_CARD_BUTTON = (
        By.XPATH,
        "//div[normalize-space()='Adicionar cartão']"
        "/ancestor::div[contains(@class, 'pp-row')]"
    )
    CARD_NUMBER_FIELD = (By.ID, "number")
    CARD_CVV_FIELD = (By.CSS_SELECTOR, "input.card-input#code")
    SAVE_CARD_BUTTON = (By.XPATH, "//button[normalize-space()='Adicionar']")

    # Localizador do comentário.
    COMMENT_FIELD = (By.ID, "comment")

    # Localizadores dos requisitos.
    REQS_CONTAINER = (By.CLASS_NAME, "reqs")
    REQUIREMENTS_HEADER = (By.CLASS_NAME, "reqs-header")
    BLANKET_AND_TISSUES_SWITCH = (
        By.XPATH,
        "//div[contains(@class, 'r-type-switch')]"
        "[contains(., 'Cobertor')]"
        "//div[contains(@class, 'switch')]"
    )
    BLANKET_AND_TISSUES_CHECKBOX = (
        By.XPATH,
        "//div[contains(@class, 'r-type-switch')]"
        "[contains(., 'Cobertor')]"
        "//input[contains(@class, 'switch-input')]"
    )
    ICE_CREAM_PLUS_BUTTON = (
        By.XPATH,
        "(//div[contains(@class, 'r-group')]"
        "[.//div[normalize-space()='Pote de sorvete']]"
        "//div[contains(@class, 'counter-plus')])[1]"
    )
    ICE_CREAM_AMOUNT = (
        By.XPATH,
        "(//div[contains(@class, 'r-group')]"
        "[.//div[normalize-space()='Pote de sorvete']]"
        "//div[contains(@class, 'counter-value')])[1]"
    )

    # Localizadores do pedido final.
    ORDER_TAXI_BUTTON = (By.CLASS_NAME, "smart-button")
    CAR_SEARCH_MODAL = (By.CLASS_NAME, "order")

    def __init__(self, driver):
        # Guarda o navegador e define a espera máxima.
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _visible_clickable_element(self, locator):
        # Retorna o primeiro elemento visível e clicável do localizador.
        def find_visible_element(driver):
            elements = driver.find_elements(*locator)

            for element in elements:
                if element.is_displayed() and element.is_enabled():
                    return element

            return False

        return self.wait.until(find_visible_element)

    def open(self, url):
        # Abre o Urban Routes.
        self.driver.get(url)

    def set_route(self, address_from, address_to):
        # Preenche os campos De e Para.
        from_field = self.wait.until(
            EC.element_to_be_clickable(self.FROM_FIELD)
        )
        from_field.clear()
        from_field.send_keys(address_from)

        to_field = self.wait.until(
            EC.element_to_be_clickable(self.TO_FIELD)
        )
        to_field.clear()
        to_field.send_keys(address_to)

    def get_from(self):
        # Retorna o valor do campo De.
        return self.driver.find_element(
            *self.FROM_FIELD
        ).get_attribute("value")

    def get_to(self):
        # Retorna o valor do campo Para.
        return self.driver.find_element(
            *self.TO_FIELD
        ).get_attribute("value")

    def select_comfort_tariff(self):
        # Abre as tarifas e seleciona Comfort somente se necessário.
        self._visible_clickable_element(self.CALL_TAXI_BUTTON).click()

        comfort_tariff = self.wait.until(
            EC.element_to_be_clickable(self.COMFORT_TARIFF)
        )

        if "active" not in comfort_tariff.get_attribute("class"):
            comfort_tariff.click()

    def get_selected_plan(self):
        # Retorna Comfort se essa tarifa estiver ativa.
        comfort_tariff = self.driver.find_element(*self.COMFORT_TARIFF)

        if "active" in comfort_tariff.get_attribute("class"):
            return "Comfort"

        return ""

    def open_phone_form(self):
        # Abre a janela de telefone.
        self.wait.until(
            EC.element_to_be_clickable(self.PHONE_BUTTON)
        ).click()

    def enter_phone_number(self, phone_number):
        # Preenche o telefone.
        phone_field = self.wait.until(
            EC.element_to_be_clickable(self.PHONE_FIELD)
        )
        phone_field.clear()
        phone_field.send_keys(phone_number)

    def click_next_phone_button(self):
        # Solicita o código SMS.
        self.wait.until(
            EC.element_to_be_clickable(self.NEXT_PHONE_BUTTON)
        ).click()

    def wait_phone_code_form(self):
        # Aguarda a tela para digitar o código SMS.
        self.wait.until(
            EC.visibility_of_element_located(self.PHONE_CODE_FIELD)
        )

    def enter_phone_code(self, code):
        # Preenche o código recebido.
        self.wait.until(
            EC.element_to_be_clickable(self.PHONE_CODE_FIELD)
        ).send_keys(code)

    def confirm_phone(self):
        # Confirma o telefone.
        self.wait.until(
            EC.element_to_be_clickable(self.CONFIRM_PHONE_BUTTON)
        ).click()

    def open_payment_method(self):
        # Abre os métodos de pagamento.
        self.wait.until(
            EC.element_to_be_clickable(self.PAYMENT_METHOD_BUTTON)
        ).click()

    def open_add_card_form(self):
        # Abre o formulário de cartão.
        self.wait.until(
            EC.element_to_be_clickable(self.ADD_CARD_BUTTON)
        ).click()

    def add_card(self, card_number, card_code):
        # Preenche e adiciona um cartão.
        self.wait.until(
            EC.element_to_be_clickable(self.CARD_NUMBER_FIELD)
        ).send_keys(card_number)

        cvv_field = self.wait.until(
            EC.element_to_be_clickable(self.CARD_CVV_FIELD)
        )
        cvv_field.send_keys(card_code)

        # Remove o foco do CVV para habilitar Adicionar.
        cvv_field.send_keys(Keys.TAB)

        self.wait.until(
            EC.element_to_be_clickable(self.SAVE_CARD_BUTTON)
        ).click()

    def add_comment_for_driver(self, comment):
        # Escreve um comentário para o motorista.
        comment_field = self.wait.until(
            EC.element_to_be_clickable(self.COMMENT_FIELD)
        )
        comment_field.clear()
        comment_field.send_keys(comment)

    def open_requirements(self):
        # Abre a seção de requisitos apenas se ainda estiver fechada.
        # (a seção já pode nascer aberta, e clicar nela de novo a fecha)
        reqs_container = self.wait.until(
            EC.presence_of_element_located(self.REQS_CONTAINER)
        )

        if "open" not in reqs_container.get_attribute("class"):
            self.wait.until(
                EC.element_to_be_clickable(self.REQUIREMENTS_HEADER)
            ).click()

    def request_blanket_and_tissues(self):
        # Solicita cobertor e lenços.
        self.open_requirements()

        self.wait.until(
            EC.element_to_be_clickable(self.BLANKET_AND_TISSUES_SWITCH)
        ).click()

    def is_blanket_and_tissues_selected(self):
        # Confirma se a opção foi marcada.
        return self.driver.find_element(
            *self.BLANKET_AND_TISSUES_CHECKBOX
        ).is_selected()

    def order_two_ice_creams(self):
        # Adiciona dois sorvetes usando um ciclo.
        self.open_requirements()

        for _ in range(2):
            self.wait.until(
                EC.element_to_be_clickable(self.ICE_CREAM_PLUS_BUTTON)
            ).click()

    def get_ice_cream_amount(self):
        # Retorna a quantidade de sorvetes.
        return int(
            self.driver.find_element(
                *self.ICE_CREAM_AMOUNT
            ).text
        )

    def order_taxi(self):
        # Faz o pedido final do táxi.
        button = self._visible_clickable_element(self.ORDER_TAXI_BUTTON)

        # Garante que o botão esteja na área visível da tela.
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )

        try:
            button.click()
        except Exception:
            # Se algo ainda estiver sobrepondo o botão, clica via JavaScript.
            self.driver.execute_script("arguments[0].click();", button)

    def is_car_search_modal_displayed(self):
        # Confirma a exibição da janela de busca.
        return self.wait.until(
            EC.visibility_of_element_located(self.CAR_SEARCH_MODAL)
        ).is_displayed()
