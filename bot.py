import cv2 as cv
import subprocess
import mouse
import random
import pickle
from selenium.webdriver.common.keys import Keys
import json
import requests
import pydirectinput
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from winreg import *
import pyautogui
import pygetwindow
from joblib import Parallel, delayed
import ctypes
import urllib3
from mss import mss
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import mss.tools as mss_tools
import winsound
import time
import string
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
from selenium import webdriver

urllib3.disable_warnings()

def configuracoesgerais():
    with open('config.json') as config:
        perfect = json.load(config)
        vvarnum = perfect["configs"]["vvarnum"]
        contasprontas = perfect["configs"]["contasprontas"]
        rewards = perfect["configs"]["rewards"]
        dcontas = perfect["configs"]["dcontas"]
        delay = perfect["configs"]["delay"]
        paisesnome = perfect["paises"]["paisesnome"]
        vpne = perfect["paises"]["vpn"]

    name = os.getenv('username')
    localcon = fr'C:\Users\{name}\desktop'
    localrewards = fr'C:\Users\{name}\desktop'
    return (vvarnum,contasprontas,rewards,dcontas,localcon,localrewards,delay,paisesnome,vpne)

vvarnum,contasprontas,rewards,dcontas,localcon,localrewards,delay,paisesnome,vpne = configuracoesgerais()

with open('contas.json') as contas:
    acc = json.load(contas)
    emails = acc["email"][0]
    senha = acc["senhas"][0]

