import streamlit as st
import os
from recommender import (
    query_by_annotation,
    query_by_image_path_results,
    IMAGE_ROOT
)

st.set_page_config(layout="wide")

st.title("Context-Aware Clothing Recommender")


#Session state
if "liked_images" not in st.session_state:
    st.session_state.liked_images = []

if "explore_image" not in st.session_state:
    st.session_state.explore_image = None

if "results" not in st.session_state:
    st.session_state.results = []



#Sidebar filters and search
st.sidebar.header("Filters")

# Descriptive labels and their respective query 'code' values
GENDER_OPTIONS   = {"Male": "M", "Female": "F"}
WEATHER_OPTIONS  = {"Hot": "H", "Mild": "M", "Cold": "C"}
CONTEXT_OPTIONS  = {
    "Casual":        "C",
    "Formal":        "F",
    "Gym":           "G",
    "Smart Casual":  "SM",
    "Street":        "S",
    "Office":        "O",
}

#selection pane 
gender_label  = st.sidebar.selectbox("Gender",  list(GENDER_OPTIONS.keys()))
weather_label = st.sidebar.selectbox("Weather", list(WEATHER_OPTIONS.keys()))
context_label = st.sidebar.selectbox("Context", list(CONTEXT_OPTIONS.keys()))

gender  = GENDER_OPTIONS[gender_label]
weather = WEATHER_OPTIONS[weather_label]
context = CONTEXT_OPTIONS[context_label]

if st.sidebar.button("Find Outfits"):

    with st.spinner("Finding styles..."):
        results = query_by_annotation(
            gender=gender,
            Weather=weather,
            Context=context,
            top_k=3,
            n_queries=3
        )

    if results:
        all_images = []
        for q, sims in results.items():
            all_images.append(q)
            all_images.extend(sims)
        st.session_state.results = list(dict.fromkeys(all_images))
    else:
        st.session_state.results = []

    #Clear any open explore panel when a new search is run
    st.session_state.explore_image = None


st.sidebar.divider()

page = st.sidebar.radio("Sections", ["Recommendations", "Liked Images"])



#Like button function
def like_button(img_path: str, key: str):
    #Render a like / unlike toggle button for an image.
    already_liked = img_path in st.session_state.liked_images
    label = " Liked" if already_liked else " Like"
    if st.button(label, key=key):
        if already_liked:
            st.session_state.liked_images.remove(img_path)
        else:
            st.session_state.liked_images.append(img_path)
        st.rerun()



#Recommendations section
if page == "Recommendations":

    #Always clear explore state when on this page so the panel never bleeds over
    st.session_state.explore_image = None

    if not st.session_state.results:
        st.info("Run a search to see recommendations.")
    else:
        cols = st.columns(4)
        for i, img_path in enumerate(st.session_state.results):
            with cols[i % 4]:
                st.image(os.path.join(IMAGE_ROOT, img_path), use_container_width=True)
                like_button(img_path, key=f"like_rec_{img_path}")


# Liked images section
if page == "Liked Images":

    st.subheader("Your Liked Styles")

    if not st.session_state.liked_images:
        st.info("No liked images yet.")
    else:
        cols = st.columns(4)
        for i, img_path in enumerate(st.session_state.liked_images):
            with cols[i % 4]:
                st.image(os.path.join(IMAGE_ROOT, img_path), use_container_width=True)
                like_button(img_path, key=f"like_liked_{i}")

                if st.button(" Explore Similar", key=f"explore_{i}"):
                    #Toggle: clicking the same image again closes the panel
                    if st.session_state.explore_image == img_path:
                        st.session_state.explore_image = None
                    else:
                        st.session_state.explore_image = img_path
                    st.rerun()

    
    #Explore similar images section
    if st.session_state.explore_image:

        st.divider()

        col_title, col_close = st.columns([8, 1])
        with col_title:
            st.subheader("Similar Styles")
        with col_close:
            if st.button("✖ Close"):
                st.session_state.explore_image = None
                st.rerun()

        query_img = st.session_state.explore_image
        similar_results = query_by_image_path_results(query_img, top_k=8)

        cols = st.columns(4)
        for i, img_path in enumerate(similar_results):
            with cols[i % 4]:
                st.image(os.path.join(IMAGE_ROOT, img_path), use_container_width=True)
                like_button(img_path, key=f"like_sim_{img_path}")