"""
Обучение DQN-агента для змейки.

Запуск:
    python train.py

После обучения сохраняются:
    snake_dqn.zip      — веса модели
    scores.npy         — история счёта по эпизодам (для графика)
"""

import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback

from snake_env import SnakeEnv


class TrainingLogger(BaseCallback):
    """
    Логирует средний счёт каждые 100 эпизодов
    и сохраняет историю наград для последующей визуализации.
    """

    def __init__(self):
        super().__init__()
        self.episode_rewards = []   # суммарная награда каждого эпизода

    def _on_step(self) -> bool:
        for info in self.locals.get('infos', []):
            if 'episode' in info:
                self.episode_rewards.append(info['episode']['r'])
                n = len(self.episode_rewards)
                if n % 100 == 0:
                    mean = np.mean(self.episode_rewards[-100:])
                    print(f"  эпизод {n:>5} | средняя награда (100 эп.): {mean:>7.2f}")
        return True


# ------------------------------------------------------------------
env = Monitor(SnakeEnv())   # Monitor нужен чтобы записывать stats по эпизодам

model = DQN(
    policy             = "MlpPolicy",   # полносвязная нейросеть (входы → слои → выходы)
    env                = env,
    verbose            = 0,
    # --- гиперпараметры ---
    learning_rate      = 1e-3,          # скорость обучения нейросети
    buffer_size        = 50_000,        # сколько переходов хранить в памяти
    learning_starts    = 1_000,         # начать обучать только после N шагов
    batch_size         = 64,            # сколько примеров брать из памяти за раз
    gamma              = 0.9,           # коэффициент дисконтирования будущих наград
    exploration_fraction = 0.4,         # долю от total_timesteps ε убывает 1.0 → финал
    exploration_final_eps = 0.01,       # финальное значение ε
    train_freq         = 4,             # обучать сеть каждые N шагов
    target_update_interval = 500,       # как часто обновлять целевую сеть
)

callback = TrainingLogger()

print("Обучение началось (500 000 шагов)…")
model.learn(total_timesteps=500_000, callback=callback)

model.save("snake_dqn")
np.save("scores.npy", np.array(callback.episode_rewards))

print("\nГотово!")
print(f"  Эпизодов сыграно : {len(callback.episode_rewards)}")
print(f"  Лучший счёт      : {max(callback.episode_rewards):.0f}")
print(f"  Модель сохранена : snake_dqn.zip")
print(f"  История наград   : scores.npy")
env.close()
