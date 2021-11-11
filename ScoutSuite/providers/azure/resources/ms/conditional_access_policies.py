from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.providers.utils import get_non_provider_id


class ConditionalAccessPolicies(AzureResources):
    async def fetch_all(self):
        for raw_conditional_access_policy in self.facade.ms.get_conditional_access_policies()['value']:
            id, conditional_access_policy = self._parse_conditional_access_policies(raw_conditional_access_policy)
            self[id] = conditional_access_policy

    def _parse_conditional_access_policies(self, raw_conditional_access_policy):
        conditional_access_policy = {}
        conditional_access_policy['id'] = get_non_provider_id(raw_conditional_access_policy['id'])
        conditional_access_policy['displayName'] = raw_conditional_access_policy['displayName']
        conditional_access_policy['createdDateTime'] = raw_conditional_access_policy['createdDateTime']
        conditional_access_policy['modifiedDateTime'] = raw_conditional_access_policy['modifiedDateTime']
        conditional_access_policy['state'] = raw_conditional_access_policy['state']
        conditional_access_policy['userRiskLevels'] = raw_conditional_access_policy['conditions']['userRiskLevels']
        conditional_access_policy['clientAppTypes'] = raw_conditional_access_policy['conditions']['clientAppTypes']
        conditional_access_policy['devices'] = raw_conditional_access_policy['conditions']['devices']
        conditional_access_policy['includeApplications'] = raw_conditional_access_policy['conditions']['applications']['includeApplications']
        conditional_access_policy['excludeApplications'] = raw_conditional_access_policy['conditions']['applications']['excludeApplications']
        conditional_access_policy['includeUserActions'] = raw_conditional_access_policy['conditions']['applications']['includeUserActions']
        conditional_access_policy['includeAuthenticationContextClassReferences'] = raw_conditional_access_policy['conditions']['applications']['includeAuthenticationContextClassReferences']
        conditional_access_policy['includeUsers'] = raw_conditional_access_policy['conditions']['users']['includeUsers']
        conditional_access_policy['excludeUsers'] = raw_conditional_access_policy['conditions']['users']['excludeUsers']
        conditional_access_policy['includeGroups'] = raw_conditional_access_policy['conditions']['users']['includeGroups']
        conditional_access_policy['excludeGroups'] = raw_conditional_access_policy['conditions']['users']['excludeGroups']
        conditional_access_policy['includeRoles'] = raw_conditional_access_policy['conditions']['users']['includeRoles']
        conditional_access_policy['excludeRoles'] = raw_conditional_access_policy['conditions']['users']['excludeRoles']
        if raw_conditional_access_policy['conditions']['locations']:
            conditional_access_policy['includeLocations'] = raw_conditional_access_policy['conditions']['locations']['includeLocations']
            conditional_access_policy['excludeLocations'] = raw_conditional_access_policy['conditions']['locations']['excludeLocations']
        conditional_access_policy['operator'] = raw_conditional_access_policy['grantControls']['operator']
        conditional_access_policy['builtInControls'] = raw_conditional_access_policy['grantControls']['builtInControls']
        conditional_access_policy['customAuthenticationFactors'] = raw_conditional_access_policy['grantControls']['customAuthenticationFactors']
        return conditional_access_policy['id'], conditional_access_policy