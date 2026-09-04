from matplotlib.ticker import MultipleLocator
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

l = 6
m = 5
k = 0.66

Q_0, P_0 = 1, 0

steps = 150

def alpha(wait):
    return 1 - np.exp(-k * wait)

def service(X, Y):
    s = min(X + Y, m)
    if X + Y == 0:
        return 0, 0

    return (s * X / (X + Y), s * Y / (X + Y))


Q = [Q_0]
P = [P_0]
efficiency = [1.0]
A = [0]
B =[0]
for i in range(steps - 1):
    S_Q, S_P = service(Q[i], P[i])
    total = S_Q + S_P
    if total > 0:
        efficiency.append(S_Q)
    else:
        efficiency.append(S_Q)
        # efficiency.append(1.0)

    
    A_nx = l
    B_nx = Q[i] * alpha((Q[i] + P[i]) / m)
    Q_nx = Q[i] + A_nx - S_Q - B_nx
    P_nx = P[i] + B_nx - S_P

    Q_nx = max(0, Q_nx)
    P_nx = max(0, P_nx)

    A.append(A_nx)
    B.append(B_nx)
    Q.append(Q_nx)
    P.append(P_nx)

W_fixed = l / m
alpha_fixed = alpha(W_fixed)
Q_fixed = l / (1 + alpha_fixed)
P_fixed = (l * alpha_fixed) / (1 + alpha_fixed)
# print(alpha((Q_fixed + P_fixed)/m))


T = np.arange(steps)
T_smooth = np.linspace(0, steps - 1, 3 * steps)

spl_Q = make_interp_spline(T, Q, k=2)
spl_P = make_interp_spline(T, P, k=2)
spl_B = make_interp_spline(T, B, k=2)
spl_eff = make_interp_spline(T, efficiency, k=2)

Q_smooth = spl_Q(T_smooth)
P_smooth = spl_P(T_smooth)
B_smooth = spl_B(T_smooth)
# eff_smooth = np.clip(spl_eff(T_smooth), 0, 1)
eff_smooth = spl_eff(T_smooth)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 7), sharex=True)

ax1.plot(T_smooth, Q_smooth, label="Реальные", color="#ee8915", lw=2)
ax1.plot(T, P, color="#392486", alpha=0.2, ls="--")
ax1.axhline(Q_fixed, color="#e7a584", alpha=0.8, ls=":")
ax1.axhline(m, color="#2c3fa0", alpha=0.7, ls=":")
ax1.set_ylabel("Реальные вызовы")
ax1.set_xlabel("Такт (3-5 сек.)")
ax1.grid(True, alpha=0.4)
ax1.legend(loc="upper right")

ax2.plot(T_smooth, P_smooth, label="Фантомные", color="#392486", lw=2)
ax2.plot(T, Q, color="#ee8915", alpha=0.2)
ax2.axhline(P_fixed, color="#59618D", alpha=0.7, ls=":")
ax2.set_ylabel("Фантомные вызовы")
ax2.set_xlabel("Такт (3-5 сек.)")
ax2.grid(True, alpha=0.4)
ax2.legend(loc="upper right")

# ax3.plot(T_smooth, eff_smooth, color="#2ca02c", lw=2, label="Пассажиры")
# ax3.axhline(np.mean(eff_smooth), color="#2ca02c", alpha=0.7, ls=":")
# ax3.set_ylabel("Пассажиропоток")
# ax3.set_xlabel("Такт (3-5 сек.)")
# # ax3.set_ylim(-0.1, 1.1)
# ax3.grid(True, alpha=0.4)
# ax3.legend(loc="lower right")

ax3.plot(T_smooth, B_smooth, color="#2899aa", lw=2, label="Покидания")
ax3.axhline(np.mean(B_smooth), color="#2899aa", alpha=0.7, ls=":")
ax3.set_ylabel("Покидания")
ax3.set_xlabel("Такт (3-5 сек.)")
# ax3.set_ylim(-0.1, 1.1)
ax3.grid(True, alpha=0.4)
ax3.legend(loc="lower right")

ax4.plot(T, A, color="#a02c3b", lw=2, label="Прибытия")
ax4.axhline(np.mean(A), color="#a02c3b", alpha=0.7, ls=":")
ax4.axhline(m, color="#2c3fa0", alpha=0.7, ls=":")
ax4.set_ylabel("Прибытия")
ax4.set_xlabel("Такт (3-5 сек.)")
ax4.grid(True, alpha=0.4)
ax4.legend(loc="lower right")

ax4.xaxis.set_major_locator(MultipleLocator(20))
ax4.xaxis.set_minor_locator(MultipleLocator(2))

plt.tight_layout()
plt.show()
