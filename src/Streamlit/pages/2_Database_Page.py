#Database

from types import SimpleNamespace
import json
import pandas as pd
import streamlit as st

from eCairn_connector import eCairnConnector

# Set Page Base UI
st.set_page_config(page_title="Database Page")
st.sidebar.header("Database Page")
st.markdown("# Database Page")


# Connect to Database
databaseConfig:SimpleNamespace
loggingConfig:SimpleNamespace

with open("config.json", "r") as f:
	config = json.load(f, object_hook=lambda x: SimpleNamespace(**x))
	databaseConfig = config.oregonstate.data
	loggingConfig = config.oregonstate.logging

db = eCairnConnector();

tab1, tab2, tab3 = st.tabs(["Manual", "Profiles", "Logging"])

with tab1:
	query_df1 = pd.DataFrame()
	# SQL input
	col1,col2 = st.columns(2, gap="large")
	with col1:
		st.subheader("Manual SQL Query")
		with st.form(key='query_form'):
			raw_code = st.text_area("Enter SQL Query")
			submit_code = st.form_submit_button("Execute")

		# Run query
		if submit_code:
			st.info("Query Submitted")
			st.code(raw_code)
			query_df1 = db.sql_executor(raw_code, databaseConfig)


			# Table

	#Results Layouts
	with col2:
		# Show DB table names
		st.subheader("Profile Database")
		with st.expander("Table Names"):
			tables_df = db.sql_executor("SHOW TABLES;", databaseConfig)
			st.dataframe(tables_df)

	if not query_df1.empty:
		st.dataframe(query_df1)

with tab2: 
	query_df2 = pd.DataFrame()
	st.subheader("Search Twitter Profiles")
	search_attribute = st.selectbox(
			'Attribute to query',
			('id', 'person_id', 'twitter_id', 'screen_name', 'name', 'location'))

	location_warning = st.empty()
	# Query by ID
	if search_attribute == 'id' or search_attribute == 'person_id' or search_attribute == 'twitter_id':

		    
		id_input = st.text_input('Please input: ' + search_attribute, placeholder="1, 2", help="Comma delimited list.")
		id_list = [id.strip() for id in id_input.split(",")]

		error_message = st.empty()

		id_btn = st.button("Run Query")
		if id_btn:
			submit_info = st.info("Query Submitted")
			
			query_df2 = db.query_by_id_list(search_attribute, id_list, databaseConfig)

			if query_df2.empty:
				submit_info.empty()
				error_message = st.error('No entries found', icon="🚨")

					
	# Other queries
	elif search_attribute == 'name' or search_attribute == 'screen_name' or search_attribute == 'location':
		search_txt = st.text_input('Search by: ' + search_attribute)

		txt_btn = st.button("execute")

		if search_attribute == 'location':
			location_warning = st.warning('Same location may be formatted differently in database for different entries', icon="⚠️")

		if txt_btn:
			submit_info = st.info("Query Submitted")
			location_warning.empty()
			query_df2 = db.query_by_text(search_attribute, search_txt, databaseConfig)
			if query_df2.empty:
				submit_info.empty()
				error_message = st.error('No entries found', icon="🚨")

	if not query_df2.empty:
		st.dataframe(query_df2)


with tab3: 
	st.subheader("Logging Database")

	info_df = db.get_logging_table("info", loggingConfig)
	input_df = db.get_logging_table("input", loggingConfig)
	model_df = db.get_logging_table("model", loggingConfig)
	output_df = db.get_logging_table("output", loggingConfig)
	pinecone_df = db.get_logging_table("pinecone", loggingConfig)

	with st.expander("exec_info"):
		st.dataframe(info_df)

	with st.expander("exec_input"):
		st.dataframe(input_df)

	with st.expander("exec_model"):
		st.dataframe(model_df)

	with st.expander("exec_output"):
		st.dataframe(output_df)

	with st.expander("exec_pinecone"):
		st.dataframe(pinecone_df)
