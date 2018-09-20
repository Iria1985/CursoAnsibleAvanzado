#!/usr/bin/python

import tempfile 
import errno
import os
import tarfile

from ansible.module_utils.basic import AnsibleModule

def run_module():
  #Definicion de los argumentos que se nos pueden pasar
  module_args = dict(
    name=dict(type='str', required=True),
    path=dict(type='str', required=True),
    dest=dict(type='str', required=False),
    version=dict(type='str', required=False, default="1.0")
  )
  result = dict(
    changed=False,
    tarball='',
    success=False
  )

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=True
  )

  if module.check_mode:
    module.exit_json(**result)
    
  #YA QUE NO ESTAMOS EN CHECK_MODE: A TRABAJAR
  dest='/tmp'
  if "dest" in module.params and module.params['dest'] is not None:    
    dest=module.params['dest']
    
  try: 
    testfile=tempfile.TemporaryFile(dir=dest)
    testfile.close()
  except OSError as e:
    errormsg="El directorio destino: "+dest+" no es escribible"
    module.fail_json(msg=errormsg, **result)

  if len(module.params['version'])>0:
    version='-'+module.params['version']
  else:
    version=''

  if dest[len(dest)-1]=='/':
     tarball=dest+module.params['name']+version+".tar.gz"
  else:
     tarball=dest+"/"+module.params['name']+version+".tar.gz" 

  try:
    with tarfile.open(tarball, "w:gz") as tar_handle:
      for root, dirs, files in os.walk(module.params['path']):
        for file in files:
          tar_handle.add(os.path.join(root,file))
  except Exception as e:
    module.fail_json(msg=e.message, **result)
      
  result['tarball'] = tarball
  result['changed'] = True
  result['success'] = True
  result['deploy_successful'] = True  

  #Si algo va mal, ejecutamos AnsibleModule.fail_json() para pasar el mensaje de error y el resultado
  if module.params['name'] == 'destroyworld':
    module.fail_json(msg='Algo no fue bien...', **result)

  #Si todo va bien llamamos a exit-json cn el resultado.
  module.exit_json(**result)

def main():
  run_module()

if __name__ == '__main__':
  main()

