import os
import random
import sys
import time
import psutil
try:
    import pygame
except ImportError:
    print("Pygame kütüphanesi bulunamadı!")
    sys.exit()

# Ekran Boyutları
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Renk Paleti (Hacker / Sci-Fi Yeşil Tonları)
BG_COLOR = (5, 10, 15)
PANEL_BG = (10, 20, 30)
GRID_COLOR = (20, 40, 60)
NEON_GREEN = (0, 255, 100)
NEON_CYAN = (0, 220, 255)
TEXT_WHITE = (200, 220, 240)
WARNING_RED = (255, 50, 50)

class SciFiTerminal:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("PYTHON KERNEL // eDEX-SIMULATOR v1.0")
        self.clock = pygame.time.Clock()
        
        # Font Ayarları
        try:
            self.font = pygame.font.SysFont("Consolas", 16)
            self.font_small = pygame.font.SysFont("Consolas", 12)
            self.font_title = pygame.font.SysFont("Consolas", 18, bold=True)
        except:
            self.font = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)
            self.font_title = pygame.font.Font(None, 26)

        # Akan Matrix/Kod Satırları Havuzu
        self.code_lines = [
            "INITIALIZING KERNEL 0x8892A...",
            "BYPASSING FIREWALL PROTOCOL...",
            "ESTABLISHING SECURE SSH TUNNEL...",
            "DECRYPTING SECURE SUB-ROUTINES...",
            "MEMORY ALLOCATION: 16384 MB OK",
            "GPU ACCELERATION ACTIVE...",
            "SCANNING LOCAL SUBNET 192.168.1.0/24...",
            "ACCESS GRANTED - WELCOME USER POYRAZ"
        ]
        self.scrolling_logs = []
        for _ in range(25):
            self.scrolling_logs.append(random.choice(self.code_lines))

        # Kullanıcı komut satırı
        self.command_text = ""
        self.terminal_history = ["SYSTEM READY. Type 'help', 'sysinfo', 'matrix', or 'clear'."]
        
        self.last_log_time = time.time()

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
                        if self.command_text.strip():
                            self.process_command(self.command_text.strip())
                        self.command_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.command_text = self.command_text[:-1]
                    else:
                        if event.unicode.isprintable():
                            self.command_text += event.unicode

            if time.time() - self.last_log_time > 0.3:
                fake_Hex = f"0x{random.randint(1000,9999)}:{random.randint(0,255):02X}"
                self.scrolling_logs.append(f"LOG_STREAM [{fake_Hex}] -> OK")
                if len(self.scrolling_logs) > 30:
                    self.scrolling_logs.pop(0)
                self.last_log_time = time.time()

            self.screen.fill(BG_COLOR)
            self.draw_grid()
            self.draw_panels()
            self.draw_system_stats()
            self.draw_matrix_stream()
            self.draw_interactive_terminal()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def draw_grid(self):
        for x in range(0, WIDTH, 40):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y), 1)

    def draw_panels(self):
        pygame.draw.rect(self.screen, PANEL_BG, (20, 20, 320, HEIGHT - 40), border_radius=8)
        pygame.draw.rect(self.screen, NEON_CYAN, (20, 20, 320, HEIGHT - 40), 1, border_radius=8)

        pygame.draw.rect(self.screen, PANEL_BG, (WIDTH - 340, 20, 320, HEIGHT - 40), border_radius=8)
        pygame.draw.rect(self.screen, NEON_GREEN, (WIDTH - 340, 20, 320, HEIGHT - 40), 1, border_radius=8)

        pygame.draw.rect(self.screen, PANEL_BG, (360, 20, WIDTH - 720, HEIGHT - 40), border_radius=8)
        pygame.draw.rect(self.screen, NEON_GREEN, (360, 20, WIDTH - 720, HEIGHT - 40), 1, border_radius=8)

    def draw_system_stats(self):
        title = self.font_title.render("SYSTEM_TELEMETRY", True, NEON_CYAN)
        self.screen.blit(title, (40, 40))

        cpu_usage = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()

        stats = [
            f"OS: Windows Python-Kernel",
            f"CPU USAGE: {cpu_usage}%",
            f"RAM TOTAL: {ram.total // (1024**2)} MB",
            f"RAM USED:  {ram.percent}%",
            f"STATUS: ONLINE",
            f"SECURITY: SECURED"
        ]

        y_offset = 90
        for stat in stats:
            color = WARNING_RED if "CPU" in stat and cpu_usage > 80 else TEXT_WHITE
            txt = self.font.render(stat, True, color)
            self.screen.blit(txt, (40, y_offset))
            y_offset += 35

    def draw_matrix_stream(self):
        title = self.font_title.render("KERNEL_STREAM", True, NEON_GREEN)
        self.screen.blit(title, (WIDTH - 320, 40))

        y_offset = 90
        for log in self.scrolling_logs[-15:]:
            txt = self.font_small.render(log, True, NEON_GREEN)
            self.screen.blit(txt, (WIDTH - 320, y_offset))
            y_offset += 25

    def draw_interactive_terminal(self):
        title = self.font_title.render("INTERACTIVE_CLI_SHELL", True, NEON_GREEN)
        self.screen.blit(title, (380, 40))

        y_offset = 90
        for line in self.terminal_history[-14:]:
            txt = self.font.render(line, True, TEXT_WHITE)
            self.screen.blit(txt, (380, y_offset))
            y_offset += 30

        input_box_y = HEIGHT - 80
        pygame.draw.rect(self.screen, (20, 35, 50), (380, input_box_y, WIDTH - 760, 40), border_radius=4)
        pygame.draw.rect(self.screen, NEON_GREEN, (380, input_box_y, WIDTH - 760, 40), 1, border_radius=4)

        cmd_display = self.font.render(f"> {self.command_text}_", True, NEON_GREEN)
        self.screen.blit(cmd_display, (395, input_box_y + 10))

    def process_command(self, cmd):
        self.terminal_history.append(f"> {cmd}")
        parts = cmd.lower().split()
        
        if not parts:
            return

        command = parts[0]

        if command == "clear":
            self.terminal_history = ["TERMINAL CLEARED."]
        elif command == "help":
            self.terminal_history.extend([
                "AVAILABLE COMMANDS:",
                " - sysinfo : Display extended system details",
                " - matrix  : Inject custom matrix logs",
                " - clear   : Clear terminal window",
                " - exit    : Close simulation"
            ])
        elif command == "sysinfo":
            self.terminal_history.append(f"CPU Cores: {psutil.cpu_count(logical=True)} | Platform: Python {sys.version.split()[0]}")
        elif command == "matrix":
            self.terminal_history.append("INJECTING VIRTUAL MATRIX PACKETS... [SUCCESS]")
        elif command == "exit":
            pygame.quit()
            sys.exit()
        else:
            self.terminal_history.append(f"Command not recognized: '{cmd}'. Type 'help'.")

if __name__ == "__main__":
    app = SciFiTerminal()
    app.run()
