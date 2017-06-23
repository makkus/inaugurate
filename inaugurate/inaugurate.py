# -*- coding: utf-8 -*-

"""Main module."""

import os
import sys

import click
from six import string_types

import yaml


class InaugurateException(Exception):

    def __init__(self, msg):

        super(InaugurateException, self).__init__(msg)


class InaugurateConfig(object):

    def __init__(self):

        self.base_dir = click.get_app_dir("inauguration", force_posix=True)
        self.ingrate_dirs = [os.path.join(self.base_dir, "trusted_ingrates")]


def load_ingrate_file(ingrate):

    if os.path.isfile(ingrate):

        with open(ingrate) as f:
            try:
                conf = yaml.safe_load(f)
                if not conf:
                    raise InaugurateException("Ingrate file '{}' is empty...".format(ingrate))
                return conf
            except (yaml.YAMLError) as e:
                raise InaugurateException("Could not parse ingrate '{}': {}".format(ingrate, e))

    return False

class Inaugurate(object):

    def __init__(self, ingrate):

        self.config = InaugurateConfig()
        self.trusted = False

        if isinstance(ingrate, string_types):
            self.ingrate = load_ingrate_file(ingrate)
            if self.ingrate is False:
                for ingrate_dir in self.config.ingrate_dirs:
                    self.ingrate = load_ingrate_file(os.path.join(ingrate_dir, ingrate))
                    if self.ingrate is not False:
                        break
            if self.ingrate is False:
                raise Exception("Ingrate '{}' not a file, and not in any of the trusted dirs '{}'".format(ingrate, self.config.ingrate_dirs))
        elif isinstance(ingrate, dict):
            self.ingrate = ingrate
        else:
            raise Exception("Ingrate type '{}' not supported: {}".format(type(ingrate), ingrate))
