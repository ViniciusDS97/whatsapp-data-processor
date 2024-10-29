import requests
import base64
import pandas as pd
from config import login, secret, src_number

class CommaAPI:
    def __init__(self, login, secret, src_number):
        """
        Inicializa a lasse CommaAPI com credenciais de autenticação e número de origem.

        Args:
            login (str): Nome de usuário para autenticação.
            secret (str): Senha ou chave secreta para autenticação.
            src_number (str): Número de origem associado às requisições da API.

        """
        self.login = login
        self.secret = secret
        self.src_number = src_number
        self.auth_string = f"{login}:{secret}"
        self.auth_encoded = base64.b64encode(self.auth_string.encode('utf-8')).decode('utf-8')
        self.headers = {
            'Authorization': f'Basic {self.auth_encoded}'
        }
        self.base_url = 'https://comma-backend.azurewebsites.net/api/v1'
        self.df = pd.DataFrame()

    def fetch_request_ids(self):
        """
        Obtém os requestIds associados ao número de origem (src_number).
        
        Returns: 
            bools: Retorna True se a operação for bem-sucedida e False caso contrário.
        """

        url = f'{self.base_url}/request_ids/{self.src_number}'
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                data = [data]
            self.df = pd.concat([self.df, pd.DataFrame(data)], ignore_index=True)
            return True
        else:
            print(f"Erro ao obter requestIds: {response.status_code} - {response.text}")
            return False

    def fetch_request_status(self, request_id):
        """
        Obtém o status de um requestId específico.

        Args:
            request_id (str): O ID da requisição cujo status será consultado.

        Returns:
            dict or None: Retorna os dados de status se a requisição for bem-sucedida, ou None em caso de falha.
        """ 
        status_url = f'{self.base_url}/request_status/{request_id}'
        status_response = requests.get(status_url, headers=self.headers)

        if status_response.status_code == 200:
            return status_response.json()
        else:
            print(f"Erro ao obter status para requestId {request_id}: {status_response.status_code} - {status_response.text}")
            return None     
        
    def requestid_data(self):
        """
        Enriquece os dados obtidos com informações detalhadas de status para cada requestId.

        Este método busca o status de cada requestId e compila as inormações em um DataFrame
        para fácil análise e exportação.
        """

        requestid_rows = []
        for index, row in self.df.iterrows():
            request_id = row['requestId']  # Corrigido para 'requestId'
            print(f"Buscando status para requestId: {request_id}")
            status_data = self.fetch_request_status(request_id)

            if status_data:
                base_row = {
                    'category': row['category'],
                    'email': row['email'],
                    'name': row['name'],
                    'registerDate': row['registerDate'],
                    'requestDate': row['requestDate'],
                    'requestId': request_id,
                    'requesterEmail': row['requesterEmail'],
                    'sms': row['sms'],
                    'srcNumber': row['srcNumber'],
                    'status': row['status'],
                    'templateId': row['templateId'],
                    'whatsapp': row['whatsapp'],
                    'appName': status_data.get('appName', None),
                    'commaNumber': status_data.get('commaNumber', None),
                    'request': status_data.get('request', None),
                    'requestDateTime': status_data.get('requestDateTime', None),
                    'requestTitle': status_data.get('requestTitle', None),
                    'clients': status_data.get('clients', [])
                }
                requestid_rows.append(base_row)

        requestid_df = pd.DataFrame(requestid_rows)
        exploded_df = requestid_df.explode('clients', ignore_index=True)

        if 'clients' in exploded_df.columns:
            clients_df = pd.json_normalize(exploded_df['clients'])
            self.requestid_df = pd.concat([exploded_df.drop(columns='clients'), clients_df], axis=1)  # Corrigido para 'self.requestid_df'
        else:
            self.requestid_df = exploded_df  # Se não houver 'clients', apenas define como 'exploded_df'

    def export_to_excel(self, filename='dados_comma.xlsx'):
        """
        Exporta os dados enriquecidos para um arquivo Excel.

        Args:
            filename (str): O nome do arquivo Excel a ser criado (padrão: 'dados_comma.xlsx').
        """

        self.requestid_df.to_excel(filename, index=False)
        print(f"Dados enriquecidos exportados para '{filename}' com sucesso.")

    def run(self):
        """
        Executa o fluxo completo de obtenção e processamento de dados.

        Este método coordena a chamada dos métodos para buscar requestIds, enriquecer os dados
        e exportá-los para um arquivo Excel.
        """

        if self.fetch_request_ids():
            self.requestid_data()
            self.export_to_excel()

if __name__ == '__main__':
    api = CommaAPI(login, secret, src_number)
    api.run()
