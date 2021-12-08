from ScoutSuite.providers.azure.resources.base import AzureResources

class CredentialUserRegistrationDetails(AzureResources):
    async def fetch_all(self):
        for raw_credential_user_registration_detail in await self.facade.ms.get_credential_user_registration_details():
            id, credential_user_registration_detail = self._parse_credential_user_registration_detail(raw_credential_user_registration_detail)
            self[id] = credential_user_registration_detail

    def _parse_credential_user_registration_detail(self, raw_credential_user_registration_detail):
        credential_user_registration_detail = {}
        credential_user_registration_detail['id'] = credential_user_registration_detail['id']
        credential_user_registration_detail['userPrincipalName'] = credential_user_registration_detail['userPrincipalName']
        credential_user_registration_detail['userDisplayName'] = credential_user_registration_detail['userDisplayName']
        credential_user_registration_detail['isRegistered'] = credential_user_registration_detail['isRegistered']
        credential_user_registration_detail['isEnabled'] = credential_user_registration_detail['isEnabled']
        credential_user_registration_detail['isCapable'] = credential_user_registration_detail['isCapable']
        credential_user_registration_detail['isMfaRegistered'] = credential_user_registration_detail['isMfaRegistered']
        credential_user_registration_detail['authMethods'] = credential_user_registration_detail['authMethods']
        return credential_user_registration_detail['id'], credential_user_registration_detail