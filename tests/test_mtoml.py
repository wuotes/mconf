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
import sys

sys.path.append(r'./mtoml')

import mtoml

#######################################################################
#                                                                     #
#         TESTS                                                       #
#                                                                     #
#######################################################################
self = mtoml.mtomlc(directory=r'./tests/')

def test_normal_load() -> None:
    assert self.load(config=r'testconf') is True

def test_unforced_reload() -> None:
    assert self.load(config=r'testconf') is False

def test_forced_reload() -> None:
    assert self.load(config=r'testconf', force_reload=True) is True

def test_fake_load() -> None:
    assert self.load(config=r'fakeconf') is False

def test_bad_load() -> None:
    assert self.load(config=r'badconf') is False

def test_if_bad_is_loaded() -> None:
    assert self.is_loaded(config=r'badconf') is False

def test_if_fake_is_loaded() -> None:
    assert self.is_loaded(config=r'fakeconf') is False

def test_if_loaded() -> None:
    assert self.is_loaded(config=r'testconf') is True

def test_save_without_changes() -> None:
    assert self.save(config=r'testconf') is False

def test_save_without_changes_forced() -> None:
    assert self.save(config=r'testconf', force_overwrite=True) is True

def test_fake_save() -> None:
    assert self.save(config=r'fakeconf') is False

def test_fake_save_forced() -> None:
    assert self.save(config=r'fakeconf', force_overwrite=True) is False

def test_save_all_without_changes() -> None:
    assert self.save_all() is False

def test_save_all_without_changes_forced() -> None:
    assert self.save_all(force_overwrite=True) is True

def test_set_bool() -> None:
    assert self.set(config=r'testconf', field=r'testval', value=True) is True

def test_get_bool() -> None:
    assert self.get(config=r'testconf', field=r'testval') is True

def test_fake_set_bool() -> None:
    assert self.set(config=r'fakeconf', field=r'testval', value=True) is False

def test_fake_get_bool() -> None:
    assert self.get(config=r'fakeconf', field=r'testval') is None

def test_get_fake() -> None:
    assert self.get(config=r'testconf', field=r'fakeval') is None

def test_group_set_bool() -> None:
    assert self.set(config=r'testconf', group=r'testgroup', field=r'testval', value=True) is True

def test_group_get_bool() -> None:
    assert self.get(config=r'testconf', group=r'testgroup', field=r'testval') is True

def test_fake_group_set_bool() -> None:
    assert self.set(config=r'fakeconf', group=r'testgroup', field=r'testval', value=True) is False

def test_fake_group_get_bool() -> None:
    assert self.get(config=r'fakeconf', group=r'testgroup', field=r'testval') is None

def test_group_get_fake() -> None:
    assert self.get(config=r'testconf', group=r'testgroup', field=r'fakeval') is None

def test_verify_save_load_get_bool() -> None:
    assert self.save(config=r'testconf') is True
    assert self.load(config=r'testconf', force_reload=True) is True
    assert self.get(config=r'testconf',field= r'testval') is True
    assert self.get(config=r'testconf', group=r'testgroup', field=r'testval') is True

def test_verify_save_load_get_str() -> None:
    assert self.set(config=r'testconf', field=r'testval', value=r'test') is True
    assert self.get(config=r'testconf', field=r'testval') == r'test'
    assert self.save(config=r'testconf') is True
    assert self.load(config=r'testconf', force_reload=True) is True
    assert self.get(config=r'testconf', field=r'testval') == r'test'

def test_bad_save_load_get_class() -> None:
    assert self.set(config=r'testconf', field=r'badval', value=mtoml.mtomlc()) is False
    assert self.save(config=r'testconf', force_overwrite=True) is True
    assert self.load(config=r'testconf', force_reload=True) is True
    assert self.get(config=r'testconf', field=r'badval') is None

def test_bad_workaround_save_load_get_class() -> None:
    for file in mtoml.mtomlc._files:
        if r'testconf' == str(file[r'config']).lower():
            file[r'data'][r'badval'] = mtoml.mtomlc()

    assert self.save(config=r'testconf', force_overwrite=True) is False
    assert self.save_all(force_overwrite=True) is False
    assert self.load(config=r'testconf', force_reload=True) is True
    assert self.get(config=r'testconf', field=r'badval') is None

def test_reloaded_bad_conf() -> None:
    assert self.load(config=r'reloadedconf') is True
    assert self.get(config=r'reloadedconf', field=r'val1') is True

    with open(self.get_dir() + r'reloadedconf.toml', r'w') as toml_file:
        toml_file.write('val1 = 1.4.6.\nval2 = "bad\n\nval3=')

    assert self.load(config=r'reloadedconf', force_reload=True) is False
    assert self.get(config=r'reloadedconf', field=r'val1') is True

    with open(self.get_dir() + r'reloadedconf.toml', r'w') as toml_file:
        toml_file.write('val1 = true\n')

    assert self.load(config=r'reloadedconf', force_reload=True) is True
    assert self.get(config=r'reloadedconf', field=r'val1') is True

def test_bad_directory_save() -> None:
    old_dir = self.get_dir()

    assert self.set_dir(directory=r'./#@^&$%*^(&//!~/') is False

    mtoml.mtomlc._mutex.acquire()
    mtoml.mtomlc._dir = r'./#@^&$%*^(&//!~/'
    mtoml.mtomlc._mutex.release()

    assert self.save(config=r'testconf', force_overwrite=True) is False
    assert self.save_all(force_overwrite=True) is False

    mtoml.mtomlc._mutex.acquire()
    mtoml.mtomlc._dir = old_dir
    mtoml.mtomlc._mutex.release()