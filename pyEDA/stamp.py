import numpy as np
import sympy


def stamp(mycircuit, elements, s=None, ac=False):
    node_number = mycircuit.get_nodes_number()

    mna = np.zeros([node_number, node_number], dtype=complex)
    rhs = np.zeros([node_number, 1], dtype=complex)

    for element in elements:
        element = element[0]
        name = element.name.lower()
        if name:
            if name[0] == 'r':  # resistor
                mna = stamp_r_mna(mna, element)
            elif name[0] == 'c':  # capacitor
                mna = stamp_c_mna(mna, element, s, ac)
            elif name[0] == 'l':  # inductor
                mna = stamp_l_mna(mna, element, s, ac)
            elif name[0] == 'v':  # voltage source
                mna = stamp_vsrc_mna(mna, element)
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

    # TODO: delete node 0 (gnd) in mna & rhs
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


def stamp_c_mna(mna, element, s=None, ac=False):
    if ac:
        mna[element.n1, element.n1] += s * element.value
        mna[element.n2, element.n2] += s * element.value
        mna[element.n1, element.n2] -= s * element.value
        mna[element.n2, element.n1] -= s * element.value
    else:
        pass

    return mna


def stamp_l_mna(mna, element, s=None, ac=False):
    mna = stamp_vsrc_mna(mna, element)
    index = mna.shape[0] - 1
    if ac:
        mna[index, index] = -s * element.value
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


def stamp_rhs(rhs, element):
    rhs = _add_row_or_column(rhs, add_a_row=True, add_a_column=False)
    rhs[rhs.shape[1] - 1] = element.value
    return rhs


def _add_row_or_column(matrix, add_a_row=False, add_a_column=False):
    if add_a_row:
        row = sympy.zeros(1, matrix.shape[1])
        matrix = matrix.row_insert(matrix.shape[0], row)
    if add_a_column:
        column = sympy.zeros(matrix.shape[0], 1)
        matrix = matrix.col_insert(matrix.shape[1], column)
    return matrix
