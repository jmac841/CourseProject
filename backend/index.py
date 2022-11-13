import json
import boto3

def lambda_handler(event, context):
    data = json.loads(json.dumps(event))
    payload = {}
    payload['inputs'] = data['data']

    runtime= boto3.client('runtime.sagemaker')
    response = runtime.invoke_endpoint(EndpointName='huggingface-pytorch-inference-2022-11-09-03-10-17-584',
                                       ContentType='application/json',
                                       Body=json.dumps(payload).encode())
                                       
    result = json.loads(response['Body'].read().decode())
    print(result)
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': result[0]['label']
    }

