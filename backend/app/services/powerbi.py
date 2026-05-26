import requests
import os

from fastapi import HTTPException

from app.models.user import UserContext
from app.services.auth import get_azure_ad_token
from dotenv import load_dotenv

load_dotenv()


class PowerBIService:

    def get_embed_info(self, user: UserContext):
        tenant_id = os.environ["TENANT_ID"]
        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]

        workspace_id = os.environ["POWERBI_WORKSPACE_ID"]
        report_id = os.environ["POWERBI_REPORT_ID"]
        dataset_id = os.environ["POWERBI_DATASET_ID"]

        # 1. Token Azure AD
        aad_token = get_azure_ad_token(
            tenant_id,
            client_id,
            client_secret
        )

        headers = {
            "Authorization": f"Bearer {aad_token}",
            "Content-Type": "application/json"
        }

        # 2. GET embedUrl
        report_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}"

        response = requests.get(report_url, headers=headers)
        response.raise_for_status()

        embed_url = response.json()["embedUrl"]

        # 3. Generate embed token (RLS via CustomData)
        generate_token_url = "https://api.powerbi.com/v1.0/myorg/GenerateToken"

        body = {
            "datasets": [{"id": dataset_id}],
            "reports": [{"id": report_id}],
            "identities": [
                {
                    "username": "embedded-user",
                    "datasets": [dataset_id],
                    "customData": user.username
                }
            ]
        }

        print("CUSTOMDATA:", user.username)

        token_response = requests.post(generate_token_url, headers=headers, json=body)

        print("STATUS:", token_response.status_code)
        print("RESPONSE:", token_response.text)

        if token_response.status_code != 200:
            return {
                "error": token_response.text
            }

        embed_token = token_response.json()["token"]

        return {
            "embedUrl": embed_url,
            "accessToken": embed_token,
            "reportId": report_id,
            "tokenType": "Embed"
        }


    def get_token_on_behalf_of(self, user_token: str):
        tenant_id = os.environ["TENANT_ID"]
        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]

        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

        data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id": client_id,
            "client_secret": client_secret,
            "assertion": user_token,
            "scope": "https://analysis.windows.net/powerbi/api/.default",
            "requested_token_use": "on_behalf_of"
        }

        response = requests.post(url, data=data)

        # DEBUG
        print("OBO STATUS:", response.status_code)
        print("OBO RESPONSE:", response.text)

        if response.status_code != 200:
            return {
                "error": response.text
            }

        return response.json()["access_token"]


    def get_embed_info_user(self, user_token: str):
        workspace_id = os.environ["POWERBI_WORKSPACE_ID"]
        report_id = os.environ["POWERBI_REPORT_ID"]

        # 1. OBO → token Power BI utente
        aad_token = self.get_token_on_behalf_of(user_token)

        headers = {
            "Authorization": f"Bearer {aad_token}"
        }

        # 2. GET embed URL
        report_url = f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}"

        response = requests.get(report_url, headers=headers)
        response.raise_for_status()

        embed_url = response.json()["embedUrl"]

        return {
            "embedUrl": embed_url,
            "accessToken": aad_token,
            "reportId": report_id,
            "tokenType": "Aad"
        }