import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from model import P, simulate, base_rates, gate_inf

plt.rcParams.update({"font.size":8,"axes.spines.top":False,"axes.spines.right":False,
                     "lines.linewidth":1.2,"figure.dpi":200})

eps1,q1 = 0.05, math.log(1.4)/0.05
eps2,q2 = 0.01, math.log(1.4)/0.01
Q10,dT  = 3.0, 10*math.log(1.4)/math.log(3.0)
rhos = [math.exp(q1*eps1), math.exp(q2*eps2), Q10**(dT/10.0)]
DELTA = 2.2872                       # timing-matched effective-voltage shift

base=P(); tb,yb = simulate(base, t_end=12.0)
res = [simulate(P(rho_a=(r,r,1.0)), t_end=12.0) for r in rhos]
tev,yev = simulate(P(shift_a=DELTA), t_end=12.0)

d12 = np.abs(res[0][1][:,0]-res[1][1][:,0]).max()
d13 = np.abs(res[0][1][:,0]-res[2][1][:,0]).max()
eff = np.abs(res[0][1][:,0]-yb[:,0]).max()
resid = np.abs(res[0][1][:,0]-yev[:,0]).max()
print("rho values:", rhos)
print("dT = %.4f C" % dT)
print("max |dV_s| among the three parameterisations: %.3e and %.3e mV" % (d12,d13))
print("effect size vs control: %.3f mV ; symmetric vs matched eff-voltage residual: %.3f mV" % (eff,resid))

# ---- Figure 1 ----
fig, ax = plt.subplots(figsize=(5.2,2.7), constrained_layout=True)
ax.plot(tb, yb[:,0], color="0.62", label="unperturbed control")
sty=[("-", "#1b4d89",2.6,r"strain, $\varepsilon=0.05$, $q_x=6.73$"),
     ("--","#c85a1e",1.5,r"strain, $\varepsilon=0.01$, $q_x=33.65$"),
     (":", "#1a7f5a",1.5,r"kinetic $Q_{10}=3$, $\Delta T=3.06\,^{\circ}\mathrm{C}$")]
for (ls,c,lw,lab),(t,y) in zip(sty,res):
    ax.plot(t,y[:,0],ls,color=c,lw=lw,label=lab)
ax.set_xlim(4.5,11); ax.set_xlabel("time (ms)"); ax.set_ylabel("somatic voltage (mV)")
ax.legend(frameon=False, fontsize=6.6, loc="upper right")
fig.savefig("fig_equivalence.pdf"); plt.close(fig)

# ---- Figure 2 ----
def tm(v):
    am,bm,_,_,_,_ = base_rates(v); return 1.0/(am+bm)
def th(v):
    _,_,ah,bh,_,_ = base_rates(v); return 1.0/(ah+bh)
V=np.linspace(-80,20,401)
flat=np.full_like(V, math.log(1.4))
lm=np.array([math.log(tm(v)/tm(v+DELTA)) for v in V])
lh=np.array([math.log(th(v)/th(v+DELTA)) for v in V])
print("eff-voltage log-tau ratio: m in [%.3f, %.3f], h in [%.3f, %.3f]"%(lm.min(),lm.max(),lh.min(),lh.max()))
mi =np.array([gate_inf(v,(1,1,1),0.0)[0] for v in V]); mie=np.array([gate_inf(v,(1,1,1),DELTA)[0] for v in V])
hi =np.array([gate_inf(v,(1,1,1),0.0)[1] for v in V]); hie=np.array([gate_inf(v,(1,1,1),DELTA)[1] for v in V])

