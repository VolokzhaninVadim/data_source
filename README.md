# About
Interaction with data source

# Install
```
pip install git+https://github.com/VolokzhaninVadim/data_source.git
```

# Usage
```
# Get local variables
from data_source.env import Env
env = Env(env_path='.env')
env_variables = env.get_env_dict()

# Get data from S3
from data_source.scraper.s3 import S3
s3 = S3(**env_variables)
s3.get_objects_list()
```

