"""
This code is a Streamlit application that hosts a semantic similarity transformer model application.

The application allows users to:

* Select a model and its tokenizer.
* Set the number of database rows to embed.
* Set the number of similar results to display.
* Click the "Embed Data" button to embed the data and upload it to Pinecone and the logger.
* View the embeddings.

The application uses the following libraries:

* `streamlit`
* `json`
* `datetime`
* `torch`
* `pinecone`

"""
# Home Page
from types import SimpleNamespace
import json
import streamlit as st
import datetime
import torch
import pinecone

#preprocessing the text
import re
import string
import nltk
from nltk.corpus import stopwords
import pandas as pd

def remove_urls_extra(text):
    # remove URLs
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    text = re.sub(r'pic.twitter.com\S+', '', text)
    text = re.sub(r't\.co\S+', '', text)
    
    # it will remove the old style retweet text "RT"
    text = re.sub(r'^RT[\s]+', '', text)

    # it will remove hyperlinks
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text)

    # only removing the hash # sign from the word
    text = re.sub(r'#', '', text)

    # it will remove single numeric terms in the tweet. 
    text = re.sub(r'[0-9]', '', text)
    
    return text

def remove_emojis(text):
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def preprocess_text(test_list):
    temp_df = pd.DataFrame(test_list)
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()
    
    stop_words = set(stopwords.words('english'))
    
    def lemmatize_text(text):
        return " ".join([lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)])
    
    def remove_stopwords(text):
        return " ".join([word for word in str(text).split() if word not in stop_words])
    
    temp_df["IFNULL(description,'')"] = temp_df["IFNULL(description,'')"].apply(remove_urls_extra)
    temp_df["IFNULL(description,'')"] = temp_df["IFNULL(description,'')"].apply(remove_emojis)
    temp_df["IFNULL(description,'')"] = temp_df["IFNULL(description,'')"].apply(str.lower)
    temp_df["IFNULL(description,'')"] = temp_df["IFNULL(description,'')"].apply(lambda x: remove_stopwords(x))
    temp_df["IFNULL(description,'')"] = temp_df["IFNULL(description,'')"].apply(lambda x: lemmatize_text(x))
    return temp_df

# Import model and logger classes
from model_class import Model
from system_logging import SystemLogging
from pinecone_helper import *
from eCairn_connector import eCairnConnector
from connection_type import Types
from plot import *

# Load configuration files
databaseConfig: SimpleNamespace
pineconeConfig: SimpleNamespace
with open("config.json", "r") as f:
    config = json.load(f, object_hook=lambda x: SimpleNamespace(**x))
    databaseConfig = config.oregonstate.data
    loggingConfig = config.oregonstate.logging
    pineconeConfig = config.pinecone

# Home Page
def set_model(test_model, logger):
    """
    Set the model and its tokenizer.

    Args:
        test_model: A `Model` object.
        logger: A `SystemLogging` object.

    Returns:
        None.
    """
    # ID
    test_model.id = st.number_input("ID", help="ID of profile for similarity. ID values start at 2, and some values may not exist in the database.")
    test_model.name = st.text_input(
        'Name', placeholder="Must be unique", help='Name for database entry')
    # Tokenizer
    test_model.tokenizer_name = st.selectbox('Tokenizer', ('sentence-transformers/all-MiniLM-L6-v2', 'Option 2'),
                                             index=0, help='Sentence Transformer Tokenizer')
    # Model
    test_model.model_name = st.selectbox('Model', ('sentence-transformers/all-MiniLM-L6-v2', 'Option 2'),
                                         index=0, help='Sentence Transformer Model')

    # TODO Make conditional with other models
    # Dimensions
    if test_model.model_name == 'sentence-transformers/all-MiniLM-L6-v2':
        test_model.dimensions = 384
    else:
        test_model.dimensions = 0
    # Pinecone namespace
    logger.pinecone_namespace = name_space = st.text_input('Pinecone Namespace',
                                                           value="Streamlit_Test", help='Pinecone namespace to store embeddings.')
    # Limit
    test_model.limit = st.number_input(
        'Limit (Maximum)', help='Number of database rows to embed.', step=1)
    # Number of similar results to get
    logger.top_n = st.number_input(
        'Similar Results', help='Number of results from embeddings.', step=1)
    # Device setting
    if torch.cuda.is_available():
        test_model.device = "cuda:0"

    else:
        test_model.device = "cpu"


def setLogger(logger, tokenizer_name, model_name, dimensions, device, name, index):
    """
    Set the logger.

    Args:
        logger: A `SystemLogging` object.
        tokenizer_name: The name of the tokenizer.
        model_name: The name of the model.
        dimensions: The number of dimensions of the model.
        device: The device to use for training.
        name: The name of the logger.
        index: The index of the Pinecone namespace.

    Returns:
        None.
    """
    logger.system_start = datetime.datetime.now()
    logger.tokenizer = tokenizer_name
    logger.model = model_name
    logger.model_dim = dimensions
    logger.input = [i for i in range(20)]
    logger.device = device
    logger.name = name
    logger.pinecone_index = index


def main():
    """
    The main function of the application.

    Returns:
        None.
    """
    # Set page title and sidebar text
    st.set_page_config(page_title="Home")
    st.sidebar.success("Home")
    st.subheader('Model Embedding')
    col1, col2 = st.columns(2)

    # Create a model class
    test_model = Model

    # Connect to Database
    db = eCairnConnector()

    # Create a logger class
    logger = SystemLogging(loggingConfig)

    # Get Model Inputs
    with col1:
        set_model(test_model, logger)
    # Check if the user wants to embed the data
    run_btn = st.button("Embed Data")

    if run_btn:
        # Set the logger parameters
        setLogger(logger,
                  test_model.tokenizer_name,
                  test_model.model_name,
                  test_model.dimensions,
                  test_model.device,
                  test_model.name,
                  pineconeConfig.index)

        if test_model.limit != 0:
            db.get_test_list(Types.Connection.FROM_TYPE_DB,
                             db_config=databaseConfig, limit=test_model.limit)
        else:
            db.get_test_list(Types.Connection.FROM_TYPE_DB,
                             db_config=databaseConfig)
        # Get the test list from the database
        test_list = db.get_dataframe()
        test_list = preprocess_text(test_list)
        test_list = test_list.to_numpy()

        # Render rows selected
        with col2:
            st.write(test_list)

        # Embed data and set progress bar
        progress_bar = st.progress(0, text="Embedding data...")
        embeddings_dataset = test_model().get_embeddings(logger, test_list, progress_bar)
        # Display a success message
        st.success('Data embedded successfully!')

        # Call the function to generate the graph
        embeddings = [x[1] for x in embeddings_dataset]
        fig = plot_embeddings_graph(embeddings)

        # Display the graph in Streamlit
        st.pyplot(fig)

        # Upload the embeddings to pinecone
        pinecone.init(api_key=pineconeConfig.key,
                      environment=pineconeConfig.env)
        index = pinecone.Index(pineconeConfig.index)


        
        pineconeCheck = uploadToPineCone(logger, index, embeddings_dataset)
        # Display a message on upload success
        if pineconeCheck:
            st.success('Pinecone upload successful')
        else:
            st.error('Pinecone upload failed', icon="🚨")

        # Logger
        loggerCheck, top_results, search_input = uploadLog(logger, index, embeddings_dataset, int(test_model.id))

        if loggerCheck:
            st.success('Logger upload successful')
        else:
            st.error('Logger upload failed', icon="🚨")

        st.table(search_input)

        # Render similar results
        st.table(top_results)


if __name__ == '__main__':
    main()
