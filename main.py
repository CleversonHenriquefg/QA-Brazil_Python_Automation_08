import time

import data
import helpers
from selenium import webdriver

from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Habilita logs para recuperar o código SMS.
        options = webdriver.ChromeOptions()
        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        # Cria o navegador e a página POM.
        cls.driver = webdriver.Chrome(options=options)
        cls.page = UrbanRoutesPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        # Fecha o navegador depois dos testes.
        cls.driver.quit()

    def prepare_comfort_trip(self):
        # Abre o site, informa a rota e seleciona Comfort.
        self.page.open(data.URBAN_ROUTES_URL)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.select_comfort_tariff()

    def confirm_phone_number(self):
        # Informa e confirma o telefone usando o código SMS.
        self.page.open_phone_form()
        self.page.enter_phone_number(data.PHONE_NUMBER)
        self.page.click_next_phone_button()
        self.page.wait_phone_code_form()

        # Pequena espera extra para garantir que a chamada de rede
        # do envio do SMS já foi registrada nos logs de performance
        # antes de tentarmos recuperar o código.
        time.sleep(2)

        code = helpers.retrieve_phone_code(self.driver)

        self.page.enter_phone_code(code)
        self.page.confirm_phone()

    def add_payment_card(self):
        # Adiciona um cartão de crédito.
        self.page.open_payment_method()
        self.page.open_add_card_form()
        self.page.add_card(data.CARD_NUMBER, data.CARD_CODE)

    def test_set_route(self):
        # Testa os campos De e Para.
        self.page.open(data.URBAN_ROUTES_URL)
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)

        assert self.page.get_from() == data.ADDRESS_FROM
        assert self.page.get_to() == data.ADDRESS_TO

    def test_select_plan(self):
        # Testa a tarifa Comfort.
        self.prepare_comfort_trip()

        assert self.page.get_selected_plan() == "Comfort"

    def test_fill_phone_number(self):
        # Testa o preenchimento e a confirmação do telefone.
        self.prepare_comfort_trip()
        self.confirm_phone_number()

    def test_fill_card(self):
        # Testa a adição do cartão.
        self.prepare_comfort_trip()
        self.add_payment_card()

    def test_comment_for_driver(self):
        # Testa o comentário ao motorista.
        self.prepare_comfort_trip()
        self.page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)

    def test_order_blanket_and_handkerchiefs(self):
        # Testa a solicitação de cobertor e lenços.
        self.prepare_comfort_trip()
        self.page.request_blanket_and_tissues()

        assert self.page.is_blanket_and_tissues_selected()

    def test_order_2_ice_creams(self):
        # Testa o pedido de duas unidades de sorvete.
        self.prepare_comfort_trip()
        self.page.order_two_ice_creams()

        assert self.page.get_ice_cream_amount() == 2

    def test_car_search_model_appears(self):
        # Testa a abertura da janela de busca de carros.
        self.prepare_comfort_trip()
        self.confirm_phone_number()
        self.add_payment_card()
        self.page.add_comment_for_driver(data.MESSAGE_FOR_DRIVER)
        self.page.order_taxi()

        assert self.page.is_car_search_modal_displayed()
