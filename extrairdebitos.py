import playwright.sync_api as pw
from dotenv import load_dotenv
import os
import pandas as pd
from tqdm import tqdm

load_dotenv()

LOGIN = os.getenv("LOGIN")
SENHA = os.getenv("SENHA")
NOME_AQUIVO = f"debito_veiculos_{LOGIN}.csv"

print("--- Iniciando o processo de extração de dados ---")

with pw.sync_playwright() as p:
    # config navegador
    navegador = p.chromium.launch(headless=False)
    contexto = navegador.new_context()
    pagina = contexto.new_page()

    print("Realizando login...")
    pagina.goto("https://portal.detran.rn.gov.br/cpforcnpj")
    pagina.get_by_role("textbox", name="CNPJ").fill(os.getenv("LOGIN"))
    pagina.get_by_role("textbox", name="Senha").fill(os.getenv("SENHA"))
    pagina.get_by_role("button", name="Entrar").click()

    # Espera o menu carregar
    pagina.get_by_role("link", name="Veículo").wait_for()
    pagina.get_by_role("link", name="Veículo").click()
    
    pagina.get_by_role("link", name="Consulta de Veículo").click()

    veiculos = pd.read_csv("veiculos.csv")
    todos_debitos = []

    pbar = tqdm(veiculos.iterrows(), total=len(veiculos))

    for _, l in pbar:
        pbar.set_description(f"Processando {l['PLACA']}...")
        PLACA = l["PLACA"]
        RENAVAM = str(l["RENAVAM"])
        pagina.get_by_role("textbox", name="Placa").fill(PLACA)
        pagina.get_by_role("textbox", name="Renavam").fill(RENAVAM)
        pagina.get_by_role("button", name="Avançar").click()

        #print(f"Carregando dados de {PLACA}...")
        pagina.wait_for_timeout(2500) # Tempo para o DB do Detran responder
        pagina.wait_for_selector("table > tbody > tr", state="visible")

        dados_veiculo = pagina.locator("table > tbody > tr > td:has(span)").all()

        try:
            pagina.wait_for_selector("p-table > div > div > table > tbody > tr", state="visible", timeout=5000) # Espera até que uma tabela de débitos seja carregada
            linhas = pagina.locator("p-table > div > div > table > tbody > tr").all()

            for linha in linhas:
                celulas = linha.locator("td").all()
                if len(celulas) >= 5:
                    debito = {
                        "Placa": PLACA,
                        "Renavam": RENAVAM,
                        "Descrição": celulas[0].inner_text().strip(),
                        "Nosso Número": celulas[1].inner_text().strip(),
                        "Vencimento": celulas[2].inner_text().strip(),
                        "Valor": celulas[3].inner_text().strip(),
                        "Total": celulas[4].inner_text().strip(),
                    }
                    todos_debitos.append(debito)

            #print(f"  → {len(todos_debitos)} débito(s) encontrado(s).")

        except pw.TimeoutError:
            #print(f"  → Nenhum débito encontrado para {PLACA}.")
            pass

        pagina.get_by_role("link", name="Consulta de Veículo").click()
        pagina.get_by_role("textbox", name="Placa").wait_for()

    # Salva em CSV após processar todos os veículos
    df = pd.DataFrame(todos_debitos)
    df.to_csv(NOME_AQUIVO, index=False, encoding="utf-8-sig")
    print(f"\n--- Dados salvos em '{NOME_AQUIVO}' ({len(df)} registros) ---")
    print("Processo finalizado com sucesso!")