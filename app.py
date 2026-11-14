import os
import random
import sys
import time
import psutil
try:
    import pygame
except ImportError:
    print("Pygame bulunamadı! 'python -m pip install pygame psutil' ile yükleyin.")
    sys.exit()

WIDTH, HEIGHT = 1366, 768
FPS = 60

# Orijinal eDEX-UI Renk Paleti (Koyu Gri-Mavi & Cyan/Beyaz Çizgiler)
BG_COLOR = (8, 12, 16)
PANEL_BG = (12, 18, 26)
BORDER_COLOR = (40, 70, 90)
TEXT_CYAN = (0, 210, 255)
TEXT_WHITE = (200, 225, 240)
KEY_BG = (16, 26, 38)

class eDEXExactClone:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("eDEX-UI // EXACT PYTHON REPLICA")
        self.clock = pygame.time.Clock()
        
        try:
            self.font = pygame.font.SysFont("Consolas", 13)
            self.font_bold = pygame.font.SysFont("Consolas", 14, bold=True)
            self.font_small = pygame.font.SysFont("Consolas", 10)
        except:
            self.font = pygame.font.Font(None, 20)
            self.font_bold = pygame.font.Font(None, 22)
            self.font_small = pygame.font.Font(None, 14)

        # Terminal ve Log Verileri
        self.terminal_history = [
            "squared@batcore",
            "OS: Debian GNU/Linux 9.5 (stretch) x86_64",
            "Kernel: 4.9.0-8-amd64",
            "Type 'help', 'sysinfo', or 'clear'."
        ]
        self.current_input = ""
        
        # Sağ panel ağ logları
        self.net_logs = ["PACKET INJECT 0x42A -> OK", "ESTABLISHED ROUTE 192.168.1.1", "SECURE TUNNEL ACTIVE"]
        self.last_tick = time.time()

        # Sanal Klavye Tuş Düzeni (Görseldeki gibi)
        self.keyboard_layout = [
            ["ESC", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "BACK"],
            ["TAB", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["CAPS", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "ENTER"],
            ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
            ["CTRL", "FN", "SPACE", "ALT GR", "CTRL"]
        ]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        if self.current_input.strip():
                            self.process_cmd(self.current_input.strip())
                        self.current_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.current_input = self.current_input[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.current_input += event.unicode

            if time.time() - self.last_tick > 0.3:
                self.net_logs.append(f"TCP_STREAM 0x{random.randint(1000,9999)} OK")
                if len(self.net_logs) > 12:
                    self.net_logs.pop(0)
                self.last_tick = time.time()

            self.screen.fill(BG_COLOR)
            
            # Arayüz Bileşenleri (Görselin Birebir Yerleşimi)
            self.draw_borders_and_panels()
            self.draw_left_panel()      # Saat, CPU, RAM, Top Processes
            self.draw_center_terminal()  # Ana Terminal & Neofetch tarzı ekran
            self.draw_right_panel()     # Ağ Durumu, Dünya Haritası temsili, Trafik
            self.draw_bottom_filesystem()# Klasörler
            self.draw_virtual_keyboard() # Fütüristik Sanal Klavye

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def draw_borders_and_panels(self):
        # Ana çerçeve çizgileri
        pygame.draw.rect(self.screen, BORDER_COLOR, (10, 10, WIDTH - 20, HEIGHT - 20), 1)

    def draw_left_panel(self):
        # Sol Panel Kutusu
        pygame.draw.rect(self.screen, PANEL_BG, (15, 15, 280, 430))
        pygame.draw.rect(self.screen, BORDER_COLOR, (15, 15, 280, 430), 1)

        # Saat (Görseldeki büyük saat formatı)
        current_time = time.strftime("%H:%M:%S")
        t_surf = self.font_bold.render(current_time, True, TEXT_CYAN)
        self.screen.blit(t_surf, (25, 25))

        # Sistem Bilgileri & CPU Grafikleri
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        
        texts = [
            f"2026 UPTIME 0:04:30 LINUX WIRED",
            f"CPU USAGE: %{cpu}",
            f"MEM: USING {ram.used // (1024**2)}MB OUT OF {ram.total // (1024**2)}MB",
            "--- TOP PROCESSES ---",
            "15184  electron    26% 2.8%",
            "12715  discord     12% 2.0%",
            "14989  electron    10% 1.5%"
        ]
        
        y = 70
        for t in texts:
            s = self.font_small.render(t, True, TEXT_WHITE)
            self.screen.blit(s, (25, y))
            y += 22

    def draw_center_terminal(self):
        # Orta Terminal Kutusu
        pygame.draw.rect(self.screen, PANEL_BG, (300, 15, 740, 430))
        pygame.draw.rect(self.screen, BORDER_COLOR, (300, 15, 740, 430), 1)

        y = 25
        for line in self.terminal_history[-15:]:
            s = self.font.render(line, True, TEXT_WHITE)
            self.screen.blit(s, (315, y))
            y = y + 22

        # Komut satırı
        inp_surf = self.font.render(f"root@edex:~# {self.current_input}_", True, TEXT_CYAN)
        self.screen.blit(inp_surf, (315, 410))

    def draw_right_panel(self):
        # Sağ Panel Kutusu
        pygame.draw.rect(self.screen, PANEL_BG, (1045, 15, 305, 430))
        pygame.draw.rect(self.screen, BORDER_COLOR, (1045, 15, 305, 430), 1)

        # Ağ Durumu
        net_texts = [
            "NETWORK STATUS",
            "STATE: IPv4    ONLINE  88.252.116.139  PING 14ms",
            "WORLD VIEW: GLOBAL MAP ACTIVE",
            "--- NETWORK TRAFFIC ---"
        ]
        y = 25
        for nt in net_texts:
            s = self.font_small.render(nt, True, TEXT_CYAN if "STATUS" in nt else TEXT_WHITE)
            self.screen.blit(s, (1055, y))
            y += 20

        # Akan loglar
        y = 130
        for log in self.net_logs[-8:]:
            s = self.font_small.render(log, True, (0, 255, 150))
            self.screen.blit(s, (1055, y))
            y += 18

    def draw_bottom_filesystem(self):
        # Sol Alt Dosya Sistemi Kutusu
        pygame.draw.rect(self.screen, PANEL_BG, (15, 450, 480, 300))
        pygame.draw.rect(self.screen, BORDER_COLOR, (15, 450, 480, 300), 1)

        folders = ["Cache", "GPUCache", "LocalStorage", "blob_storage", "fonts", "keyboards", "themes"]
        fx = 30
        fy = 480
        for i, folder in enumerate(folders):
            pygame.draw.rect(self.screen, (25, 40, 60), (fx, fy, 55, 45), border_radius=4)
            pygame.draw.rect(self.screen, BORDER_COLOR, (fx, fy, 55, 45), 1, border_radius=4)
            fs = self.font_small.render(folder[:8], True, TEXT_WHITE)
            self.screen.blit(fs, (fx + 4, fy + 50))
            fx += 65
            if (i + 1) % 6 == 0:
                fx = 30
                fy += 75

    def draw_virtual_keyboard(self):
        # Sağ Alt Fütüristik Klavye Alanı
        pygame.draw.rect(self.screen, PANEL_BG, (500, 450, 850, 300))
        pygame.draw.rect(self.screen, BORDER_COLOR, (500, 450, 850, 300), 1)

        start_y = 470
        for row in self.keyboard_layout:
            start_x = 515
            for key in row:
                w = 45 if len(key) > 1 else 38
                if key == "SPACE": w = 280
                elif key in ["ENTER", "BACK", "SHIFT"]: w = 65
                
                pygame.draw.rect(self.screen, KEY_BG, (start_x, start_y, w, 36), border_radius=3)
                pygame.draw.rect(self.screen, BORDER_COLOR, (start_x, start_y, w, 36), 1, border_radius=3)
                
                ks = self.font_small.render(key, True, TEXT_CYAN)
                self.screen.blit(ks, (start_x + 6, start_y + 10))
                
                start_x += w + 6
            start_y += 44

    def process_cmd(self, cmd):
        self.terminal_history.append(f"root@edex:~# {cmd}")
        parts = cmd.lower().split()
        if not parts: return
        
        if parts[0] == "clear":
            self.terminal_history = ["Terminal cleared."]
        elif parts[0] == "help":
            self.terminal_history.extend(["Commands: sysinfo, clear, matrix, exit"])
        elif parts[0] == "sysinfo":
            self.terminal_history.append(f"CPU Cores: {psutil.cpu_count()} | RAM Usage: %{psutil.virtual_memory().percent}")
        elif parts[0] == "matrix":
            self.terminal_history.append("INJECTING MATRIX CODESTREAM... [SUCCESS]")
        elif parts[0] == "exit":
            pygame.quit()
            sys.exit()
        else:
            self.terminal_history.append(f"Command not recognized: {cmd}")

if __name__ == "__main__":
    app = eDEXExactClone()
    app.run()
