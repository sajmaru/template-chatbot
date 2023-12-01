'''
Google Cloud Storage Data Read-Write Functions

This Python script provides functions for reading and writing data to Google Cloud Storage (GCS) buckets. GCS is a popular cloud storage service offered by Google Cloud Platform.

Functions:
1. `write_json_to_bucket(bucket_name, path, data)`: Writes JSON data to a GCS bucket at the specified path.

2. `write_pkl_to_bucket(bucket_name, path, data)`: Writes Pickle data to a GCS bucket at the specified path.

3. `read_from_bucket(bucket_name, path)`: Reads data from a GCS bucket at the specified path. The function returns a blob object that can be further processed to read the data.

Example Usage:
```python
# Example usage for writing JSON data to a GCS bucket
data = {'name': 'John', 'age': 30}
bucket_name = 'your-bucket-name'
path = 'data/sample.json'
result = write_json_to_bucket(bucket_name, path, data)
print(result)

# Example usage for reading data from a GCS bucket
bucket_name = 'your-bucket-name'
path = 'data/sample.json'
blob = read_from_bucket(bucket_name, path)
# You can further process 'blob' to read the data
'''
##############################################################

from google.cloud import storage
import json
import pickle

''' Data Read-Write Functions '''

# Write JSON data to a Google Cloud Storage bucket
def write_json_to_bucket(bucket_name, path, data):
    # Get the bucket
    bucket = storage.Client().get_bucket(bucket_name)
    
    # Create a blob (object) in the bucket with the specified path and upload the JSON data
    blob = bucket.blob(path)
    blob.upload_from_string(data=json.dumps(data), content_type='application/json')
    
    # Return a confirmation message
    return f"JSON data uploaded to {path}"

# Write Pickle data to a Google Cloud Storage bucket
def write_pkl_to_bucket(bucket_name, path, data):
    # Get the bucket
    bucket = storage.Client().get_bucket(bucket_name)
    
    # Create a blob (object) in the bucket with the specified path and upload the Pickle data
    blob = bucket.blob(path)
    blob.upload_from_string(pickle.dumps(data))
    
    # Return a confirmation message
    return f"Pickle data uploaded to {path}"

# Read data from a Google Cloud Storage bucket
def read_from_bucket(bucket_name, path):
    # Get the bucket
    bucket = storage.Client().get_bucket(bucket_name)
    
    # Get the blob (object) from the bucket with the specified path
    blob = bucket.blob(path)
    
    # Return the blob object, which can be further processed to read the data
    return blob