fig,ax=plt.subplots(1,3,figsize=(7.1,2.3),constrained_layout=True)
ax[0].axhline(0,color="0.88",lw=0.6)
ax[0].plot(V,flat,color="#1b4d89",label=r"symmetric ($m$ and $h$)")
ax[0].plot(V,lm,"--",color="#c85a1e",label=r"effective voltage, $m$")
ax[0].plot(V,lh,":",color="#1a7f5a",label=r"effective voltage, $h$")
ax[0].set_xlabel("$V$ (mV)"); ax[0].set_ylabel(r"$\log[\tau_x(V,0)/\tau_x(V,\varepsilon)]$")
ax[0].legend(frameon=False,fontsize=5.8,loc="upper left")
ax[0].set_title("(a) relaxation-time signature",fontsize=7.5,loc="left")
ax[1].plot(V,mi,color="#1b4d89"); ax[1].plot(V,mie,"--",color="#c85a1e")
ax[1].plot(V,hi,color="#1b4d89",alpha=0.55); ax[1].plot(V,hie,"--",color="#c85a1e",alpha=0.55)
ax[1].text(-20,0.82,r"$m_\infty$",fontsize=7); ax[1].text(-72,0.80,r"$h_\infty$",fontsize=7)
ax[1].set_xlabel("$V$ (mV)"); ax[1].set_ylabel("steady-state occupancy")
ax[1].set_title("(b) steady-state signature",fontsize=7.5,loc="left")
ax[2].plot(tb,yb[:,0],color="0.62",label="control")
ax[2].plot(res[0][0],res[0][1][:,0],color="#1b4d89",label="symmetric")
ax[2].plot(tev,yev[:,0],"--",color="#c85a1e",label="effective voltage")
ax[2].set_xlim(4.5,11); ax[2].set_xlabel("time (ms)"); ax[2].set_ylabel("somatic voltage (mV)")
ax[2].legend(frameon=False,fontsize=6); ax[2].set_title("(c) whole-cell waveform",fontsize=7.5,loc="left")
fig.savefig("fig_discrimination.pdf"); plt.close(fig)
print("done")

# ---- numbers added in the citation revision ----
print("--- gate-selective thermal floor (Frankenhaeuser & Moore 1963 Q10 values) ---")
Q10m, Q10h, Q10n = 1.71, 2.35, 3.12
for a, b, na, nb in ((Q10m, Q10h, "m", "h"), (Q10m, Q10n, "m", "n")):
    per = abs(math.log(a / b)) / 10.0
    print("  d log(rho_%s/rho_%s): %.4f per C; %.4f at 0.31 C (ratio %.4f); "
          "rho ratio at dT=%.2f C is %.4f"
          % (na, nb, per, per * 0.31, math.exp(per * 0.31), dT, (a / b) ** (dT / 10.0)))
print("--- conductance divergence table, eps=0.05, dT=%.4f C ---" % dT)
strain_factor = 1.0 / 1.05
for q in (1.1, 1.3, 1.7):
    warm = q ** (dT / 10.0)
    print("  Q10_g=%.1f: strain %.3f, warming %.3f, divergence %.1f%%"
          % (q, strain_factor, warm, 100 * (warm / strain_factor - 1)))

# ---- calibration robustness check for Section 5.3 ----
from scipy.optimize import minimize_scalar
def _resid(d):
    _, y = simulate(P(shift_a=float(d)), t_end=12.0)
    return float(np.abs(y[:, 0] - res[0][1][:, 0]).max())
_opt = minimize_scalar(_resid, bracket=(2.5, 2.8, 3.0), method="brent",
                       options={"xtol": 1e-4})
print("--- effective-voltage calibration ---")
print("  timing-matched delta %.4f mV: residual %.3f mV (%.1f%% of effect)"
      % (DELTA, _resid(DELTA), 100 * _resid(DELTA) / eff))
print("  residual-minimising delta %.4f mV: residual %.3f mV (%.1f%% of effect)"
      % (_opt.x, _opt.fun, 100 * _opt.fun / eff))
_lm = np.array([math.log(tm(v) / tm(v + _opt.x)) for v in V])
_lh = np.array([math.log(th(v) / th(v + _opt.x)) for v in V])
print("  at the best-case delta: L_m in [%.3f, %.3f], L_h in [%.3f, %.3f]; "
      "symmetric flat at %.3f" % (_lm.min(), _lm.max(), _lh.min(), _lh.max(),
                                  math.log(1.4)))
