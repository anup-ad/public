import mysql.connector
import os
import sys
import time
import update_db_vars as cred


database = None
domainFQDN = 'some_domain.com'
userName = '{}\some_user'.format(domain)
vmName = sys.argv[1].upper()

def iniate_connection(user,pw,host,db):
    try:
        global database
        database = mysql.connector.connect(user=user,password=pw,host=host, database=db)
        return database.cursor()
    except Exception as x:
        print(str(x))
        time.sleep(3)
        sys.exit(2)

cursor = iniate_connection(cred.user,cred.pwd,'dbhost01', 'vmware_inventory')

sql = "SELECT vm_id,vcenter FROM vms_info WHERE hostname = '{}' LIMIT 1".format(vmName)

cursor.execute(sql)

for i in cursor:
    vmid, vcenter = i
    os.system('start vmrc.exe "vmrc://{}@{}.{}/?moid={}"'.format(userName,vcenter,domainFQDN,vmid))
    print('VMID: '+vmid)
    print('Vcenter: '+ vcenter)

database.disconnect()

sys.exit(0)



