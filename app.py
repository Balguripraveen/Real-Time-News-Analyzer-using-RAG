import streamlit as st
from news_fetcher import fetch_news
from rag_pipeline import (
    build_vector_db,
    generate_answer,
    extract_topic
    )
# Page Config

st.set_page_config(
    page_title="AI News Analyzer",
    page_icon="📰",
    layout="wide"
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "news_loaded" not in st.session_state:
    st.session_state.news_loaded = False

# Custom CSS

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stChatMessage {
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 10px;
}

h1 {
    color: #00FFAA;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# Title

st.title("📰 AI Real-Time News Analyzer")

st.markdown(
    "# Chat with latest news"
)

# Sidebar

# -----------------------------------
# Sidebar
# -----------------------------------
with st.sidebar:

    st.header("⚙️ Controls")

    if st.button("🔄 Load Latest News"):

        with st.spinner("Fetching and indexing news..."):

            articles = fetch_news("latest news")

            build_vector_db(articles)

            st.session_state.news_loaded = True

        st.success("News Loaded Successfully!")

    st.markdown("---")

    st.markdown("""
    ### 💡 Example Questions
    - Latest AI news
    - Technology updates
    - US politics
    - Stock market news
    """)


# Chat Messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# User Input
prompt = st.chat_input("Ask about latest news...")


#response generation

if prompt:

    if not st.session_state.news_loaded:

        st.warning("Please load news first!")

    else:

        # Store user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # Display user message
        with st.chat_message("user"):

            st.markdown(prompt)

        # AI response
        with st.chat_message("assistant"):

            with st.spinner("Analyzing latest news..."):
                topic = extract_topic(prompt)
                st.info(f"Detected Topic: {topic}")
                articles = fetch_news(topic)
                build_vector_db(articles)
                response = generate_answer(prompt)

                st.markdown(response)

        # Store AI response

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )