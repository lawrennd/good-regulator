import numpy as np, itertools
def occ(pi,P,nu,g):
    S=P.shape[0]; Ppi=np.einsum('sa,sat->st',pi,P)
    ds=(1-g)*np.linalg.solve(np.eye(S)-g*Ppi.T,nu); return ds[:,None]*pi
H=lambda p:-(p[p>0]*np.log(p[p>0])).sum()
wins=0; trials=30
for seed in range(trials):
    r=np.random.default_rng(seed); S,A,Z,g=5,2,4,0.9
    P=r.dirichlet(np.ones(S)*0.5,size=(S,A)); K=r.dirichlet(np.ones(Z)*0.5,size=(S,A)); nu=np.ones(S)/S
    best=min(H((occ(np.eye(A)[list(a)],P,nu,g)[...,None]*K).sum((0,1))) for a in itertools.product(range(A),repeat=S))
    res=[]
    for init in range(5):
        q=r.dirichlet(np.ones(Z)); beta=200.0
        for it in range(300):
            rq=(K*np.log(q)).sum(-1)                  # E-step: soft VI, uniform prior pi0
            V=np.zeros(S)
            for _ in range(500):
                Q=beta*rq+g*P@V; m=Q.max(1); V=m+np.log(np.exp(Q-m[:,None]).mean(1))
            pi=np.exp(Q-V[:,None])/A; pi/=pi.sum(1,keepdims=True)
            q=(occ(pi,P,nu,g)[...,None]*K).sum((0,1)); q=np.maximum(q,1e-300)   # M-step
        res.append(H(q))
    wins+= min(res)<=best+1e-3
    if seed<5: print(f"seed {seed}: brute-force min H={best:.4f}  EM best-of-5={min(res):.4f}  EM runs={np.round(res,4)}")
print(f"EM best-of-5 reaches the brute-force optimum in {wins}/{trials} MDPs")
