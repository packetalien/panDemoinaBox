#!/usr/bin/env python
# Copyright (c) 2019, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Richard Porter rporter@paloaltonetworks.com>

'''
Palo Alto Networks |vmfuscon.py|

This file is the Virtual Machine wrapper class for vmrun in Fusion.

This software is provided without support, warranty, or guarantee.
Use at your own risk.
'''
__author__ = "Richard Porter (@packetalien)"
__copyright__ = "Copyright 2019, Palo Alto Networks"
__version__ = "1.3"
__license__ = "MIT"
__status__ = "Development"

import logging, json, requests, os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from time import strftime
from subprocess import call
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#TODO: Give these loggers some class :)

logger = logging.getLogger(__name__)
logLevel = 'DEBUG'
maxSize = 10000000
numFiles = 10
handler = RotatingFileHandler('controller.log',maxBytes=maxSize,backupCount=numFiles)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel("DEBUG")

# Variables so we can get our JSON data

vminfojson = "https://lumberjack.labinabox.net/liab/vminfo.json"
lumberjackurl = "https://lumberjack.labinabox.net"


# Starting LiaB Data gathering and builders

def lumberjack_check(url):
    ''' This function verifies access to the Lab in a Box resource server. Lumberjack.
    It looks for a 200 response_code by calling the url variable passed. It expects 
    a single variable.
    url: The function expects a web URL
    There is no error checking in the variable pass in this function yet. 
    TODO: Add URL validation for the url variable.
    '''
    r = requests.get(url, verify=False) # certificate checking is false here for SSL Inspection
    response = r.status_code
    logger.debug("Web resource check returned a status code of: %s" % response)
    return response

def get_home_dir():
    """
    Return the HOME DIR for the running OS
    :return: str: Home directory path
    TODO: Update 2.7 Legacy code with this newer function. Look for getuser() function.
    """
    home = str(Path.home())
    logger.debug("Looked up home directory and found: %s" % home)
    return home

def get_current_dir():
    '''
    Returns the CURRENT DIR for the running application.
    '''
    current = str(Path.cwd())
    logger.debug("Current running directory is: %s" % current)
    return current

# Search directories for configuration (*.json) files
DATA_DIRECTORIES = [
    get_home_dir(), get_current_dir(),
]

def find_and_open(filename):
    """
    Iterate through configured data directories for filename, and return
    the contents of Read() if found, or raise FileNotFound if not.
    :param filename: Filename to look for
    :return: str: File contents
    """
    if os.path.exists(filename):
        return open(filename).read()
    for d in DATA_DIRECTORIES:
        f = d + os.sep + filename
        if os.path.exists(f):
            return open(f).read()
    raise FileNotFoundError("Error: {} not located in data dirs ({}) or current dir.".format(filename, ", ".join(DATA_DIRECTORIES)))

def get_json_data(vminfojson,lumberjackurl):
    ''' Function to retrieve JSON data files from web resources.
    This function will get the latest vminfo.json from lumberjack.labinabox.net. It expects
    three variables and if the Lumberjack server is down, it will load the local JSON 
    files.
    vminfojson: The url of the VMInfo JSON data file.
    lumberjackurl: the current root source of JSON data files.
    '''
    lumberjack_status = lumberjack_check(lumberjackurl)
    try:
        if lumberjack_status == 200:
            v = requests.get(vminfojson)
            vminfo = v.text
            return vminfo
        else:
            vminfo = find_and_open("vminfo.json")
            return vminfo
    except:
        logger.debug("Something went wrong loading the vminfo.json")

# Getting vminfo JSON

vminfo = get_json_data(vminfojson,lumberjackurl)
vminfo = json.loads(vminfo)


