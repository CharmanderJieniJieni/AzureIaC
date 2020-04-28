from azure.common.credentials import ServicePrincipalCredentials, UserPassCredentials
import adal, sys, os, subprocess

# TENANT_ID = os.environ.get('TENANT_ID')
# CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
# CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
USERNAME = os.environ.get("AZURE_USERNAME")
PASSWORD = os.environ.get("AZURE_PASSWORD")
TENANT = os.environ.get("TENANT")

class SessionError(Exception):
    pass


class Session:
    def __init__(self):
        self.__credentials = ServicePrincipalCredentials(tenant=TENANT, client_id=USERNAME, secret=PASSWORD)

    @property
    def credentials(self):
        return self.__credentials

    def az_cli_login(self):
        """used for SDK incapable calls"""
        try:
            subprocess.run(["az","login","--service-principal","--username",USERNAME,"--password",PASSWORD,"--tenant",TENANT], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise SessionError(e.output)

