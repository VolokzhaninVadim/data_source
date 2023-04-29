# Work with S3
import boto3
from botocore.config import Config

# Work with operating system
import os


class S3:
    def __init__(
        self,
        endpoint_url: str = None,
        aws_access_key_id: str = None,
        aws_secret_access_key: str = None,
        bucket: str = None,
        service_name: str = 's3',
        signature_version: str = 's3v4',
        connect_timeout: int = 5,
        read_timeout: int = 5,
        retries: dict = {'max_attempts': 10},
        **kwargs
    ):
        '''
        Work with S3.

        Parameters
        ----------
        endpoint_url : str, optional
            Endpoint url in S3, by default None
        aws_access_key_id : str, optional
            Access key in S3, by default None
        aws_secret_access_key : str, optional
            Secret access key in S3, by default None
        bucket : str, optional
            Bucket in S3, by default None
        service_name: str, optional
            Service name, by default 's3'
        signature_version: str, optional
             Signature version, by default 's3v4'
        connect_timeout: int, optional
            Connect timeout, by default 5
        read_timeout: int, optional
            Read timeout, by default 5
        retries: dict, optional
            Dict of retries, by default {'max_attempts': 10}
        '''

        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_value = bucket
        self.signature_version = signature_version
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.retries = retries
        self.service_name = service_name
        self.config = Config(
                signature_version=self.signature_version,
                connect_timeout=self.connect_timeout,
                read_timeout=self.read_timeout,
                retries=self.retries,
            )
        self.resource = boto3.resource(
            service_name=self.service_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            config=self.config,
        )
        self.bucket = self.resource.Bucket(self.bucket_value)

    def get_objects_list(self, start_position: str = '') -> list:
        '''
        Getting objects list in Ы3.

        Parameters
        ----------
        start_position : str, optional
            Start position of path for filtering, by default ''

        Returns
        -------
        list
            List of objects.
        '''
        object_list = []
        if start_position == '':
            for obj in self.bucket.objects.all():
                key = obj.key
                object_list.append(key)
            return sorted(object_list)
        else:
            for obj in self.bucket.objects.filter(Prefix=start_position):
                key = obj.key
                object_list.append(key)
            return sorted(object_list)

    def get_binary_file(self, s3_file: str) -> bytes:
        '''
        Get file from s3.

        Parameters
        ----------
        s3_file : str
            Path to file in s3.

        Returns
        -------
        bytes
            Bytes of file in s3.
        '''

        for i in self.bucket.objects.filter(Prefix=s3_file).all():
            body = i.get()['Body'].read()
            return body

    def save_local_file(self, s3_file: str, path: str = None) -> None:
        '''
        Saving file from s3 to loсal file.

        Parameters
        ----------
        s3_file : str
            Path to file in S3.
        path : str, optional
            Path to file for save it, by default None
        '''

        # Open file in s3
        file = self.get_binary_file(s3_file)
        # Checking path and saving file in current directory
        if path is None:
            with open(os.path.basename(s3_file), mode='wb') as f:
                f.write(file)
        # Checking path and creating path
        else:
            if not os.path.exists(path):
                os.mkdir(path)
            with open(path + '/' + os.path.basename(s3_file), mode='wb') as f:
                f.write(file)

    def save_file(self, path_to_file: str, path_s3: str = None) -> None:
        '''
        Save file in S3.

        Parameters
        ----------
        path_to_file : str
            Path to file
        path_s3 : str, optional
            Path in S3, by default None

        Raises
        ------
        AttributeError
        This AttributeError checks if both path to S3 directory
        and path to local file are passed as arguments correctly.
        In case of empty path to S3 directory the Error is raised.
        In case of local file does not have extension the Error is also raised.
        '''
        if path_s3 is None:
            raise AttributeError('You must pass a value to the path_s3 argument.')
        try:
            prepared_file_name = [x for x in os.path.splitext(path_to_file) if x != '']
            if prepared_file_name[1]:
                with open(path_to_file, 'rb') as file:
                    self.bucket.Object(path_s3 + '/' + os.path.basename(path_to_file)).put(Body=file)
        except IndexError:
            raise AttributeError('You must pass a value to the path_to_file argument.')

    def delete_file(self, file_name: str) -> None:
        '''
        Delete file.

        Parameters
        ----------
        file_name : str
            File path.
        '''

        self.resource.Object(self.bucket.name, file_name).delete()
