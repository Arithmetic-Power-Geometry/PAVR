import streamlit as st, pandas as pd
from pavr.core import simulate_session
from pavr.experiments import evaluate, summarize
st.set_page_config(page_title='PAVR',page_icon='🧠',layout='wide')
st.markdown("""<style>.block-container{max-width:1250px;padding-top:1.4rem}.hero{padding:1.2rem 1.5rem;border-radius:18px;border:1px solid rgba(120,120,120,.25);margin-bottom:1rem}</style>""",unsafe_allow_html=True)
st.markdown('<div class="hero"><h1>PAVR</h1><h3>Personalized Adaptive Virtual Reality</h3><p>Early cybersickness prediction with minimum-disruption intervention.</p></div>',unsafe_allow_html=True)
a,b,c=st.tabs(['Live Session','Policy Benchmark','About'])
with a:
    c1,c2,c3=st.columns(3)
    seed=c1.number_input('Seed',0,100000,7); steps=c2.slider('Session steps',30,300,120,10); bias=c3.slider('Personal susceptibility',-0.5,0.5,0.0,0.05)
    df=pd.DataFrame(simulate_session(int(seed),int(steps),float(bias)))
    m1,m2,m3,m4=st.columns(4)
    m1.metric('Mean risk',f'{df.risk_pred.mean():.3f}'); m2.metric('Post-adaptation risk',f'{df.risk_post.mean():.3f}'); m3.metric('Intervention rate',f"{(df.intervention!='none').mean()*100:.1f}%"); m4.metric('Burden',f'{df.burden.mean():.3f}')
    st.line_chart(df.set_index('t')[['risk_pred','risk_post']]); st.bar_chart(df['intervention'].value_counts()); st.dataframe(df,use_container_width=True); st.download_button('Download CSV',df.to_csv(index=False).encode(),'pavr_session.csv','text/csv')
with b:
    n=st.slider('Synthetic sessions',50,1000,240,10); s=pd.DataFrame(summarize(evaluate(n_sessions=n))).T; st.dataframe(s.style.format('{:.4f}'),use_container_width=True); st.bar_chart(s[['mean_risk','high_risk_fraction','burden']]); st.caption('Synthetic computational validation only; not human-subject evidence.')
with c:
    st.markdown('**Pipeline:** VR telemetry → personalized risk prediction → early warning → minimum-cost intervention → reassessment.\n\nPAVR is a research prototype, not a clinical device.')
