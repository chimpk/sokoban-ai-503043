import pygame
import sys

class SokobanGameApp:
    """
    Lớp điều phối chính ứng dụng Pygame (R5).
    Xử lý:
      - Vòng lặp game (Game loop).
      - Chọn thuật toán UCS / A*.
      - Bắt sự kiện phím (Space, Left, Right).
      - Hiển thị thông số (Action count, Cost, Status).
    """
    def __init__(self, map_path: str):
        # TODO: Member 4 implement
        pygame.init()
        self.map_path = map_path
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Sokoban Solver GUI")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Các thông số cần quản lý
        self.running = True
        self.current_algo = "UCS"
        self.action_count = 0
        self.cost = 0
        self.status = "Waiting..."

    def run(self) -> None:
        """Khởi chạy ứng dụng."""
        # TODO: Member 4 implement
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60) # Khóa tốc độ 60 FPS
            
        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """Bắt sự kiện phím (Space, Left, Right)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.status = f"Running {self.current_algo}..."
                    self.action_count += 1
                elif event.key == pygame.K_LEFT:
                    self.current_algo = "UCS"
                elif event.key == pygame.K_RIGHT:
                    self.current_algo = "A*"

    def _update(self):
        """Xử lý logic trò chơi từng frame."""
        pass

    def _draw(self):
        """Hiển thị thông số và vẽ map."""
        self.screen.fill((40, 40, 40)) # Màu nền

        # Hiển thị thông số (Action count, Cost, Status)
        algo_text = self.font.render(f"Algorithm (Left/Right): {self.current_algo}", True, (255, 255, 255))
        stats_text = self.font.render(f"Actions: {self.action_count} | Cost: {self.cost} | Status: {self.status}", True, (200, 255, 200))
        hint_text = self.font.render("Press SPACE to run solution", True, (255, 200, 100))

        self.screen.blit(algo_text, (20, 20))
        self.screen.blit(stats_text, (20, 60))
        self.screen.blit(hint_text, (20, 100))

        pygame.display.flip()