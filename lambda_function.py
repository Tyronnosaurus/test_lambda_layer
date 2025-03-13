import boto3
from can import TRCReader
from asammdf import MDF
import colorama


s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    print(colorama.Fore.GREEN + "Hello, World!" + colorama.Fore.Reset)

    # Optional. These only work if the Lambda is tested with an S3:PUT event template, for example
    # record = event['Records'][0]
    # print(colorama.Fore.GREEN + f"Source bucket: {record['s3']['bucket']['name']}" + colorama.Fore.Reset)
    # print(colorama.Fore.GREEN + f"Object key: {record['s3']['object']['key']}"     + colorama.Fore.Reset)
    
    # Test the libraries
    print( MDF(version='4.11')._mdf.version )
    print(TRCReader("trc_sample.trc").file_version)

    return {
        "statusCode": 200,
        "body": f"Byeeee"
    }