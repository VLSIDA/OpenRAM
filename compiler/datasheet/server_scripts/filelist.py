import os
from deliverable import *
class filelist:
    
    
    def __init__(self):
        self.list = []
    
    def update_filelist(self,path,outdir):
        out_file = open(outdir,'w')
        for root, dirs, files in os.walk(path):
            for file in files:
                self.list.append(root + '/' + file)
                out_file.write('{}/{}\n'.format(root,file))
                #print('{}/{}'.format(root,file))




