import os
import logging
import boto3
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 環境変数から対象インスタンス ID を取得（コンマ区切り）
INSTANCE_IDS = [i.strip() for i in os.getenv('INSTANCE_IDS', '').split(',') if i.strip()]


def lambda_handler(event, context):
    """EC2 インスタンスを起動または停止する Lambda のエントリポイント。

    イベント例:
    {
        "action": "start" | "stop",
        "instance_ids": ["i-12345678", "i-87654321"]  # 任意。環境変数より優先
    }
    """
    action = event.get('action', 'start').lower()
    ids = event.get('instance_ids', INSTANCE_IDS)

    if not ids:
        logger.error('No instance IDs provided')
        return {'status': 'error', 'message': 'No instance IDs provided'}

    if action not in ('start', 'stop'):
        logger.error('Invalid action: %s', action)
        return {'status': 'error', 'message': f'Invalid action {action}'}

    try:
        if action == 'start':
            ec2.start_instances(InstanceIds=ids)
        else:
            ec2.stop_instances(InstanceIds=ids)
        logger.info('%s action executed for instances: %s', action, ids)
        return {'status': 'success', 'action': action, 'instances': ids}
    except ClientError as e:
        logger.exception('Failed to %s instances %s: %s', action, ids, e)
        return {'status': 'error', 'message': str(e)}
