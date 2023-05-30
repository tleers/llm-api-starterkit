from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All

# FASTAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
)

# LANGCHAIN
gpt4_all_model_path = "./ggml-gpt4all-j-v1.3-groovy.bin"
callbacks = [StreamingStdOutCallbackHandler()]
local_llm = GPT4All(model=gpt4_all_model_path, callbacks=callbacks, verbose=True)

# NEW CODE
ner_and_graph_prompt_string = """
	Your first task is to extract all entities (named entity recognition).
	Secondly, create a mermaid.js graph describing the relationships between these entities.
	{text}
"""

ner_graph_prompt = PromptTemplate(
    template=ner_and_graph_prompt_string,
    input_variables=['text'],
)

ner_graph_chain = LLMChain(
    llm=local_llm,
    prompt=ner_graph_prompt,
)

@app.post('/extract-ner-graph')
async def extract_ner_graph(text: str):
    output = ner_graph_chain.run(text=text)
    return {'output': output}