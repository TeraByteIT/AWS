#!/usr/bin/env python

#########################################################################
# Author      : Marcus Dempsey
# Date        : 13/06/2017
# Dependancies: You need to have the AWS CLI tools installed on the machine that you are running this from:
#               - pip install awscli
#########################################################################

import sys, os, commands, requests, argparse

def s3_enumeration(argv):
   W            = '\033[0m'	 # white (normal)
   B            = '\033[34m' # blue
   R            = '\033[31m' # red
   G            = '\033[32m' # green
   targetBucket = ""         # Target S3 bucket to enumerate
   inputFile    = ""         # The file that will list all the names to try and enumerate against

   parser = argparse.ArgumentParser()
   parser.add_argument("-b", "--bucket", dest="S3Bucket",help="Select a target S3 bucket", required=True)
   parser.add_argument("-f", "--file", dest="inputFile",help="Select a bucket file to enumerate against", required=True)
   args = parser.parse_args()
   S3Bucket = args.S3Bucket
   inputFile = args.inputFile

   try:
       with open(args.inputFile, 'r') as f:
          bucketNames = [line.strip() for line in f]

          print (G + "[*]" + W + " Enumerating: '%s' from '%s'." % (S3Bucket, f.name))
          for name in bucketNames:
             try:
                 request = requests.head("http://%s%s.s3.amazonaws.com" % (name, S3Bucket))
                 if request.status_code != 404:
                    print (B + "[?]" + W + " Checking potential match: %s%s (returns %s)" % (name, S3Bucket, request.status_code))
                    try:
                        check = commands.getoutput("/usr/local/bin/aws s3 ls s3://%s%s" % (name, S3Bucket))
                        print (G + "[+]" + W + " Found following items of interest:")
                        print check
                    except:
                        print R + "[!]" + W + " There was an error trying to list the S3 bucket contents, are the AWS CLI tools installed?"
             except:
                print R + "[!]" + W + " There was an error trying to request: " + "http://%s%s.s3.amazonaws.com" % (name, S3Bucket)
       print ""
       print B + "[*]" + W + " Enumeration of '%s' buckets complete." % (S3Bucket)
   except:
      print R + "[!]" + W + " An exception occured when trying to open the file: " + inputFile

if __name__ == '__main__':
	s3_enumeration(sys.argv[1:])