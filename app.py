"""
    Streamlit app for the project
"""
from pathlib import Path
import requests
import streamlit as st
from wv import Model


def download_from_one_drive(url: str, target: Path) -> None:
    """ Download a file from the internet """
    if "?" in url:
        url = url[:url.index("?")]
    url += "?download=1"

    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with target.open('wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)


@st.cache_resource
def load_model(name: str) -> Model:
    """ Load a model from the cloud if not already loaded """
    try:
        save_dest = Path('model')
        save_dest.mkdir(exist_ok=True)

        f_checkpoint = save_dest.joinpath(name)
        if not f_checkpoint.exists():
            with st.spinner("Downloading model... please wait"):
                download_from_one_drive(cloud_model_location, f_checkpoint)
        return Model(f_checkpoint)
    except OSError as e:
        st.error(f"Error: {e.strerror}")


cloud_model_location = "https://myerauedu-my.sharepoint.com/:t:/g/personal/paulusw_erau_edu/ET7q4WvkFEJNtziyn8-cPCgBta1PlXLolFr-BrDqcY9Nsg"

st.title('Simple Word Relationship App')
st.write('a to b is like c to ?')
model = load_model("glove_short.txt")
st.toast("Model loaded successfully")

king = model.find_word("king")
man = model.find_word("man")
woman = model.find_word("woman")
q = king - man + woman
q.normalize()
x = model.find_similar_words(q, 10)
st.text(x)
st.divider()
st.text(f"'king' to 'man' is like '{x[0].text}' to 'woman'")
