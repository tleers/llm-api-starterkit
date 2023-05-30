from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All

# FASTAPI
app = FastAPI()

# Why CORS? See README.md. You can ignore this if you are not deploying this code anywhere.
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
)

gpt4_all_model_path = "./ggml-gpt4all-j-v1.3-groovy.bin"

# LANGCHAIN
callbacks = [StreamingStdOutCallbackHandler()]
local_llm = GPT4All(model=gpt4_all_model_path, callbacks=callbacks, verbose=True)


ner_and_graph_prompt_string = """
	You are a information extractor robot.
	
	Your first task is to extract all entities (named entity recognition).
	Secondly, create a mermaid.js graph describing the relationships between these entities.
	{extra_tasks}
	{text}
"""

ner_graph_prompt = PromptTemplate(
    template=ner_and_graph_prompt_string,
    input_variables=['extra_tasks', 'text'],
)

ner_graph_chain = LLMChain(
    llm=local_llm,
    prompt=ner_graph_prompt,
)

@app.post('/extract-ner-graph')
async def extract_ner_graph(extra_tasks: str, text: str):
    output = ner_graph_chain.run(extra_tasks=extra_tasks, text=text)
    return {'output': output}

from langchain import OpenAI
langchain_llm = OpenAI(model_name="gpt-4", temperature=0)

ner_graph_openai_chain = LLMChain(
	llm=langchain_llm,
	prompt=ner_graph_prompt,
)

@app.post('/extract-ner-graph-openai')
async def extract_ner_graph_openai(extra_tasks: str, text: str):
    output = ner_graph_openai_chain.run(extra_tasks=extra_tasks, text=text)
    return {'output': output}