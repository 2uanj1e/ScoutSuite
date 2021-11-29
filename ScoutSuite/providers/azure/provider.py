import os

from ScoutSuite.core.console import print_exception

from ScoutSuite.providers.base.provider import BaseProvider
from ScoutSuite.providers.azure.services import AzureServicesConfig


class AzureProvider(BaseProvider):
    """
    Implements provider for Azure
    """

    def __init__(self,
                 subscription_ids=[], all_subscriptions=None,
                 report_dir=None, timestamp=None, services=None, skipped_services=None,
                 result_format='json',
                 **kwargs):
        services = [] if services is None else services
        skipped_services = [] if skipped_services is None else skipped_services

        self.metadata_path = '%s/metadata.json' % os.path.split(os.path.abspath(__file__))[0]

        self.provider_code = 'azure'
        self.provider_name = 'Microsoft Azure'
        self.environment = 'default'

        self.programmatic_execution = kwargs['programmatic_execution']
        self.credentials = kwargs['credentials']

        if subscription_ids:
            self.subscription_ids = subscription_ids
        elif self.credentials.default_subscription_id:
            self.subscription_ids = [self.credentials.default_subscription_id]
        else:
            self.subscription_ids = []
        self.all_subscriptions = all_subscriptions

        try:
            self.account_id = self.credentials.get_tenant_id()
        except Exception as e:
            self.account_id = 'undefined'

        self.services = AzureServicesConfig(self.credentials,
                                            programmatic_execution=self.programmatic_execution,
                                            subscription_ids=self.subscription_ids,
                                            all_subscriptions=self.all_subscriptions)

        self.result_format = result_format

        super().__init__(report_dir, timestamp,
                         services, skipped_services, result_format)

    def get_report_name(self):
        """
        Returns the name of the report using the provider's configuration
        """
        try:
            return f'azure-tenant-{self.credentials.get_tenant_id()}'
        except Exception as e:
            print_exception(f'Unable to define report name: {e}')
            return 'azure'

    def preprocessing(self, ip_ranges=None, ip_ranges_name_key=None):
        """
        Tweak the Azure config to match cross-service resources and clean any fetching artifacts

        :param ip_ranges:
        :param ip_ranges_name_key:
        :return: None
        """
        ip_ranges = [] if ip_ranges is None else ip_ranges

        # Don't do this if we're running a local execution
        if not self.last_run:
            self._match_rbac_roles_and_principals()

        super().preprocessing()

    def _match_rbac_roles_and_principals(self):
        """
        Matches ARM role assignments to AAD service principals
        """
        try:
            if 'rbac' in self.service_list and 'aad' in self.service_list:
                for subscription in self.services['rbac']['subscriptions']:
                    for assignment in self.services['rbac']['subscriptions'][subscription]['role_assignments'].values():
                        role_id = assignment['role_definition_id'].split('/')[-1]
                        for group in self.services['aad']['groups']:
                            if group == assignment['principal_id']:
                                self.services['aad']['groups'][group]['roles'].append({'subscription_id': subscription,
                                                                                       'role_id': role_id})
                                self.services['rbac']['subscriptions'][subscription]['roles'][role_id]['assignments'][
                                    'groups'].append(group)
                                self.services['rbac']['subscriptions'][subscription]['roles'][role_id][
                                    'assignments_count'] += 1
                        for user in self.services['aad']['users']:
                            if user == assignment['principal_id']:
                                self.services['aad']['users'][user]['roles'].append({'subscription_id': subscription,
                                                                                     'role_id': role_id})
                                self.services['rbac']['subscriptions'][subscription]['roles'][role_id]['assignments'][
                                    'users'].append(user)
                                self.services['rbac']['subscriptions'][subscription]['roles'][role_id][
                                    'assignments_count'] += 1
                        for service_principal in self.services['aad']['service_principals']:
                            if service_principal == assignment['principal_id']:
                                self.services['aad']['service_principals'][service_principal]['roles'].append(
                                    {'subscription_id': subscription,
                                     'role_id': role_id})
                                self.services['rbac']['subscriptions'][subscription]['roles'][role_id]['assignments'][
                                    'service_principals'].append(service_principal)
                                self.services['rbac']['subscriptions'][subscription]['roles'][role_id][
                                    'assignments_count'] += 1
        except Exception as e:
            print_exception('Unable to match RBAC roles and principals: {}'.format(e))

        """
        Match Microsoft Graph conditional access policies to AAD users
        TODO: The preprocess logic below should be migrated to conditions.py and browser.py
        """
        try:
            if 'aad' in self.service_list and 'ms' in self.service_list:
                for policy in self.services['ms']['conditional_access_policies']:
                    # Find the policy based mfa that this user is included in by user id
                    include_users = self.services['ms']['conditional_access_policies'][policy]['includeUsers']
                    # Find the policy based mfa that this user is excluded from by user id
                    exclude_users = self.services['ms']['conditional_access_policies'][policy]['excludeUsers']
                    # Find the policy based mfa that this user is included in by group id
                    include_groups = self.services['ms']['conditional_access_policies'][policy]['includeGroups']
                    # Find the policy based mfa that this user is excluded from by group id
                    exclude_groups = self.services['ms']['conditional_access_policies'][policy]['excludeGroups']
                    for user in self.services['aad']['users']:
                        # Initialize attributes for this user
                        if 'includedByUsers' not in self.services['aad']['users'][user]:
                            self.services['aad']['users'][user]['includedByUsers'] = []
                        if 'excludedByUsers' not in self.services['aad']['users'][user]:
                            self.services['aad']['users'][user]['excludedByUsers'] = []
                        if 'includedByGroups' not in self.services['aad']['users'][user]:
                            self.services['aad']['users'][user]['includedByGroups'] = []
                        if 'excludedByGroups' not in self.services['aad']['users'][user]:
                            self.services['aad']['users'][user]['excludedByGroups'] = []

                        if (self.services['aad']['users'][user][
                                'id'] in exclude_users or 'All' in exclude_users) and 'mfa' in \
                                self.services['ms']['conditional_access_policies'][policy]['builtInControls']:
                            self.services['aad']['users'][user]['excludedByUsers'].append(
                                self.services['ms']['conditional_access_policies'][policy]['id'])
                        if (self.services['aad']['users'][user]['id'] in include_users or 'All' in include_users) and (
                                self.services['ms']['conditional_access_policies'][policy]['id'] not in
                                self.services['aad']['users'][user]['excludedByUsers']):
                            self.services['aad']['users'][user]['includedByUsers'].append(
                                self.services['ms']['conditional_access_policies'][policy]['id'])
                        if (any(group in exclude_groups for group in
                                self.services['aad']['users'][user]['groups']) or 'All' in exclude_groups) and 'mfa' in \
                                self.services['ms']['conditional_access_policies'][policy]['builtInControls']:
                            self.services['aad']['users'][user]['excludedByGroups'].append(
                                self.services['ms']['conditional_access_policies'][policy]['id'])
                        if (any(group in include_groups for group in
                                self.services['aad']['users'][user]['groups']) or 'All' in include_groups) and (
                                self.services['ms']['conditional_access_policies'][policy]['id'] not in
                                self.services['aad']['users'][user]['excludedByGroups'] and 'mfa' in
                                self.services['ms']['conditional_access_policies'][policy]['builtInControls']):
                            self.services['aad']['users'][user]['includedByGroups'].append(
                                self.services['ms']['conditional_access_policies'][policy]['id'])
        except Exception as e:
            print_exception('Unable to match conditional access policies to AAD users: {}'.format(e))
