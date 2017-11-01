#!/usr/bin/env python

import os
import json

with open('config.json') as config_json:
    config = json.load(config_json)

numfiles = len(os.listdir(config["surfdir"]))
print numfiles
