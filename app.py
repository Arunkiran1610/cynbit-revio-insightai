"""Streamlit showcase for Cynbit Revio InsightAI."""
import pandas as pd
import streamlit as st
from src.engine import classify, analyze_reviews

st.set_page_config(page_title='Revio InsightAI | Cynbit concept', page_icon='📊', layout='wide')
st.title('Revio InsightAI')
st.caption('Concept extension for Cynbit Revio • synthetic data • rule-based explainable baseline • not affiliated with Cynbit')
st.info('This demo uses deterministic heuristic classification, not a trained or calibrated AI model. Review replies are suggestions requiring human approval.')

tab1, tab2 = st.tabs(['Review triage', 'Operational dashboard'])
with tab1:
    review = st.text_area('Customer review', 'I waited 45 minutes and the staff was rude. Really disappointed.', height=110)
    rating = st.slider('Star rating', 1, 5, 1)
    if st.button('Analyze review', type='primary'):
        try:
            r = classify(review, rating)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric('Sentiment', r.sentiment.title())
            c2.metric('Issue', r.issue.replace('_', ' ').title())
            c3.metric('Priority', r.priority.title())
            c4.metric('Evidence strength', f'{r.confidence:.0%}')
            st.write('**Assigned team:**', r.team)
            st.write('**Matched terms:**', r.evidence)
            if r.needs_review:
                st.warning('Human review required: safety, ambiguity, or low evidence.')
            st.subheader('Suggested action')
            st.write(r.action)
            st.subheader('Draft customer response — approval required')
            st.text_area('Edit before publication', r.reply, height=125)
        except ValueError as e:
            st.error(str(e))
with tab2:
    st.write('Load the provided **synthetic** sample or upload a CSV with columns `review`, `rating`, `location`, `date`.')
    uploaded = st.file_uploader('Optional CSV', type='csv')
    try:
        if uploaded is None:
            df = pd.read_csv('data/synthetic_reviews.csv')
        else:
            df = pd.read_csv(uploaded)
        if not {'review','rating'}.issubset(df.columns):
            st.error('Required columns: review, rating')
        elif df.empty:
            st.warning('No reviews found.')
        elif len(df) > 5000:
            st.error('For demo safety, upload at most 5,000 reviews.')
        else:
            df['rating'] = pd.to_numeric(df['rating'], errors='raise').astype(int)
            if not df['rating'].between(1,5).all():
                raise ValueError('Ratings must be 1–5.')
            df['review'] = df['review'].fillna('')
            df = pd.DataFrame(analyze_reviews(df.to_dict('records')))
            c1, c2, c3 = st.columns(3)
            c1.metric('Reviews', len(df))
            c2.metric('Negative', int((df.sentiment == 'negative').sum()))
            c3.metric('Require human review', int(df.needs_review.sum()))
            st.subheader('Issue volume')
            st.bar_chart(df.issue.value_counts())
            st.subheader('Prioritized action queue')
            rank = {'critical':0,'high':1,'medium':2,'low':3}
            df['priority_order'] = df.priority.map(rank)
            st.dataframe(df.sort_values('priority_order').drop(columns=['priority_order']), use_container_width=True, hide_index=True)
            st.download_button('Download analyzed CSV', df.drop(columns=['priority_order']).to_csv(index=False), 'revio_insights.csv', 'text/csv')
            st.caption('Counts describe the demo input only; they are not Cynbit business metrics.')
    except (ValueError, KeyError, pd.errors.ParserError) as exc:
        st.error(f'Cannot process file: {exc}')
