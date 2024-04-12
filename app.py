import numpy as np
from scipy.stats import zscore
from pathlib import Path  # Import Path module
from wv import Model


def process_input(input_text):
    model = Model(("model/glove_short.txt"))
    input_list = [word.strip() for word in input_text.split(",")]
    if len(input_list) > 1:
        word_vectors = [model.find_word(word).vector for word in input_list if model.find_word(word)]
        if len(word_vectors) > 1:
            z_scores = zscore(np.array(word_vectors))
            threshold = 0.7
            filtered_words = []
            filtered_out_words = []
            prev_word = model.find_word(input_list[0])
            for word, z_score in zip(input_list[1:], z_scores[1:]):
                current_word = model.find_word(word)
                if prev_word and current_word and prev_word.similarity(current_word) >= threshold:
                    filtered_words.append(word)
                else:
                    filtered_out_words.append(word)
                prev_word = current_word
            return filtered_words, filtered_out_words
    return [], []

# This part remains expansive for Streamlit
import streamlit as st

user_input_text = st.text_input("Insert a list with commas")
if user_input_text:
    filtered_words, filtered_out_words = process_input(user_input_text)
    st.write("Filtered words:", filtered_words)
    st.write("Filtered out words:", filtered_out_words)
else:
    st.write("No input provided")


