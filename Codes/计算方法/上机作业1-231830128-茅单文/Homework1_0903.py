import matplotlib.pyplot as plt

# direct formula
sqrt5_4 = 2.236
sqrt5_6 = 2.23607
sqrt5_8 = 2.2360798
sqrt5_10 = 2.236067976
sqrt5_12 = 2.23606797750

ratio_4 = (1+sqrt5_4)/2
ratio_6 = (1+sqrt5_6)/2
ratio_8 = (1+sqrt5_8)/2
ratio_10 = (1+sqrt5_10)/2
ratio_12 = (1+sqrt5_12)/2

phi_4 = 1
phi_6 = 1
phi_8 = 1
phi_10 = 1
phi_12 = 1

res_4 = []
res_6 = []
res_8 = []
res_10 = []
res_12 = []

for i in range(1,21):
    phi_4 = phi_4 * ratio_4
    res_4.append(phi_4)
for i in range(1,21):
    phi_6 = phi_6 * ratio_6
    res_6.append(phi_6)
for i in range(1,21):
    phi_8 = phi_8 * ratio_8
    res_8.append(phi_8)
for i in range(1,21):
    phi_10 = phi_10 * ratio_10
    res_10.append(phi_10)
for i in range(1,21):
    phi_12 = phi_12 * ratio_12
    res_12.append(phi_12)

print("DIRECT FORMULA\nsqrt5\tratio\tphi\n")
print(f"{sqrt5_4}\t{ratio_4}\t{phi_4}\n")
print(f"{sqrt5_6}\t{ratio_6}\t{phi_6}\n")
print(f"{sqrt5_8}\t{ratio_8}\t{phi_8}\n")
print(f"{sqrt5_10}\t{ratio_10}\t{phi_10}\n")
print(f"{sqrt5_12}\t{ratio_12}\t{phi_12}\n")

# Fibonacci sequence
f0 = 0
f1 = 1

for i in range(0,20):
    f2 = f0 + f1
    f0 = f1
    f1 = f2

ratio_f = f1 / f0
phi_f = 1
res_f = []

for i in range(1,21):
    phi_f = phi_f * ratio_f
    res_f.append(phi_f)

print("FIBONACCI SEQUENCE\n\tratio\tphi\n")
print(f"\t{ratio_f}\t{phi_f}\n")

# divergence
div_4 = [a - b for a, b in zip(res_4, res_12)]
div_6 = [a - b for a, b in zip(res_6, res_12)]
div_8 = [a - b for a, b in zip(res_8, res_12)]
div_10 = [a - b for a, b in zip(res_10, res_12)]
div_f = [a - b for a, b in zip(res_f, res_12)]

# plot
x = list(range(1, 21))

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

axs[0].scatter(x, res_4, marker='o', label='4 Sig. Fig.')
axs[0].scatter(x, res_6, marker='p', label='6 Sig. Fig.')
axs[0].scatter(x, res_8, marker='^', label='8 Sig. Fig.')
axs[0].scatter(x, res_10, marker='s', label='10 Sig. Fig.')
axs[0].scatter(x, res_12, marker='*', label='12 Sig. Fig.')
axs[0].scatter(x, res_f, marker='d', label='Fibonacci')
axs[0].set_xlabel('n')
axs[0].set_ylabel('Value')
axs[0].set_title('n ~ Value')
axs[0].legend()
axs[0].grid(True)

axs[1].scatter(x, div_4, marker='o', label='4 Sig. Fig.-12 Sig. Fig.')
axs[1].scatter(x, div_6, marker='p', label='6 Sig. Fig.-12 Sig. Fig.')
axs[1].scatter(x, div_8, marker='^', label='8 Sig. Fig.-12 Sig. Fig.')
axs[1].scatter(x, div_10, marker='s', label='10 Sig. Fig.-12 Sig. Fig.')
axs[1].scatter(x, div_f, marker='d', label='Fibonacci-12 Sig. Fig.')
axs[1].set_xlabel('n')
axs[1].set_ylabel('Difference')
axs[1].set_title('n ~ Difference')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()