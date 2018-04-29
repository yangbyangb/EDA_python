import re
import numpy as np
import math
import matplotlib.pyplot as plt

delta = 1e-12
Is = 1


def f(x):
    y = 2 / 3 * x - 5 / 3 + math.exp(40 * x)
    return y


def df(x):
    d = (f(x) - f(x - delta)) / delta
    return d


def line2zero(x0):
    y = f(x0)
    k = df(x0)
    x1 = x0 - y / k
    return x1


def cmpr(x):
    if f(x) <= delta:
        flag = True
    else:
        flag = False
    return flag


x = 10

while True:
    if cmpr(x):
        print(x)
        break
    else:
        x = line2zero(x)


def i_diode(vd):
    i = Is * (math.exp(40 * vd) - 1)
    return i


def v_diode(id):
    v = math.log((id / Is + 1), math.e) / 40
    return v


def plot_i_v(start, stop, point_num):
    x = np.linspace(start, stop, point_num, endpoint=True)
    i = []
    for index in range(len(x)):
        i += [i_diode(x[index])]

    ymax = max(i, key=lambda v : v)
    ymin = min(i, key=lambda v : v)
    m = ymax * 1.2
    n = ymin * 1.2

    plt.plot(x, i, color="blue", linewidth=1.0, linestyle="-")
    plt.xlim(start, stop)
    plt.xticks(np.linspace(start, stop, 9, endpoint=True))
    plt.ylim(n, m)
    plt.yticks(np.linspace(n, m, 5, endpoint=True))
    plt.xlabel('voltage $V_D$/V')
    plt.ylabel('current $i_D$/A')
    plt.title('I-V for diode\n', fontsize=12)

    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

    plt.savefig("I-V_D.png", dpi=288)
    plt.show()

    return


plot_i_v(-0.1, 0.1, 1000)
