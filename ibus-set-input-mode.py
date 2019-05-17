#!/usr/bin/env python

import sys
from gi import require_version as gi_require_version
gi_require_version('GLib', '2.0')
gi_require_version('IBus', '1.0')
from gi.repository import IBus
from gi.repository import GLib

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

modes_dict = {
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

engine = ic.get_engine()
engine_name = engine.get_name()

if (engine_name not in modes_dict):
    sys.stderr.write("Unknown engine: %s\n" % engine_name)
    sys.exit(1)

modes = modes_dict[engine_name]

if (mode not in modes):
    sys.stderr.write("Unknown mode: %s\n" % mode)
    sys.exit(1)

ic.property_activate(modes[mode], IBus.PropState.CHECKED)

ic.focus_out()
