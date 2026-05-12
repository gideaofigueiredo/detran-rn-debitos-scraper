# 🚗 DETRAN/RN - Extrator de Débitos Veiculares

Web scraper para extração automática de débitos veiculares do [portal do DETRAN/RN](https://portal.detran.rn.gov.br). Consulta em lote a partir de uma lista de placas e RENAVAMs, exportando os resultados para CSV.

## ✨ Funcionalidades

- 🔐 Login automático no portal do DETRAN/RN via CNPJ (Consultas só podem ser feitas na área logada do Portal de Serviços)
- 📋 Consulta em lote a partir de um arquivo CSV com placas e RENAVAMs
- 📊 Extração de débitos: descrição, nosso número, vencimento, valor e total
- 💾 Exportação dos resultados para CSV
- 📈 Barra de progresso com `tqdm`
- ⚡ Execução em modo headless (sem interface gráfica)

## 📁 Estrutura

```
├── extrairdebitos.py    # Script principal
├── veiculos.csv         # Lista de veículos para consulta (placa + renavam)
├── .env                 # Credenciais de acesso (não versionado)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/gideaofigueiredo/detran-rn-debitos-scraper.git
cd detran-rn-debitos-scraper
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Configure as credenciais

Crie um arquivo `.env` na raiz do projeto:

```env
LOGIN=seu_cnpj_aqui
SENHA=sua_senha_aqui
```

### 5. Prepare a lista de veículos

Edite o arquivo `veiculos.csv` com as placas e RENAVAMs dos veículos que deseja consultar:

```csv
PLACA,RENAVAM
ABC1D23,1234567890
XYZ9H87,9876543210
```

## ▶️ Uso

```bash
python extrairdebitos.py
```

O script irá:
1. Fazer login no portal do DETRAN/RN
2. Consultar cada veículo do `veiculos.csv`
3. Extrair os débitos encontrados
4. Salvar o resultado em `debito_veiculos_<CNPJ>.csv`

### Exemplo de saída

```
--- Iniciando o processo de extração de dados ---
Realizando login...
Extraindo débitos:  45%|████████████▌        | 53/118 [02:15<02:45, 2.55s/it]
Carregando dados de ABC1D23...
  → 10 débito(s) encontrado(s).

--- Dados salvos em 'debito_veiculos_12345678000100.csv' (250 registros) ---
Processo finalizado com sucesso!
```

### Estrutura do CSV de saída

| Placa | Renavam | Descrição | Nosso Número | Vencimento | Valor | Total |
|-------|---------|-----------|--------------|------------|-------|-------|
| ABC1D23 | 1234567890 | Licenciamento Anual - 2026 | 31112349... | 10/06/2026 | R$ 90,00 | R$ 90,00 |

## 🛠️ Tecnologias

- [Python 3.13](https://www.python.org/)
- [Playwright](https://playwright.dev/python/) — automação do navegador
- [pandas](https://pandas.pydata.org/) — manipulação de dados e exportação CSV
- [tqdm](https://tqdm.github.io/) — barra de progresso
- [python-dotenv](https://pypi.org/project/python-dotenv/) — gerenciamento de variáveis de ambiente

## ⚠️ Aviso

Este projeto é destinado exclusivamente para uso pessoal e educacional. Utilize com responsabilidade e de acordo com os termos de uso do portal do DETRAN/RN.
