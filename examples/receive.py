#!/usr/bin/env python
# Uses the python-amqp package
# Source at: https://github.com/celery/py-amqp                                                                       
import amqp
import json
import datetime
import os

def connectAnonymous():
   return amqp.Connection(host="info1.dyn.xsede.org:5671",virtual_host="xsede")

def connectUserPass():
   #ssl_opts = {}
   # should check server CA chain                                                                                      
   ssl_opts = {"ca_certs": "/Users/navarro/jpclient.pem"}                                                                            
   return amqp.Connection(host="info1.dyn.xsede.org:5671",virtual_host="xsede",
                          ssl=ssl_opts,userid="navarro",password="jpfnspubsub")

def connectX509():
   ssl_opts = {"ca_certs": "/path/to/pem",
               "keyfile": "/path/to/key.pem",
               "certfile": "/path/to/cert.pem"}
   return amqp.Connection(host="info1.dyn.xsede.org:5671",virtual_host="xsede",
                          ssl=ssl_opts)

def callback1(exc,exchange,routing_key,message):
   print("message on exchange %s with routing key %s" % (exchange,routing_key))

def callback(message):
   st = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
   print("%s exchange=%s, routing_key=%s, size=%s" %
        (st, message.delivery_info["exchange"], message.delivery_info["routing_key"], len(message.body) ) )
   dir = os.path.join(os.getcwd(), 'cache', message.delivery_info["exchange"])
   if os.access(dir, os.W_OK):
      file = dir + '/' + message.delivery_info["routing_key"] + '.' + st
      fd = open(file, 'w')
      fd.write(message.body)
      fd.close()
   doc = json.loads(message.body)
   # do stuff with the json document                                                                                   

if __name__ == "__main__":
   conn = connectUserPass()
   #conn = connectAnonymous()
   channel = conn.channel()
   declare_ok = channel.queue_declare()
   queue = declare_ok.queue
   channel.queue_bind(queue,"glue2.applications","#")
   channel.queue_bind(queue,"glue2.compute","#")
   channel.queue_bind(queue,"glue2.computing_activities","#")
   channel.queue_bind(queue,"glue2.computing_activity","#")
   channel.basic_consume(queue,callback=callback)

   while True:
       channel.wait()
