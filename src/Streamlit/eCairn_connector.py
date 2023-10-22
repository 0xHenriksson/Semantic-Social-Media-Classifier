from types import SimpleNamespace
from sqlalchemy import create_engine, text
import pandas as pd
from connection_type import Types

class eCairnConnector:
	"""
    A class for connecting to and querying our test database from eCairn.

    Args:
        databaseConfig: A dictionary containing the database connection information.
    """
	def __init__(self):
		"""
        Initializes the database connection.

        Args:
            databaseConfig: A dictionary containing the database connection information.
        """
		self._data = None
	
	def get_test_list(self, method: Types.Connection, **kwargs):
		"""
        Gets a list of test data from the database.

        Args:
            method: The method to use to get the test data.
            kwargs: Additional keyword arguments.

        Returns:
            A list of test data.
        """
		self._kwargs = kwargs
		
		if method == Types.Connection.FROM_TYPE_DB:
			if "db_config" not in self._kwargs.keys():
				raise ValueError("Expected to find value for `db_config`. No value found.")
			elif type(self._kwargs["db_config"]) != SimpleNamespace:
				raise TypeError("Expected to find type {} for `db_config`. Found type {}.".format(SimpleNamespace, type(self._kwargs["db_config"])))
			else:
				if "limit" in self._kwargs.keys():
					self._from_db(self._kwargs["db_config"], limit=self._kwargs["limit"])
				else:
					self._from_db(self._kwargs["db_config"])

		elif method == Types.Connection.FROM_TYPE_CSV:
			if "csv_filename" not in self._kwargs.keys():
				raise ValueError("Expected to find value for `csv_filename`. No value found.")
			elif type(self._kwargs["csv_filename"]) != str:
				raise TypeError("Expected to find type {} for `csv_filename`. Found type {}.".format(str, type(self._kwargs["csv_filename"])))
			else:
				self._from_csv(self._kwargs["csv_filename"])

		elif method == Types.Connection._READ_ID_LIST:
			if "limit" in self._kwargs.keys():
				self._test_list_by_ids(self._kwargs["id_list"], limit = self._kwargs["limit"])
			else:
				self._test_list_by_ids(self._kwargs["id_list"])


	def _from_db(self, databaseConfig:SimpleNamespace, limit=1000) -> None:
		"""
        Gets a list of test data from the database.

        Args:
            databaseConfig: A dictionary containing the database connection information.
            limit: The maximum number of rows to return.
        """
		uri = f'mariadb+mysqlconnector://{databaseConfig.user}:{databaseConfig.password}@{databaseConfig.host}/{databaseConfig.database}'
		engine = create_engine(uri)
		sql_query = f"SELECT person_id, IFNULL(description,'') FROM twitter_profiles ORDER BY twitter_profiles.person_id ASC LIMIT {limit}"
		self._data = pd.read_sql_query(sql=text(sql_query), con=engine.connect())

	def _from_csv(self, file:str) -> None:
		"""
        Gets a list of test data from a CSV file.

        Args:
            file: The path to the CSV file.
        """
		self._data = pd.read_csv(file, index_col=0)

	def _test_list_by_ids(self, databaseConfig:SimpleNamespace, ref_list:list, limit = 10000) -> None:
		"""
        Gets a list of test data from the database by ID.

        Args:
            databaseConfig: A dictionary containing the database connection information.
            ref_list: A list of IDs.
            limit: The maximum number of rows to return.

        Returns:
            A list of test data.
        """
	
		uri = f'mariadb+mysqlconnector://{databaseConfig.user}:{databaseConfig.password}@{databaseConfig.host}/{databaseConfig.database}'
		engine = create_engine(uri)
		sql_query = f"SELECT person_id, IFNULL(description,'') FROM twitter_profiles WHERE person_id IN ({','.join(map(lambda x: str(x), ref_list))}) ORDER BY twitter_profiles.person_id ASC limit {limit};"
		self._data = pd.read_sql_query(sql=text(sql_query), con=engine.connect())

	def get_dataframe(self) -> pd.DataFrame:
		"""
        Gets the DataFrame containing the test data.

        Returns:
            A DataFrame containing the test data.
        """
		return self._data

	@classmethod
	def get_eCairn_byID(cls, db_config:SimpleNamespace, ref_list:list) -> pd.DataFrame:
		"""
        Gets a DataFrame containing the test data from the database by ID.

        Args:
            db_config: A dictionary containing the database connection information.
            ref_list: A list of IDs.

        Returns:
            A DataFrame containing the test data.
        """
		new_instance = cls(Types.Connection._READ_ID_LIST, db_config=db_config, id_list = ref_list)
		return new_instance.get_dataframe()
    
	def sql_executor(self, sql_query, databaseConfig:SimpleNamespace):
		uri = f'mariadb+mysqlconnector://{databaseConfig.user}:{databaseConfig.password}@{databaseConfig.host}/{databaseConfig.database}'
		engine = create_engine(uri)
		
		data = pd.read_sql_query(sql=text(sql_query), con=engine.connect())
		cols = list(data.columns)
		df = pd.DataFrame(data, columns=cols)
		return df

	def query_by_id_list(self, attr, ref_list:list, databaseConfig:SimpleNamespace):
		"""
        Queries the database for the rows with the given IDs.

        Args:
            attr: The attribute to query.
            ref_list: A list of IDs.
            databaseConfig: A dictionary containing the database connection information.

        Returns:
            The rows with the given IDs.
        """
		uri = f'mariadb+mysqlconnector://{databaseConfig.user}:{databaseConfig.password}@{databaseConfig.host}/{databaseConfig.database}'
		engine = create_engine(uri)
		
		sql_query = f"SELECT {attr}, IFNULL(description,'') FROM twitter_profiles WHERE {attr} IN ({','.join(map(lambda x: str(x), ref_list))}) ORDER BY twitter_profiles.{attr} ASC;"
		data = pd.read_sql_query(sql=text(sql_query), con=engine.connect())
		cols = list(data.columns)
		df = pd.DataFrame(data, columns=cols)

		return df
	
	def query_by_text(self, attr, input, databaseConfig:SimpleNamespace):
		"""
        Queries the database for the rows that match the given text.

        Args:
            attr: The attribute to query.
            input: The text to match.
            databaseConfig: A dictionary containing the database connection information.

        Returns:
            The rows that match the given text.
        """
		uri = f'mariadb+mysqlconnector://{databaseConfig.user}:{databaseConfig.password}@{databaseConfig.host}/{databaseConfig.database}'
		engine = create_engine(uri)
					
		sql_query = f"SELECT * FROM twitter_profiles WHERE {attr} = '{input}';"
		data = pd.read_sql_query(sql=text(sql_query), con=engine.connect())
		cols = list(data.columns)
		df = pd.DataFrame(data, columns=cols)

		return df

	def get_logging_table(self, tbl, loggingConfig:SimpleNamespace):
		"""
        Gets the logging table from the database.

        Args:
            tbl: The name of the logging table.
            loggingConfig: A dictionary containing the database connection information.

        Returns:
            The logging table.
        """
		uri = f'mariadb+mysqlconnector://{loggingConfig.user}:{loggingConfig.password}@{loggingConfig.host}/{loggingConfig.database}'
		engine = create_engine(uri)

		sql_query = f"SELECT * FROM exec_{tbl};"

		data = pd.read_sql_query(sql=text(sql_query), con=engine.connect())
		cols = list(data.columns)
		df = pd.DataFrame(data, columns=cols)
		return df
