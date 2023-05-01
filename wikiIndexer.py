from llama_index import GPTSimpleVectorIndex
from llama_index import LLMPredictor, PromptHelper, ServiceContext
from langchain import OpenAI
import openai

class wikiQuery:
    def __init__(self, api_key):
        openai.api_key = api_key

    def load_llm_model(self):
         # set maximum input size
        max_input_size = 1024
        # set number of output tokens
        num_outputs = 1024
        # set maximum chunk overlap
        max_chunk_overlap = 20
        # set chunk size limit
        chunk_size_limit = 600 

        # define prompt helper
        prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

        # define LLM
        llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.3, model_name="text-davinci-003", max_tokens=num_outputs))
    
        # documents = SimpleDirectoryReader(data_path).load_data()
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        
        return service_context
    
    def build_page_index(self, documents, service_context):

        index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)
        
        return index
    
    def load_gpt_index(self, index_json_file):

        index = GPTSimpleVectorIndex.load_from_disk(index_json_file)
        
        return index
