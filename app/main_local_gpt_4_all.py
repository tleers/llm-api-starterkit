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

summarize_template_string = """
        Provide a summary for the following text:
        {text}
"""

summarize_prompt = PromptTemplate(
    template=summarize_template_string,
    input_variables=['text'],
)

summarize_chain = LLMChain(
    llm=local_llm,
    prompt=summarize_prompt,
)

# We use async, because we are calling another API that may take a while, and we don't want to wait for this to finish necessarily and our computer resources be tied up in this function.
# See https://fastapi.tiangolo.com/async/#in-a-hurry


@app.post('/summarize-text')
async def summarize_text(text: str):
    summary = summarize_chain.run(text=text)
    return {'summary': summary}
