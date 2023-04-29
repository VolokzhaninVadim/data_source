# Work with variables
from dotenv import load_dotenv

# Work with operating system
import os


class Env:
    def __init__(
        self,
        env_path: str = './.env'
    ) -> None:
        '''
        Access to environment variables.

        Parameters
        ----------
        env_path: str, optional
            Path to enviroment variables.
            Example './.env':
            endpoint_url='https://endpoint_url'
            aws_access_key_id='aws_access_key_id'
            aws_secret_access_key='aws_secret_access_key'
        '''
        self.env_path = env_path

    def get_env_dict(self) -> dict:
        '''
        Get environment dictionary.

        Returns
        -------
        dict
            Environment dictionary
        '''
        load_dotenv(dotenv_path=self.env_path, override=True)
        env_dict = os.environ
        return env_dict
