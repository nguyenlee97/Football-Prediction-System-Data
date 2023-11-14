import requests
import boto3
import datetime

def save_csv_to_s3(csv_data, bucket_name, file_path):
    s3 = boto3.client('s3')
    s3.put_object(Body=csv_data, Bucket=bucket_name, Key=file_path)
    print(f"CSV file saved to S3 path: s3://{bucket_name}/{file_path}")

def lambda_handler(event, context):
    api_url = "https://www.football-data.co.uk/mmz4281/2324/E0.csv"
    bucket_name = "footballprediction-matchresultbucket"

    # Get the current date
    current_date = datetime.datetime.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day

    # Create the file path in S3
    file_path = f"raw-data/year={year}/month={month}/day={day}/EPLmatch.csv"
    print(file_path)

    # Call the API and retrieve the CSV data
    response = requests.get(api_url)
    if response.status_code == 200:
        csv_data = response.content

        # Save the CSV data to S3 bucket
        save_csv_to_s3(csv_data, bucket_name, file_path)
    else:
        print(f"Failed to retrieve CSV data from the API. Status code: {response.status_code}")

    # Return a response
    return {
        'statusCode': 200,
        'body': 'CSV file saved to S3 successfully'
    }