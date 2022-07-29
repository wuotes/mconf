# mconf
A Python module that can handle multiple TOML configuration files.

[![codefactor](https://www.codefactor.io/repository/github/wuotes/mconf/badge?style=plastic)](https://www.codefactor.io/repository/github/wuotes/mconf/) [![circleci](https://circleci.com/gh/wuotes/mconf.svg?style=shield)](https://app.circleci.com/pipelines/github/wuotes/mconf) [![codecov](https://codecov.io/gh/wuotes/mconf/branch/main/graph/badge.svg)](https://codecov.io/gh/wuotes/mconf) 

```
from mconf import mconf

class pets(mconf):
    def __init__(self):
        mconf.__init__('.\PATH_TO_CONFIGS\')  # set the relative path to the config directory, defaults to the current directory

        if not self.is_loaded('dogs'):  # all instances share the same files
            self.load('dogs')  # load a config file named "dogs.toml"

        if not self.is_loaded('cats'):
            self.load('cats')  # load a config file named "cats.toml"

        # This module should not throw any exceptions, if a method fails it returns either False or None.

    def __del__(self):
        self.save_all()  # save all loaded configs

    def add_new_dog_breed(self, breed):
        dog_breeds = self.get('dogs', 'breeds')  # gets the current list of dog breeds
        dog_breeds.append(breed)                 # we are assuming it returned a list for brevity but if 'get' fails it returns None
        self.set('dogs', 'breeds', dog_breeds)   # sets the variable 'breeds' in the config 'dogs' to our new list
```