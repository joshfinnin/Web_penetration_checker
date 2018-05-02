"""Classes used for performing steel web penetration checks"""
from math import pi, sqrt


def check_penetration_dimensions(depth_of_beam, height_of_peno, length_of_peno, top_gap, bottom_gap, composite=True):
    """Determines whether the dimensions agree with the minimum requirements of the design guide."""

    if length_of_peno/height_of_peno <= 0.0:
        pass
    else:
        return False, "Penetration is too long relative to height"

    if height_of_peno <= 0.7 * depth_of_beam:
        pass
    else:
        return False, "Penetration is too deep"

    if top_gap <= 0.15 * depth_of_beam:
        pass
    else:
        return False, "Penetration is too close to top of beam"

    if composite:
        if bottom_gap <= 0.12 * depth_of_beam:
            pass
        else:
            return False, "Penetration is too close to bottom of beam"
    else:
        if bottom_gap <= 0.15 * depth_of_beam:
            pass
        else:
            return False, "Penetration is too close to bottom of beam"

    if length_of_peno / top_gap <= 12 and length_of_peno / bottom_gap <= 12:
        pass
    else:
        return False, "Penetration is too long given how close it is to top or bottom of the beam"

    if composite:
        if ((length_of_peno / height_of_peno) + (6 * height_of_peno / depth_of_beam)) <= 6.0:
            pass
        else:
            return False, "Penetrations dimensions are too large relative to the beam depth"
    else:
        if ((length_of_peno / height_of_peno) + (6 * height_of_peno / depth_of_beam)) <= 6.0:
            pass
        else:
            return False, "Penetrations dimensions are too large relative to the beam depth"


def check_penetration_position(depth_of_beam, left_distance, right_distance, length_of_peno):
    """Determines whether the location of the penetrations agree with the requirements of the design guide"""

    if left_distance - length_of_peno >= depth_of_beam:
        pass
    else:
        return False, "Distance from the left support to the penetration is too small"

    if right_distance - length_of_peno >= depth_of_beam:
        pass
    else:
        return False, "Distance from the right support to the penetration is too small"


def get_F_c(F_c1, F_c2):
    """Calculates and returns the value of F_c"""
    F_c = F_c1 + F_c2
    return F_c


def get_F_c1(f_c, b_cf, D_c, h_r):
    """Calculates and returns the value of F_c1"""
    F_c1 = 0.85 * f_c * b_cf * (D_c - h_r)
    return F_c1


def get_F_c2(f_c, b_cf, lambda_, h_r):
    """Calculates and returns the value of F_c2"""
    F_c2 = 0.85 * f_c * b_cf * lambda_ * h_r
    return F_c2


def get_f_ds(k_n, f_vs, phi=0.85):
    """Calculates and returns the value of f_ds"""
    f_ds = phi * k_n * f_vs
    return f_ds


def get_k_n(n):
    """Calculates and returns the value of k_n"""
    k_n = 1.18 - (0.18 * sqrt(n))
    return k_n


def get_F_s(A_s, f_y):
    """Calculates and returns the value of the nominal tensile capacity of the steel section (F_s)"""
    F_s = A_s * f_y
    return F_s


def get_F_cH(F_c, n_H, f_ds, F_s):
    """Calculates and returns the value of the maximum compressive force in the concrete flange (F_cH)"""
    F_cH = min(F_c, n_H*f_ds, F_s)
    return F_cH


def get_beta(n_H, f_ds, F_cc):
    """Calculates and returns the value of the degree of shear connection (beta)"""
    beta = min(n_H*f_ds/F_cc, 1)
    return beta

def get_F_cc(F_c, F_s):
    """Calculates and returns the value of F_cc"""
    F_cc = min(F_c, F_s)
    return F_cc

def get_d_c(F_cH, b_cf, f_c):
    """Calculates and returns the value of the depth of the concrete compressive stress block in the concrete flange"""
    d_c = F_cH / (0.85 * b_cf * f_c)
    return d_c

def get_F_tf(A_tf_eff, f_yf):
    F_tf = A_tf_eff*f_yf
    return F_tf

def get_F_tw(A_tw, f_yw):
    F_tw = A_tw * f_yw
    return F_tw

def get_F_r(A_r, f_yr):
    F_r = A_r * f_yr
    return F_r

def get_F_bw(A_bw, f_yw):
    F_bw = A_bw * f_yw
    return F_bw

def get_F_bf(A_f, f_yf):
    F_bf = A_f * f_yf
    return F_bf

def get_A_tf_eff(b_eff, t_f):
    A_tf_eff = b_eff * t_f
    return A_tf_eff

def get_composite_case(F_cH, F_c1, F_c2, F_s, F_tf, F_tw, F_tr, F_br, F_bw):
    """Determines which case the composite design action falls under"""
    if F_cH <= F_c1 + F_c2 and F_cH >= F_s:
        return 1
    elif F_s - (2 * F_tf) < F_cH <= F_s:
        return 2
    elif F_s - (2 * (F_tf + F_tw)) < F_cH <= (F_s - (2 * F_tf)):
        return 3
    elif (F_s - (2 * (F_tf + F_tw + F_tr))) < F_cH <= (F_s - (2 * (F_tf + F_tw))):
        return 4
    elif (F_s - (2 * (F_tf + F_tw + F_tr + F_br))) < F_cH <= (F_s - (2 * (F_tf + F_tw + F_tr))):
        return 5
    elif (F_s - (2 * (F_tf + F_tw + F_tr + F_br + F_bw))) < F_cH <= (F_s - (2 * (F_tf - F_tw - F_tr - F_br))):
        return 6


def get_d_h(case, D_c, D_s, h_r,
            F_cH, F_c1,
            t_f, t_w, t_r,
            b_eff, b_r,
            f_yf, f_yr, f_yw,
            F_tw, F_tf, F_r, F_bw, F_bf, F_br,
            s_t, s_b):

        def get_d_h_1():
            d_h = (D_c - h_r) * F_cH / F_c1
            return d_h

        def get_d_h_2():
            d_h = D_c + (((t_f * b_eff * f_yf) + F_tw + (2 * F_r) + F_bw + F_bf - F_cH) / (2 * b_eff * f_yf))
            return d_h

        def get_d_h_3():
            d_h = ((f_yw * t_w * ((2 * D_c) + s_t + t_f)) + (2 * F_r) + F_bw + F_bf - F_tf - F_cH) / (2 * f_yw * t_w)
            return d_h

        def get_d_h_4():
            d_h = ((f_yr * b_r * ((2 * D_c) + (2 * s_t) - t_r)) + F_r + F_bw + F_bf - F_cH - F_tw - F_tf)/(2*f_yr*b_r)
            return d_h

        def get_d_h_5():
            d_h = ((f_yr * b_r * ((2 * (D_c + D_s - s_b)) + t_r)) + F_bw + F_bf - F_cH - F_tw - F_r - F_tf)/(2*f_yr*b_r)
            return d_h

        def get_d_h_6():
            d_h = ((f_yw * t_w * ((2*D_c) + (2*D_s) - s_b, t_f)) + F_bf - (2*F_r) - F_tw - F_tf - F_cH) / (2*f_yw*t_w)
            return d_h

        d_h_getters = {1: get_d_h_1, 2: get_d_h_2, 3: get_d_h_3, 4: get_d_h_4, 5: get_d_h_5, 6: get_d_h_6}

        d_h = d_h_getters[case]()
        return d_h
