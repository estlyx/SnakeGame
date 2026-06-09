import numpy as np
import matplotlib.pyplot as plt

scores = np.load("scores.npy")  # shape: (4055,)

window = 100
# Скользящее среднее (эпизоды 1..100, 2..101, ...)
moving_avg = np.convolve(scores, np.ones(window) / window, mode="valid")
episodes = np.arange(window, len(scores) + 1)

plt.figure(figsize=(10, 5))
plt.plot(episodes, moving_avg, linewidth=1.5, label=f"Среднее за {window} эпизодов")
plt.xlabel("Эпизод")
plt.ylabel("Награда")
plt.title("Кривая обучения DQN (Snake)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("learning_curve.png", dpi=150)
plt.show()