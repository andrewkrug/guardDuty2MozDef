import boto3
import json
import os
import unittest


from moto import mock_sns, mock_sqs


class guardDuty2MozDefTest(unittest.TestCase):
    @mock_sns
    def test_handle(self):
        conn = boto3.client('sns', region_name='us-west-2')
        conn.create_topic(Name="fake-gd2md-topic")
        response = conn.list_topics()
        topic_arn = response["Topics"][0]['TopicArn']
        os.environ['SNS_OUTPUT_TOPIC_ARN'] = topic_arn
        fixture = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'fixtures/sample_event_1.json'
        )

        with open(fixture) as event_json:
            event = json.load(event_json)

        from gd2md import guardDuty2MozDef
        res = guardDuty2MozDef.handle(event=event, context={})
        assert res is not None

    @mock_sns
    def test_send_to_sns(self):
         conn = boto3.client('sns', region_name='us-west-2')
         conn.create_topic(Name="fake-gd2md-topic")
         response = conn.list_topics()
         topic_arn = response["Topics"][0]['TopicArn']

         os.environ['SNS_OUTPUT_TOPIC_ARN'] = topic_arn

         assert os.getenv('SNS_OUTPUT_TOPIC_ARN') is not None

         mock_event = {}

         from gd2md import guardDuty2MozDef
         res = guardDuty2MozDef.send_to_sns(event=mock_event, sns_client=conn)
         # Once the message is sucessfully passed to SNS it will return a messageId.
         assert res.get('MessageId', None) is not None

    def test_event_conversion(self):
        fixture = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'fixtures/sample_event_1.json'
        )

        with open(fixture) as event_json:
            event = json.load(event_json)

        from gd2md import guardDuty2MozDef
        res = guardDuty2MozDef.transform_event(event['Records'][0])
        assert res is not None
