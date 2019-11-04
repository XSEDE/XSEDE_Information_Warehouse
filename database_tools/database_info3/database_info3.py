#!/usr/bin/env python3
from datetime import datetime
import shlex
import subprocess

last_backup={}

cmd = shlex.split("aws s3 ls s3://xci.xsede.org/info.xsede.org/rds.backup/ --profile newbackup")
cmd_proc = subprocess.Popen(cmd, bufsize=1, stdout=subprocess.PIPE)
for line in iter(cmd_proc.stdout):
   try:
      filename = line.strip().decode("utf-8").split()[3]
      name_fields = filename.split('.')
      name_prefix = name_fields[0]
      name_epoch = name_fields[2]
   except:
      continue
   if name_prefix not in last_backup or last_backup[name_prefix]['epoch'] < name_epoch:
      last_backup[name_prefix] = {'epoch': name_epoch, 'filename': filename}
cmd_proc.terminate()

for i in last_backup:
   filename = last_backup[i]['filename']
   cmd = shlex.split("aws s3 cp s3://xci.xsede.org/info.xsede.org/rds.backup/{0} ./{0} --profile newbackup".format(filename))
   cmd_proc = subprocess.run(cmd, bufsize=1, stdout=subprocess.PIPE)
   print('{0} Downloaded {1}, rc={2}'.format(str(datetime.now()), filename, str(cmd_proc.returncode)))

delete_files = []

cmd = shlex.split("ls -1")
cmd_proc = subprocess.Popen(cmd, bufsize=1, stdout=subprocess.PIPE)
for line in iter(cmd_proc.stdout):
   try:
      filename = line.strip().decode("utf-8").split()[3]
      name_fields = filename.split('.')
      name_prefix = name_fields[0]
      name_dump = name_fields[1]
      name_epoch = name_fields[2]
   except:
      continue
   if name_prefix in last_backup and last_backup[name_prefix]['filename'] != filename:
      delete_files.append(filename)
cmd_proc.terminate()

for filename in delete_files:
   cmd_proc = subprocess.run(['rm' , filename], stdout = subprocess.PIPE)
   print('{0} Deleted local {1}, rc={2}'.format(str(datetime.now()), filename, str(cmd_proc.returncode)))
   
