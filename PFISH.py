#
# p-fish : Python File System Hash Program
# Author: C. Hosmer
# July 2013
# Version 1.0
#
import logging  # Python Standard Library Logger
import time # Python Standard Library time functions
import sys # Python Library system specific parameters
import _pfish # _pfish Support Function Module

if __name__ == '__main__':
    PFISH_VERSION = '1.0'

    # Turn on logging

    logging.basicConfig(filename='pFishLog.log',level= logging.DEBUG)
    format='%(asctime)s %(message)s'

    # Process the command line arguments

    _pfish.ParseCommandLine()

    # Record the Starting Time

    startTime = time.time()

    # Record the welcome message

    logging.info('')
    logging.info('Welcome to p-fish Version: '+ PFISH_VERSION + '  ... New Scan Started')
    logging.info('')

    _pfish.DisplayMessage('Welcome to p-fish ... Version: '+ PFISH_VERSION)

    # Record information regarding the System

    logging.info('System: '+ sys.platform)
    logging.info('Version: '+ sys.version)

    # Traverse the file system directories and hash files

    filesProcessed = _pfish.WalkPath()

    # Record the End time and calculate the duration

    endTime = time.time()
    duration = endTime - startTime

    logging.info('Files Processed: ' + str(filesProcessed))
    logging.info('Elapsed Time: ' + str(duration) + ' seconds')
    logging.info('')
    logging.info('Program Terminated Normally')
    logging.info('')
    _pfish.DisplayMessage("Program End")