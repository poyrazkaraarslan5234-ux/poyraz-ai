import os
import random
import sys
import time
import psutil
try:
    import pygame
except ImportError:
    print("Pygame bulunamadı! CMD'ye 'python -m pip install pygame psutil' yazarak yükle.")
    sys.exit()

# Ekran Çözünürlüğü (Tam ekran veya geniş pencereli)
WIDTH, HEIGHT = 1366, 768
FPS = 60

# eDEX-UI Orijinal Renk Paleti (Cyan / Neon Yeşil / Koyu Siber Tema)
BG_DARK = (4, 8, 12)
PANEL_BG = (8, 16, 24)
BORDER_CYAN = (0, 200, 255)
NEON_GREEN = (0, 255, 120)
TEXT_DIM = (100, 140, 180)
TEXT_BRIGHT = (220, 245, 255)
WARN_RED = (255, 60, 60)

class eDEXClone:
    def __init__(self):
        pygame.init()
        # Tam ekran siber deneyim için
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("eDEX-UI // CYBERPUNK KERNEL SIMULATOR")
        self.clock = pygame.time.Clock()
        
        # Fontlar
        try:
            self.font = pygame.font.SysFont("Consolas", 15)
            self.font_small = pygame.font.SysFont("Consolas", 11)
            self.font_title = pygame.font.SysFont("Consolas", 16, bold=True)
        except:
            self.font = pygame.font.Font(None, 22)
            self.font_small = pygame.font.Font(None, 16)
            self.font_title = pygame.font.Font(None, 24)

        # Akan Hacker Log Akışı (Sağ Panel)
        self.logs = [
            "INIT ROOT KERNEL 0x77FF...",
            "MOUNTING VIRTUAL FILESYSTEM /dev/sda1...",
            "BYPASSING GATEWAY 192.168.1.1",
            "ESTABLISHING SECURE SOCKET...",
            "ENCRYPTION KEY: AES-256-GCM VERIFIED",
            "MEMORY MAP LOCK: SUCCESS"
        ]
        
        # Terminal Geçmişi ve Aktif Komut Satırı
        self.history = [
            "eDEX-UI [Version 2.2.8-Clone]",
            "Type 'help' for available system protocols, 'matrix' for stream, or 'clear'."
        ]
        self.current_input = ""
        self.last_tick = time.time()
        self.network_bytes_old = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

    def run(self):
        running = True
        while running:
            # Olay Kontrolleri (Klavye & Fare)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        if self.current_input.strip():
                            self.execute_command(self.current_input.strip())
                        self.current_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.current_input = self.current_input[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.current_input += event.unicode

            # Arka plan akış loglarını güncelle
            if time.time() - self.last_tick > 0.25:
                hex_rand = f"0x{random.randint(10000,99999):X}"
                self.logs.append(f"PACKET_INSPECT [{hex_rand}] -> OK")
                if len(self.logs) > 25:
                    self.logs.pop(0)
                self.last_tick = time.time()

            # Çizim Katmanları
            self.screen.fill(BG_DARK)
            self.draw_cyber_grid()
            self.draw_panels_layout()
            self.draw_left_telemetry()
            self.draw_right_stream()
            self.draw_center_terminal()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def draw_cyber_grid(self):
        # Arka plana hafif siber kareler çizelim
        for x in range(0, WIDTH, 50):
            pygame.draw.line(self.screen, (10, 25, 40), (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 50):
            pygame.draw.line(self.screen, (10, 25, 40), (0, y), (WIDTH, y), 1)

    def draw_panels_layout(self):
        # Sol Panel (Sistem Durumu)
        pygame.draw.rect(self.screen, PANEL_BG, (15, 15, 300, HEIGHT - 30), border_radius=6)
        pygame.draw.rect(self.screen, BORDER_CYAN, (15, 15, 300, HEIGHT - 30), 1, border_radius=6)

        # Sağ Panel (Akan Loglar / Paketler)
        pygame.draw.rect(self.screen, PANEL_BG, (WIDTH - 315, 15, 300, HEIGHT - 30), border_radius=6)
        pygame.draw.rect(self.screen, NEON_GREEN, (WIDTH - 315, 15, 300, HEIGHT - 30), 1, border_radius=6)

        # Orta Panel (Ana Terminal Ekranı)
        pygame.draw.rect(self.screen, PANEL_BG, (330, 15, WIDTH - 660, HEIGHT - 30), border_radius=6)
        pygame.draw.rect(self.screen, BORDER_CYAN, (330, 15, WIDTH - 660, HEIGHT - 30), 1, border_radius=6)

    def draw_left_telemetry(self):
        # Sol Panel Başlık
        title = self.font_title.render("SYSTEM_TELEMETRY", True, BORDER_CYAN)
        self.screen.blit(title, (30, 30))

        # Canlı Donanım Değerleri
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        items = [
            f"OS KERNEL : Windows NT",
            f"CPU USAGE : %{cpu}",
            f"RAM USED  : %{ram.percent} ({ram.used // (1024**2)}MB)",
            f"DISK FREE : {disk.free // (1024**3)} GB",
            f"STATUS    : ACTIVE",
            f"SECURITY  : ENCRYPTED"
        ]

        y = 80
        for text in items:
            color = WARN_RED if "CPU" in text and cpu > 85 else TEXT_BRIGHT
            rendered = self.font.render(text, True, color)
            self.screen.blit(rendered, (30, y))
            y += 35

    def draw_right_stream(self):
        # Sağ Panel Başlık
        title = self.font_title.render("KERNEL_STREAM", True, NEON_GREEN)
        self.screen.blit(title, (WIDTH - 295, 30))

        y = 80
        for log in self.logs[-18:]:
            rendered = self.font_small.render(log, True, NEON_GREEN)
            self.screen.blit(rendered, (WIDTH - 295, y))
            y = y + 25

    def draw_center_terminal(self):
        # Orta Panel Başlık
        title = self.font_title.render("INTERACTIVE_CLI_SESSION", True, BORDER_CYAN)
        self.screen.blit(title, (350, 30))

        # Terminal Geçmiş Satırları
        y = 80
        for line in self.history[-16:]:
            rendered = self.font.render(line, True, TEXT_BRIGHT)
            self.screen.blit(rendered, (350, y))
            y += 28

        # Komut Giriş Alanı Kutusu
        input_y = HEIGHT - 70
        width_box = WIDTH - 700
        pygame.draw.rect(self.screen, (12, 22, 35), (350, input_y, width_box, 40), border_radius=4)
        pygame.draw.rect(self.screen, BORDER_CYAN, (350, input_y, width_box, 40), 1, border_radius=4)

        prompt_text = self.font.render(f"root@edex-ui:~# {self.current_input}_", True, NEON_GREEN)
        self.screen.blit(prompt_text, (365, input_y + 11))

    def execute_command(self, cmd):
        self.history.append(f"root@edex-ui:~# {cmd}")
        parts = cmd.lower().split()
        if not parts:
            return

        command = parts[0]
        if command == "clear":
            self.history = ["Terminal cleared."]
        elif command == "help":
            self.history.extend([
                "AVAILABLE COMMANDS:",
                "  sysinfo - Show detailed OS & hardware stats",
                "  matrix  - Inject synthetic bypass code",
                "  clear   - Wipe terminal history",
                "  exit    - Shut down simulation"
            ])
        elif command == "sysinfo":
            self.history.append(f"CPU Cores: {psutil.cpu_count()} | Platform: Python Pygame Core")
        elif command == "matrix":
            self.history.append("INJECTING VIRTUAL MATRIX STREAM... [OK]")
        elif command == "exit":
            pygame.quit()
            sys.exit()
        else:
            self.history.append(f"Command not found: '{cmd}'. Type 'help'.")

if __name__ == "__main__":
    app = eDEXClone()
    app.run()
