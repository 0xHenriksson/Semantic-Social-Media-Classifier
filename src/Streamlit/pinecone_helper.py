"""
model_class.py

This file is part of our Streamlit application that uses transformer models to calculate
the similarity of social media posts. This particular module contains helper functions 
for chunking data and uploading it to Pinecone, a vector database used for storing 
embeddings. It also includes methods for logging the upload process and querying the 
database for similar embeddings.
"""
import datetime
import numpy as np
import itertools

def chunks(iterable, batch_size=100):
		"""A helper function to break an iterable into chunks of size batch_size."""
		# Create an iterator
		it = iter(iterable)
		# Slice the iterator to get a chunk of the specified size
		chunk = tuple(itertools.islice(it, batch_size))
		# Yield chunks until the iterator is exhauseted
		while chunk:
			yield chunk
			chunk = tuple(itertools.islice(it, batch_size))

def uploadToPineCone(logger, index, embeddings_dataset):
	"""Function to upload embeddings to Pinecone."""
	vector_dim = 384
	vector_count = len(embeddings_dataset)

	# Upsert data with 100 vectors per upsert request
	# Log the start time of the upload process
	logger.pinecone_Ustart = datetime.datetime.now()
	try:
		# Chunk the data and upload it to pinecone
		for ids_vectors_chunk in chunks(embeddings_dataset, batch_size=100):
			# Upsert to pinecone index
			index.upsert(vectors=ids_vectors_chunk, namespace=logger.pinecone_namespace)  # Assuming `index` defined elsewhere
		# Log the stop time of the upload
		logger.pinecone_Ustop = datetime.datetime.now()
		return True
	
	except Exception as e:
		# If there's an error, log the stop time and return false
		logger.pinecone_Ustop = datetime.datetime.now()
		return False
	
	
def uploadLog(logger, index, embeddings_dataset, search_id):
	"""Function to log the upload process and query Pinecone for similar embeddings."""
	
	# Log the start time of the query process
	logger.pinecone_Qstart = datetime.datetime.now()
	# Find the index of the embedding for the search_id in the dataset
	for list_index, item in enumerate(embeddings_dataset):
		if item[0] == f"vector-{search_id}":
			new_index = list_index
			break
	# Query Pinecone for the top most similar embeddings
	top = index.query(
		vector=[embeddings_dataset[new_index][1]],
		top_k = logger.top_n+1,
		include_values=False,
		namespace=logger.pinecone_namespace,
		include_metadata=True
	)
	# Log the stop time of the query process
	logger.pinecone_Qstop = datetime.datetime.now()
	# Extract the ids and scores of the most similar embeddings
	logger.output = [(int(i["metadata"]['original_id']), float(i["score"])) for i in top["matches"][1:]]
	results = [(int(i["metadata"]['original_id']), str(i["metadata"]['bio_text']), float(i["score"])) for i in top["matches"][1:]]
	# Compute the min, max, and average similarity score
	logger.pinecone_Kmin = min(map(lambda x: x[1], logger.output))
	logger.pinecone_Kmax = max(map(lambda x: x[1], logger.output))
	logger.pinecone_Kavg = float(np.average(list(map(lambda x: x[1], logger.output))))
	# Log the end time of the system process
	logger.system_stop = datetime.datetime.now()
	# Upload the log to the database
	return logger.upload_to_db(), results, embeddings_dataset[new_index][2]
