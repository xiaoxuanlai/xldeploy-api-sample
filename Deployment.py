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


#---Prepare an initial deployment ： retrieve a "deployment spec", specifit the Environment and package version in the request  
headers = {'Content-Type': 'application/xml'}

initial_deployment = requests.get(base+'deployment/prepare/initial/?environment=Environments/new-ci-envir&version=Applications/PetClinic-ear/1.0', auth = (password.login, password.pw))
print initial_deployment.text

#---Preview the deployment plan before mapping : calculate the plan that XLdeploy will execute for the given deployment(initial_deployment). the input of this step is the output of initialization(xml data)

preview_deployment = requests.post(base+'deployment/previewblock', data = initial_deployment.text, headers = headers, auth = (password.login, password.pw))
print preview_deployment.text

#---Mapping the deployment plan to the target environment
map_deployment = requests.post(base+'deployment/prepare/deployeds', data = initial_deployment.text, headers = headers, auth = (password.login, password.pw))
print map_deployment.text

#---Preview again the deployment plan after mapping, we can check the update after mapping 
preview2_deployment = requests.post(base+'deployment/previewblock', data = map_deployment.text, headers = headers, auth = (password.login, password.pw))
print preview2_deployment.text


#---Validate the deployment :  pass the deployment spec to POST /deployment/validate to validate the deployment spec
vali_deployment = requests.post(base+'deployment/validate', data = map_deployment.text, headers = headers, auth = (password.login, password.pw))
print vali_deployment.text

#---Create a deployment task : after validation, submit the deployment spec to the server to create a deployment task that is prepared to run, the output of this step is a task ID which are waiting for start
task_deployment = requests.post(base+'deployment', data = vali_deployment.text, headers = headers, auth = (password.login, password.pw))
print task_deployment.text

#---Pass the ID of task to /task/{taskid}/start, start the deployment task
task_start = requests.post(base+'task/'+task_deployment.text+'/start', headers = headers, auth = (password.login, password.pw))
print task_start.text


