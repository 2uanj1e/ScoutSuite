This page details how to handle rate limiting. 

Request throttling is mostly an issue for AWS accounts, due to AWS' implementation of API request quotas (https://docs.aws.amazon.com/AWSEC2/latest/APIReference/throttling.html). As AWS API request quotas are per-service and account-wide, running Scout against an account where systems exist that make frequent/numerous API requests (e.g. DevOps pipelines) can easily reach the request quota, which will result in requests failing. This may not only be an issue when attempting to complete a scan, but can also negatively impact the other systems which rely on the APIs. Consequently, avoiding reaching the request quotas is preferable.

# Default Behavior

Scout handles rate limiting by implementing an incremental backoff. When the tool detects that the cloud provider is throttling requests, it will retry these requests with incremental delays. This is often sufficient to complete a run, without hitting the quotas "too often".

In addition to the default behaviour, a number of optional configurations can help ensure Scout does not reach these limits.

# Additional Options

The below options are available to limit the amount of requests made by Scout.

Limiting the number of running threads:

```console
  --max-workers MAX_WORKERS
                        Maximum number of threads (workers) used by Scout
                        Suite (default is 10)
```

Limiting the frequency of requests (per second):

```console
  --max-rate MAX_RATE   Maximum number of API requests per second
```

Identifying suitable values for the above can generally be done by trial and error. For AWS, if requests to a specific service are being throttled, reviewing the quotas for the service can help define a suitable request rate (e.g. https://docs.aws.amazon.com/AWSEC2/latest/APIReference/throttling.html).