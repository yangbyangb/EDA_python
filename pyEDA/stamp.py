import numpy as np
import cmath
import sympy


def stamp(mycircuit, elements,
          dc_sweep_source=None, dc_sweep_v_value=None,
          ac=False, s=None,
          tran=False, tran_stamp_value=None, v_t_minus_h=None, i_t_minus_h=None):

    node_number = mycircuit.get_nodes_number()

    mna = np.zeros([node_number, node_number], dtype=complex)
    rhs = np.zeros([node_number, 1], dtype=complex)

    h = 1e-12

    for element in elements:
        tran_branch_index = 0
        element = element[0]
        name = element.name.lower()
        if name:
            if name[0] == 'r':  # resistor
                mna = stamp_r_mna(mna, element)
            elif name[0] == 'c':  # capacitor
                tran_branch_index += 1
                mna = stamp_c_mna(mna, element, s, ac, tran)
                if tran:
                    v = (v_t_minus_h[element.n1] - v_t_minus_h[element.n2])
                    rhs = stamp_rhs(rhs=rhs, element=element,
                                    tran_stamp_value=(element.value / h * v))
            elif name[0] == 'l':  # inductor
                tran_branch_index += 1
                element.branch_number4tran = tran_branch_index
                mna = stamp_l_mna(mna, element, s, ac, tran)
                if ac:
                    rhs = _add_row_or_column(rhs, add_a_row=True, add_a_column=False)
                if tran:
                    rhs = stamp_rhs(rhs=rhs, element=element,
                                    tran_stamp_value=(-element.value / h * i_t_minus_h[element.branch_number4tran]))
            elif name[0] == 'v':  # voltage source
                mna = stamp_vsrc_mna(mna, element)
                if dc_sweep_source:
                    if name == dc_sweep_source:
                        rhs = stamp_rhs(rhs, element, dc_sweep_v_value=dc_sweep_v_value)
                    else:
                        rhs = stamp_rhs(rhs, element)
                elif tran_stamp_value:
                    rhs = stamp_rhs(rhs, element, tran_stamp_value=tran_stamp_value)
                elif mycircuit.ac:
                    rhs = stamp_rhs(rhs, element, s=s)
                else:
                    rhs = stamp_rhs(rhs, element)
            elif name[0] == 'i':  # current source
                rhs = stamp_isrc_rhs(rhs, element)
            elif name[0] == 'd':  # diode
                mna = stamp_d_mna(mna, element)
            elif name[0] == 'm':  # MOSFET
                mna = stamp_mos_mna(mna, element)
            elif name[0] == 'e':  # vcvs
                mna = stamp_vcvs_mna(mna, element)
                rhs = stamp_rhs(rhs, element)
            elif name[0] == 'f':  # cccs
                mna = stamp_cccs_mna(mna, element)
            elif name[0] == 'g':  # vccs
                mna = stamp_vccs_mna(mna, element)
            elif name[0] == 'h':  # ccvs  # TODO: complete this
                mna = stamp_ccvs_mna(mna, element)

    # delete node 0 (gnd) in mna & rhs
    mna = np.delete(mna, 0, 0)
    mna = np.delete(mna, 0, 1)
    rhs = np.delete(rhs, 0, 0)
    return mna, rhs


def stamp_r_mna(mna, element):
    mna[element.n1, element.n1] += element.g
    mna[element.n2, element.n2] += element.g
    mna[element.n1, element.n2] -= element.g
    mna[element.n2, element.n1] -= element.g
    return mna


def stamp_c_mna(mna, element, s=None, ac=False, tran=False):
    if ac:
        mna[element.n1, element.n1] += s * element.value
        mna[element.n2, element.n2] += s * element.value
        mna[element.n1, element.n2] -= s * element.value
        mna[element.n2, element.n1] -= s * element.value
    elif tran:
        h = 1e-12

        index = mna.shape[0]
        mna = _add_row_or_column(mna, add_a_row=True, add_a_column=True)
        mna[element.n1, index] = +1
        mna[element.n2, index] = -1
        mna[index, element.n1] = + element.value / h
        mna[index, element.n2] = - element.value / h
        mna[index, index] = -1

    else:
        pass

    return mna


def stamp_l_mna(mna, element, s=None, ac=False, tran=False):
    mna = stamp_vsrc_mna(mna, element)
    index = mna.shape[0] - 1
    if ac:
        mna[index, index] = -s * element.value

    elif tran:
        h = 1e-12
        mna[element.n1, index] = +1
        mna[element.n2, index] = -1
        mna[index, element.n1] = +1
        mna[index, element.n2] = -1
        mna[index, index] = - element.value / h

    else:
        pass
    return mna


def stamp_vsrc_mna(mna, element):
    index = mna.shape[0]
    mna = _add_row_or_column(mna, add_a_row=True, add_a_column=True)
    mna[element.n1, index] = +1
    mna[element.n2, index] = -1
    mna[index, element.n1] = +1
    mna[index, element.n2] = -1
    return mna


def stamp_isrc_rhs(rhs, element):
    rhs[element.n1, 0] -= element.dc_value
    rhs[element.n2, 0] += element.dc_value
    return rhs


def stamp_vcvs_mna(mna, element):  # e
    mna = stamp_vsrc_mna(mna, element)
    index = mna.shape[0] - 1
    mna[index, element.nc1] = -element.value
    mna[index, element.nc2] = +element.value
    return mna


def stamp_cccs_mna(mna, element):  # f
    # TODO
    return mna


def stamp_vccs_mna(mna, element):  # g
    mna[element.n1, element.nc1] += element.value
    mna[element.n2, element.nc2] += element.value
    mna[element.n1, element.nc2] -= element.value
    mna[element.n2, element.nc1] -= element.value
    return mna


def stamp_ccvs_mna(mna, element):  # h
    # TODO
    return mna


def stamp_d_mna(mna, element):


    return mna


def stamp_mos_mna(mna, element):

    return mna


def stamp_rhs(rhs, element, dc_sweep_v_value=None, tran_stamp_value=None, s=None):
    rhs = _add_row_or_column(rhs, add_a_row=True, add_a_column=False)

    if dc_sweep_v_value:
        rhs[rhs.shape[0] - 1] = dc_sweep_v_value
    elif tran_stamp_value:
        rhs[rhs.shape[0] - 1] = tran_stamp_value
    else:
        if element.dc_value:
            rhs[rhs.shape[0] - 1] = element.dc_value
        elif element.abs_ac:
            rhs[rhs.shape[0] - 1] = element.abs_ac
    return rhs


def _add_row_or_column(matrix, add_a_row=False, add_a_column=False):
    if add_a_row:
        row = np.zeros((1, matrix.shape[1]))
        matrix = np.row_stack((matrix, row))
    if add_a_column:
        column = np.zeros((matrix.shape[0], 1))
        matrix = np.column_stack((matrix, column))
    return matrix