class defs():

    def openvpn(connect = False):
        subprocess.run('taskkill /f /im openvpn-gui.exe',capture_output=True)
        subprocess.run('taskkill /f /im openvpn.exe',capture_output=True)
        if connect:
            subprocess.Popen(r'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --command disconnect_all',shell=True)
            time.sleep(1)
            if vpnome != "Brazil":
                subprocess.Popen(fr'"C:\Program Files\OpenVPN\bin\openvpn-gui.exe" --connect {vpnome}.ovpn',shell=True)

        def get_ip():
            response = requests.get('https://www.trackip.net/ip?json').json()
            return response["IP"]

        def get_location():
            ip_address = get_ip()
            response = requests.get(f"https://api.findip.net/{ip_address}/?token=f3038d016cbc4511b927e2f792342c38").json()
            return response["country"]["names"]["en"]

        pais = get_location()
        if vpnome == "Eua":
            nome = "United States"
        elif vpnome == "Japan":
            nome = "Japan"
        elif vpnome == "Brazil":
            nome = "Brazil"
        while pais != nome:
            pais = get_location()
        print(pais)

    def abrir_rewards():
        lnk_path = f'{localrewards}\Microsoft Rewards.lnk'
        subprocess.call(lnk_path, shell=True)

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

    def questssite():
        global delay
        chrome_options = ChromeOptions()
        chrome_options.add_extension(r'testes\ABS.zip')

        driver = webdriver.Chrome('chromedriver', options=chrome_options)
        driver.get(
            "https://login.live.com/oauth20_authorize.srf?client_id=9c941f7c-a811-4e9c-8e66-29fdec50490f&scope=openid+profile+offline_access&redirect_uri=https%3a%2f%2frewards.bing.com%2fsignin-oidc&response_type=code&state=CfDJ8LbKok95JvtCpPQvgHivJ2oOUlAAWyaJkDAfSmfRusYfNHEokkOLAPjqIUezOyoi04jgL5UxQ7tScP5ck2VMxwB08sNcJEmn9jLdwbZr72PWADL1LC4M8oi4ETq1aEQT7wXI6VW3te0O7HuXHF5w13C3OM3nq4IbqcI5-xrQ5zmRG6u4jEc9NjbZb5dKotzmOiVDBGXh89dWLzfkzo3JBnWOetgDTvKPv2lU3GMso6RmH6ChaldXpbCqK-JxQpTTXUDipP9h2esQRoV4PW0sY9ePQjP5SteiAtM9Yf7CsFrrz7FgKcMoUYYEBi4hCt6m7izQBv6ha_QzlQ2fkg_CvysT4aaIkTG_zeCebI7r5QuNrfxMaQyufkcwVia679KnAGozWdNUgNKjuCKxXhNVlB4&response_mode=form_post&nonce=638078422087204591.YmY1MTAzMzQtZmYzYS00YjlkLTk1MjItMzllYzgzZDEwN2E0YmFhNmE4NTItNDBlMy00YWYzLTg4MDYtYzZhYTc0YWFhNzVm&code_challenge=QZfu44MPSFRqlLi7ztNUGr5Ygc7UQ1f7_liq5MQqy5o&code_challenge_method=S256&x-client-SKU=ID_NET6_0&x-client-Ver=6.23.1.0&uaid=3ede82304fa64dcbaccd22be1e2eeaa5&msproxy=1&issuer=mso&tenant=consumers&ui_locales=pt-BR&client_info=1&epct=AQABAAAAAAD--DLA3VO7QrddgJg7Wevrk34DsGWxchCtYRdtaXGiy4K5gK7nOlDnvbu3iGWm6V3QEQoiCYvjEWDCF-toLQNgoUNPPYdjm00mbWfF09sSxOByi_k-Xo7pXEJf5Uuy0sCt7uO_L-asA4IYXtPkw-VJNFJ-Lf0mxA4Djpjd7IXNlCkATMrQlZkSUN2z5KlLFFs5lEtuMVJJBIvEdGUGPYmFR2R4j26RoeqJAOUMUWzdXSAA&jshs=0&fl=easi2&cobrandid=03c8bbb5-2dff-4721-8261-a4ccff24c81a&lw=1#")
        defs.bingantibug('//*[@id="i0116"]', driver)
        driver.find_element('xpath', '//*[@id="i0116"]').send_keys(emails)

        defs.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
        time.sleep(2)

        defs.bingantibug('//*[@id="i0118"]', driver)
        driver.find_element('xpath', '//*[@id="i0118"]').send_keys(senha)

        defs.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element('xpath', '//*[@id="idSIButton9"]').click()

        defs.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element('xpath', '//*[@id="idSIButton9"]').click()

        delay = 999
        defs.bingantibug('//*[@id="dailypointColumnCalltoAction"]', driver)
        delay = 8
        driver.get("https://www.bing.com/rewards/signin")
        defs.bingantibug("/html/body/div[2]/div[2]/span/a", driver)
        driver.find_element('xpath', "/html/body/div[2]/div[2]/span/a").click()
        driver.get("https://rewards.bing.com/")
        defs.bingantibug('//*[@id="dailypointColumnCalltoAction"]', driver)
        time.sleep(2)
        print('achei')
        if paises == "eua":
            el = driver.find_elements(By.XPATH, "//*[contains(text(), 'answer')]")
        elif paises == "brazil":
            el = driver.find_elements(By.XPATH, "//*[contains(text(), 'conhece')]")
        for x in range(0, len(el)):
            if el[x].is_displayed():
                driver.implicitly_wait(10)
                ActionChains(driver).move_to_element(el[x]).click(el[x]).perform()
                driver.switch_to.window(driver.window_handles[0])
        el = driver.find_elements(By.CLASS_NAME, "ds-card-sec")
        for x in range(0, len(el)):
            if el[x].is_displayed():
                try:
                    el[x].send_keys(Keys.CONTROL + Keys.ENTER)
                except:
                    pass
        time.sleep(50)
        print('Quests do Site Finalizada')

    def achar_task1k():
        global vvar
        scroll = -3
        tem = defs.clicar(var = "1k", mouse=False, vp=False)
        while tem == 'nao':
            tem = defs.clicar(var = "1k", mouse=False, vp=False)
            if tem == 'sim':
                defs.click()
                time.sleep(5)
                return
            mouse.wheel(scroll)
            tem = defs.clicar(var = "sobre", mouse=False, vp=False)
            if tem == 'sim':
                scroll = 3
                break
        tem = defs.clicar(var = "1k", mouse=False, vp=False)
        if tem == 'sim':
            defs.click()
            time.sleep(5)
            return
        tem = defs.clicar(var = "mostrartodas", mouse=False, vp=False)
        if tem == 'nao':
            tem = defs.clicar(var = "mostrartodas", mouse=False, vp=False)
            while tem == 'nao':
                global vvarnum
                vvarnum = 0.7
                mouse.wheel(scroll)
                tem = defs.clicar(var = "mostrartodas", mouse=False, vp=False)
            vvarnum = 0.9
            tem = defs.clicar(var = "mostrartodas", vp=False)
            tem = defs.clicar(var = "mostrartodas", mouse=False, vp=False)
            while tem == 'sim':
                tem = defs.clicar(var = "mostrartodas", mouse=False, vp=False)
            mouse.wheel(scroll)
            tem = defs.clicar(var="1k", mouse=False, vp=False)
            while tem == 'nao':
                tem = defs.clicar(var="1k", mouse=False, vp=False)
                if tem == 'sim':
                    break
                pyautogui.moveTo(1400,750)
                scroll = -3
                mouse.wheel(scroll)
            tem = defs.clicar(var="cont", vp= False)
            tem = defs.clicar(var="1000puntos", mouse=False, vp=False)
            while tem != "sim":
                tem = defs.clicar(var="1000puntos", mouse=False, vp=False)

    def clicarnave():
        global vvar
        tem = defs.clicar("web")
        tem = defs.clicar("nave", mouse=False)
        while not tem == 'sim':
            tem = defs.clicar("nave", mouse=False)
        tem = defs.clicar("conc", mouse=False)
        while tem == 'nao':
            tem = defs.clicar("nave")
            tem = defs.clicar("qrnave", mouse=False, vp=False)
            while tem == 'nao':
                tem = defs.clicar("qrnave", mouse=False, vp=False)
            pyautogui.press('enter')
            vvar = 'moedagigante'
            defs.tentar()
            defs.IA2()
            while existe2 == 'sim':
                vvar = 'moedagigante'
                defs.tentar()
                defs.IA2()
            subprocess.run('taskkill /f /im msedge.exe', capture_output=True)
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
        chrome_options.headless = True

        driver = webdriver.Chrome('chromedriver',options=chrome_options)
        driver.get('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&id=264960&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253ftoWww%253d1%2526redig%253d3389C7EB769248EB8086CD884D2595CF%2526wlexpsignin%253d1%26sig%3d0A6C406EFB686EA604025253FA7C6FDA&wp=MBI_SSL&lc=1046&CSRFToken=9399de60-9308-4156-8667-596b86a444d0&aadredir=1')

        defs.bingantibug('//*[@id="i0116"]', driver)
        driver.find_element('xpath', '//*[@id="i0116"]').send_keys(emails)

        defs.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
        time.sleep(2)

        defs.bingantibug('//*[@id="i0118"]', driver)
        driver.find_element('xpath', '//*[@id="i0118"]').send_keys(senha)

        defs.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element('xpath', '//*[@id="idSIButton9"]').click()

        defs.bingantibug('//*[@id="idSIButton9"]', driver)
        driver.find_element('xpath', '//*[@id="idSIButton9"]').click()
        pickle.dump( driver.get_cookies() , open(r"paths\cookies.pkl","wb"))
        print('Loguei no bing')
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

    def achar_task500():
        global vvar
        defs.clicar(var="500",vp=False)
        tem = defs.clicar(var="avt", vp=False,mouse=False)
        while tem == "nao":
            tem = defs.clicar(var="avt", vp=False, mouse=False)

        tem = defs.clicar(var="conc", mouse=False)
        while tem == 'nao':
            tem = defs.clicar(var="games")
            tem = defs.clicar(var="detalhamento", mouse=False, vp=False)
            while tem == 'nao':
                tem = defs.clicar(var="detalhamento", mouse=False, vp=False)
            tem = defs.clicar(var="voltar", vp=False)
            tem = defs.clicar(var="icasa", vp=False, mouse=False)
            while tem == 'nao':
                tem = defs.clicar(var="icasa", vp=False, mouse=False)
        tem = defs.clicar(var="voltar", vp=False)
        tem = defs.clicar(var="detalhamento", mouse=False, vp=False)
        while tem == 'nao':
            tem = defs.clicar(var="detalhamento", mouse=False, vp=False)
        tem = defs.clicar(var="detalhamento", num=1, vp=False)

    def abs(num, agent = "user-agent=Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"):
        global driver3  
        chrome_options = ChromeOptions()
        chrome_options.add_argument(agent)
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        chrome_options.headless = True

        driver3 = webdriver.Chrome('chromedriver',desired_capabilities=caps, options=chrome_options)
        driver3.get('http://bing.com')
        time.sleep(2)
        cookies = pickle.load(open(r"paths\cookies.pkl", "rb"))
        for cookie in cookies:
            driver3.add_cookie(cookie)
        Resultyy = ''.join(random.choice(string.ascii_letters) for i in range(8))

        urls = f'https://www.bing.com/search?q={Resultyy}'
        for posts in range(num):
            driver3.get(urls)    
            driver3.execute_script("window.open('');")
            chwd = driver3.window_handles
            driver3.switch_to.window(chwd[-1])
            Resultyy = ''.join(random.choice(string.ascii_letters) for i in range(8))
            urls = f'https://www.bing.com/search?q={Resultyy}'
        driver3.quit()

    def clicar(var, mouse = True, num = 0, vp = True):
        global vvar
        if vp:
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
        else:
            if mouse:
                vvar = var
                defs.tentar()
                defs.IA2()
                defs.click(num)
            else:
                vvar = var
                defs.tentar()
                defs.IA2()
                return existe2

    def tasksn(qual):
        def clicarbing(fazer='nao'):
            global vvar
            defs.clicar("conc")
            tem = defs.clicar("bing", mouse=False)
            while tem == 'nao':
                pydirectinput.press('down')
                time.sleep(0.5)
                tem = defs.clicar("bing", mouse=False)
            tem = defs.clicar("conc", mouse=False)
            if fazer == 'nao':
                if tem == 'nao':
                    results = Parallel(n_jobs=6)(delayed(defs.abs)(10) for _ in range(0,6))
            if fazer == 'sim':
                defs.abs(10)
            tem = defs.clicar("conc", mouse=False)
            while tem == 'nao':
                print('eu vejo o bing')
                defs.clicar("bing")
                tem = defs.clicar(var="qr", mouse=False,vp=False)
                while tem == 'nao':
                    tem = defs.clicar(var="qr", mouse=False,vp=False)
                pyautogui.press('enter')
                vvar = "bing"
                defs.tentarvp()
                defs.IA2()
                while existe2 == 'sim':
                    vvar = "bing"
                    defs.tentar()
                    defs.IA2()
                subprocess.run('taskkill /f /im msedge.exe', capture_output=True)
                vvar = "bing"
                defs.tentarvp()
                defs.IA2()
                while existe2 == 'sim':
                    vvar = "bing"
                    defs.tentarvp()
                    defs.IA2()
                time.sleep(4)
                clicarbing('sim')

        def clicarloja():
            global vvar
            global vvarnum
            defs.clicar("conc")
            tem = defs.clicar(var="loja",mouse=False)
            while tem == 'nao':
                pydirectinput.press('down')
                time.sleep(0.5)
                tem = defs.clicar(var="loja",mouse=False)
            tem = defs.clicar(var="conc",mouse=False)
            while tem == 'nao':
                tem = defs.clicar(var="loja")
                tem = defs.clicar(var="voltaganhos",mouse=False,vp=False)
                while tem == 'nao':
                    tem = defs.clicar(var="voltaganhos",mouse=False,vp=False)
                tem = defs.clicar(var="voltar",vp=False)
                tem = defs.clicar(var="moedagigante",vp=False,mouse=False)
                while tem == 'nao':
                    tem = defs.clicar(var="moedagigante",vp=False,mouse=False)
                vvarnum = 0.9
                clicarloja()
        
        def clicarxbox():
            global vvar
            defs.clicar("conc")
            tem = defs.clicar(var="xbox",mouse=False)
            while tem == 'nao':
                pydirectinput.press('down')
                time.sleep(0.5)
                tem = defs.clicar(var="xbox", mouse=False)
            tem = defs.clicar(var="conc", mouse=False)
            while tem == 'nao':
                print('eu vejo o xbox')
                tem = defs.clicar(var="xbox")
                tem = defs.clicar(var="novoapp", mouse=False,vp=False)
                while tem == 'nao':
                    tem = defs.clicar(var="novoapp", mouse=False,vp=False)
                tem = defs.clicar(var="bola",vp=False)
                clicarxbox()

        def clicarmoeda():
            global vvar
            global vvarnum
            defs.clicar("conc")
            tem = defs.clicar(var="moeda",mouse=False)
            while tem == 'nao':
                pydirectinput.press('down')
                time.sleep(0.5)
                tem = defs.clicar(var="moeda",mouse=False)
            tem = defs.clicar(var="conc",mouse=False)
            while tem == 'nao':
                print('eu vejo a moeda')
                tem = defs.clicar(var="moeda")
                tem = defs.clicar(var="moedas",mouse=False, vp=False)
                while tem == 'nao':
                    tem = defs.clicar(var="moedas",mouse=False, vp=False)
                tem = defs.clicar(var="voltar",vp=False)
                tem = defs.clicar(var="moedagigante",vp=False,mouse=False)
                while tem == 'nao':
                    tem = defs.clicar(var="moedagigante",vp=False,mouse=False)
                vvarnum = 0.9
                clicarmoeda()

        def clicarrewards():
            global vvar
            global vvarnum
            defs.clicar("conc")
            tem = defs.clicar(var="rewards",mouse=False)
            while not tem == 'sim':
                pydirectinput.press('down')
                time.sleep(0.5)
                tem = defs.clicar(var="rewards",mouse=False)
            tem = defs.clicar(var="conc",mouse=False)
            while tem == 'nao':
                tem = defs.clicar(var="rewards")
                tem = defs.clicar(var="detalhamento",mouse=False,vp=False)
                while tem == 'nao':
                    tem = defs.clicar(var="detalhamento",mouse=False,vp=False)
                tem = defs.clicar(var="voltar",vp=False)
                tem = defs.clicar(var="moedagigante",vp=False,mouse=False)
                while tem == 'nao':
                    tem = defs.clicar(var="moedagigante",vp=False,mouse=False)
                vvarnum = 0.9
                clicarrewards()
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

            bbox = (rect.left, rect.top, rect.right, rect.bottom)
            shot = sct.grab(bbox)
            mss_tools.to_png(shot.rgb, shot.size, output=fr"paths\rewardss.png")

    def tentarvp():
        time.sleep(0.2)

        with mss() as sct:
            global bbox
            hwnd = ctypes.windll.user32.FindWindowW(0, 'Microsoft Rewards')
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
            monitor = sct.monitors[1]

            bbox = (rect.left+750, rect.top+550, rect.right-10, rect.bottom-10)
            shot = sct.grab(bbox)
            mss_tools.to_png(shot.rgb, shot.size, output=r'paths\rewardss.png')

    # def printqrs():
    #     im2 = pyautogui.screenshot(r'paths\rewardss.png')

    def mudarregiao():
        if paises == "eua":
            name = "US"
            nation = "244"
        elif paises == "brazil":
            name = "BR"
            nation = "32"
        elif paises == "japan":
            name = "JP"
            nation = "122"

        key = OpenKey(HKEY_CURRENT_USER, r'Control Panel\International\Geo', 0, KEY_ALL_ACCESS)
        SetValueEx(key, "Name", 0, REG_SZ, name)
        SetValueEx(key, "Nation", 0, REG_SZ, nation)

    def detalhamento():
        global vvar
        global vvarnum
        time.sleep(5)
        vvarnum = 0.75
        if paises != "japan":
            tem2 = defs.clicar(var="explore", mouse=False, vp=False)
        else:
            tem2 = defs.clicar(var="xing", mouse=False, vp=False)
        vvarnum = 0.9
        tem = defs.clicar(var="detalhamento",mouse=False,vp=False)
        if tem == "sim":
            return
        elif tem2 == "sim":
            if paises != "japan":
                defs.clicar(var="explore", vp=False)
            else:
                defs.clicar(var="xing", vp=False)
        else:
            time.sleep(5)
            tem = defs.clicar(var="detalhamento", mouse=False, vp=False)
            vvarnum = 0.75
            if paises != "japan":
                tem2 = defs.clicar(var="explore", mouse=False, vp=False)
            else:
                tem2 = defs.clicar(var="xing", mouse=False, vp=False)
            vvarnum = 0.9
            if tem2 == "sim":
                if paises != "japan":
                    defs.clicar(var="explore", vp=False)
                else:
                    defs.clicar(var="xing", vp=False)
            elif tem != "sim":
                subprocess.run('taskkill /f /im Microsoft.Rewards.Xbox.exe', capture_output=True)
                time.sleep(1)
                defs.abrir_rewards()
                time.sleep(2)
                defs.detalhamento()



