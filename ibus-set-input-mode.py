#!/bin/sh

# Copyright 2019 Takuro Ashie <ashie@clear-code.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Find an available python command because recent systems install only "python3"
# instead of "python" by default. Note that """ means a block comment on Python,
# and ":" means no-op on shell script.

""":"
for cmd in python3 python; do
  $cmd -V > /dev/null 2>&1 && exec $cmd $0 "$@"
done

echo "Cannot find Python interpreter!"
exit 1
":"""

import os.path
import sys
import json
from gi import require_version as gi_require_version
gi_require_version('GLib', '2.0')
gi_require_version('IBus', '1.0')
from gi.repository import IBus
from gi.repository import GLib

modes_dict_default = {
    "anthy": {
        "on":            "InputMode.Hiragana",
        "active":        "InputMode.Hiragana",
        "hiragana":      "InputMode.Hiragana",
        "off":           "InputMode.Latin",
        "inactive":      "InputMode.Latin",
        "katakana":      "InputMode.Katakana",
        "half-katakana": "InputMode.HalfWidthKatakana",
        "latin":         "InputMode.Latin",
        "wide-latin":    "InputMode.WideLatin",
    },
    "kkc": {
        "on":            "InputMode.Hiragana",
        "active":        "InputMode.Hiragana",
        "hiragana":      "InputMode.Hiragana",
        "off":           "InputMode.Direct",
        "inactive":      "InputMode.Direct",
        "katakana":      "InputMode.Katakana",
        "half-katakana": "InputMode.HankakuKatakana",
        "latin":         "InputMode.Latin",
        "wide-latin":    "InputMode.WideLatin",
    },
    "mozc-jp": {
        "on":            "InputMode.Hiragana",
        "active":        "InputMode.Hiragana",
        "hiragana":      "InputMode.Hiragana",
        "off":           "InputMode.Direct",
        "inactive":      "InputMode.Direct",
        "katakana":      "InputMode.Katakana",
        "half-katakana": "InputMode.HalfWidthKatakana",
        "latin":         "InputMode.Latin",
        "wide-latin":    "InputMode.WideLatin",
    },
    "skk": {
        "on":            "InputMode.Hiragana",
        "active":        "InputMode.Hiragana",
        "hiragana":      "InputMode.Hiragana",
        "off":           "InputMode.Latin",
        "inactive":      "InputMode.Latin",
        "katakana":      "InputMode.Katakana",
        "half-katakana": "InputMode.HankakuKatakana",
        "latin":         "InputMode.Latin",
        "wide-latin":    "InputMode.WideLatin",
    },
}


def load_config_file(path):
    conf = dict()
    try:
        with open(path, "r") as f:
            conf.update(json.load(f))
    except Exception as e:
        pass
    return conf


def load_config_dir(confdir):
    conf = dict()
    try:
        files = os.listdir(confdir)
        for filename in files:
            path = os.path.join(confdir, filename)
            conf.update(load_config_file(path))
    except Exception as e:
        pass
    return conf


def load_config_path(path):
    conf = dict()
    if (os.path.isdir(path)):
        conf.update(load_config_dir(path))
    elif (os.path.isfile(path)):
        conf.update(load_config_file(path))
    return conf


def load_config():
    conf = dict(modes_dict_default)
    system_config_path = "/etc/ibus-set-input-mode"
    conf.update(load_config_path(system_config_path))
    user_config_path = os.path.expanduser("~/.config/ibus-set-input-mode")
    conf.update(load_config_path(user_config_path))
    return conf


if (len(sys.argv) != 2):
    sys.stderr.write('''Usage: %s MODE
    MODE: on, off, hiragana, katakana, half-katakana, latin, wide-latin
'''
                     % sys.argv[0])
    sys.exit(1)

mode = sys.argv[1]

IBus.init()
bus = IBus.Bus()

ic = bus.create_input_context("ibus-set-input-mode")
# "Capabilite" isn't a typo, it's actually declared in ibustypes.h
ic.set_capabilities(IBus.Capabilite.FOCUS | IBus.Capabilite.PROPERTY)

ic.focus_in()

engine = ic.get_engine()
engine_name = engine.get_name()

modes_dict = load_config()

if (engine_name not in modes_dict):
    sys.stderr.write("Unknown engine: %s\n" % engine_name)
    sys.exit(1)

modes = modes_dict[engine_name]

if (mode not in modes):
    sys.stderr.write("Unknown mode: %s\n" % mode)
    sys.exit(1)

ic.property_activate(modes[mode], IBus.PropState.CHECKED)

ic.focus_out()
