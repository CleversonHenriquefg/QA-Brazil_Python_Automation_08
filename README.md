# Projeto 8 — Automação Web com Selenium

Neste projeto desenvolvi uma suíte de testes automatizados para o Urban Routes. A ideia foi reproduzir, pelo navegador, o fluxo que uma pessoa faria ao pedir um táxi: informar o endereço, escolher a tarifa Comfort, adicionar telefone e cartão, escrever uma mensagem para o motorista, selecionar itens extras e finalizar o pedido.

Usei Python, Pytest, Selenium e o padrão Page Object Model (POM). Separei os testes da parte que interage com a tela para que o código fique mais organizado e fácil de manter.

## O que é validado

Os testes cobrem as etapas solicitadas no Sprint 8:

1. Preenchimento dos campos de origem e destino.
2. Seleção da tarifa Comfort.
3. Inclusão e confirmação do número de telefone por código SMS.
4. Inclusão de um cartão de pagamento.
5. Inclusão de comentário para o motorista.
6. Solicitação de cobertor e lenços.
7. Pedido de duas unidades de sorvete.
8. Finalização do pedido e validação da janela de busca por carros.

## Organização dos arquivos

```text
.
├── data.py
├── helpers.py
├── main.py
├── pages.py
├── requirements.txt
└── README.md
```

### `data.py`

Centralizei neste arquivo os dados usados em todos os testes. Dessa forma, se a URL do servidor for alterada pela TripleTen, preciso mudar somente a constante `URBAN_ROUTES_URL`.

Também deixei definidos os endereços, telefone, dados do cartão e a mensagem para o motorista. Isso evita valores repetidos dentro dos testes.

### `helpers.py`

Este arquivo contém a função `retrieve_phone_code(driver)`, que foi fornecida para recuperar o código de confirmação do telefone.

A função lê os logs de performance do Chrome, procura a resposta da requisição relacionada ao telefone e extrai os números do código SMS. Por esse motivo, o navegador precisa ser iniciado com o registro de performance habilitado.

A função `is_url_reachable(url)` também está disponível para verificar se o servidor pode ser acessado.

### `pages.py`

Neste arquivo está a classe `UrbanRoutesPage`. Ela representa a página do Urban Routes e concentra os localizadores e as ações feitas na interface.

A escolha de usar POM foi importante para não colocar comandos como `find_element()` diretamente nos testes. Assim, o arquivo `main.py` fica focado na regra do teste, enquanto o `pages.py` cuida da interação com a página.

#### Principais métodos da página

| Método | Objetivo |
| --- | --- |
| `open(url)` | Abre o endereço do Urban Routes no navegador. |
| `set_route(address_from, address_to)` | Preenche os campos **De** e **Para**. |
| `get_from()` e `get_to()` | Retornam o conteúdo preenchido nos campos para realizar os asserts da rota. |
| `select_comfort_tariff()` | Abre as opções de tarifa e seleciona Comfort somente se ela ainda não estiver ativa. |
| `get_selected_plan()` | Verifica se a tarifa Comfort ficou marcada. |
| `open_phone_form()` | Abre a janela de preenchimento do telefone. |
| `enter_phone_number(phone_number)` | Preenche o telefone informado no teste. |
| `click_next_phone_button()` | Solicita o envio do código SMS. |
| `wait_phone_code_form()` | Aguarda o campo do código de confirmação aparecer. |
| `enter_phone_code(code)` e `confirm_phone()` | Preenchem e confirmam o código obtido nos logs. |
| `get_registered_phone_number()` | Retorna o número de telefone exibido após a confirmação, para validar que corresponde ao informado. |
| `open_payment_method()` | Abre a seção de métodos de pagamento. |
| `open_add_card_form()` | Abre a janela para adicionar cartão. |
| `add_card(card_number, card_code)` | Preenche número e CVV do cartão. Após o CVV, usa a tecla Tab para remover o foco e habilitar o botão **Adicionar**. |
| `get_current_payment_method()` | Retorna o texto da forma de pagamento selecionada, para validar que ficou como "Cartão". |
| `add_comment_for_driver(comment)` | Escreve a mensagem para o motorista. |
| `get_driver_comment()` | Retorna o valor atual do campo de comentário, para validar que o texto foi preenchido corretamente. |
| `open_requirements()` | Abre a seção de requisitos somente quando ela ainda está fechada. |
| `request_blanket_and_tissues()` | Marca a opção de cobertor e lenços. |
| `is_blanket_and_tissues_selected()` | Confere se o checkbox da opção ficou selecionado. |
| `order_two_ice_creams()` | Usa um ciclo `for` para clicar duas vezes no botão de adicionar sorvete. |
| `get_ice_cream_amount()` | Retorna a quantidade exibida na tela para validar que são dois sorvetes. |
| `order_taxi()` | Localiza o botão final, rola até ele e realiza o pedido. |
| `is_car_search_modal_displayed()` | Aguarda e confirma a exibição da janela de busca por carros. |

Também utilizei `WebDriverWait` e condições esperadas do Selenium para esperar elementos ficarem visíveis ou clicáveis. Isso deixa os testes mais estáveis do que depender apenas de esperas fixas.

## Testes em `main.py`

A classe `TestUrbanRoutes` reúne os cenários executados pelo Pytest.

### Preparação e encerramento

O método `setup_class()` cria o Chrome uma única vez e habilita os logs de performance necessários para a recuperação do SMS. Também cria uma instância da classe `UrbanRoutesPage`.

O método `teardown_class()` fecha o navegador depois que todos os testes terminam.

### Métodos de apoio

Criei alguns métodos para evitar repetição:

- `prepare_comfort_trip()`: abre o site, preenche a rota e seleciona Comfort.
- `confirm_phone_number()`: abre o formulário de telefone, solicita o SMS, recupera o código com `retrieve_phone_code()` e confirma o número.
- `add_payment_card()`: abre a área de pagamento e adiciona o cartão.

### Cenários automatizados

- `test_set_route()`: valida se os campos de origem e destino receberam exatamente os valores esperados.
- `test_select_plan()`: valida se a tarifa selecionada é Comfort.
- `test_fill_phone_number()`: executa o fluxo de confirmação de telefone.
- `test_fill_card()`: adiciona um cartão de pagamento.
- `test_comment_for_driver()`: preenche a mensagem para o motorista.
- `test_order_blanket_and_handkerchiefs()`: marca cobertor e lenços e verifica se a opção foi selecionada.
- `test_order_2_ice_creams()`: adiciona duas unidades de sorvete e valida a quantidade exibida.
- `test_car_search_model_appears()`: executa o fluxo principal de pedido com Comfort, telefone, cartão e comentário; por fim, confirma que a janela de busca de carros aparece.

Cada cenário começa com o estado necessário para não depender da execução do teste anterior. Isso ajuda a manter os testes independentes.

## Como executar

1. Atualize a URL em `data.py` com o endereço ativo do servidor disponibilizado pela TripleTen.
2. Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

3. Execute os testes:

```bash
python -m pytest main.py -s
```

## Dependências

- Selenium
- Pytest
- Requests

## Observação

O servidor Urban Routes é temporário. Quando ele é reiniciado pela plataforma, a URL anterior deixa de funcionar. Nesse caso, basta atualizar `URBAN_ROUTES_URL` em `data.py` antes de executar novamente.
