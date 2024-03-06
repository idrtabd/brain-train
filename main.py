#pip install fastapi uvicorn httpx python-dotenv
#create a file .env
#To run: uvicorn main:app --reload
from fastapi import FastAPI, HTTPException
import random
from starlette.middleware.cors import CORSMiddleware
import httpx
import os
from dotenv import load_dotenv
import sqlite3


################################
# Connect to or create a SQLite database
conn = sqlite3.connect('braintrain.db')
# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, name TEXT NOT NULL)''')
# Create table lessons, make the id autoincrement
cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons3 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_text TEXT
    )
''')


conn.commit()

# Save (commit) the changes

# Select and display all rows in the table
cursor.execute("SELECT * FROM users")
print("Users in the database:")
for row in cursor.fetchall():
    print(row)

# Close the connection when done
conn.close()
################################

app = FastAPI()

@app.get("/hello")
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
async def simple_openai_call(myQuery3: str):
    # Log the query
    print(f" =============== LOGGING =================")
    print(f" =============== LOGGING =================")
    print(f"Query received: {myQuery3}")
    print(f" =============== LOGGING =================")
    print(f" =============== LOGGING =================")


    WOLFRAM_KEY = os.getenv("WOLFRAM_KEY")
    #print wolfram key
    # print(f"WOLFRAM_KEY IS " + WOLFRAM_KEY)
    # Prepare the payload for the OpenAI API call
    data = {
        "prompt": myQuery3,
        "max_tokens": 50
    }
    
    WOLFRAM_URL="http://api.wolframalpha.com/v1/result?appid="
    wolfram_url_full = WOLFRAM_URL + WOLFRAM_KEY + "&i=" + myQuery3

    #log the url - concat the wolfram url to hello world
    print(f"WOLFRAM FINAL URL IS " + wolfram_url_full)
    
    # Make the call to WOLFRAM ALPHA, it's a GET request
    async with httpx.AsyncClient() as client:
        response = await client.get(wolfram_url_full)
        #convert the response to text
        response_text = response.text
        #return the response with httpcode 200
        # print response_text
        print(f"REsponse TExt is " + response_text)
        return response_text
    

#Post Request for UploadLessonText
@app.post("/UploadLessonText")
async def upload_lesson_text(lessonText: str):
    #LOG THE LESSON TEXT and return the same
    print(f" =============== LOGGING =================")
    print(f"Lesson Text received: {lessonText}")
    #return a unique lesson plan id for further use to reference
    #for now, generate random number
    # lesson_plan_id = random.randint(1, 1000000)
    #save the lesson text and id to the database in the lessons table
    conn = sqlite3.connect('braintrain.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO lessons3 (lesson_text) VALUES (?)", (lessonText,))
    # get the last row id
    lesson_plan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"Lesson Plan ID": lesson_plan_id, "Lesson Text": lessonText}

#GET request to get the prepared lesson plan, arguments are lesson plan id
@app.get("/GetLessonPlan")

async def get_lesson_plan(lessonPlanId: int):
    try:
        # LOG THE LESSON PLAN ID and return the same
        print(f" =============== LOGGING =================")
        print(f"Lesson Plan ID received: {lessonPlanId}")
        # Get the lesson plan from the database using the lesson plan id
        conn = sqlite3.connect('braintrain.db')
        cursor = conn.cursor()
        cursor.execute("SELECT lesson_text FROM lessons3 WHERE id=?", (lessonPlanId,))
        lesson_text = cursor.fetchone()
        conn.close()
        # return the lesson plan
        return {"Lesson Plan ID": lessonPlanId, "Lesson Plan": lesson_text}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}