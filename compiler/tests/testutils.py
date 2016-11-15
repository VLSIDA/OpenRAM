

def isclose(value1,value2,error_tolerance=1e-2):
    """ This is used to compare relative values. """
    import debug
    relative_diff = abs(value1 - value2) / max(value1,value2)
    check = relative_diff <= error_tolerance
    if not check:
        debug.info(1,"NOT CLOSE {0} {1} relative diff={2}".format(value1,value2,relative_diff))
    else:
        debug.info(2,"CLOSE {0} {1} relative diff={2}".format(value1,value2,relative_diff))
    return (check)

def isdiff(file1,file2):
    """ This is used to compare two files and display the diff if they are different.. """
    import debug
    import filecmp
    import difflib
    check = filecmp.cmp(file1,file2)
    if not check:
        debug.info(2,"MISMATCH {0} {1}".format(file1,file2))
        f1 = open(file1,"r")
        s1 = f1.readlines()
        f2 = open(file2,"r")
        s2 = f2.readlines()
        for line in difflib.unified_diff(s1, s2):
            debug.error(line)   
    else:
        debug.info(2,"MATCH {0} {1}".format(file1,file2))
    return (check)

def header(filename, technology):
    tst = "Running Test for:"
    print "\n"
    print " ______________________________________________________________________________ "
    print "|==============================================================================|"
    print "|=========" + tst.center(60) + "=========|"
    print "|=========" + technology.center(60) + "=========|"
    print "|=========" + filename.center(60) + "=========|"
    import globals
    OPTS = globals.get_opts()
    print "|=========" + OPTS.openram_temp.center(60) + "=========|"
    print "|==============================================================================|"
