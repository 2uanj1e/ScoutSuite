from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.utils import get_non_provider_id


class Clusters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_clusters = await self.facade.elasticache.get_clusters(self.region, self.vpc)
        for raw_cluster in raw_clusters:
            name, resource = self._parse_cluster(raw_cluster)
            self[name] = resource

    def _parse_cluster(self, raw_cluster):
        raw_cluster['id'] = get_non_provider_id(raw_cluster.pop('CacheClusterId'))
        raw_cluster['name'] = raw_cluster.pop('CacheClusterId')
        raw_cluster['arn'] = 'arn:aws:elasticache:{}:{}:cluster/{}'.format(self.region,
                                                                             self.facade.owner_id,
                                                                             raw_cluster.get('name'))
        return raw_cluster['id'], raw_cluster
