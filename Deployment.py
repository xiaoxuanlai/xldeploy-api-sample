#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------here is a sample for how to use XLdeploy API, including how to import package, create new ci, create deployment task and excute it 

import requests
import password

base= 'http://localhost:4516/deployit/'

#---import new package   

uploadpackage = 'PetClinic-1.0.dar'

files = {'fileData': (uploadpackage, open('resources/'+ uploadpackage, 'rb'), 'application/octet-stream')} 

package = requests.post(base + "package/upload/"+uploadpackage, files = files, auth = (password.login, password.pw))

print package.text


#---create new ci which the type is Infrastructure, the name of it is "new-ci-inf"
myxml = '''<overthere.LocalHost id="Infrastructure/new-ci-inf">
  <os>UNIX</os>
</overthere.LocalHost>'''
headers = {'Content-Type': 'application/xml'}
inf = requests.post(base+'repository/ci/Infrastructure/new-ci-inf', data = myxml, headers = headers, auth = (password.login, password.pw))
print inf.text


#---create new ci which the type is Environment,the name of it is "new-ci-envir", in this Environment, include the new ci "new-ci-inf" created before
myxml = '''<udm.Environment id="Environments/new-ci-envir">
  <members>
    <ci ref="Infrastructure/new-ci-inf"/>
    <ci ref="Infrastructure/my-new-ci"/>
  </members>
</udm.Environment>'''
headers = {'Content-Type': 'application/xml'}
envir = requests.post(base+'repository/ci/Environments/new-ci-envir', data = myxml, headers = headers, auth = (password.login, password.pw))

print envir.text

