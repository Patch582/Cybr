#
# p-fish support functions - where all the real work gets done
#
# Author: C. Hosmer
# July 2013
# Version 1.0
#
# DisplayMessage()  ParseCommandLine()   WalkPath()
# HashFile() class _CVSWriter
# ValidateDirectory() ValidateDirectoryWriteable()
#
import os  # Python Standard Library  - Miscellaneous operating system interfaces
import stat # Python Standard Library - functions for interpreting os results
import time # Python Standard Library - Time access and conversion functions
import hashlib # Python Standard Library - Secure hashes and message digests
import argparse # Python Standard Library - Parser for command-line options, arguments
import csv # Python Standard Library - reader and writer for csv files
import logging # Python Standard Library - logging facility

log = logging.getLogger('main._pfish')

#
# Name: ParseCommandLine() Function
# 
# Desc: Process and Validate the command line arguments
#       use Python Standard Library module argparse
#
# Input: none
# 
# Actions:
#     Uses the standard library argparse to prcess the command line
#     establishes a global variable gl_args where any of the functions can
#     obtain argument information
#

def ParseCommandLine():

    parser = argparse.ArgumentParser('Python file system hashing .. p-fish')
    parser.add_argument('-v', '-verbose', help='allows progress messages to be displayed', action='store_true')

    # setup a group where the selection is mutually exclusive and required

    group = parser.add_mutually_exclusive_group(required= True)
    group.add_argument('--md5', help = 'specifies MD5 algorithm', action='store_true')
    group.add_argument('--sha256', help = 'specifies SHA256 algorithm', action='store_true')
    group.add_argument('--sha512', help = 'specifies SHA512 algorithm', action='store_true')

    parser.add_argument('-d', '--rootPath', type= ValidateDirectory, required=True, help = 'specify the root path for hashing')
    parser.add_argument('-d', '--rootPath', type= ValidateDirectoryWriteable, required=True, help = 'specify the path for the logs and reports to be written to')

 	# create a global object to hold the validated arguments, these will be available to all the Functions within the _pfish.py module

 	global gl_args
 	global gl_hashType

 	gl_args = parser.parse.parse_args()

 	if gl_args.md5:
 		gl_hashType = 'MD5' 
 	elif gl_args.sha256:
 		gl_hashType = 'SHA256'
 	elif gl_args.sha512:
 		gl_hashType = 'SHA512'
 	else:
 		gl_hashType = 'Unknown'
 		logging.error('Unknown Hash Type Specified')

 	DisplayMessage("Command line processed: Successfully")

 	return

 	# End ParseCommandLine ========================================================================

#
# Name: WalkPath() Function
#
# Desc: Walk the path specified on the command line
#		 use Python standard Library module os and sys
#
# Input: none, uses command line arguments
#
# Actions:
# 		Uses the standard library modules os and sys to traverse the directory structure starting a root
#		path specified by the user. For each file discovered, Walkpath will call the 
# 		Function HashFile() to perform the file hashing
#

def WalkPath():

	processCount = 0
	errorCount = 0

	oCVS = _CVSWriter(gl_args.reportPath + 'fileSystemReport.csv', gl_hashType)

	# Create a loop that processes all the files starting at the rootPath, all sub-directories will also be processed

	log.info('Root Path: ' + gl_args.rootPath)

	for root, dirs, files in os.walk(gl_args.rootPath):

		# for each file obtain the filename and call the HashFile Function

		for file in files:
			fname = os.path.join(root, file)
			result = HashFile(fname, file, oCVS)

			# if hashing was successful then increment the ProcessCount

			if result = True:
				processCount += 1

				# if not sucessful, then increment the ErrorCount

			else:
				errorCount += 1

	oCVS.writerClose()

	return(processCount)

	# End WalkPath ================================================================================


#
# Name: HashFile() Function
#
# Desc: Processes a single file which includes performing a hash of the file and the extraction
#		of metadata regarding the file processed. 
#		Use Python Standard library modules hashlib, os, and sys
#
# Input: theFile = the full path of the file
#		 simpleName = just the filename itself
#
# Actions:
# 		Attempts to hash the file and extract metadata
#		Call GenerateReport for successful hashed files
#

def HashFile(theFile, simpleName, o_result):

	# Verify that the path is valid

	if os.path.exists(theFile):

		# Verify that the path is not a symbolic link

		if not os.path.islink(theFile):

			# Verify that the file is real

			if os.path.isfile(theFile):
				try:
					
					# Attempt to open the file
					f = open(theFile, 'rb')

				except IOError:
					
					# if open fails report the error
					log.warning('Open Failed: ' + theFile)

					return
				else:
					try:
						pass
					except Exception as e:
						raise e
					else:
						pass

	return False

	# End HashFile ================================================================================