from ScoutSuite.providers.azure.resources.base import AzureCompositeResources
from ScoutSuite.core.console import print_exception

from .conditional_access_policies import ConditionalAccessPolicies
from .credential_user_registration_details import CredentialUserRegistrationDetails


class MS(AzureCompositeResources):
    _children = [
        (ConditionalAccessPolicies, 'conditional_access_policies'),
        (CredentialUserRegistrationDetails, 'credential_user_registration_details')
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)