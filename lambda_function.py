import boto3
from can import TRCReader
from asammdf import MDF
import colorama


s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """ This Lambda should be configured to be triggered when a .trc file is uploaded to an S3 bucket (using a bucket event). """
    
    print(colorama.Fore.CYAN + "Hello, World!" + colorama.Fore.Reset)

    record = event['Records'][0]
    print(colorama.Fore.GREEN + f"Source bucket: {record['s3']['bucket']['name']}" + colorama.Fore.Reset)
    print(colorama.Fore.GREEN + f"Object key: {record['s3']['object']['key']}"     + colorama.Fore.Reset)
    
    # Test the libraries
    mdf: MDF = MDF(version='4.11')
    trc = TRCReader("trc_sample.trc")

    return {
        "statusCode": 200,
        "body": f"Byeeee"
    }