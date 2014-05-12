#!/usr/bin/env python

import socket
import yaml
from subprocess import Popen, PIPE
import subprocess


def construct_ruby_object(loader, suffix, node):
    return loader.construct_yaml_map(node)

def construct_ruby_sym(loader, node):
    return loader.construct_yaml_str(node)

# for the correct loader for the Ruby object, so PyYAML can read the data after that
yaml.add_multi_constructor(u"!ruby/object:", construct_ruby_object)
yaml.add_constructor(u"!ruby/sym:", construct_ruby_sym)

certout = subprocess.check_output(['puppet', 'ca', 'list', '--render-as', 'yaml']) 
list = yaml.load(certout)

for i in list:
    oprnt = "unknown host"
    cname = i['name']
    pingc = Popen(['/bin/ping', '-c2', cname], stdout = PIPE, stderr = PIPE) #.stdout.read()
    output, error_output = pingc.communicate()

    if pingc.returncode: 
      #print (error_output)
      print output
    else:
      print "OK"