def main():
    global conta
    global senha
    global paises
    global nomebr
    global vpnome

    for paises, vpnome in zip(paisesnome, vpne):
        subprocess.run('taskkill /f /im Microsoft.Rewards.Xbox.exe', capture_output=True)

        if paises == 'eua':
            defs.abrir_bing()
        if paises == 'eua':
            if contasprontas == 'nao':
                defs.ativarconta()
                defs.contaconfig()
        defs.mudarregiao()
        defs.openvpn(True)
        defs.abrir_rewards()
        time.sleep(3)
        win = pygetwindow.getWindowsWithTitle('Microsoft Rewards')[0]
        time.sleep(2)
        defs.detalhamento()
        if paises == "eua":
            time.sleep(2)
            defs.achar_task500()
        time.sleep(3)
        defs.achar_task1k()
        defs.clicarnave()
        # Achar task de 1k, clicar na task da nave, abrir a abs.

        defs.tasksn('bing')

        # if paises == "eua":
        #     results = Parallel(n_jobs=4)(delayed(defs.abs)(10) for _ in range(0, 3))
        # results = Parallel(n_jobs=4)(delayed(defs.abs)(10,  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42") for _ in range(0, 4))
        defs.tasksn('loja')
        defs.tasksn('xbox')
        defs.tasksn('moeda')
        if paises == "eua":
            defs.tasksn('rewards')
        # Pesquisa.

        subprocess.run('taskkill /f /im Microsoft.Rewards.Xbox.exe', capture_output=True)
        if paises != "japan":
            defs.questssite()
        winsound.PlaySound(r'paths/si.wav', winsound.SND_FILENAME)

if __name__ == '__main__':
    main()
