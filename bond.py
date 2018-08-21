#!/usr/bin/python
#conding=utf-8
import pexpect
import os
import sys
import time
import re
ii = [交换机管理ip]

for host in ii:
    user = 'xxx'
    password = 'xxx'
    ssh_newkey = 'Are you sure you want to continue connecting'
    c = pexpect.spawn('ssh -l %s %s' % (user, host))
    i = c.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])
    
    if i == 0:  # Timeout
       pass
    
    if i == 1:  # SSH does not have the public key. Just accept it.
        c.sendline('yes')
        c.expect('password: ')
        i = c.expect([pexpect.TIMEOUT, 'password:'])
        if i == 0:  # Timeout
            print 'ERROR!'
        print 'SSH could not login. Here is what SSH said:'
    c.sendline(password)
    c.sendline('\n')
    time.sleep(1)
    c.sendline('super')
    time.sleep(0.2)
    c.expect(['Password', pexpect.EOF, pexpect.TIMEOUT])
    c.sendline('xxxx')
    time.sleep(0.2)
    c.sendline('display  arp | in 10.253.')
    time.sleep(0.2)
    c.sendline("                   ")
    time.sleep(0.3)
    c.sendline('quit')
    c.expect(['quit', pexpect.EOF, pexpect.TIMEOUT])
    #print c.before
    f = open(('/home/python/ssh/'+host),'w')
    f.write(c.before)
    f.close()
    ss = 'dos2unix  ' + host
    os.system(ss)
    c.sendline('quit')
def get_ip():
    ips = []
    with open("写个文件记录下sw的arp信息", "a+") as f:
        for i in f.readlines():
            ips.append(i.strip())
    return ips

def judge(host,  message):
    ip_list = get_ip()
    for ip in ip_list:
        if ip in message:
            rs={}
            n = re.findall(r'XGE\d+/\d+/\d+',message)
            m =  re.findall(r'/\d+',message)
            s = m[1].replace('/','')
            rs['n']=n
            rs['host']=host
            rs['s'] =s
            print rs
            return rs


ip_list = [交换机管理ip]

for ip in ip_list:
    with open("/home/python/ssh/{}".format(ip), "a+") as f:
        for msg in f.readlines():
            #print msg.strip()
            if judge(ip, msg.strip()):
                factor = judge(ip, msg.strip())
                
                host= factor['host']
                s = factor['s']
                user = 'xxx'
                password = 'xxxx'
                ssh_newkey = 'Are you sure you want to continue connecting'
                c = pexpect.spawn('ssh -l %s %s' % (user, host))
                i = c.expect([pexpect.TIMEOUT, ssh_newkey, 'password: '])

                if i == 0:  # Timeout
                   pass

                if i == 1:  # SSH does not have the public key. Just accept it.
                    c.sendline('yes')
                    c.expect('password: ')
                    i = c.expect([pexpect.TIMEOUT, 'password:'])
                    if i == 0:  # Timeout
                        print 'ERROR!'
                    print 'SSH could not login. Here is what SSH said:'
                c.sendline(password)
                c.sendline('\n')
                time.sleep(1)
                c.sendline('super')
                c.expect(['Password', pexpect.EOF, pexpect.TIMEOUT])
                c.sendline('xxxx')
                c.sendline("display  ip interface brief")
                c.sendline("sys")
                c.sendline("interface  Bridge-Aggregation" + str(int(s)+100))
                c.sendline("link-aggregation mode dynamic")
                c.sendline("port access vlan xxx")
                c.sendline("interface  Ten-GigabitEthernet 1/0/" + s)
                c.sendline("port link-aggregation group "+str(int(s)+100))
                c.sendline("interface  Ten-GigabitEthernet 2/0/" + s)
                c.sendline("port link-aggregation group "+str(int(s)+100))
                c.sendline('quit') 
                c.sendline('quit')
                c.expect(['quit', pexpect.EOF, pexpect.TIMEOUT])
                print c.before
