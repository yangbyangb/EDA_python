import cmath
import numpy as np
import matplotlib.pyplot as plt
from scipy import sparse


import parser
import stamp
import analysis


def simulate():
    mycircuit, elements = parser.parse('diode_test.sp')

    op_result = None
    dc_result = None
    ac_result = None
    tran_result = None

    if mycircuit.op:
        mna, rhs = stamp.stamp(mycircuit=mycircuit, elements=elements, s=None, ac=None)
        op_result = analysis.op(mna=mna, rhs=rhs)
        print("Operating Point:\n", op_result, "\n")

    if mycircuit.dc:
        dc_result = analysis.dc_sweep(mycircuit=mycircuit, elements=elements,
                                      start=mycircuit.dc_start, stop=mycircuit.dc_stop,
                                      point_number=mycircuit.dc_point_number,
                                      source=mycircuit.dc_source, sweep_type=mycircuit.dc_type)
        x = np.linspace(mycircuit.dc_start, mycircuit.dc_stop, mycircuit.dc_point_number, endpoint=True)
        rslt_num = len(dc_result)
        y = np.zeros(len(x))
        for i in range(len(dc_result[0]) - 1):
            for j in range(rslt_num):
                y[j] = dc_result[j][i]

            plt.plot(x, y, linewidth=1.0, linestyle="-")
            plt.xlim(mycircuit.dc_start, mycircuit.dc_stop)
            plt.xticks(np.linspace(mycircuit.dc_start, mycircuit.dc_stop, 5, endpoint=True))
            ymax = max(y, key=lambda a: a)
            ymin = min(y, key=lambda a: a)
            plt.yticks(np.linspace(ymax, ymin, 5, endpoint=True))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Node %d DC sweep result\n' % (i+1), fontsize=12)

            ax = plt.gca()
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.spines['bottom'].set_position(('data', 0))
            ax.yaxis.set_ticks_position('left')
            ax.spines['left'].set_position(('data', 0))

            plt.savefig("Node %d DC sweep result.png" % (i+1), dpi=288)
            plt.show()

    if mycircuit.ac:
        ac_result = analysis.ac(mycircuit=mycircuit, elements=elements,
                                start=mycircuit.ac_start, stop=mycircuit.ac_stop, point_number=mycircuit.ac_point_number,
                                sweep_type=mycircuit.ac_type)

        if mycircuit.ac_type.upper() == 'LIN':
            x = np.linspace(mycircuit.ac_start, mycircuit.ac_stop, mycircuit.ac_point_number, endpoint=True)
        elif mycircuit.ac_type.upper() == 'LOG':
            x = 10 ** (np.linspace(np.log10(mycircuit.ac_start), np.log10(mycircuit.ac_stop), mycircuit.ac_point_number))
        else:
            pass

        rslt_num = len(ac_result)
        y = np.zeros(len(x))
        for i in range(len(ac_result[0]) - 1):
            for j in range(rslt_num):
                y[j] = get_complex_magnitude(ac_result[j][i][0])

            plt.plot(x, y, linewidth=1.0, linestyle="-")
            plt.xlim(mycircuit.ac_start, mycircuit.ac_stop)
            plt.xticks(
                np.linspace(mycircuit.ac_start, mycircuit.ac_stop, 5, endpoint=True))
            ymax = max(y, key=lambda a: a)
            ymin = min(y, key=lambda a: a)
            plt.yticks(np.linspace(ymax, ymin, 5, endpoint=True))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Node %d AC result (/V)\n' % (i+1), fontsize=12)

            plt.savefig("Node %d AC result.png" % (i+1), dpi=288)
            plt.show()

    if mycircuit.tran:
        t, tran_result = analysis.tran(mycircuit=mycircuit, elements=elements,
                                       start=mycircuit.tran_start, stop=mycircuit.tran_stop, step=mycircuit.tran_step)

        rslt_num = len(tran_result)
        y = np.zeros(len(t))
        for i in range(len(tran_result[0]) - 1):
            for j in range(rslt_num):
                y[j] = np.real(tran_result[j][i][0])

            plt.plot(t, y, linewidth=1.0, linestyle="-")
            plt.xlim(mycircuit.tran_start, mycircuit.tran_stop)
            plt.xticks(np.linspace(mycircuit.tran_start, mycircuit.tran_stop, 5, endpoint=True))
            ymax = max(y, key=lambda a: a)
            ymin = min(y, key=lambda a: a)
            plt.yticks(np.linspace(ymax, ymin, 5, endpoint=True))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title('Node %d TRAN result\n' % (i+1), fontsize=12)

            ax = plt.gca()
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.spines['bottom'].set_position(('data', 0))
            ax.yaxis.set_ticks_position('left')
            ax.spines['left'].set_position(('data', 0))

            plt.savefig("Node %d TRAN result.png" % (i+1), dpi=288)
            plt.show()


def get_complex_magnitude(cmplx):
    magnitude = abs(cmplx)
    return magnitude


def get_complex_phase(cmplx):
    phase = cmath.phase(cmplx)
    return phase
