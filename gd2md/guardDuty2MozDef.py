import boto3
import json
import logging

from datetime import datetime
from os import getenv
from pytz import timezone


logger = logging.getLogger(__name__)
SNS_OUTPUT_TOPIC_ARN = getenv('SNS_OUTPUT_TOPIC_ARN')

def convert_my_iso_8601(iso_8601):
    assert iso_8601[-1] == 'Z'
    iso_8601 = iso_8601[:-1] + '000'
    iso_8601_dt = datetime.strptime(iso_8601, '%Y-%m-%dT%H:%M:%S.%f')
    return str(iso_8601_dt.replace(tzinfo=timezone('UTC')))

def send_to_sns(event, sns_client):
    """Send the transformed message to the SNS topic that outputs to another SQS queue."""
    return sns_client.publish(
        TopicArn=SNS_OUTPUT_TOPIC_ARN,
        Message=json.dumps(event)
    )

def _get_resource_info(guardduty_event):
    resource = guardduty_event['detail'].get('resource', {})
    instance_detail = resource.get('instanceDetails', None)
    if instance_detail is not None:
        return instance_detail.get('instanceId')
    else:
        return 'guardduty-{account_id}'.format(account_id=event.get('account'))

def transform_event(event):
    """Take guardDuty SNS notification and turn it into a standard MozDef event."""
    guardduty_event = json.loads(event['Sns']['Message'])
    mozdef_event = {
        'timestamp': convert_my_iso_8601(event['Sns'].get('Timestamp')),
        'hostname': _get_resource_info(guardduty_event),
        'processname': 'guardduty',
        'processid': 1337,
        'severity': 'INFO',
        'summary': guardduty_event.get('title'),
        'category': guardduty_event.get('type'),
        'source': 'guardduty',
        'tags': [
            guardduty_event['detail']['service']['action']['actionType']
        ],
        'details': guardduty_event.get('detail')
    }
    return mozdef_event

def handle(event, context):
    """Basic lambda handler."""
    sns_client = boto3.client('sns')
    for record in event.get('Records', []):
        mozdef_event = transform_event(record)
        res = send_to_sns(mozdef_event, sns_client)
    return mozdef_event
