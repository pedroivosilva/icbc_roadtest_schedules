from datetime import datetime as dt
from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil import parser
import os
from dotenv import load_dotenv

load_dotenv()

# get environment variables
DRIVER_LAST_NAME = os.getenv('DRIVER_LAST_NAME')
DRIVER_LICENSE = os.getenv('DRIVER_LICENSE')
ICBC_KEYWORD = os.getenv('ICBC_KEYWORD')


def open_browser():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        return True, driver
    except Exception as e:
        return False, e


# def get_icbc_roadtest_page(d):
#     try:
#         d.get('https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver')
#     return
#
#
# def auth():
#
#     return
#
#
# def start_reschedule():
#
#     return
#
#
# def choose_office():
#
#     return
#
# def select_office():
#
#     return
#
#
# def get_appointments():
#
#     return

def check_available_dates():
    # Inicialize o driver do navegador (neste caso, Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # edge_options = webdriver.EdgeOptions()
    # edge_options.add_argument("--remote-allow-origins=*")
    # edge_options.add_argument("--headless=new")
    # driver = webdriver.Edge(options=edge_options)

    # Vá para a página da web
    driver.get('https://onlinebusiness.icbc.com/webdeas-ui/login;type=driver')

    # Configure todos os waits
    wait = WebDriverWait(driver, 5)
    wait_long = WebDriverWait(driver, 10)

    # Aguarde carregar o primeiro campo para iniciar o preenchimento
    wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='drvrLastName']")))

    # Preencher campo nome
    drivers_last_name = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='drvrLastName']")
    drivers_last_name.send_keys(DRIVER_LAST_NAME)

    # Preencher o campo drivers license
    drivers_license = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='licenceNumber']")
    drivers_license.send_keys(DRIVER_LICENSE)

    # Preencher o campo keyword
    icbc_keyword = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='keyword']")
    icbc_keyword.send_keys('ICBC_KEYWORD')

    # Marcar o checkbox
    checkbox = driver.find_element(By.CSS_SELECTOR, "span.mat-checkbox-inner-container")
    checkbox.click()

    # Encontrar o botão sign in, aguardar ficar clicavel e clicar
    sign_in = driver.find_element(By.CSS_SELECTOR, "button.primary.collapsible-action-button")
    wait.until(EC.element_to_be_clickable(sign_in)).click()

    by_office_check = False

    while not by_office_check:
        # Aguardar carregar o botao de reschedule e a guia "Your upcoming appointments" na proxima pagina
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.raised-button.primary")))
            wait.until(EC.presence_of_element_located((By.XPATH, "//div"
                                                                  "[contains(text(), 'Your upcoming appointments')]")))
        # Caso nao carregue os dois significa que o driver ja esta na tela de busca e que ainda nao existe
        # o botao de reschedule. Neste caso a excecao e aguardar carregar somente o botao da aba "Your upcoming
        # appointments.
        except common.exceptions.TimeoutException:
            wait.until(EC.presence_of_element_located((By.XPATH, "//div"
                                                                 "[contains(text(), 'Your upcoming appointments')]")))

        upcoming_appointments = driver.find_element(By.XPATH, "//div"
                                                                  "[contains(text(), 'Your upcoming appointments')]")
        upcoming_appointments.click()

        # Clicar no botao Reschedule appointment
        driver.find_element(By.XPATH, "//button[contains(text(), 'Reschedule appointment')]").click()

        # Aguardar carregar o popup de confirmacao
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.primary.ng-star-inserted")))

        # Clicar no botao de confirmacao Yes
        driver.find_element(By.CSS_SELECTOR, "button.primary.ng-star-inserted").click()

        # Aguardar carregar o campo Location da pagina de busca
        wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='finishedAutocomplete']")))

        # # ESTRATEGIA 1
        #
        # # Comecar a preencher o campo location com Langley
        # location = driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='finishedAutocomplete']")
        # location.send_keys("Langley")
        #
        # # Aguardar aparecer "Langley, BC" na lista
        # wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='mat-option-268']")))
        #
        # # Clicar em Langley, BC na lista suspensa
        # select_location = driver.find_element(By.XPATH, "//*[@id='mat-option-268']")
        # select_location.click()

        # ESTRATEGIA 2

        # Clicar em 'By office'
        by_office = driver.find_element(By.XPATH, "//html/body/div[2]/div/div/mat-dialog-container"
                                                  "/app-search-modal/div/div/form/div[1]/mat-tab-group"
                                                  "/mat-tab-header/div[2]/div/div/div[2]/div")
        by_office.click()

        # Aguardar carregar o campo principal
        try:
            wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[formcontrolname='officeControl']")))
            # Clicar no campo principal para exibir as opcoes
            driver.find_element(By.CSS_SELECTOR, "input[formcontrolname='officeControl']").click()
            by_office_check = True
        except common.exceptions.TimeoutException:
            try:
                wait_long.until(EC.presence_of_element_located((By.XPATH, "//div[starts-with"
                                                                          "(@id,'QSIWebResponsiveDialog') and "
                                                                          "contains(text(), 'Help us improve our')]")))
                no_thanks = driver.find_element(By.XPATH, "//button[contains(text(), 'No thanks')]")
                no_thanks.click()
                by_office_check = True
            except:
                by_office_check = False


    # Aguardar que apareca a opcao de langley
    wait.until(EC.presence_of_element_located((By.XPATH, "//html/body/div[2]/div[2]/div/div/mat-option[37]/span")))

    # Clicar na opcao de Langley Willowbrook Center
    willowbrook_location = driver.find_element(By.XPATH, "//html/body/div[2]/div[2]/div/div/mat-option[37]/span")
    willowbrook_location.click()

    # Aguarda carregar todas as datas disponiveis
    wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/mat-dialog-container"
                                                         "/app-eligible-tests/div/div[2]/mat-button-toggle-group/div")))

    # Nao consegui clicar no botao view more! por isso esta pegando somente as ultimas 5 datas.
    #
    # # Aguarda carregar o botao View More
    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "i.fa.fa-chevron-down.view-more-chevron")))
    #
    # # Clicar em View More
    # view_more = driver.find_element(By.CSS_SELECTOR, "i.fa.fa-chevron-down.view-more-chevron")
    # view_more.click()

    # Captura todas as datas disponiveis
    appointment_listings_all = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/mat-dialog-container"
                                                         "/app-eligible-tests/div/div[2]/mat-button-toggle-group/div")
    appointment_listings_all = appointment_listings_all.text
    appointment_listings_all = appointment_listings_all.splitlines()

    # Remove todos os horarios da lista e deixa somente as datas.
    appointment_listings = []
    appointment_listings_parse = appointment_listings_all[:]
    for i in appointment_listings_all:
        if i[0].isdigit():
            appointment_listings_parse.remove(i)
        else:
            try:
                date = parser.parse(i)
                appointment_listings.append(str(date.date()))
            except ValueError:
                appointment_listings_parse.remove(i)

    appointment_listings = sorted(appointment_listings)

    driver.quit()

    return appointment_listings


def next_appointment_days(listings: list) -> int:
    today = dt.today().date()
    earliest = listings[0]
    earliest_dt = dt.strptime(earliest, "%Y-%m-%d").date()
    delta = earliest_dt - today
    return delta.days


def next_appointment_date(listings: list) -> str:
    earliest = listings[0]
    earliest = dt.strptime(earliest, "%Y-%m-%d").date()
    return earliest.isoformat()


if __name__ == '__main__':
    monitor = True
    while monitor:
        # try:
        appointments = check_available_dates()
        print(appointments)
        # except Exception as e:
        #     print(e)
        #     monitor = False