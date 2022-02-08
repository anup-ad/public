#!/usr/bin/python3
import sys
import os
try:
    import netaddr
except:
    print('Could not find module netaddr. Attempting to install it.')
    try:
        os.system('python3 -m pip install netaddr')
        import netaddr
    except Exception as x:
        print(str(x))
        print('Could not install module netaddr. Please run "pip install netaddr" manually before running this tool.')
        sys.exit(2)

mask = str(input('Enter the netmask to convert: '))

try:
    bits = netaddr.IPAddress(mask).netmask_bits()
    print('CIDR for Netmask %s : /%s' % (mask,bits))
except Exception as x:
    print(str(x))
