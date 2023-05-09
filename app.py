import pathlib
import platform
import pandas as pd
import streamlit as st
import plotly.express as px


from fastai.vision.all import *
from fastai.learner import load_learner
from huggingface_hub import hf_hub_download

plt = platform.system()
if plt == 'Windows': 
    pathlib.PosixPath = pathlib.WindowsPath


classes = ['amman', 'ayyappa', 'bhairava', 'brahma', 'buddha', 'durga', 'ganesha', 'hanuman', 'kaali', 'krishna', 'kurma', 'lakshmi', 'lingam', 'matsya', 'murugan', 'narasimha', 'nataraja', 'parasurama', 'rama', 'sai-baba', 'saraswati', 'shiva', 'theerthankaras', 'vamana', 'varaha', 'vishnu']
REPO_ID = st.secrets["REPO_ID"]

st.set_page_config(
    page_title="Identify the deity using Computer Vision.",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is an *extremely* cool app!"
    }
)

st.title(":sparkles: I:orange[deit]ify")
st.header("Discover the deity with a snap.")

# @st.cache_resource allows us to cache a function's output in memory. 
@st.cache_resource
def get_learner():
    learner = load_learner(hf_hub_download(f"{REPO_ID}", "model.pkl"))
    return learner

img = st.file_uploader(
    label='choose a file', 
    type=['png', 'jpg', 'jpeg'], 
    label_visibility="hidden"
)

if img is not None:
    data = img.getvalue()
    img = PILImage.create(img)


submit = st.button(label="submit", type="primary", use_container_width=True)

if submit:

    learner = get_learner()
    _,_, probs = learner.predict(img)
    scores, indices = torch.topk(probs[0], 5)
    scores = scores.tolist()
    indices = indices.tolist()

    df = pd.DataFrame({
        "labels": [classes[id] for id in indices],
        "scores (%)": [score*100 for score in scores]
    })

    fig = px.bar(
        data_frame=df,
        x="labels",
        y="scores (%)",
        height=280,
        width=400,
        text_auto=True,
        color="labels",
        orientation="v",
        template="plotly_white",
    )

    fig.update_traces(width=0.6)

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        xaxis_title=None,
        xaxis=(dict(showgrid=False)),
        yaxis=dict(visible=False, showticklabels=False),
        margin=dict(l=0, r=0, t=20, b=20),
        xaxis_fixedrange=True,
        yaxis_fixedrange=True
    )

    tab1, tab2 = st.tabs(["result", "about"])
    with tab1:
        # presents a bar chart with the probabilities of top-5-predictions.
        st.plotly_chart(fig)
    with tab2:
        # all the facts and knowledge about the deity goes here. 
        tab2.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor")
    