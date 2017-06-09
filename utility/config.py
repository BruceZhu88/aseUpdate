# -*- coding: utf-8 -*-

import configparser
import string

class getconfig(object):
    @classmethod  
    def confToDict(cls,configFile, d=""):
        cp = configparser.ConfigParser()
        cp.optionxform = str  # Keep the capital letter format
        cp.read(configFile)
        if not d:
            d=dict()
            for s in cp.sections():
                d[s] = dict()
                for i in cp.items(s):
                    d[s][i[0]]=i[1]
        return d

    @classmethod             
    def getTestConfig(cls,default):
        #print "getTestconfig  %s" % default
        d=dict()
        #d,section = confToDict(default, d)
        d=cls.confToDict(default, d)
        return d
    
    @classmethod  
    def getparameters(cls,filename):
        
        d=cls.getTestConfig(filename) 
        
        local_version1=d['Firmware']['local_version1']
        #print "local_version: %s" %local_version

        local_version2=d['Firmware']['local_version2']

        old_version=d['Firmware']['old_version']
        #print "old_version: %s" %old_version
 
        new_version=d['Firmware']['new_version']
        #print "new_version: %s" %new_version   
        
        IP=d['IPAdress']['IP']
        #print "new_version: %s" %IP   

        cycle=d['Running_cycle']['cycle']
        #print "new_version: %s" %IP   
                
        title=d['Title']['title']
        #print "new_version: %s" %IP   
        
        return local_version1,local_version2,old_version,new_version,IP,cycle,title
    
if __name__=='__main__':
    local_version,old_version,new_version,IP,cycle,title=getconfig.getparameters('config.ini')  
    print(old_version)
