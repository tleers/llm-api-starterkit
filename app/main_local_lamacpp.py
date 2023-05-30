from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import LlamaCpp, PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# FASTAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
)

# LANGCHAIN
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
local_llm = LlamaCpp(
    #model_path="./ggml-vic7b-uncensored-q4_0.bin",
    model_path="awizardLM-7B.ggmlv3.q4_0.bin",
    callback_manager=callback_manager,
    verbose=True
)

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

@app.post('/summarize-text')
async def summarize_text(text: str):
    summary = summarize_chain.run(text=text)
    return {'summary': summary}
