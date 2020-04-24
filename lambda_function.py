import os
import logging
import elasticsearch
import curator
import json

logger = logging.getLogger()

client = elasticsearch.Elasticsearch(
    [
        {
            "host": os.environ['ES_HOSTNAME'],
            'port': 443
        }
    ],
    use_ssl=True
)


def lambda_handler(event, context):

    try:
        retention_days = int(os.environ['ES_RETENTION_DAYS'])
    except ValueError:
        logger.error("ES_RETENTION_DAYS must be set as environment variable")
        return

    index_list = curator.IndexList(client)
    index_list.filter_by_regex(
        kind='prefix',
        value='jaeger-'
    )

    index_list.filter_by_age(
        source='creation_date',
        direction='older',
        unit='days',
        unit_count=retention_days
    )

    return index_list.working_list()
