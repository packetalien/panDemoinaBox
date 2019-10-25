#!/usr/bin/env python3
DOCUMENTATION = '''
Copyright (c) 2019, Palo Alto Networks

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

Author: Richard Porter <rporter@paloaltonetworks.com>
'''

import argparse, sys, requests, vmfuscon, time
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import xml.etree.ElementTree as ET
from vmfuscon import vmfuscon

#Arguments passed from user input from meta-cnc file
parser = argparse.ArgumentParser(description='Get meta-cnc Params')
parser.add_argument("-v", "--liab_vm", help="Get the VM to Snapshot", required=True)

# Get the VM Name from meta-cnc
try:
    snapvm = args.liab_vm
    # Create VMWare Fusion Controller Class
    snapshot = vmfuscon(snapvm)
    print("Snapshot in progress")
    print("\n")
    # Create timestamp'd snapshot
    snapshot.snap_vm()
    print("Snapshot successful")
except:
    print("Something went wrong with snapshot, please check controller.log for details.")

# Main included "just" in case this file is executed directly
if __name__ == "__main__":
    try:
        print("Hey, you are executing me locally? You sure that is right?")
        print("Giving you a couple of seconds to hit ctrl+c, don't say I didn't warn you...")
        print("This function is designed for LiaB Control Panel")
        print("Ninjas")
        sleep(5)
        snapvm = args.liab_vm
        # Create VMWare Fusion Controller Class
        snapshot = vmfuscon(snapvm)
        print("Snapshot in progress")
        print("\n")
        # Create timestamp'd snapshot
        snapshot.snap_vm()
        print("Snapshot successful")
    except:
        print("Something went wrong with snapshot, please check controller.log for details.")





