

def isclose(value1,value2,error_tolerance=1e-2):
    """ This is used to compare relative values.. """
    import debug
    relative_diff = abs(value1 - value2) / max(value1,value2)
    check = relative_diff <= error_tolerance
    if not check:
        debug.info(2,"NOT CLOSE {0} {1} relative diff={2}".format(value1,value2,relative_diff))
    else:
        debug.info(2,"CLOSE {0} {1} relative diff={2}".format(value1,value2,relative_diff))
    return (check)

def header(str, tec):
    tst = "Running Test for:"
    print "\n"
    print " ______________________________________________________________________________ "
    print "|==============================================================================|"
    print "|=========" + tst.center(60) + "=========|"
    print "|=========" + tec.center(60) + "=========|"
    print "|=========" + str.center(60) + "=========|"
    print "|==============================================================================|"
