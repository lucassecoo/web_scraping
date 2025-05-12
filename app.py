from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import json
import multiprocessing
from selenium.webdriver.common.action_chains import ActionChains
import random
import time

app = Flask(__name__)

with open('produtos.json') as f:
    produtos = json.load(f)

def buscar_preco_produto(produto_info):
    print(f"Iniciando a busca de preços para o produto: {produto_info['nome']}")  # qual produto está sendo processado
    urls = produto_info['urls']
    precos = {}
    url_mapeamento = {}

    for loja, info in urls.items():
        url = info['url']
        seletor = info['seletor']
        nome_loja = info['nome_loja']
        url_mapeamento[nome_loja] = url  # salva nome da loja com a URL

        print(f"Iniciando busca de preço na loja: {nome_loja} (URL: {url})")  # qual loja está sendo acessada

        # Configurações Selenium...
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        driver = webdriver.Chrome(service=Service('./chromedriver.exe'), options=chrome_options)
        driver.get(url)
        #chrome_options.add_argument("--disable-javascript")

        # Simula um movimento do mouse
        actions = ActionChains(driver)
        actions.move_by_offset(random.randint(0, 100), random.randint(0, 100)).perform()
        time.sleep(random.uniform(1, 3))  # Pausa aleatória entre 1 e 3 segundos


        try:
            time.sleep(5)
            wait = WebDriverWait(driver, 60)  # Aumente o tempo de espera se necessário
            print(f'Aguardando o elemento CSS do produto: {produto_info['nome']} na loja: {nome_loja}')  # Depuração: aguardando o seletor
            preco_elemento = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, seletor)) 
            ) # Depuração: aguarda o programa encontrar o seletor css por 60 segundos
            print(f'Elemento encontrado! Buscando o preço do produto: {produto_info['nome']} na loja: {nome_loja}') 
            preco_texto = preco_elemento.text
            match = re.search(r'R\$[\s\S]*\d+[\.,]\d{2}', preco_texto)
            if match:
                preco = float(match.group().replace('R$', '').replace('.', '').replace(',', '.').strip())
                precos[nome_loja] = preco
                print(f'Preço do {produto_info['nome']} encontrado na {nome_loja}: {preco}')  # Depuração: preço encontrado
            else:
                precos[nome_loja] = float('inf')
                print(f'Preço não encontrado na {nome_loja}, atribuindo infinito.')  # preço não encontrado
        except Exception as e:
            print(f"Erro ao buscar preço de {nome_loja}: {e}")  # erro durante a busca
            precos[nome_loja] = float('inf')
        finally:
            driver.quit()
            print(f"Fechando o navegador da loja: {nome_loja}")  # Depuração: navegador fechado

    if precos:
        menor_loja = min(precos, key=precos.get)
        menor_preco = precos[menor_loja]
        print(f"Menor preço encontrado para {produto_info['nome']}: {menor_preco} na loja {menor_loja}")  # Depuração: menor preço
    else:
        menor_preco = None
        menor_loja = None
        print(f"Nenhum preço encontrado para o produto {produto_info['nome']}")  # Depuração: sem preços

    return {
    'produto': produto_info['nome'],
    'imagem': produto_info.get('imagem', ''), 
    'descricao': produto_info.get('descricao', produto_info['nome']), 
    'menor_preco': menor_preco,
    'precos': precos,
    'menor_loja': menor_loja,
    'urls_mapeadas': url_mapeamento
}


@app.route('/')
def index():
    print("Iniciando o processo de busca de preços para todos os produtos...")
    resultados = []
    
    # Criar um pool de processos para rodar as buscas de preços
    with multiprocessing.Pool() as pool:
        # Dispara as tarefas em paralelo
        produtos_resultados = pool.map(buscar_preco_produto, produtos)
        resultados.extend(produtos_resultados)

    print("Busca concluída para todos os produtos!")
    return render_template('index.html', produtos=resultados)

if __name__ == '__main__':
    app.run(debug=True)
