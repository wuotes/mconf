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

from mtoml import mtoml

#######################################################################
#                                                                     #
#         TESTS                                                       #
#                                                                     #
#######################################################################
self = mtoml(r'./tests/')

def test_normal_load() -> None:
    assert self.load(r'testconf') is True

def test_unforced_reload() -> None:
    assert self.load(r'testconf') is False

def test_forced_reload() -> None:
    assert self.load(r'testconf', force_reload=True) is True

def test_fake_load() -> None:
    assert self.load(r'fakeconf') is False

def test_bad_load() -> None:
    assert self.load(r'badconf') is False

def test_if_bad_is_loaded() -> None:
    assert self.is_loaded(r'badconf') is False

def test_if_fake_is_loaded() -> None:
    assert self.is_loaded(r'fakeconf') is False

def test_if_loaded() -> None:
    assert self.is_loaded(r'testconf') is True

def test_save_without_changes() -> None:
    assert self.save(r'testconf') is False

def test_save_without_changes_forced() -> None:
    assert self.save(r'testconf', force_overwrite=True) is True

def test_fake_save() -> None:
    assert self.save(r'fakeconf') is False

def test_fake_save_forced() -> None:
    assert self.save(r'fakeconf', force_overwrite=True) is False

def test_save_all_without_changes() -> None:
    assert self.save_all() is False

def test_save_all_without_changes_forced() -> None:
    assert self.save_all(force_overwrite=True) is True

def test_set_bool() -> None:
    assert self.set(r'testconf', r'testval', True) is True

def test_get_bool() -> None:
    assert self.get(r'testconf', r'testval') is True

def test_fake_set_bool() -> None:
    assert self.set(r'fakeconf', r'testval', True) is False

def test_fake_get_bool() -> None:
    assert self.get(r'fakeconf', r'testval') is None

def test_get_fake() -> None:
    assert self.get(r'testconf', r'fakeval') is None

def test_verify_save_load_get_bool() -> None:
    assert self.save(r'testconf') is True
    assert self.load(r'testconf', force_reload=True) is True
    assert self.get(r'testconf', r'testval') is True

def test_verify_save_load_get_str() -> None:
    assert self.set(r'testconf', r'testval', r'test') is True
    assert self.get(r'testconf', r'testval') == r'test'
    assert self.save(r'testconf') is True
    assert self.load(r'testconf', force_reload=True) is True
    assert self.get(r'testconf', r'testval') == r'test'

def test_bad_save_load_get_class() -> None:
    assert self.set(r'testconf', r'badval', mtoml()) is False
    assert self.save(r'testconf', force_overwrite=True) is True
    assert self.load(r'testconf', force_reload=True) is True
    assert self.get(r'testconf', r'badval') is None

def test_bad_workaround_save_load_get_class() -> None:
    for file in self.files:
        if r'testconf' == str(file[r'filename']).lower():
            file[r'data'][r'badval'] = mtoml()

    assert self.save(r'testconf', force_overwrite=True) is False
    assert self.save_all(force_overwrite=True) is False
    assert self.load(r'testconf', force_reload=True) is True
    assert self.get(r'testconf', r'badval') is None

def test_reloaded_bad_conf() -> None:
    assert self.load(r'reloadedconf') is True
    assert self.get(r'reloadedconf', r'val1') is True

    with open(self.dir + r'reloadedconf.toml', r'w') as toml_file:
        toml_file.write('val1 = 1.4.6.\nval2 = "bad\n\nval3=')

    assert self.load(r'reloadedconf', force_reload=True) is False
    assert self.get(r'reloadedconf', r'val1') is True

    with open(self.dir + r'reloadedconf.toml', r'w') as toml_file:
        toml_file.write('val1 = true\n')

    assert self.load(r'reloadedconf', force_reload=True) is True
    assert self.get(r'reloadedconf', r'val1') is True

def test_bad_directory_save() -> None:
    old_dir = self.dir
    self.dir = r'./#@^&$%*^(&//!~/'

    assert self.save(r'testconf', force_overwrite=True) is False
    assert self.save_all(force_overwrite=True) is False

    self.dir = old_dir