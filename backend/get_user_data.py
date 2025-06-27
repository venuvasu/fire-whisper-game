import decimal
import json
from dal.user_data import get_user_record

def default_serializer(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def handler(event, context):
    claims = event['requestContext']['authorizer']['jwt']['claims']
    user_id = claims.get('sub')

    user_data = get_user_record(user_id)

    return {
        'statusCode': 200,
        'body': json.dumps(user_data, default=default_serializer),
        'headers': {
            'Content-Type': 'application/json'
        }
    }