#!/usr/bin/env python2.7

import sys
import os
import re
import smtplib

import sys
import os
import re
import unittest

import getpass
import datetime


USER = getpass.getuser()
TO_FIELD = "openram@soe.ucsc.edu"
#TO_FIELD = "mrg@ucsc.edu"
#TO_FIELD = "bchen12@ucsc.edu"
FROM_FIELD = USER+"@ucsc.edu"


LOCAL = "/soe/"+USER+"/unit_test"

sys.path.append(LOCAL+"/setup_scripts")
sys.path.append(LOCAL+"/compiler")
sys.path.append(LOCAL+"/compiler/tests")

TECH_NAME = "NONE"

#REPOS = "http://gforge.soe.ucsc.edu/svn/openram/trunk"
#REPOS = "http://svn.soe.ucsc.edu/svn/openram/trunk"
#REPOS = "gitosis@mada0.soe.ucsc.edu:openram.git"
REPOS = "git@github.com:mguthaus/OpenRAM.git"


MAIL = "/usr/sbin/sendmail"

# Add warnings/errors to email message. 
# Abort if warnings or errors.
def checkout(rev):
    """
    FOR SVN
    """
    print "Checking out revision " + rev

    # if it doesnt exist check it out
    if not os.path.isdir(LOCAL):
        cmd = "svn co -r" + rev + " " + REPOS + " " + LOCAL
        if os.system(cmd):
            print "Cannot check out repository: " + REPOS
            sys.exit(-1)
    # if it does exist just update to current revision
    else:
        try:
            os.chdir(LOCAL)
        except OSError:
            print "Cannot find repository at " + LOCAL
            sys.exit(-2)
        cmd = "svn update -r" + rev
        if os.system(cmd):
            print "Cannot update repository: " + REPOS
            sys.exit(-1)
    
    print "Done."

def git_clone():
    """
    FOR GIT
    """
    if not os.path.isdir(LOCAL):
        print "Cloning git repository at " + LOCAL
        cmd = "git clone " + REPOS + " " + LOCAL
        if os.system(cmd):
            email_error("Cannot clone out repository at " + LOCAL)

    else:
        print "Pulling git repository at " + LOCAL
        try:
            os.chdir(LOCAL)
        except OSError:
            email_error("Cannot find repository at " + LOCAL)

        cmd = "git pull"
        if os.system(cmd):
            email_error("Cannot update repository at " + LOCAL)
    print "Done."

def remove_cached_files():
    """
    removes cached .pyc files
    """
    if os.path.isdir(LOCAL):
        print "Removing Cached Files"
        cmd = "find {0} -type f -iname \*.pyc -delete".format(LOCAL)
        os.system(cmd)
        print "Done."

def regress():
    print "Running Regressions"
    try:
        os.chdir(LOCAL+"/compiler")
    except OSError:
        print "Cannot find repository at " + LOCAL
        sys.exit(-2)

    # get a list of all files in the python directory
    files = os.listdir("tests") 
    # assume any file that ends in "test.py" in it is a regression test
    nametest = re.compile("test\.py$", re.IGNORECASE) 
    tests = filter(nametest.search, files)
    tests.sort()
    
    # import all of the modules
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, tests)
    modules = map(__import__, moduleNames)
    
    suite = unittest.TestSuite()
    load = unittest.defaultTestLoader.loadTestsFromModule

    import traceback
    for m in modules:
        try:
            t=load(m)
            suite.addTests(t)
        except ImportError:
            print traceback.format_exc()
            #email_error(traceback.format_exc())

    result=unittest.TextTestRunner(verbosity=2).run(suite)

    print "Done."

    return (tests,result)

def email_start(toField,subj):
    p = os.popen("%s -t" % MAIL, 'w')

    p.write("From: <"+FROM_FIELD+">\n")
    p.write("Subject: {0} {1} ({2})\n".format(subj,datetime.datetime.now().replace(second=0,microsecond=0),TECH_NAME))
    p.write("To: <"+toField+">\n") # replace with openram
    p.write("\n\n")

    p.write("{0} Pacific Time\n".format(datetime.datetime.now().replace(second=0,microsecond=0)))
    p.write("\nTECHNOLOGY: {0}\n\n".format(TECH_NAME))
    return p;

def email_failure(sysinfo):
    type, value, tb = sysinfo
    import traceback
    p = email_start(TO_FIELD,"ERROR running regression")
    p.write(str(value)+"\n")
    traceback.print_tb(tb,None,p)

    p.write("\nLAST 5 CHECK-INS:\n\n")
    try:
        os.chdir(LOCAL)
    except OSError:
        print "Cannot find repository at " + LOCAL
        sys.exit(-2)
    log=os.popen("git log -5").read()
    p.write(log)

    p.close()

def email_results(tests,results):
    if results.wasSuccessful():
    	p = email_start(TO_FIELD,"PASSED regression result")
        p.write("TESTS:\n")
        for t in tests:
            p.write(t + "\n")
        
        p.write("\nREGRESSION TEST RESULTS:\n\n")
    else:
    	p = email_start(TO_FIELD,"FAILED regression result")
        p.write("TESTS:\n")
        for t in tests:
            p.write(t + "\n")

        p.write("\nREGRESSION TEST RESULTS:\n\n")
            
        for failure in results.failures:
            p.write("FAIL: "+str(failure[0])+"\n")
            p.write("      "+str(failure[1])+"\n")
            p.write("----------------------------\n")

        for error in results.errors:
            p.write("ERROR: "+str(error[0])+"\n")
            p.write("       "+str(error[1])+"\n")
            p.write("----------------------------\n")


    for skip in results.skipped:
        p.write("SKIP:"+str(skip[0])+"\n")
        p.write("----------------------------\n")

    p.write("\nLAST 5 CHECK-INS:\n\n")
    try:
        os.chdir(LOCAL)
    except OSError:
        print "Cannot find repository at " + LOCAL
        sys.exit(-2)
    log=os.popen("git log -5").read()
    p.write(log)

    p.close()

def email_error(error_msg):
    p = email_start(TO_FIELD,"FAILED to run regression")
    
    p.write("UNABLE TO RUN REGRESSION TESTS\n")
    p.write(error_msg)

    p.write("\nLAST 5 CHECK-INS:\n")
    try:
        os.chdir(LOCAL)
    except OSError:
        print "Cannot find repository at " + LOCAL
        sys.exit(-2)

    log=os.popen("git log -5").read()
    p.write(log)

    p.close()

    sys.exit(-3)

if __name__ == "__main__":
    # We must clone the repository before parsing any arguments
    remove_cached_files()
    git_clone()

    # now we can import the globals which sets up everything
    import globals
    globals.parse_args()
    # Update our local copy to the correct tech name for the email
    #globals TECH_NAME
    TECH_NAME = globals.OPTS.tech_name
    
    try:
        (tests,results) = regress()
        email_results(tests,results)
    except:
        email_failure(sys.exc_info())
    sys.exit(0)

