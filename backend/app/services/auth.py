import requests

def get_azure_ad_token(tenant_id, client_id, client_secret):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://analysis.windows.net/powerbi/api/.default"
    }

    response = requests.post(url, data=data)

    # Se qualcosa va storto, vogliamo vedere subito l'errore
    if response.status_code != 200:
        raise Exception(f"Errore AAD: {response.text}")

    return response.json()["access_token"]