from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from train import features

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='OfferLift',layout='wide')
@st.cache_resource
def load():return joblib.load(ROOT/'model.joblib'),json.loads((ROOT/'dist/data.json').read_text())
m,d=load()
def predict(df):
    x=features(df)[m['features']]
    return m['models'][0].predict_proba(x)[:,1],m['models'][1].predict_proba(x)[:,1]
st.title('OfferLift')
st.caption("Hillstrom randomized email experiment · Men's email versus no email")
a,b,c=st.tabs(['Experiment evidence','Customer explorer','Batch scoring'])
with a:
    st.dataframe(pd.DataFrame(d['arms']),hide_index=True)
    st.metric('Test average conversion effect',f"{100*d['ate'][0]:.2f} percentage points")
    st.write('95% approximate interval (percentage points):',[round(v*100,3) for v in d['ate'][1:]])
    st.line_chart(pd.DataFrame({k:pd.Series({r['fraction']:r['gain'] for r in v}) for k,v in d['curves'].items()}))
    st.write('Test Qini areas',d['qini']);st.write('Bootstrap Qini interval',d['qini_ci'])
    st.warning('Uplift ranking did not outperform random targeting on this test set. Do not claim verified targeting improvement.')
    f=st.slider('Target population (%)',5,100,20,5)/100
    margin=st.number_input('Assumed margin per extra conversion ($)',min_value=0.0,value=20.0)
    cost=st.number_input('Assumed contact cost ($)',min_value=0.0,value=.05)
    rows=pd.DataFrame(d['rows']);k=int(len(rows)*f);res=[]
    for name,key in [('Uplift','uplift'),('Conversion','p1')]:
        r=rows.sort_values(key,ascending=False,kind='stable').head(k);gain=float((2*r.y*(2*r.t-1)).sum())
        res.append({'strategy':name,'estimated_extra_conversions':gain,'simulated_profit':gain*margin-k*cost})
    st.dataframe(pd.DataFrame(res),hide_index=True)
with b:
    rec=st.slider('Months since last purchase',1,12,4);hist=st.number_input('Historical spend ($)',min_value=0.,value=200.)
    mens=st.checkbox("Previously purchased men's products",True);womens=st.checkbox("Previously purchased women's products")
    newbie=st.checkbox('New customer');zipc=st.selectbox('Area',['Rural','Surburban','Urban']);channel=st.selectbox('Channel',['Multichannel','Phone','Web'])
    df=pd.DataFrame([{'recency':rec,'history':hist,'mens':int(mens),'womens':int(womens),'newbie':int(newbie),'zip_code':zipc,'channel':channel}]);p0,p1=predict(df)
    st.metric('Estimated uplift',f'{(p1[0]-p0[0])*100:+.2f} pp');st.write({'without_email':float(p0[0]),'with_email':float(p1[0])})
    st.caption('Estimated conditional effect, not an observed individual treatment effect.')
with c:
    st.download_button('Sample CSV',(ROOT/'dist/sample.csv').read_bytes(),'sample.csv')
    f=st.file_uploader('Upload CSV',type='csv')
    if f:
        try:
            df=pd.read_csv(f);p0,p1=predict(df);out=df.assign(control_probability=p0,treatment_probability=p1,estimated_uplift=p1-p0)
            st.dataframe(out.head());st.download_button('Download scores',out.to_csv(index=False),'scores.csv')
        except Exception as e:st.error(str(e))
st.info('Email experiment results cannot establish cashback effectiveness. Profit estimates are assumptions, not measured savings.')
