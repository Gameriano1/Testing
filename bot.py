import cv2 as cv
import subprocess
import mouse
import random
import pickle
import json
import PySimpleGUI as sg
import requests
import pydirectinput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from testes.last import nomear
import pyautogui
import ctypes
from mss import mss
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import mss.tools as mss_tools
import winsound
from multiprocessing import Process
import time
import string
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
from selenium import webdriver

def configuracoesgerais():
    with open('config.json') as config:
        perfect = json.load(config)
        vvarnum = perfect["configs"]["vvarnum"]
        contasprontas = perfect["configs"]["contasprontas"]
        rewards = perfect["configs"]["rewards"]
        dcontas = perfect["configs"]["dcontas"]
        delay = perfect["configs"]["delay"]
        paisesnome = perfect["paises"]["paisesnome"]
        nomebrasileiro = perfect["paises"]["nomebrasileiro"]
        vpne = perfect["paises"]["vpn"]

    name = os.getenv('username')
    localcon = fr'C:\Users\{name}\desktop'
    localrewards = fr'C:\Users\{name}\desktop'
    return (vvarnum,contasprontas,rewards,dcontas,localcon,localrewards,delay,paisesnome,nomebrasileiro,vpne)

vvarnum,contasprontas,rewards,dcontas,localcon,localrewards,delay,paisesnome,nomebrasileiro,vpne = configuracoesgerais()
print(vpne)

with open('contas.json') as contas:
    acc = json.load(contas)
    emails = acc["email"][0]
    senhas = acc["senhas"][0]


