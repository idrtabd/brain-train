#pip install fastapi uvicorn httpx python-dotenv
#create a file .env
#To run: uvicorn main:app --reload
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/SimpleOpenAICall")
async def simple_openai_call(myQuery: str):
    # Log the query
    print(f" =============== LOGGING =================")
    print(f" =============== LOGGING =================")
    print(f"Query received: {myQuery}")
    print(f" =============== LOGGING =================")
    print(f" =============== LOGGING =================")

    # Prepare the payload for the OpenAI API call
    data = {
        "prompt": myQuery,
        "max_tokens": 50
    }
    
    OPENAI_URL="https://api.openai.com/v1/engines/davinci-codex/completions"

    # Make the call to OpenAI
    async with httpx.AsyncClient() as client:
        response = await client.post(
            OPENAI_URL,
            json=data,
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"}
        )

    if response.status_code == 200:
        # Return the response from OpenAI
        return response.json()
    else:
        # Handle potential errors
        raise HTTPException(status_code=response.status_code, detail="Error calling OpenAI API")


@app.get("/SimpleWolfram")
async def simple_openai_call(myQuery2: str):
    # Log the query
    print(f" =============== LOGGING =================")
    print(f" =============== LOGGING =================")
    print(f"Query received: {myQuery2}")
    print(f" =============== LOGGING =================")
    print(f" =============== LOGGING =================")


    WOLFRAM_KEY = os.getenv("WOLFRAM_KEY")
    #print wolfram key
    print(f"WOLFRAM_KEY IS " + WOLFRAM_KEY)
    # Prepare the payload for the OpenAI API call
    data = {
        "prompt": myQuery2,
        "max_tokens": 50
    }
    
    WOLFRAM_URL="http://api.wolframalpha.com/v1/result?appid"
    wolfram_url_full = WOLFRAM_URL + WOLFRAM_KEY + "&i=" + myQuery2

    #log the url
    print(f"WOLFRAM FINAL URL IS " + wolfram_url_full)
    
    # Make the call to OpenAI
    async with httpx.AsyncClient() as client:
        response = await client.post(
            wolfram_url_full,
            json=data,
            #set headers to accept json
            headers={"Accept": "application/json"}
        )

    if response.status_code == 200:
        # Return the response from OpenAI
        # return response.json()
        #return response.text
        return {"message": response.text}     
    else:
        # Handle potential errors
        raise HTTPException(status_code=response.status_code, detail="Error calling OpenAI API")
