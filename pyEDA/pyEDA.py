import cmath
import numpy as np
import matplotlib.pyplot as plt


import parser
import stamp
import analysis


mycircuit, elements = parser.parse('netlist_example_1.sp')

mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements, s=None, ac=None)

op_result = analysis.op(mna=mna, rhs=rhs)
dc_result = None
ac_result = None
tran_result = None

if mycircuit.op:
    print("Operating Point:\n", op_result, "\n")

if mycircuit.dc:
    dc_result = analysis.dc_sweep(mycircuit=mycircuit, elements=elements,
                                  start=mycircuit.dc_start, stop=mycircuit.dc_stop,
                                  point_number=mycircuit.dc_point_number,
                                  source=mycircuit.dc_source, sweep_type=mycircuit.dc_type)
    x = np.linspace(mycircuit.dc_start, mycircuit.dc_stop, mycircuit.dc_point_number, endpoint=True)
    rslt_num = dc_result.shape[1]
    y = []
    for i in range(rslt_num):
        for j in range(len(x)):
            y += [dc_result[i][j]]

            plt.plot(x, y, linewidth=1.0, linestyle="-")
            plt.xlim(mycircuit.dc_start, mycircuit.dc_stop)
            plt.xticks(np.linspace(mycircuit.dc_start, mycircuit.dc_stop, mycircuit.dc_point_number / 10, endpoint=True))
            ymax = max(y, key=lambda a: a) * 1.2
            ymin = min(y, key=lambda a: a) * 1.2
            plt.yticks(np.linspace(ymax, ymin, 5, endpoint=True))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('DC sweep result\n', fontsize=12)

            ax = plt.gca()
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.spines['bottom'].set_position(('data', 0))
            ax.yaxis.set_ticks_position('left')
            ax.spines['left'].set_position(('data', 0))

            plt.savefig("DC sweep result.png", dpi=288)
            plt.show()

if mycircuit.ac:
    ac_result = analysis.ac(mycircuit=mycircuit, elements=elements,
                            start=mycircuit.ac_start, stop=mycircuit.ac_stop, point_number=mycircuit.ac_point_number,
                            sweep_type=mycircuit.ac_type)

if mycircuit.tran:
    t, tran_result = analysis.tran(mycircuit=mycircuit, elements=elements,
                                   start=mycircuit.tran_start, stop=mycircuit.tran_stop, step=mycircuit.tran_step)

    y = tran_result

    plt.plot(t, y, linewidth=1.0, linestyle="-")
    plt.xlim(mycircuit.dc_start, mycircuit.dc_stop)
    plt.xticks(np.linspace(mycircuit.dc_start, mycircuit.dc_stop, mycircuit.dc_point_number / 10, endpoint=True))
    ymax = max(y, key=lambda a: a) * 1.2
    ymin = min(y, key=lambda a: a) * 1.2
    plt.yticks(np.linspace(ymax, ymin, 5, endpoint=True))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('TRAN result\n', fontsize=12)

    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))
    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))

    plt.savefig("TRAN result.png", dpi=288)
    plt.show()


def get_complex_magnitude(cmplx):
    magnitude = abs(cmplx)
    return magnitude


def get_complex_phase(cmplx):
    phase = cmath.phase(cmplx)
    return phase