class defs():

    def openvpn(connect = False):
        os.system('taskkill /f /im openvpn-gui.exe')
        os.system('taskkill /f /im openvpn.exe')
        if connect:
            x = subprocess.Popen(r'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --command disconnect_all', shell=True)
            time.sleep(3)
            if vpnome != "Brazil":
                x = subprocess.Popen(fr'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --connect {vpnome}.ovpn', shell=True)
            time.sleep(1)

        def get_ip():
            response = requests.get('https://api64.ipify.org?format=json').json()
            return response["ip"]

        def get_location():
            ip_address = get_ip()
            response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
            location_data = {
                "ip": ip_address,
                "city": response.get("city"),
                "region": response.get("region"),
                "country": response.get("country_name")
            }
            return location_data
        x = get_location()
        local = x["country"]
        if vpnome == "Eua":
            nome = "United States"
        elif vpnome == "Japan":
            nome = "Japan"
        elif vpnome == "Brazil":
            nome = "Brazil"
        while local != nome:
            x = get_location()
            local = x["country"]
        print(local)


    def abrir_rewards():
        lnk_path = f'{localrewards}\Microsoft Rewards.lnk'
        subprocess.call(lnk_path, shell=True)

    def abrir_config():
        global rewards
        rewards = 'conf'
        lnk_path = f'{localcon}\Configurações.lnk'
        subprocess.call(lnk_path, shell=True)
        time.sleep(2)
        global vvar
        vvar = 'configura'
        defs.telaconfig()
        defs.IA2()
        if existe2 == 'sim':
            defs.click()
        vvar = 'regiao'
        defs.telaconfig()
        defs.IA2()
        while not existe2 == 'sim':
            defs.telaconfig()
            defs.IA2()
        defs.click()
        vvar = 'reg'
        defs.telaconfig()
        defs.IA2()
        while not existe2 == 'sim':
            defs.telaconfig()
            defs.IA2()
        rewards = 'rewardss'

    def IA2(um=0):
        global existe2
        global rewards
        global max_loc
        rewards_img = cv.imread(fr'paths\{rewards}.png', cv.IMREAD_ANYCOLOR)
        if um == 0:
            detalhamento_img = cv.imread(fr'imagens\{vvar}.png', cv.IMREAD_ANYCOLOR)
        elif um == 1:
            detalhamento_img = cv.imread(fr'paises\{vvar}.png', cv.IMREAD_ANYCOLOR)
        elif um == 2:
            detalhamento_img = cv.imread(fr'pesquisa\{vvar}.png', cv.IMREAD_ANYCOLOR)

        result = cv.matchTemplate(rewards_img, detalhamento_img, cv.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        threshold = vvarnum
        if max_val >= threshold:
            existe2 = 'sim'

            global w
            w = detalhamento_img.shape[1]
            global h
            h = detalhamento_img.shape[0]
        else:
            existe2 = 'nao'

    def click(um=0):
        if um == 0:
            pydirectinput.click(
                x=(max_loc[0] + int(w/2) + bbox[0]), 
                y=(max_loc[1] + int(h/2) + bbox[1])
            )
        elif um == 1:
            pydirectinput.moveTo(
                x=(max_loc[0] + int(w/2) + bbox[0]), 
                y=(max_loc[1] + int(h/2) + bbox[1])
            )

    def achar_task1k():
        global vvar
        scroll = -3
        vvar = '1k'
        defs.tentar()
        defs.IA2()
        while existe2 == 'nao':
            vvar = '1k'
            defs.tentar()
            defs.IA2()
            if existe2 == 'sim':
                defs.click()
                time.sleep(5)
                return
            pyautogui.moveTo(1400,750)
            mouse.wheel(scroll)
            vvar = 'sobre'
            defs.tentar()
            defs.IA2()
            if existe2 == 'sim':
                scroll = 3
                break
        vvar = '1k'
        defs.tentar()
        defs.IA2()
        if existe2 == 'sim':
            defs.click()
            time.sleep(5)
            return
        vvar = 'mostrartodas'
        defs.tentar()
        defs.IA2()
        if existe2 == 'nao':
                vvar = 'mostrartodas'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    global vvarnum
                    vvarnum = 0.7
                    mouse.wheel(scroll)
                    defs.tentar()
                    defs.IA2()
                vvarnum = 0.9
                vvar = 'mostrartodas'
                defs.tentar()
                defs.IA2()
                defs.click()
                vvar = 'casa'
                defs.tentar()
                defs.IA2()
                while not existe2 == 'sim':
                    vvar = 'casa'
                    defs.tentar()
                    defs.IA2()
                mouse.wheel(scroll)
                vvar = '1k'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    vvar = '1k'
                    defs.tentar()
                    defs.IA2()
                    if existe2 == 'sim':
                        break
                    pyautogui.moveTo(1400,750)
                    scroll = -3
                    mouse.wheel(scroll)
                vvar = 'cont'
                defs.tentar()
                defs.IA2()
                defs.click()

    def clicarnave():
        global vvar
        tem = defs.clicar("web")
        tem = defs.clicar("nave", mouse=False)
        while not existe2 == 'sim':
            defs.tentarvp()
            defs.IA2()
        tem = defs.clicar("conc", mouse=False)
        while existe2 == 'nao':
            tem = defs.clicar("nave")
            vvar = 'qrnave'
            defs.tentar()
            defs.IA2()
            while existe2 == 'nao':
                vvar = 'qrnave'
                defs.tentar()
                defs.IA2()
            pyautogui.press('enter')
            vvar = 'moedagigante'
            defs.printqrs()
            defs.IA2()
            while existe2 == 'sim':
                vvar = 'moedagigante'
                defs.printqrs()
                defs.IA2()
            os.system('taskkill /f /im msedge.exe')
            time.sleep(4)
            defs.clicarnave()

    def bingantibug(xpath, driverz):
        try:
            myElem = WebDriverWait(driverz, delay).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            raise Exception('A Pagina nao acrregou a tempo')

    def abrir_bing():
        global bixo
        global troxa
        global driver
        chrome_options = ChromeOptions()

        driver = webdriver.Chrome('chromedriver',options=chrome_options)
        driver.get('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&id=264960&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253ftoWww%253d1%2526redig%253d3389C7EB769248EB8086CD884D2595CF%2526wlexpsignin%253d1%26sig%3d0A6C406EFB686EA604025253FA7C6FDA&wp=MBI_SSL&lc=1046&CSRFToken=9399de60-9308-4156-8667-596b86a444d0&aadredir=1')

        defs.bingantibug('//*[@id="i0116"]', driver)
        driver.find_element('xpath', '//*[@id="i0116"]').send_keys(emails)
        print('digitei a conta')

        defs.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
        print('cliquei em proximo')
        time.sleep(2)

        defs.bingantibug('//*[@id="i0118"]', driver)
        driver.find_element('xpath', '//*[@id="i0118"]').send_keys(senha)
        print('digitei a senha')

        defs.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
        print('cliquei em entrar')

        defs.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
        print('cliquei em proximo')
        pickle.dump( driver.get_cookies() , open(r"paths\cookies.pkl","wb"))
        print('terminei')
        driver.close()
        
    def ativarconta():

        global bixo

        driver = webdriver.Chrome('chromedriver')
        driver.get('https://bing.com')
        driver.minimize_window()  
        driver.maximize_window()  
        driver.minimize_window()
        driver.maximize_window()
        driver.maximize_window()
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('https://rewards.microsoft.com/')
        cookies2 = pickle.load(open("cookies3.pkl", "rb"))
        for cookie in cookies2:
            driver.add_cookie(cookie)
        driver.get('https://rewards.microsoft.com/')
        bixo = '//*[@id="start-earning-rewards-link"]'
        defs.achar()
        print('achei')
        time.sleep(5)
        driver.find_element('xpath', bixo).click()

        bixo = '//*[@id="rx-user-status-action"]'
        defs.achar()
        print('achei')
        time.sleep(5)
        driver.get('https://rewards.microsoft.com/optout')


        bixo = '//*[@id="opt-out-page"]/div[4]/div[3]/form/button'
        defs.achar()
        print('achei')
        time.sleep(5)
        driver.find_element('xpath', bixo).click()
        time.sleep(1)  
        pyautogui.press('enter')
        pyautogui.keyDown('alt')
        pyautogui.press('esc')
        pyautogui.keyUp('alt')
        driver.close()  
   
    def contaconfig():
        global vvar
        global rewards
        global configimg
        configimg = 'conf'
        rewards = configimg
        lnk_path = f'{localcon}\Configurações.lnk'
        subprocess.call(lnk_path, shell=True)
        time.sleep(2)
        cc = pyautogui.locateCenterOnScreen('cckk.png', confidence=0.8)
        pyautogui.click(cc)
        time.sleep(5)
        defs.telaconfig()
        vvar = 'pararentrar'
        defs.IA2()
        if existe2 == 'sim':
            pararentrar = pyautogui.locateCenterOnScreen('pararentrar.png', confidence=0.7)
            pyautogui.click(pararentrar)
            time.sleep(3)
        iec = pyautogui.locateCenterOnScreen('iec.png', confidence=0.8)
        pyautogui.click(iec)
        time.sleep(3)
        minhalista = list(pyautogui.locateAllOnScreen('crosoft.png',confidence=0.98))
        print(minhalista)
        if not minhalista:
            print('se fudeu kkkkk')
    
        for i in minhalista:
            pyautogui.click(minhalista[0])
            time.sleep(1)
            remover = pyautogui.locateCenterOnScreen('remover.png', confidence=0.7)
            print(remover)
            pyautogui.click(remover)
            time.sleep(1)
            sim = pyautogui.locateCenterOnScreen('sim.png', confidence=0.7)
            pyautogui.click(sim)
            time.sleep(1)

        addconta = pyautogui.locateCenterOnScreen('adicionarconta.png', confidence=0.7)
        pyautogui.click(addconta)

        time.sleep(1)
        defs.telaconfig()
        vvar = 'outlook'
        defs.IA2()

        while not existe2 == 'sim':
            defs.telaconfig()
            vvar = 'outlook'
            defs.IA2()
        outlookcom = pyautogui.locateCenterOnScreen('msn.png', confidence=0.7)
        pyautogui.click(outlookcom)

        time.sleep(1)
        defs.telaconfig()
        vvar = 'proximo'
        defs.IA2()

        while not existe2 == 'sim':
            defs.telaconfig()
            vvar = 'proximo'
            defs.IA2()
        pyautogui.click(1113, 203)
        pyautogui.write(conta)

        proximo = pyautogui.locateCenterOnScreen('proximo.png', confidence=0.7)
        pyautogui.click(proximo)

        time.sleep(1)
        defs.telaconfig()
        vvar = 'entrar'
        defs.IA2()

        while not existe2  == 'sim':
            defs.telaconfig()
            vvar = 'entrar'
            defs.IA2()

        pyautogui.click(1108, 237)
        pyautogui.write(senha)

        entrar = pyautogui.locateCenterOnScreen('entrar.png', confidence=0.7)
        pyautogui.click(entrar)

        time.sleep(1)
        defs.telaconfig()
        vvar = 'prox2'
        defs.IA2()

        while not existe2 == 'sim':
            defs.telaconfig()
            vvar = 'prox2'
            defs.IA2()
        prox2 = pyautogui.locateCenterOnScreen('prox2.png',confidence=0.7)
        pyautogui.click(prox2)

        time.sleep(1)
        defs.telaconfig()
        vvar = 'app'
        defs.IA2()

        while not existe2 == 'sim':
            defs.telaconfig()
            vvar = 'app'
            defs.IA2()
        terminar = pyautogui.locateCenterOnScreen('terminar.png', confidence=0.7)
        pyautogui.click(terminar)

        time.sleep(1)
        defs.telaconfig()
        vvar = 'email'
        defs.IA2()

        while not existe2 == 'sim':
            defs.telaconfig()
            vvar = 'email'
            defs.IA2()
        email = pyautogui.locateCenterOnScreen('email.png', confidence=0.7)
        pyautogui.click(email)

        time.sleep(1)

        gerenciar = pyautogui.locateCenterOnScreen('gerenciar.png', confidence=0.7)
        pyautogui.click(gerenciar)

        time.sleep(1)
        defs.telaconfig()
        vvar = 'salvar'
        defs.IA2()

        while not existe2 == 'sim':
            defs.telaconfig()
            vvar = 'salvar'
            defs.IA2()
        pyautogui.click(1155, 314)
        time.sleep(1)
        excluir = pyautogui.locateCenterOnScreen('excluir.png', confidence=0.7)
        pyautogui.click(excluir)

        time.sleep(1)
        defs.telaconfig()
        vvar = 'terminar'
        defs.IA2()

        while not existe2 == 'sim':
            defs.telaconfig()
            vvar = 'terminar'
            defs.IA2()

        time.sleep(1)
        terminar = pyautogui.locateCenterOnScreen('terminar.png', confidence=0.7)
        pyautogui.click(terminar)

        rewards = 'rewardss'

    def abs(num, agent = "user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"):
        global driver3  
        chrome_options = ChromeOptions()
        chrome_options.add_argument(agent)
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        chrome_options.headless = False


        driver3 = webdriver.Chrome('chromedriver',desired_capabilities=caps, options=chrome_options)
        driver3.get('http://bing.com')
        time.sleep(2)
        cookies = pickle.load(open(r"paths\cookies.pkl", "rb"))
        for cookie in cookies:
            driver3.add_cookie(cookie)
        Resultyy = ''.join(random.choice(string.ascii_letters) for i in range(8))

        urls = f'https://www.bing.com/search?q={Resultyy}'
        for posts in range(num):
            print(posts)
            driver3.get(urls)    
            driver3.execute_script("window.open('');")
            chwd = driver3.window_handles
            driver3.switch_to.window(chwd[-1])
            Resultyy = ''.join(random.choice(string.ascii_letters) for i in range(8))
            urls = f'https://www.bing.com/search?q={Resultyy}'

        time.sleep(5)
        driver3.quit()

    def clicar(var, mouse = True, num = 0):
        global vvar
        if mouse:
            vvar = var
            defs.tentarvp()
            defs.IA2()
            defs.click(num)
        else:
            vvar = var
            defs.tentarvp()
            defs.IA2()
            return existe2

    def tasksn(qual):
        def clicarbing(fazer='nao'):
            global vvar
            defs.clicar("nave", num=1)
            tem = defs.clicar("bing", mouse=False)
            while tem == 'nao':
                # if paises == 'brazil':
                #     mouse.wheel(-3.6)
                # else
                mouse.wheel(-6.5)
                time.sleep(0.7)
                tem = defs.clicar("bing", mouse=False)
            tem = defs.clicar("conc", mouse=False)
            if fazer == 'nao':
                if existe2 == 'nao':
                    defs.abs(67)
            if fazer == 'sim':
                defs.abs(10)
            while existe2 == 'nao':
                print('eu vejo o bing')
                defs.clicar("bing")
                vvar = 'qr'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    vvar = 'qr'
                    defs.tentar()
                    defs.IA2()
                pyautogui.press('enter')
                vvar = 'moedagigante'
                defs.printqrs()
                defs.IA2()
                while existe2 == 'sim':
                    vvar = 'moedagigante'
                    defs.printqrs()
                    defs.IA2()
                os.system('taskkill /f /im msedge.exe')
                abs(7)
                clicarbing('sim')

        def clicarloja(scroll = -6.5):
            global vvar
            global vvarnum
            vvar = 'conc'
            defs.tentarvp()
            defs.IA2()
            defs.click(1)
            #while not existe2 == 'sim':
            #tentarvp()
            #IA2()
            vvar = 'loja'
            defs.tentarvp()
            defs.IA2()

            while existe2 == 'nao':
                mouse.wheel(scroll)
                time.sleep(0.9)
                vvar = 'loja'
                defs.tentarvp()
                time.sleep(0.2)
                defs.IA2()
            vvar = 'conc'
            defs.tentarvp()
            defs.IA2()
            while existe2 == 'nao':
                print('eu vejo o loja')
                vvar = 'loja'
                defs.tentarvp()
                defs.IA2()
                defs.click()
                vvar = 'voltaganhos'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    defs.tentar()
                    defs.IA2()
                click = pyautogui.locateCenterOnScreen(r'imagens\voltar.png',confidence=0.7)
                pyautogui.click(click)
                vvar = 'moedagigante'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    defs.tentar()
                    defs.IA2()
                vvarnum = 0.9
                clicarloja(-6.5)
        
        def clicarxbox(scroll = -6.5):
            global vvar
            vvar = 'conc'
            defs.tentarvp()
            defs.IA2()
            defs.click(1)
            time.sleep(0.4)
            #while not existe2 == 'sim':
            #tentarvp()
            #IA2()
            vvar = 'xbox'
            defs.tentarvp()
            defs.IA2()

            while existe2 == 'nao':
                mouse.wheel(scroll)
                time.sleep(0.9)
                vvar = 'xbox'
                defs.tentarvp()
                time.sleep(0.2)
                defs.IA2()
            vvar = 'conc'
            defs.tentarvp()
            defs.IA2()
            while existe2 == 'nao':
                print('eu vejo o xbox')
                vvar = 'xbox'
                defs.tentarvp()
                defs.IA2()
                defs.click()
                vvar = 'novoapp'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    vvar = 'novoapp'
                    defs.tentar()
                    defs.IA2()
                vvar = 'bola'
                defs.tentar()
                defs.IA2()
                defs.click()
                clicarxbox(-6.5)

        def clicarmoeda(scroll = -6.5):
            global vvar
            global vvarnum
            vvar = 'conc'
            defs.tentarvp()
            defs.IA2()
            defs.click(1)
            time.sleep(0.9)
            #while not existe2 == 'sim':
            #tentarvp()
            #IA2()
            vvar = 'moeda'
            defs.tentarvp()
            defs.IA2()


            while existe2 == 'nao':
                mouse.wheel(scroll)
                time.sleep(0.9)
                vvar = 'moeda'
                defs.tentarvp()
                time.sleep(0.2)
                defs.IA2()
            vvar = 'conc'
            defs.tentarvp()
            defs.IA2()
            while existe2 == 'nao':
                print('eu vejo a moeda')
                vvar = 'moeda'
                defs.tentarvp()
                defs.IA2()
                defs.click()

                vvar = 'moedas'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    defs.tentar()
                    defs.IA2()
                click = pyautogui.locateCenterOnScreen(r'imagens\voltar.png',confidence=0.7)
                pyautogui.click(click)
                vvar = 'moedagigante'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    defs.tentar()
                    defs.IA2()
                vvarnum = 0.9
                clicarmoeda(-6.5)

        def clicarrewards(scroll = -6.5):
            global vvar
            global vvarnum
            vvar = 'conc'
            defs.tentarvp()
            defs.IA2()
            defs.click(1)
            time.sleep(0.9)
            #while not existe2 == 'sim':
            #tentarvp()
            #IA2()
            vvar = 'rewards'
            defs.tentarvp()
            defs.IA2()


            while not existe2 == 'sim':
                mouse.wheel(scroll)
                time.sleep(0.9)
                defs.tentarvp()
                time.sleep(0.2)
                defs.IA2()
            vvar = 'conc'
            defs.tentarvp()
            defs.IA2()
            while existe2 == 'nao':
                print('eu vejo a rewards')
                vvar = 'rewards'
                defs.tentarvp()
                defs.IA2()
                defs.click()
                vvar = 'detalhamento'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    defs.tentar()
                    defs.IA2()
                click = pyautogui.locateCenterOnScreen(r'imagens\voltar.png',confidence=0.7)
                pyautogui.click(click)
                vvar = 'moedagigante'
                defs.tentar()
                defs.IA2()
                while existe2 == 'nao':
                    defs.tentar()
                    defs.IA2()
                vvarnum = 0.9
                clicarrewards(-6.5)
        if qual == 'bing':
            clicarbing()
        elif qual == 'loja':
            clicarloja()
        elif qual == 'xbox':
            clicarxbox()
        elif qual == 'moeda':
            clicarmoeda()
        elif qual == 'rewards':
            clicarrewards()

    def tentar():

        with mss() as sct:
            global bbox
            hwnd = ctypes.windll.user32.FindWindowW(0, 'Microsoft Rewards')
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
            monitor = sct.monitors[1]

            bbox = (rect.left+5, rect.top, rect.right-7, rect.bottom-7)
            shot = sct.grab(bbox)
            mss_tools.to_png(shot.rgb, shot.size, output=r'paths\rewardss.png')

    def tentarvp():

        with mss() as sct:
            global bbox
            hwnd = ctypes.windll.user32.FindWindowW(0, 'Microsoft Rewards')
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
            monitor = sct.monitors[1]

            bbox = (rect.left+750, rect.top+550, rect.right-10, rect.bottom-10)
            shot = sct.grab(bbox)
            mss_tools.to_png(shot.rgb, shot.size, output=r'paths\rewardss.png')

    def telaconfig():

        with mss() as sct:
            global bbox
            hwnd = ctypes.windll.user32.FindWindowW(0, 'Configurações')
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
            monitor = sct.monitors[1]

            bbox = (rect.left+5, rect.top, rect.right-7, rect.bottom-7)
            shot = sct.grab(bbox)
            mss_tools.to_png(shot.rgb, shot.size, output=r'paths\conf.png')

    def mudarregiao():
        global vvar
        global vvarnum
        global vpnname
        global rewards
        vvarnum = 0.85
        rewards = 'conf'
        vvar = f'{paises}'
        defs.telaconfig()
        defs.IA2(1)
        if existe2 == 'sim':
            pass
        else:
            defs.IA2(1)
            defs.click()
            vvar = f'{paises}kk'
            defs.telaconfig()
            defs.IA2(2)
            while not existe2 == 'sim':
                vvarnum = 0.8
                vvar = f'{paises}kk'
                defs.telaconfig()
                defs.IA2(2)
                team = nomear(nomebr)
                pydirectinput.write(str(team[0]))
                pydirectinput.write(str(team[1]))
            defs.click()
        vvar = f'{paises}'
        defs.telaconfig()
        defs.IA2(1)
        if existe2 == 'nao':
            defs.mudarregiao()
        rewards = 'rewardss'
        vvarnum = 0.9

    def printqrs():
        im2 = pyautogui.screenshot(r'paths\rewardss.png')

def guimain():
    global listafinal
    listafinal = []
    lista = str(emails + ':' + senhas + '\n')
    listafinal.append(lista)

    sg.theme('DarkAmber')
    layout = [[sg.Text("Bem vindo a farm de robux automatica!", font=('Axial', 25), size=(25, 3), text_color="orange")],
              [sg.Button("Iniciar", size=(25, 4), button_color=("Orange", "grey13"))],
              [sg.Button("Visualizar conta:senha", size=(25, 4), button_color=("Orange", 'grey13'))],
              [sg.Text("Feito por Shad, shadzz#5571", text_color="Orange")]]

    window = sg.Window("Comprador De Robux", layout, margins=(100, 100))

    while True:
        event, values = window.read()
        if event == "Visualizar conta:senha":
            gui2()
        if event == "Rodar":
            break
        elif event == sg.WIN_CLOSED:
            exit()
    window.close()

def gui2():
    global textx
    textx = ''.join(listafinal)
    layout = [[sg.Text("Emails         ||          Senhas" + '\n' + textx, key="new", font=('Axial', 12),
                       text_color="orange")]]
    window = sg.Window("Contas & Senhas", layout, margins=(100, 100))
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()


def main():
    global conta
    global senha
    global paises
    global nomebr
    global vpnome

    # p1 = Process(target=defs.abs, args=(10,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42"))
    # p1.start()
    # p2 = Process(target=defs.abs, args=(10,))
    # p2.start()
    # p1.join()
    # p2.join()
    # exit()

    for paises, nomebr, vpnome in zip(paisesnome, nomebrasileiro, vpne):
        time.sleep(4)
        defs.openvpn(True)
        continue
        exit()
        os.system('taskkill /f /im SystemSettings.exe')
        os.system('taskkill /f /im Microsoft.Rewards.Xbox.exe')

        oku1 = open(r"paisatual/okuser1.txt", "w+")
        oku2 = open(r"paisatual/okuser2.txt", "w+")
        pais_usuario = open(r"paisatual/pais.txt", "w+")

        if paises == 'eua':
            defs.abrir_bing()
        if paises == 'eua':
            if contasprontas == 'nao':
                defs.ativarconta()
                defs.contaconfig()
        os.system('taskkill /f /im SystemSettings.exe')
        defs.abrir_config()
        defs.telaconfig()
        defs.mudarregiao()
        os.system('taskkill /f /im SystemSettings.exe')
        defs.openvpn()
        defs.abrir_rewards()
        defs.antibug()

        pais_usuario.write(paises)
        pais_usuario.close()
        # Escreve o nome do pais em um txt

        if dcontas == 'sim':
            okusuario1 = open("paisatual/okusuario1.txt", "r")
            ok1 = okusuario1.read()
            while not ok1 == 'ok':
                okusuario1 = open("paisatual/okusuario1.txt", "r")
                ok1 = okusuario1.read()
            oku1.write('ok')
            oku1.close()
        defs.achar_task1k()
        defs.clicarnave()
        # Achar task de 1k, clicar na task da nave, abrir a abs.

        defs.tasksn('bing')
        if paises == "eua":
            defs.abs(25)
        defs.abs(45,
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42")
        defs.tasksn('loja')
        defs.tasksn('xbox')
        defs.tasksn('moeda')
        if paises == "eua":
            defs.tasksn('rewards')
        # Pesquisa.

        if dcontas == 'sim':
            okusuario2 = open("paisatual/okusuario2.txt", "r")
            ok = okusuario2.read()
            while not ok == 'ok':
                okusuario2 = open("paisatual/okusuario2.txt", "r")
                ok = okusuario2.read()
            oku2.write('ok')
            oku2.close()
        # Basicamente sistema de conversa entre 2 usuarios via arquivo txt
        os.system('taskkill /f /im Microsoft.Rewards.Xbox.exe')
        time.sleep(5)
        winsound.PlaySound(r'paths/si.wav', winsound.SND_FILENAME)
        time.sleep(5)

if __name__ == '__main__':
    main()