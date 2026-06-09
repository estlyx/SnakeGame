"""
Смотрим как обученный агент играет в змейку.

Запуск:
    python play_agent.py

Требует: snake_dqn.zip (запусти сначала train.py)
"""

from stable_baselines3 import DQN
from snake_env import SnakeEnv

EPISODES = 5   # сколько партий сыграть

env   = SnakeEnv(render_mode='human')
model = DQN.load("snake_dqn", env=env)

print(f"Агент загружен. Играем {EPISODES} партий…\n")

for ep in range(1, EPISODES + 1):
    obs, _    = env.reset()
    done      = False
    total_rew = 0.0

    while not done:
        # deterministic=True — всегда выбираем лучшее действие, без случайности
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, _, info = env.step(action)
        total_rew += reward

    print(f"Партия {ep}: счёт = {info['score']},  суммарная награда = {total_rew:.1f}")

env.close()
