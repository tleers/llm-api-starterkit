# LLM-API-starterkit

This repository is the most minimal implementation of an LLM API possible, focusing on making this tech accessible to coders new to LLMs & APIs.
I do not recommend deploying the code as-is. For a more fleshed out example, take a look at https://github.com/tleers/servelm.

# Quick-start

There's three steps to starting the demo or doing development on this template.

1. Installation of general python package requirements/dependencies
2. Selection of LLM model & dependencies
3. Running the FastAPI application

(Optional) 4. look at other examples and include DevOps, MLOps & LLMOps best practices for robust & reproducible development that can be deployed more readily.

## 1. Installation of dependencies

We use the most common way of installing dependencies, which is using `pip install` with a requirements.txt.

Tutorial was created using `Python 3.10`.

```bash
pip install -r requirements.txt
```

It is advised to at the very least install these requirements in a virtual environment. To create a virtual environment and install the requirements there, use the following:
```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Ideally, we use dependency management with `poetry` for a smoother experience (see https://github.com/tleers/servelm). We ignore this additional complexity for now.

## 2. LLM model preparation

### 2.1 **With an OpenAI key**

1. Change the filename of .env.example to .env
2. Add your OpenAI API key to .env

Done.

### 2.2 **Without an OpenAI key**

Note that you need sufficiently powerful hardware to run a local model. It's easier to use the OpenAI API if you're initially experimenting. Making an account means you get free credits, which are usually more than you need.

#### **X86-64 architectures (Windows, Linux, non-Apple silicon Mac)**
We use LlamaCpp. 
https://python.langchain.com/en/latest/modules/models/llms/integrations/llamacpp.html

1. Download model weights that are compatible with the llamacpp implementation. 
I use vicuna 1.1 quantized https://huggingface.co/vicuna/ggml-vicuna-7b-1.1/blob/main/ggml-vic7b-uncensored-q4_0.bin, as recommended on https://old.reddit.com/r/LocalLLaMA/wiki/models

2. Make sure the model weights are in the current directory and you know the filename. 
In this tutorial, the filename is `ggml-vic7b-uncensored-q4_0.bins`

#### **ARM64 architectures or M1/M2 Mac**
LangChain support for LLamaCpp is currently iffy on Apple Silicon. Therefore, we instead use the GPT4ALL integration.
Download the model file here:


1. Download model weights from https://gpt4all.io/index.html
There are many different ones available, take a look at what best fits your usecase. I use
"ggml-gpt4all-j-v1.3-groovy.bin"

2. Make sure the model weights are in the current directory and you know the filename. 
In this tutorial, the filename is `ggml-gpt4all-j-v1.3-groovy.bin`


## 3. Running the FastAPI application

You should be ready to run the most basic example.

With OpenAI API
```bash
uvicorn app.main_openai:app --port 80 --env-file .env
```

With local LLM using Vicuna, compatible with X86_64 architecture
```bash
uvicorn app.main_local_lamacpp:app --port 80
```

With local LLM using GPT4All, compatible with X86_64 as well as arch_64 (mac m1, m2) architectures.
```bash
uvicorn app.main_local_gpt_4_all:app --port 80
```

Go to `https://localhost:80/docs` to see the automatically generated API documentation. 

You can also try out the summarization endpoint by clicking `Try it out!`

![Showing FastAPI with the Try it out button](docs/try_it_out.png)

## (Optional) 4. Best practices & deployment

See https://github.com/tleers/servelm.

# FAQ

## Why CORS?
Cross-Origin Resource Sharing (CORS) is a security measure implemented in web browsers to prevent requests to different origins (domain, scheme, or port) from being allowed by default. It's a mechanism that uses additional HTTP headers to tell browsers to give a web application running at one origin, access to selected resources from a different origin.

When you create an API using FastAPI, it's common that your API (running on one origin, typically a different server or port) will be accessed from a web application (running on a different origin). By default, this kind of "cross-origin" request is blocked by the browser for security reasons, as it could potentially allow malicious web applications to make requests to an API on behalf of a user without their knowledge.

To explicitly allow certain cross-origin requests to your FastAPI application, you would enable CORS, which involves setting the appropriate HTTP headers to tell browsers that certain origins are trusted and allowed to make these requests. FastAPI has a middleware for this, which you can configure to allow specific origins (websites), HTTP methods (GET, POST, etc.), headers, and whether credentials are allowed.

While CORS is essential for making your FastAPI API accessible from different origins, be cautious about which origins you trust. Allowing all origins (with a wildcard '*') can expose your API to potential security risks.

Please note that CORS is a browser-enforced security feature and doesn't provide security against API misuse that could occur from non-browser clients (e.g., curl, Postman, etc.).

