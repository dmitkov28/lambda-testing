import json
import boto3

def lambda_handler(event, context):
    bucket = event.get('bucket')
    key = event.get('key')
    
    if not bucket or not key:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'bucket and key are required'})
        }
    
    s3 = boto3.client('s3')
    
    try:
        # Read the JSON file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        data = json.loads(response['Body'].read().decode('utf-8'))
        
        # Do something with the data
        total = sum(data.get('numbers', []))
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Successfully processed file',
                'total': total,
                'data': data
            })
        }
    except s3.exceptions.NoSuchKey:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'File not found'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }