import pinecone
import mysql

"""
model_class.py

This file is part of our application that uses transformer models to calculate
the similarity of social media posts. It defines the SystemLogging class which is used to
record various aspects of the system's operation, including model execution times, 
input/output sizes, and interactions with the Pinecone vector database.
"""


class SystemLogging:
    def __init__(self, loggingConfig):
        # Various properties to hold system, model, and Pinecone interaction details
        self.name = None
        self.system_start = None
        self.system_stop = None
        self.model_start = None
        self.model_stop = None
        self.tokenizer = None
        self.model = None
        self.input: list
        self.output: list
        self._input_len = None
        self._output_len = None
        self.device: str
        self.pinecone_namespace = None
        self.pinecone_index = None
        self.top_n = None
        self.model_dim = None
        self.pinecone_Ustart = None
        self.pinecone_Ustop = None
        self.pinecone_Qstart = None
        self.pinecone_Qstop = None
        self.pinecone_Kmin = None
        self.pinecone_Kmax = None
        self.pinecone_Kavg = None
	# The configuration object for MySQL database
        self._loader = loggingConfig
	# Define SQL insert statements to be used for logging
        self._insert_stmnts = {
            "info" : "INSERT INTO exec_info (exec_start, exec_stop, input_size, output_size, name) VALUES (%s, %s, %s, %s, %s)",
            "model" : "INSERT INTO exec_model (exec_id, tokenizer, model, mod_start, mod_stop, device, dim) VALUES ((SELECT exec_id FROM exec_info WHERE name = %s), %s, %s, %s, %s, %s, %s)",
            "pinecone" : "INSERT INTO exec_pinecone (exec_id, namespace, exec_pinecone.index, upsert_start, upsert_stop, query_start, query_stop, kmin, kmax, kavg) VALUES ((SELECT exec_id FROM exec_info WHERE name = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            "input" : "INSERT INTO exec_input (exec_id, person_id) VALUES ((SELECT exec_id FROM exec_info WHERE name = %s), %s)",
            "output" : "INSERT INTO exec_output (exec_id, person_id, k_value) VALUES ((SELECT exec_id FROM exec_info WHERE name = %s), %s, %s)"
        }
    @property
    def input(self):
        return self._input
    
    @input.setter
    def input(self, value):
        self._input_len = len(value) or None
        self._input = value
    
    @property
    def output(self):
        return self._output
    
    @output.setter
    def output(self, value):
        self._output_len = len(value) or None
        self._output = value

    @property
    def device(self):
        return self._device
    
    @device.setter
    def device(self, value):
        if value == "cuda:0":
            self._device = "GPU"
        elif value == "cpu":
            self._device = "CPU"
        else:
            raise ValueError("device must be of type cuda:0 or cpu")
        
    def upload_to_db(self):
        try:
            database = mysql.connector.connect(
				host=self._loader.host,
				user=self._loader.user,
				password=self._loader.password,
				database=self._loader.database
			)
            cursor = database.cursor()
            info_data = (self.system_start, self.system_stop, self._input_len, self._output_len, self.name)
            cursor.execute(self._insert_stmnts["info"], info_data)
            model_data = (self.name, self.tokenizer, self.model, self.model_start, self.model_stop, self.device, self.model_dim)
            cursor.execute(self._insert_stmnts["model"], model_data)
            input_data = [(self.name, i) for i in self.input]
            cursor.executemany(self._insert_stmnts["input"], input_data)
            output_data = [(self.name, i[0], round(i[1], 2)) for i in self.output]
            cursor.executemany(self._insert_stmnts["output"], output_data)
            pinecone_data = (self.name, self.pinecone_namespace, self.pinecone_index, self.pinecone_Ustart, self.pinecone_Ustop, self.pinecone_Qstart, self.pinecone_Qstop, self.pinecone_Kmin, self.pinecone_Kmax, self.pinecone_Kavg)
            cursor.execute(self._insert_stmnts["pinecone"], pinecone_data)
            database.commit()
            cursor.close()
            return True
        
        except Exception as e:
            return False
             

    def check_vars(self):
        newlist = [self.name,
        self.system_start,
        self.system_stop,
        self.model_start,
        self.model_stop,
        self.tokenizer,
        self.model,
        self.input,
        self.output,
        self._input_len,
        self._output_len,
        self.device,
        self.pinecone_namespace,
        self.pinecone_index,
        self.model_dim,
        self.pinecone_Ustart,
        self.pinecone_Ustop,
        self.pinecone_Qstart,
        self.pinecone_Qstop,
        self.pinecone_Kmin,
        self.pinecone_Kmax,
        self.pinecone_Kavg]
        return newlist


        
