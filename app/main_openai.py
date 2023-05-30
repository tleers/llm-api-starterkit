from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain

# FASTAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
)

# LANGCHAIN
langchain_llm = OpenAI(temperature=0)

summarize_template_string = """
        Provide a summary for the following text:
        {text}
"""

summarize_prompt = PromptTemplate(
    template=summarize_template_string,
    input_variables=['text'],
)

summarize_chain = LLMChain(
    llm=langchain_llm,
    prompt=summarize_prompt,
)

@app.post('/summarize-text')
async def summarize_text(text: str):
    summary = summarize_chain.run(text=text)
    return {'summary': summary}
