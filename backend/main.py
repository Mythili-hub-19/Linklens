# BACKEND

# IMPORTING FUNCTIONS
from pathlib import Path
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from detection import analyze_input


# CREATING THE FASTAPI APPLICATION
app = FastAPI()


# CREATION OF AN API ENDPOINT
@app.get("/analyze")
#GET - used when a client requests infomation from a server
#(Http request needs to be connected from frontend server sending it (js) to the endpoint path /analyze)



# Defining the Python function underneath /analyze path
def analyze(text: str = ""):

    # IMPLEMENT INPUT VALIDATION
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Input cannot be empty."
        )
#HTTPException is a FastAPI exception used to send an HTTP error response to the client . Needed when user submits 
#empty input




#CALL DETECTION FUNCTION
    result = analyze_input(text) #return must be aligned with other functions of analyze

# RETURN THE RESULT
    return result

#When FastAPI receives a request, it calls analyze() and executes its indented statements in order.
#result and return both statements are part of the work that the analyze() function is supposed to perform whenever
# someone sends a request to /analyze, hence need to be indented

# CONNECTING FRONTEND STATIC FILES TO FASTAPI
STATIC_FOLDER = Path(__file__).resolve().parent / "static"

app.mount(
    "/",
    StaticFiles(directory=STATIC_FOLDER, html=True),
    name="static"
)

#StaticFiles  is a FastAPI utility for serving static website files, such as HTML, CSS, Javascript and images



#IN MID CODE EXPLANATIONS



#API INTERFACE : (API ENDOINT, HTTP REQUEST , JSON RESPONSE)


#the endpoints must be registered with ur application instance.i.e'y aplication instance must be created before u
#write decorators for it.


#1You connect your FastAPI endpoint to the detection function by calling the imported function inside analyze()
#2and passing the text received from the frontend to it.
#3Now, inside that function, call the imported function:


# DECORATOR- a decorator modifies or registers a function's behaviour.
#Here, FastAPI route decorator tells FastAPI: When a GET request arrives a this path , execute  the python function
#associated with it .
