import uvicorn
from fastapi import FastAPI, File, UploadFile
from typing import List
from pyresparser import ResumeParser
from collections import Counter
import app1 as my_script
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()


class Item(BaseModel):
    jd: str
    resume: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
@app.get('/process')
def results():
    return my_script.process_resumes()

@app.post('/process')
async def calculate(item: Item):
    lst = my_script.process_resumes(item.jd, item.resume)
    return JSONResponse(content=lst)

# @app.post('/process')
# async def calculate(item: Item):
#     print(item.jd)
#     print(item.resume)
#     #return {"jd": item.jd, "resume": item.resume}
#     lst = [{"name": "jhfhdjf", "score" : "67"}, {"name": "gdfgjdgfhs", "score" : "22"}]
#     return JSONResponse(content=lst)


if __name__== '__main__':
    uvicorn.run(app, host='127.0.0.1', port  = 8000)