#!/bin/env python

import time
import httplib
import os
import sys
import optparse


class Resource:

    def __init__(self, resource, method="GET", status="200"):

        self.path = resource
        self.method = method
        self.status = status
        self.body = None
        self.log_file = None
        self.body = ""

    def timedTest(self, connection):
        """
        Test the resouce on the connection and return, in seconds, the  
        time elapsed for the response  
        """
        start_time = time.time()
        connection.connect()
        connection.request(self.method, self.path)
        duration = time.time() - start_time
        response = connection.getresponse()
        self.body = response.read()
        if response.status != self.status:
            msg = "Unexpected response: " + response.reason
            connection.close()
            raise RuntimeError(msg)

        connection.close()
        return duration

    def multiTest(self, connection, iterations):
        """
        Run multiple tests and output the average duration of the successful tests.
        """
        completed_iters = 0
        total_time = 0

        print ("\nTesting https://%s/%s for #%d iterations" %
               (connection.host, self.path, iterations))
        for test in range(1, iterations + 1):
            try:
                response_time = self.timedTest(connection)
                total_time += response_time
                print ("[%d: Duration: %g seconds]" % (test, response_time))
                completed_iters += 1
                responce_body = self.body
            except RuntimeError as e:
                print ("\033[1;31mTest https://%s/%s failed on iteraton %d:  %s\033[0;0m" %
                       (connection.host, self.path, test, str(e)))

        average = total_time / completed_iters
        if completed_iters > 0:
            print ("\033[;1mCompleted %d iterations of test https://%s/%s.  Average Response time = %g\033[0;0m\n" %
                   (completed_iters, connection.host, self.path, average))
            # only print the last response valid response if writing to a log file
            if sys.stdout.fileno() != 1:
                print(responce_body)


class Test:

    def __init__(self):
        """
        Constructor. Parses the command line arguments and uses them to
        initialize the instance member variables.
        """

        usage = "usage: %prog [options] <input file>"
        parser = optparse.OptionParser(usage=usage)
        parser.disable_interspersed_args()

        parser.add_option("-o", "--logfile", dest="logfile",
                          help="Name of file to which output should be logged", default=None)
        parser.add_option("-i", "--iterations", type=int, dest="iters",
                          help="Number of iterations of the test to run", default=3)
        #parser.add_option("-p", "--parallel", type=int, dest="parallel", help="Number of  tests to run in parallel - Unimplimented", default=1)
        parser.add_option("-s", "--servers", dest="servers",
                          help="Host name of servers to test.", default=None)

        (options, args) = parser.parse_args()

        if len(args) != 1:
            parser.print_help()
            sys.exit(1)
        else:
            self.test_input = args[0]

        if options.logfile:
            try:
                sys.stdout = open(options.logfile, 'w')
            except IOError as e:
                sys.stderr.write("Could not open file %s: %s\n" %
                                 (options.logfile,  str(e)))
                sys.exit(1)

        if options.servers:
            self.servers = options.servers.split()
        else:
            self.servers = ["info4.dyn.xsede.org", "info.xsede.org"]

        self.iterations = options.iters

        # self.maxThreads = options.parallel  #This is not yet implimented

    def main(self):

        try:

            test_file = open(self.test_input)
        except IOError as e:
            sys.stderr.write("Could not open file %s: %s\n" %
                             (self.test_input,  str(e)))
            sys.exit(1)

        for server in self.servers:
            con = httplib.HTTPSConnection(server)
            try:
                for test_path in test_file:
                    url_test = Resource(test_path.strip(), "GET", 200)
                    url_test.multiTest(con, 3)
                test_file.seek(0)

            except IOError as e:
                sys.stderr.write(
                    "Could not open connection to  %s: %s\n" % (server,  str(e)))
                sys.stderr.write(
                    "Skipping remaining tests for %s\n" % (server))


if __name__ == '__main__':

    Test().main()
    sys.exit(0)
