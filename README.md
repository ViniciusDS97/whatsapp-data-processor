# Comma API Data Processor

Este projeto é uma ferramenta desenvolvida em Python para integração com a API Comma. Ele permite a extração e enriquecimento de dados de solicitações, além de gerar relatórios em formato Excel.

## Funcionalidades

- **Extração de Dados**: Recupera informações de requisições através da API Comma usando um número de origem.
- **Enriquecimento de Dados**: Obtém detalhes adicionais sobre cada solicitação, como status e informações do cliente.
- **Exportação para Excel**: Gera um arquivo Excel contendo os dados processados, facilitando a análise e visualização.

## Requisitos

- Python 3.11 ou superior
- Bibliotecas:
  - `requests`
  - `pandas`
  - `openpyxl` (para exportação em Excel)

Você pode instalar as bibliotecas necessárias utilizando o seguinte comando:

```bash
pip install requests pandas openpyxl
