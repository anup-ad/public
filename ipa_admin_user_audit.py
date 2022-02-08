import csv
from datetime import date, datetime
import sys
import subprocess
import hashlib

#
# This utility pulls info on Users with higher privileges configured in IPA, and outputs the result in CSV. 
# The checksum for resulting CSV is also presented at the end to maintain data integrity as the CSV passes through human hands.
# IMPORTANT: Kerberos ticket required for user with admin privileges for this utility to work. 
#


today = datetime.now()
dateToday = today.strftime('%m-%d-%Y--%H-%M-%S')
reportFile = 'scrip_linux_sysadmins_report_{}.csv'.format(dateToday)

ipaAdminGroups = ['admingroup1','admingroup2']
ipaSudoRules = ['sudorule']
ipaHbacRules = ['hbacrule']

sysAdmins = []
indSysAdmins = []
data = []


def os_cmd_exec(cmd):
    result = None
    try:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (op, error) = process.communicate()
        result = op.decode('utf-8')
        rc = process.wait()
    except:
        result = None
    return result


def get_users_from_group(groupName):
    ipaCommand = "ipa group-show %s --all | grep -i users: | awk NR==1 | sed 's/Member users://'" % groupName
    users = os_cmd_exec(ipaCommand).replace('\n','').replace(',','').split()
    print('Group: {0}\nUsers: {1}'.format(groupName,users))
    print('-'*20)
    return users

def get_indirect_users_from_group(groupName):
    ipaCommand = "ipa group-show %s --all | grep -i users: | awk NR==2 | sed 's/Indirect Member users://'" % groupName
    users = os_cmd_exec(ipaCommand).replace('\n','').replace(',','').split()
    print('Group: {0}\nIndirect Users: {1}'.format(groupName,users))
    print('-'*20)
    return users

def get_users_from_sudo(sudoRule):
    ipaCommand = "ipa sudorule-show %s --all | grep -i users: | awk NR==1 | sed 's/Users://'" % sudoRule
    users = os_cmd_exec(ipaCommand).replace('\n','').replace(',','').split()
    print('Sudo Rule: {0}\nUsers: {1}'.format(sudoRule,users))
    print('-'*20)
    return users

def get_users_from_hbac(hbacRule):
    ipaCommand = "ipa hbacrule-show %s --all | grep -i users: | awk NR==1 | sed 's/Users://'" % hbacRule
    users = os_cmd_exec(ipaCommand).replace('\n','').replace(',','').split()
    print('HBAC Rule: {0}\nUsers: {1}'.format(hbacRule,users))
    print('-'*20)
    return users

def get_users_info(user):
    ipaUserProperties = ['User login:',
                         'First name:',
                         'Last name:']
    result = []
    for i in ipaUserProperties:
        if 'Indirect' in i:
            ipaCommand = "ipa user-show {0} --all | grep '{1}' |sed 's/{1}//'|sed -e 's/^[[:space:]]*//'".format(user,i)
        else:
            ipaCommand = "ipa user-show {0} --all | grep '{1}' | grep -v Indirect |sed 's/{1}//'|sed -e 's/^[[:space:]]*//'".format(user,i)
        result.append(os_cmd_exec(ipaCommand).replace('\n',''))
    ipaCommand = "ipa user-show %s --all | grep expiration | awk '{print $4}'" % user

    return result


def write_csv(fileName,header=False,data=False):
    f = open(fileName, 'a+', encoding='utf-8')
    writer = csv.writer(f)
    if header:
        writer.writerow(header)
    if data:
        writer.writerow(data)
    f.close()

def gen_md5_hash(fileName):
    md5Hash = hashlib.md5()
    f = open(fileName, 'rb')
    content = f.read()
    f.close()
    md5Hash.update(content)
    result = md5Hash.hexdigest()

    return result



def main():
    global sysAdmins


    message = 'SYS-ADMIN User Audit Utility'
    print('\n'+message)
    print('-'*len(message)+'\n')

    for i in ipaAdminGroups:
        for j in get_users_from_group(i):
            if j not in sysAdmins:
                sysAdmins.append(j)
        if i == 'admins':
            for j in get_indirect_users_from_group(i):
                if j not in indSysAdmins:
                    indSysAdmins.append(j)
                    sysAdmins.append(j)

    for i in ipaSudoRules:
        for j in get_users_from_sudo(i):
            if j not in sysAdmins:
                sysAdmins.append(j)

    for i in ipaHbacRules:
        for j in get_users_from_hbac(i):
            if j not in sysAdmins:
                sysAdmins.append(j)
    sysAdmins.sort()
    print('\nCreating CSV (This will take a while).. ')
    csvHeader = ['Username',
                 'First Name',
                 'Last Name']
    write_csv(reportFile,header=csvHeader)
    #counter = 0
    #print('Writing User Data:')
    for i in sysAdmins:
        write_csv(reportFile,data=(get_users_info(i)))
        
    print('\nDone!\nCSV file stored under ./{}'.format(reportFile))
    print('Checksum for report file: {}\n'.format(gen_md5_hash(reportFile)))

if __name__ == '__main__':
    main()
