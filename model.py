"""Numerics for the identifiability note."""
import math
import numpy as np

# ---------------- classical HH rate functions (squid, 6.3 C) ----------------
def vtrap(x, y):
    z = x / y
    if abs(z) < 1e-7:
        return y * (1.0 + z/2.0 + z*z/12.0)
    return x / (-math.expm1(-z))

def base_rates(v):
    am = 0.1 * vtrap(v + 40.0, 10.0)
    bm = 4.0 * math.exp(-(v + 65.0) / 18.0)
    ah = 0.07 * math.exp(-(v + 65.0) / 20.0)
    bh = 1.0 / (1.0 + math.exp(-(v + 35.0) / 10.0))
    an = 0.01 * vtrap(v + 55.0, 10.0)
    bn = 0.125 * math.exp(-(v + 65.0) / 80.0)
    return am, bm, ah, bh, an, bn

# ---------------- two-compartment model with per-gate rate multipliers -------
class P:
    def __init__(self, rho_s=(1,1,1), rho_a=(1,1,1), shift_s=0.0, shift_a=0.0,
                 g_na_s=120., g_na_a=240., g_k=36., g_l=0.3, c_m=1.0,
                 e_na=50., e_k=-77., e_l=-54.387, g_c=2.0,
                 pulse=(5.,6.,20.)):
        self.__dict__.update(locals()); del self.self

def rates(v, rho, shift):
    am, bm, ah, bh, an, bn = base_rates(v + shift)
    rm, rh, rn = rho
    return am*rm, bm*rm, ah*rh, bh*rh, an*rn, bn*rn

def rhs(t, y, p):
    vs, ms, hs, ns, va, ma, ha, na = y
    ams,bms,ahs,bhs,ans,bns = rates(vs, p.rho_s, p.shift_s)
    ama,bma,aha,bha,ana,bna = rates(va, p.rho_a, p.shift_a)
    ina_s = p.g_na_s*ms**3*hs*(vs-p.e_na); ik_s = p.g_k*ns**4*(vs-p.e_k); il_s = p.g_l*(vs-p.e_l)
    ina_a = p.g_na_a*ma**3*ha*(va-p.e_na); ik_a = p.g_k*na**4*(va-p.e_k); il_a = p.g_l*(va-p.e_l)
    on, off, amp = p.pulse
    iext = amp if on <= t < off else 0.0
    dvs = (-ina_s-ik_s-il_s + p.g_c*(va-vs) + iext)/p.c_m
    dva = (-ina_a-ik_a-il_a + p.g_c*(vs-va))/p.c_m
    return np.array([dvs,
                     ams*(1-ms)-bms*ms, ahs*(1-hs)-bhs*hs, ans*(1-ns)-bns*ns,
                     dva,
                     ama*(1-ma)-bma*ma, aha*(1-ha)-bha*ha, ana*(1-na)-bna*na])

def gate_inf(v, rho, shift):
    am,bm,ah,bh,an,bn = rates(v, rho, shift)
    return am/(am+bm), ah/(ah+bh), an/(an+bn)

def rest_state(p):
    from scipy.optimize import fsolve
    ms,hs,ns = gate_inf(-65., p.rho_s, p.shift_s)
    ma,ha,na = gate_inf(-65., p.rho_a, p.shift_a)
    y0 = np.array([-65.,ms,hs,ns,-65.,ma,ha,na])
    import copy
    q = copy.copy(p); q.pulse = (p.pulse[0], p.pulse[1], 0.0)
    return fsolve(lambda z: rhs(0., z, q), y0)

def simulate(p, dt=0.002, t_end=20.0, y0=None):
    n = int(round(t_end/dt)); t = np.linspace(0., t_end, n+1)
    y = np.empty((n+1, 8)); y[0] = rest_state(p) if y0 is None else y0
    for i in range(n):
        ti, yi = t[i], y[i]
        k1 = rhs(ti, yi, p); k2 = rhs(ti+dt/2, yi+dt*k1/2, p)
        k3 = rhs(ti+dt/2, yi+dt*k2/2, p); k4 = rhs(ti+dt, yi+dt*k3, p)
        y[i+1] = yi + dt*(k1+2*k2+2*k3+k4)/6
    return t, y
