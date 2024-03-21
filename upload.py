import requests
import tarfile
import os

def compress_folder_to_tar_gz(input_folder, output_filename):
    """
    Compresses an entire folder into a tar.gz file.
    """
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(input_folder, arcname=os.path.basename(input_folder))

def upload_file(url, file_path):
    """
    Uploads a file to a specified URL using HTTP POST.
    """
    with open(file_path, 'rb') as file:
        files = {'file': (os.path.basename(file_path), file)}
        response = requests.post(url, files=files)
        return response

# Specify the folder to compress and the output tar.gz file name
folder_to_compress = 'yy_03_16_17_21_34'
tar_gz_filename = 'compressed_folder.tar.gz'

# Compress the folder
compress_folder_to_tar_gz(folder_to_compress, tar_gz_filename)

# Specify the URL of the server endpoint to upload the file
upload_url  = 'http://10.0.64.138:8989/api-upload/uploadfile'
# upload_url  = 'http://localhost:8989/api-upload/uploadfile'

# Upload the compressed file
response = upload_file(upload_url, tar_gz_filename)

# Print server response
print(response.text)

