
def setup_output_path():
    import os
    # find the home path of test code 
    output_path = os.path.realpath(os.environ.get("OPENRAM_HOME")+"/../wl_characterizer_output/")
    try:
        os.makedirs(output_path, 0750)
    except OSError as e:
        if e.errno == 17:  # errno.EEXIST
            os.chmod(output_path, 0750)
    return output_path

def header(filename, technology,output_path):
    tst = "Running WL Test for:"
    print "\n"
    print " ______________________________________________________________________________ "
    print "|==============================================================================|"
    print "|=========" + tst.center(60) + "=========|"
    print "|=========" + technology.center(60) + "=========|"
    print "|=========" + filename.center(60) + "=========|"
    print "|=========" + output_path.center(60) + "=========|"
    print "|==============================================================================|"
