"""
model_class.py

This file is part of our Streamlit application that uses transformer models to calculate
the similarity of social media posts. The central class, Model, encapsulates the logic
for loading pretrained transformer models and tokenizers, and calculating embeddings
for a given set of texts.
"""

# Import libraries
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import numpy as np
import seaborn as sns
from types import SimpleNamespace
import datetime
import time
import itertools
import streamlit as st

# Define the main Model class
class Model:
	# Initialize Model class attributes
	def __init__(self):
		self.name = None
		self.tokenizer_name = None
		self.model_name = None
		self.dimensions = None
		self.limit = None
		self.id = None
		self.device = None
	# Define getters and setters for each attribute
	@property
	def id(self):
		return self._name

	@id.setter
	def id(self, value):
		self._name = value
	
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def tokenizer_name(self):
		return self._tokenizer_name

	@tokenizer_name.setter
	def tokenizer(self, value):
		self._tokenizer_name = value

	@property
	def model_name(self):
		return self._model_name

	@model_name.setter
	def model_name(self, value):
		self._model_name = value

	@property
	def dimensions(self):
		return self._dimensions

	@dimensions.setter
	def dimensions(self, value):
		self._dimensions = value

	@property
	def limit(self):
		return self._limit

	@limit.setter
	def limit(self, value):
		self._limit = value
		
	@property
	def device(self):
		return self._device

	@device.setter
	def device(self, value):
		self._device = value
	
	# Generate embeddings for a list of texts
	def get_embeddings(cls, logger, test_list, progress_bar):
		# Set up the pretained model and tokenizer
		tokenizer, model = cls.pretrained_setup()
		# Start the logging for the model processing
		logger.model_start = datetime.datetime.now()
		embeddings_dataset = []
		next_read = time.time() + 5
		total = len(test_list)

		one_percent = 100 // total
		progress_complete = 0
		# Loop through the list of texts
		for item in test_list:
			# Print progress every 5 seconds
			if time.time() > next_read:
				print(f"{len(embeddings_dataset)}/{total}")
				next_read = time.time() + 5
			embeddings_dataset.append( (f'vector-{item[0]}', cls.emb(str(item[1]),model,tokenizer)[0].tolist(), {"original_id": item[0], "bio_text": str(item[1])}) )
		
			progress_complete += one_percent
			progress_bar.progress(progress_complete, text="Embedding data...")
		# COmplete progres bar
		progress_bar.progress(100)
		# Log the end of the model processing
		logger.model_stop = datetime.datetime.now()
		# Return the dataset with embeddings
		return embeddings_dataset
	
	# Method to generate embeddings for a single text
	@classmethod
	def emb(cls, text, model, tokenizer):
		# Encode the input text
		encoded_input = tokenizer(text =text, padding=True, truncation=True, return_tensors='pt').to(cls.device)
		# Use the model to generate embeddings
		with torch.no_grad():
			model_output = model(**encoded_input)
		# Pool the embeddings
		sentence_embeddings = cls.mean_pooling(model_output, encoded_input['attention_mask'])
		# Normalize embedding
		sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
		# Return the embeddings
		return np.array(sentence_embeddings.to('cpu'))
	
	# Mean Pooling - Take attention mask into account for correct averaging
	def mean_pooling(model_output, attention_mask):
		#First element of model_output contains all token embeddings
		token_embeddings = model_output[0] 
		# We will expand the attention_mask to match the dimensions of token_embeddings
		input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
		# Then we compute the weighted average of token embeddings, considering the attention mask
		return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)


	# Function to load up the pretrained model and tokenizer
	@classmethod
	def pretrained_setup(cls):
		# Load the tokenizer
		tokenizer = AutoTokenizer.from_pretrained(cls.tokenizer_name)
		# Load the model
		model = AutoModel.from_pretrained(cls.model_name).to(cls.device)
		# Return tokenizer and model
		return tokenizer, model
	
	
