# Checks for the "working backwards" section of cai_occupancy.tex
import numpy as np
from scipy.optimize import minimize
r=np.random.default_rng(0); S,A,Z,g,lam=4,3,3,0.9,0.5
P=r.dirichlet(np.ones(S),size=(S,A)); nu=np.ones(S)/S
mu=r.dirichlet(np.ones(S*A)).reshape(S,A); rq=r.normal(size=(S,A))
def occ(pi):
    Ppi=np.einsum('sa,sat->st',pi,P); ds=(1-g)*np.linalg.solve(np.eye(S)-g*Ppi.T,nu); return ds[:,None]*pi
def primal(th):
    pi=np.exp(th.reshape(S,A)); pi/=pi.sum(1,keepdims=True); d=occ(pi)
    return -(d*rq).sum()+lam*(d*np.log(d/mu)).sum()
best=min((minimize(primal,r.normal(size=S*A),method='BFGS',options={'gtol':1e-10}) for _ in range(5)),key=lambda o:o.fun)
# REPS dual: d = mu exp(delta_V/lam - 1), delta_V = rq + g P V - V
def dual(V):
    delta=rq+g*P@V-V[:,None]; return (1-g)*nu@V+lam*(mu*np.exp(delta/lam-1)).sum()
V=minimize(dual,np.zeros(S),method='BFGS',options={'gtol':1e-12}).x
d=mu*np.exp((rq+g*P@V-V[:,None])/lam-1)
flow=d.sum(1)-(1-g)*nu-g*np.einsum('sa,sat->t',d,P)
print("REPS: max flow residual",abs(flow).max()," sum d",d.sum())
print("REPS objective",-(d*rq).sum()+lam*(d*np.log(d/mu)).sum()," policy-search objective",best.fun)
# (1-lam) identity, deterministic channel, uniform mu
f=r.integers(0,Z,size=(S,A)); d=occ(r.dirichlet(np.ones(A),size=S)); n=S*A
H=lambda x:-(x[x>0]*np.log(x[x>0])).sum()
pz=np.bincount(f.ravel(),weights=d.ravel(),minlength=Z)
lhs=H(pz)+lam*((d*np.log(d*n)).sum())
HSAgZ=H(d.ravel())-H(pz)
print("identity:",lhs,(1-lam)*H(pz)-lam*HSAgZ+lam*np.log(n))

# Joint-KL form: E_dK[-ln q] + lam KL(d||mu) = lam (KL(dK || Pi_q) - ln Z_q), Pi_q = mu K q^(1/lam) / Z_q
K=r.dirichlet(np.ones(Z),size=(S,A)); q=r.dirichlet(np.ones(Z)); d=r.dirichlet(np.ones(S*A)).reshape(S,A)
lhs=-(d[...,None]*K*np.log(q)).sum()+lam*(d*np.log(d/mu)).sum()
Pi=mu[...,None]*K*q**(1/lam); Zq=Pi.sum(); Pi/=Zq; J=d[...,None]*K
print("joint KL:",lhs, lam*((J*np.log(J/Pi)).sum()-np.log(Zq)))
