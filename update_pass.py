#!/usr/local/bin/python
import glob
import ConfigParser
from StringIO import StringIO
import hvac
import os
import re
import fileinput
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


homedir = os.environ['HOME']

config = ConfigParser.ConfigParser()
with open("%s/.vault-token" % homedir) as f:
    VAULT_TOKEN = f.read()
    

for tfvarfile in glob.glob('*.tfvars'):
    with open(tfvarfile) as f:
        f = StringIO("[top]\n" + f.read())
        config.readfp(f)
        template = config.get('top', 'vcenter_template')
        version = template.replace('"',"").split('/')[1].split('-')[3]
url = ""

client = hvac.Client(url=url, 
    token=VAULT_TOKEN, verify=False)

template_path = "<Vault_Path>/{}"

data = client.read(template_path.format(version))
password = data.get("data").get("password")

secret_file = ""

for line in fileinput.input('{}/{}'.format(homedir, secret_file), inplace=1, backup='.bak'):
    line = re.sub(r'provision_passwd.+', r'provision_passwd = "%s"' % password, line.rstrip())
    print(line)