class vmfuscon(object):
    """vmfuscon is a wrapper for manipulating Virtual Machines 
    specifically within Lab in a Box on MacOS Fusion. A LiaB Controller 
    will have the following properties:
    
    Attributes:
        name: A string representing the Virtual Machines name.
        vm_type: A string representing what kind of Virtual Machine it is.
        (e.g., Ubuntu, PanOS, etc.)
        vm_hash: A string representing the HASH of the OVA package.
        gdrive_url: A string representing the gDrive URL for download.
        status: A boolean representing if the Virtual Machine is 
        required or optional.
        vm_vmx: A string representing the Virtual Machine configuration file
        name (e.g., virtual_machine.vmx). This file is used with the native
        VMware vmrun application.
        vm_vm: A string representing the directory for method calls to the vmx file
        with vmrun. This attribute should be instatiated from the Lab in a Box 
        vminfo.json. A call to the macos will return an attribute with .vmwarevm for 
        Fusion users, and windows will return a directory without .vmwarevm.
        """
    def __init__(self,liabvm):
        self.name = vminfo.get(liabvm).get("name")
        self.vm_type = vminfo.get(liabvm).get("type")
        self.vm_hash = vminfo.get(liabvm).get("vm_hash")
        self.gdrive_url = vminfo.get(liabvm).get("sourceurl")
        self.status = vminfo.get(liabvm).get("status")
        self.vm_vmx = vminfo.get(liabvm).get("vmx")
        self.vm_vm = vminfo.get(liabvm).get("macos")
    def get_current_dir(self):
        '''
        Returns the CURRENT DIR for the running application.
        '''
        current = str(Path.cwd())
        logger.debug("Current running directory is: %s" % current)
        return current
    def hash_ova(self):
        pass
    def load_device_state(self):
        pass
    def load_logdb(self):
        pass
    def update_demo_files(self):
        pass
    def get_local_user(self):
        """
        Return the HOME DIR for the running OS
        :return: str: Home directory path
        TODO: Update 2.7 Legacy code with this newer function. Look for getuser() function.
        """
        home = str(Path.home())
        logger.debug("Returned home directory of: %s" % home)
        return home
    def find_and_open(self,filename):
        """
        Iterate through configured data directories for filename, and return
        the contents of Read() if found, or raise FileNotFound if not.
        :param filename: Filename to look for
        :return: str: File contents
        """
        self.DATA_DIRECTORIES = [self.get_local_user(), self.get_current_dir()]
        if os.path.exists(filename):
            return open(filename).read()
        for d in DATA_DIRECTORIES:
            f = d + os.sep + filename
            if os.path.exists(f):
                return open(f).read()
        raise FileNotFoundError("Error: {} not located in data dirs ({}) or current dir.".format(filename, ", ".join(self.DATA_DIRECTORIES)))
    def snapstamp(self):
        tagtime = strftime("%Y%m%d-%H%M%S")
        tagstamp = "liabsnapshot" + tagtime
        logger.debug("Sending %s as a snapshot timestamp" % tagstamp)
        return tagstamp
    '''def get_local_user(self):
        """Gets the current user that is executing the functions and returns user and home directory."""
        localuser = getpass.getuser()
        home = expanduser("~")
        return localuser, home
    '''
    def start_vm(self):
        """Returns true if the Virtual Machine successfully starts."""
        home = self.get_local_user()
        basedir = "/Documents/Virtual Machines.localized/IT-Managed-VMs"
        startvm = home + basedir + self.vm_vm + self.vm_vmx
        logger.debug("Starting: %s" % startvm)
        call(["/Applications/VMware Fusion.app/Contents/Library/vmrun","start",startvm])
        return True
    def suspend_vm(self):
        """Returns true if the Virtual Machine successfully suspends """
        home = self.get_local_user()
        basedir = "/Documents/Virtual Machines.localized/IT-Managed-VMs"
        suspendvm = home + basedir + self.vm_vm + self.vm_vmx
        call(["/Applications/VMware Fusion.app/Contents/Library/vmrun","suspend",suspendvm])
        logger.debug("Suspending %s" % suspendvm)
        return True
    def snap_vm(self):
        """Returns true if the function successfully snapshots the Virtual Machine. """
        home = self.get_local_user()
        basedir = "/Documents/Virtual Machines.localized/IT-Managed-VMs"
        snapvm = home + basedir + self.vm_vm + self.vm_vmx
        snapstamp = self.snapstamp()
        call(["/Applications/VMware Fusion.app/Contents/Library/vmrun","snapshot",snapvm,snapstamp])
        logger.debug("Created new snapshot: %s" % snapstamp)
        return True
    def get_json_data(self,vminfojson,lumberjackurl):
        ''' Function to retrieve JSON data files from web resources.
        This function will get the latest vminfo.json from lumberjack.labinabox.net. It expects
        three variables and if the Lumberjack server is down, it will load the local JSON 
        files.
        vminfojson: The url of the VMInfo JSON data file.
        lumberjackurl: the current root source of JSON data files.
        '''
        lumberjack_status = lumberjack_check(lumberjackurl)
        try:
            if lumberjack_status == 200:
                v = requests.get(vminfojson)
                vmraw = v.text
                vminfo = json.loads(vmraw)
                return vminfo
            else:
                vminfo = find_and_open("vminfo.json")
                return vminfo
        except:
            logger.debug("Something went wrong loading the vminfo.json")

vminfo = get_json_data(vminfojson,lumberjackurl)
vminfo = json.loads(vminfo)