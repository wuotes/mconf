# mtoml
Manage multiple TOML configurations from a single thread-safe module.

`pip install mtoml`

[![codefactor](https://www.codefactor.io/repository/github/wuotes/mtoml/badge?style=plastic)](https://www.codefactor.io/repository/github/wuotes/mtoml/) [![circleci](https://circleci.com/gh/wuotes/mtoml.svg?style=shield)](https://app.circleci.com/pipelines/github/wuotes/mtoml) [![codecov](https://codecov.io/gh/wuotes/mtoml/branch/main/graph/badge.svg)](https://codecov.io/gh/wuotes/mtoml) 

```
from sys import stderr

import mtoml

class pets(mtoml.mtomlc):
    def __init__(self):
        # set the relative path to the config directory
        # if not specified, defaults to the current directory
        # unless a directory was set prior to this class init
        mtoml.mtomlc.__init__(directory = '.\PATH_TO_CONFIGS\')

        # mtomlc does not need to be inherited and may be an instance var
        self.conf = mtoml.mtomlc(directory = '\PATH_TO_CONFIGS\')

        # mtoml methods may be accessed through any instance
        self.conf.set_dir(directory = '\PATH_TO_CONFIGS\')
        self.set_dir(directory = '.\PATH_TO_CONFIGS\')

        # or directly through the module itself
        mtoml.set_dir(directory = '.\PATH_TO_CONFIGS\')

        # all instances share the same files
        if mtoml.is_loaded(config = 'dogs') is False:
            # load a toml config named "dogs.toml"
            if mtoml.load(config = 'dogs') is False:
                # if something goes wrong mtoml won't throw exceptions
                # and instead returns either None or False
                print('Unable to load config "dogs"!', file = stderr)

    def __del__(self):
        # not a good idea to put this here in practice
        # but this is "save all changes before exit"
        mtoml.save_all()

        # where as this is would force a full write
        # to save eveything even if nothing changed
        mtoml.save_all(force_overwrite = True)

    def add_dog_breed(self, breed):
        # get the current list of dog breeds that we are
        # assuming is a list in this case
        breeds = mtoml.get(config = 'dogs', field = 'breeds')
        breeds.append(breed)

        # if the field is part of a group, simply specify the group
        breed_info = mtoml.get(config = 'dogs', group = 'breeds', field = breed)

        # update the config with our new list
        mtoml.set(config = 'dogs', field = 'breeds', value = breeds)

        # any attempt to call get(config = 'dogs', field = 'breeds')
        # will return our updated list but those updates
        # haven't been saved yet, we need explicitly save
        mtoml.save(config = 'dogs')

        # now even if another app wants to access
        # our toml config about dogs it will show
        # the updated list, otherwise our new list
        # would not be saved until the class instance
        # is cleaned up through __del__()
```