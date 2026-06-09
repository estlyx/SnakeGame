import numpy as np
import gymnasium as gym
from gymnasium import spaces

from snake_game import SnakeGame

CELL_PX = 30   # размер одной клетки в пикселях при рендеринге


class SnakeEnv(gym.Env):
    """
    Gymnasium-среда для змейки.

    observation_space : Box(11,)  — 11 признаков состояния игры
    action_space      : Discrete(3) — прямо / вправо / влево
    render_mode       : 'human' — показывает окно pygame в реальном времени
                        None    — без отрисовки (быстрое обучение)
    """

    metadata = {'render_modes': ['human'], 'render_fps': 20}

    def __init__(self, render_mode=None):
        self.game        = SnakeGame()
        self.render_mode = render_mode

        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(11,), dtype=np.float32
        )
        self.action_space = spaces.Discrete(3)

        self._window = None   # pygame-окно, создаётся при первом рендере
        self._clock  = None

    # ------------------------------------------------------------------
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        obs = self.game.reset()
        if self.render_mode == 'human':
            self._render_frame()
        return obs, {}

    def step(self, action):
        reward, done, score = self.game.step(int(action))
        obs      = self.game._state()
        info     = {'score': score}
        truncated = False          # у нас нет внешнего лимита времени
        if self.render_mode == 'human':
            self._render_frame()
        return obs, float(reward), done, truncated, info

    def render(self):
        if self.render_mode == 'human':
            self._render_frame()

    def close(self):
        if self._window is not None:
            import pygame
            pygame.display.quit()
            pygame.quit()
            self._window = None

    # ------------------------------------------------------------------
    def _render_frame(self):
        import pygame

        g   = self.game
        W   = g.width  * CELL_PX
        H   = g.height * CELL_PX

        if self._window is None:
            pygame.init()
            pygame.display.init()
            self._window = pygame.display.set_mode((W, H))
            pygame.display.set_caption('Snake RL Agent')
            self._clock = pygame.time.Clock()

        canvas = pygame.Surface((W, H))
        canvas.fill((50, 153, 213))   # синий фон

        # Еда — красный квадрат
        pygame.draw.rect(
            canvas, (213, 50, 80),
            (g.food.x * CELL_PX, g.food.y * CELL_PX, CELL_PX, CELL_PX)
        )

        # Змейка — тёмно-зелёная голова, чёрное тело
        for i, pt in enumerate(g.snake):
            color = (0, 150, 0) if i == 0 else (0, 0, 0)
            pygame.draw.rect(
                canvas, color,
                (pt.x * CELL_PX, pt.y * CELL_PX, CELL_PX - 1, CELL_PX - 1)
            )

        # Счёт
        font = pygame.font.SysFont(None, 28)
        canvas.blit(font.render(f'Score: {g.score}', True, (255, 255, 255)), (5, 5))

        self._window.blit(canvas, (0, 0))
        pygame.display.flip()

        # Обрабатываем закрытие окна
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()

        self._clock.tick(self.metadata['render_fps'])
