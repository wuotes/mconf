#######################################################################
# Copyright (c) 2022 Jordan Schaffrin                                 #
#                                                                     #
# This Source Code Form is subject to the terms of the Mozilla Public #
# License, v. 2.0. If a copy of the MPL was not distributed with this #
# file, You can obtain one at http://mozilla.org/MPL/2.0/.            #
#######################################################################

#######################################################################
#                                                                     #
#         IMPORTS                                                     #
#                                                                     #
#######################################################################
from decimal import Decimal
from datetime import datetime
from sys import stderr
from threading import Lock
from typing import Any, Type

import copy
import tomli
import tomli_w

#######################################################################
#                                                                     #
#         CONFIG                                                      #
#                                                                     #
#######################################################################
class mconf:
    ###################################################################
    #     CLASS VARIABLES                                             #
    ###################################################################
    files: list = []
    dir: str = r'./'
    mutex: Type[Lock] = Lock()

    ###################################################################
    #     CONSTRUCTOR, INSTANCE VARIABLES                             #
    ###################################################################
    def __init__(self: r'mconf', directory: str = r'./') -> None:
        mconf.mutex.acquire()

        if r'./' != directory:
            mconf.dir = directory

        mconf.mutex.release()

    ###################################################################
    #     LOAD                                                        #
    ###################################################################
    def load(self: r'mconf', filename: str, force_reload: bool = False) -> bool:
        file_data: dict = None

        mconf.mutex.acquire()

        for file in mconf.files:
            if filename.lower() == str(file[r'filename']):
                if force_reload is False:
                    mconf.mutex.release()

                    print('[{0}] Configuration \'{1}\' failed to load due to previous unsaved changes. (force_reload: False)'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename), file=stderr)

                    return False

                try:
                    with open(self.dir + filename + r'.toml', r'rb') as toml_file:
                        file_data = tomli.load(toml_file, parse_float=Decimal)

                except Exception as toml_exception:
                    print('[{0}] An exception was thrown while attempting to reload the configuration \'{1}\': {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename, str(toml_exception)), file=stderr)

                if file_data is None:
                    mconf.mutex.release()

                    print('[{0}] The configuration \'{1}\' failed to load.'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename), file=stderr)

                    return False

                file[r'data'] = file_data
                file[r'unsaved_changes'] = False

                mconf.mutex.release()

                print('[{0}] Configuration \'{1}\' loaded successfully.'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename), file=stderr)

                return True

        try:
            with open(self.dir + filename + r'.toml', r'rb') as toml_file:
                file_data = tomli.load(toml_file, parse_float=Decimal)

        except Exception as toml_exception:
            print('[{0}] An exception was thrown while attempting to load the configuration \'{1}\': {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename, str(toml_exception)), file=stderr)

        if file_data is None:
            mconf.mutex.release()

            print('[{0}] The configuration \'{1}\' failed to load.'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename), file=stderr)

            return False

        file_header = {
            r'filename': filename.lower(),
            r'unsaved_changes': False,
            r'data': file_data,
        }

        mconf.files.append(file_header)
        mconf.mutex.release()

        print('[{0}] Configuration \'{1}\' loaded successfully.'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename), file=stderr)

        return True

    ###################################################################
    #     IS_LOADED                                                   #
    ###################################################################
    def is_loaded(self: r'mconf', filename: str) -> bool:
        mconf.mutex.acquire()

        for file in mconf.files:
            if filename.lower() == str(file[r'filename']):
                mconf.mutex.release()

                return True

        mconf.mutex.release()

        return False

    ###################################################################
    #     SAVE                                                        #
    ###################################################################
    def save(self: r'mconf', filename: str, force_overwrite: bool = False) -> bool:
        is_valid_toml: bool = True

        mconf.mutex.acquire()

        for file in mconf.files:
            if filename.lower() == str(file[r'filename']):
                if force_overwrite is False and file[r'unsaved_changes'] is False:
                    mconf.mutex.release()

                    return False

                try:
                    tomli.loads(tomli_w.dumps(file[r'data']))

                except Exception as toml_exception:
                    is_valid_toml = False

                    print('[{0}] An exception was thrown while preparing to save the configuration \'{1}\': {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename, str(toml_exception)), file=stderr)

                if is_valid_toml is False:
                    mconf.mutex.release()

                    return False

                try:
                    with open(self.dir + filename + r'.toml', r'wb') as toml_file:
                        tomli_w.dump(file[r'data'], toml_file)

                    file[r'unsaved_changes'] = False
                
                except Exception as toml_exception:
                    is_valid_toml = False

                    print('[{0}] An exception was thrown while saving the configuration \'{1}\': {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename, str(toml_exception)), file=stderr)

                mconf.mutex.release()

                if is_valid_toml is False:
                    return False

                return True

        mconf.mutex.release()

        print('[{0}] The configuration \'{1}\' does not exist.'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename))

        return False

    ###################################################################
    #     SAVE_ALL                                                    #
    ###################################################################
    def save_all(self: r'mconf', force_overwrite: bool = False) -> bool:
        saved_all: bool = True

        mconf.mutex.acquire()

        for file in mconf.files:
            if force_overwrite is False and file[r'unsaved_changes'] is False:
                saved_all = False
                
                continue

            is_valid_toml: bool = True
            
            try:
                tomli.loads(tomli_w.dumps(file[r'data']))

            except Exception as toml_exception:
                is_valid_toml = False
                saved_all = False

                print('[{0}] An exception was thrown while preparing to save the configuration \'{1}\': {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), str(file[r'filename']), str(toml_exception)), file=stderr)

            if is_valid_toml is False:
                continue

            try:
                with open(self.dir + str(file[r'filename']) + r'.toml', r'wb') as toml_file:
                    tomli_w.dump(file[r'data'], toml_file)

                file[r'unsaved_changes'] = False
                
            except Exception as toml_exception:
                saved_all = False

                print('[{0}] An exception was thrown while saving the configuration \'{1}\': {2}'.format(datetime.now().strftime('%m/%d %I:%M %p'), str(file[r'filename']), str(toml_exception)), file=stderr)

        mconf.mutex.release()

        return saved_all

    ###################################################################
    #     GET                                                         #
    ###################################################################
    def get(self: r'mconf', filename: str, field: str) -> Any:
        mconf.mutex.acquire()

        for file in mconf.files:
            if filename.lower() == str(file[r'filename']):
                if field in file[r'data'].keys():
                    value = file[r'data'][field]

                    mconf.mutex.release()

                    return value

        mconf.mutex.release()

        return None

    ###################################################################
    #     SET                                                         #
    ###################################################################
    def set(self: r'mconf', filename: str, field: str, value: Any) -> bool:
        is_valid_toml: bool = True

        mconf.mutex.acquire()

        for file in mconf.files:
            if filename.lower() == str(file[r'filename']):
                try:
                    toml_copy = copy.deepcopy(file[r'data'])
                    toml_copy[field] = value

                    # this will throw an exception if the modifications resulted in an invalid toml format
                    tomli.loads(tomli_w.dumps(toml_copy))

                    file[r'unsaved_changes'] = True
                    file[r'data'] = toml_copy

                except:
                    is_valid_toml = False

                    print('[{0}] The configuration \'{1}\' and field \'{2}\' attempted value set resulted in an invalid TOML format.'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename, field), file=stderr)

                mconf.mutex.release()

                return is_valid_toml

        mconf.mutex.release()

        print('[{0}] The configuration \'{1}\' does not exist.'.format(datetime.now().strftime('%m/%d %I:%M %p'), filename), file=stderr)

        return False
