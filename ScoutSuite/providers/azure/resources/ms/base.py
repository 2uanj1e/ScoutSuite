from ScoutSuite.providers.azure.resources.base import AzureCompositeResources
from ScoutSuite.core.console import print_exception

from .conditional_access_policies import ConditionalAccessPolicies


class MS(AzureCompositeResources):
    _children = [
        (ConditionalAccessPolicies, 'conditional_access_policies'),
    ]

    async def fetch_all(self):
        await self._fetch_children(resource_parent=self)