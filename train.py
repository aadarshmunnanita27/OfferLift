from pathlib import Path
import argparse, json, hashlib, urllib.request
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

ROOT=Path(__file__).resolve().parent
URL='https://www.minethatdata.com/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv'
MIRROR='https://raw.githubusercontent.com/W-Tran/uplift-modelling/master/data/hillstrom/Kevin_Hillstrom_MineThatData_E-MailAnalytics_DataMiningChallenge_2008.03.20.csv'

def features(d):
    x=d[['recency','history','mens','womens','newbie']].copy()
    for k,values in {'zip_code':['Rural','Surburban','Urban'],'channel':['Multichannel','Phone','Web']}.items():
        for val in values: x[k+'_'+val]=(d[k]==val).astype(int)
    return x

def export(m):
    ts=[]
    for t in m.estimators_:
        a=t[0].tree_;ts.append({'left':a.children_left.tolist(),'right':a.children_right.tolist(),'feature':a.feature.tolist(),'threshold':a.threshold.tolist(),'value':a.value[:,0,0].tolist()})
    p=float(m.init_.class_prior_[1])
    return {'base':float(np.log(p/(1-p))),'rate':m.learning_rate,'trees':ts}

def effect(y,t):
    a=y[t==1];b=y[t==0]
    if not len(a) or not len(b): return [0,0,0]
    diff=float(a.mean()-b.mean());se=float(np.sqrt(a.var()/len(a)+b.var()/len(b)))
    return [diff,diff-1.96*se,diff+1.96*se]

def curve(y,t,s):
    ix=np.argsort(-s,kind='stable');z=2*y*(2*t-1);cs=np.cumsum(z[ix]);n=len(y)
    pts=[{'fraction':0.,'gain':0.}]
    for f in np.linspace(.05,1,20):
        k=max(1,int(n*f));pts.append({'fraction':float(f),'gain':float(cs[k-1]/n)})
    xx=np.array([r['fraction'] for r in pts]);gg=np.array([r['gain'] for r in pts]);q=float(np.trapezoid(gg-xx*gg[-1],xx))
    return pts,q

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data');args=ap.parse_args();out=ROOT/'dist';out.mkdir(exist_ok=True)
    path=Path(args.data) if args.data else ROOT/'data/hillstrom.csv'
    if not path.exists():
        path.parent.mkdir(exist_ok=True)
        try: urllib.request.urlretrieve(URL,path)
        except Exception: urllib.request.urlretrieve(MIRROR,path)
    all_d=pd.read_csv(path);d=all_d[all_d.segment.isin(['Mens E-Mail','No E-Mail'])].reset_index(drop=True)
    x=features(d);y=d.conversion.to_numpy();t=(d.segment=='Mens E-Mail').astype(int).to_numpy()
    a,b=train_test_split(np.arange(len(d)),test_size=.4,stratify=t*2+y,random_state=42)
    v,te=train_test_split(b,test_size=.5,stratify=(t*2+y)[b],random_state=42)
    runs=[];options=[]
    for depth in [1,2]:
        ms=[]
        for arm in [0,1]:
            ix=a[t[a]==arm];m=GradientBoostingClassifier(n_estimators=80,max_depth=depth,min_samples_leaf=150,learning_rate=.04,random_state=42).fit(x.iloc[ix],y[ix]);ms.append(m)
        u=ms[1].predict_proba(x.iloc[v])[:,1]-ms[0].predict_proba(x.iloc[v])[:,1]
        _,q=curve(y[v],t[v],u);runs.append({'depth':depth,'validation_qini':q});options.append(ms)
    pick=int(np.argmax([r['validation_qini'] for r in runs]));ms=options[pick]
    p0=ms[0].predict_proba(x.iloc[te])[:,1];p1=ms[1].predict_proba(x.iloc[te])[:,1];u=p1-p0
    curves={};scores={}
    for name,s in [('Uplift',u),('Conversion',p1)]: curves[name],scores[name]=curve(y[te],t[te],s)
    rng=np.random.default_rng(42);qs=[]
    for _ in range(300):
        ix=rng.integers(0,len(te),len(te));qs.append(curve(y[te][ix],t[te][ix],u[ix])[1])
    rows=[]
    for j,i in enumerate(te): rows.append({'id':int(i),'x':{k:(float(d.loc[i,k]) if k in ['recency','history','mens','womens','newbie'] else str(d.loc[i,k])) for k in ['recency','history','mens','womens','newbie','zip_code','channel']},'y':int(y[i]),'t':int(t[i]),'p0':float(p0[j]),'p1':float(p1[j]),'uplift':float(u[j])})
    arms=[{'name':name,'n':len(g),'conversion':float(g.conversion.mean()),'visit':float(g.visit.mean())} for name,g in all_d.groupby('segment')]
    data={'n':len(all_d),'included':len(d),'features':x.columns.tolist(),'split':{'train':len(a),'validation':len(v),'test':len(te)},'runs':runs,'depth':runs[pick]['depth'],'models':[export(m) for m in ms],'arms':arms,'ate':effect(y[te],t[te]),'curves':curves,'qini':scores,'qini_ci':np.quantile(qs,[.025,.975]).tolist(),'rows':rows,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (out/'data.json').write_text(json.dumps(data,separators=(',',':')))
    (ROOT/'metrics.json').write_text(json.dumps({k:data[k] for k in ['split','runs','depth','arms','ate','qini','qini_ci','sha256']},indent=2))
    joblib.dump({'models':ms,'features':x.columns.tolist()},ROOT/'model.joblib');np.savez(ROOT/'split.npz',train=a,validation=v,test=te)
    d.iloc[te[:10]][['recency','history','mens','womens','newbie','zip_code','channel']].to_csv(out/'sample.csv',index=False)
    print((ROOT/'metrics.json').read_text())

if __name__=='__main__':main()
