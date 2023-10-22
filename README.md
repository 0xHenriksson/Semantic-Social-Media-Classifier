# Profile People Using Social Media
 
This application employs advanced Natural Language Processing (NLP) techniques, coupled with vector database technology, to profile individuals based on their social media data. By leveraging transformer-based models, our application finds users similar to a given profile, thus extending the scope of profiling beyond the confines of traditional analysis.

At the core of our tool is Pinecone, a high-performance vector database, adept at storing and querying the embeddings produced by our NLP models. The result is an efficient and effective profiling system that can handle extensive datasets while maintaining an impressive speed of execution.

Our tool manifests as a Streamlit web application, known for its user-friendly interface, smooth user experience, and effortless deployment. Users can interact with various settings like selecting a model and its corresponding tokenizer, determining the volume of database rows for embedding, deciding the count of similar results to display, and even examining the produced embeddings in detail.

## Getting Started

#### Prerequisites
You will need Python 3.7+ installed on your machine. Also, it is recommended to create a virtual environment to avoid conflicts with other packages.

#### Installation
To install all the required Python libraries, navigate to the project root directory and run the following command:

    python -m pip --no-cache-dir install -r .\requirements.txt

#### To run the Streamlit application, navigate to Src/Streamlit directory, then run the following command in your terminal:
```streamlit run Home.py```

## Project Structure
The project structure is as follows:

- Src : This directory contains the current working version of the project.
- Src/Streamlit : This directory contains the Streamlit application files.
- Src/Streamlit/Home.py : This is the main script for running the Streamlit application.
- Src/model_class.py : This Python module defines the model class used in the application.
- Src/system_logging.py : This Python module defines the system logging class used in the application.
- docs : This directory contains documentation and scripts relevant to the project.
- features : This directory includes features that have not yet been implemented into a working version. Additionally, it includes test versions of these features as individual components.
## How It Works
**Model and Tokenizer Selection:** We offer a selection of transformer-based models and their respective tokenizers. These models are the core of the profiling process, converting social media data into meaningful numerical representations or 'embeddings'. Depending on your specific needs and the nature of your data, you can choose among several models with varying complexity and performance characteristics. Each model comes with a recommended tokenizer, which is responsible for converting the input text into a format that the model can understand.

**Database Row Selection for Embedding:** After selecting a model and tokenizer, you can choose the number of rows from your database to be embedded. This gives you flexibility in managing computational resources and processing time. If you're running an exploratory analysis, you might choose a smaller number of rows, while a comprehensive analysis might involve embedding all rows in the database.

**Number of Similar Results to Display:** Once the data is embedded and similar users are found, you can select how many of these results to display. This allows you to control the depth of your analysis. If you're looking for a broad range of similar profiles, you might display a large number of results. Conversely, if you're only interested in the most similar profiles, you might choose to display a smaller number.

**Embed Data Button:** Once you've made your selections, you can click the "Embed Data" button to start the process. The chosen data is embedded, and the results are uploaded to the Pinecone vector database and logged for record-keeping purposes. This information can later be used for further analysis, debugging, or system improvement.

**Interpreting the Results:** Once the embeddings have been generated and similar profiles found, the application displays the results in a user-friendly format. For each similar profile, the application displays various information, such as the profile's name, description, and location. You can use this information to better understand the similar profiles and draw insights based on your specific use-case.

## Future Work
Future work involves the implementation of additional features that have not yet been incorporated into the working version of the application. We plan to expand different types of social media attributes, implement ranking, and experiment with a similarity metric for embedding evaluation.

## Feedback
If you have any feedback or run into issues, please file an issue on this GitHub repository.
