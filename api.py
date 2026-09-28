import uvicorn
 
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="HCI Mini Review App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

questions = [{
                "id": 0,
                "q": "Is Fitts' Law an example of a predictive model or a descriptive model?",
                "a": "Predictive model"
                },
             {
                "id": 1,
                "q": "Does this course focus more on genius design, systems design, or user-centered design?",
                "a": "User-centered design"
                },
             {
                "id": 2,
                "q": "What is the main goal of the ideation phase of iterative design?",
                "a": "Generating as many possible design solutions as possible"
                }
            ]

class QuestionRequest(BaseModel):
    question: str
    answer: str

@app.get("/questions")
def get_questions():
    return questions

@app.post("/add")
def add_question(req: QuestionRequest):
    questions.append({ 
        "id": len(questions),
        "q": req.question,
        "a": req.answer
    })

@app.delete("/delete/{id}")
def delete_question(id: int):
    #search questions to see if id matches one that exits
    for question in questions:
        
        if question.get("id") == id:
            #if id matches on that exists, remove that question and...
            questions.remove(question)
            #...reset id numbers so everything works later with toggling
            i = 0
            for question in questions:
                question["id"] = i
                i = i + 1
            #return so we dont raise exception
            return
    #question was not in list, raise exception
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with ID {id} not found")
    return

@app.put("/update/{id}")
def update_question(id: int, req: QuestionRequest):
    #find question in list if exists
    for question in questions:
        if question.get("id") == id:
            #assign new question and answer pair
            question["q"] = req.question
            question["a"] = req.answer
            #return so we dont riase exception
            return
    #question was not in list, raise 404
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with ID {id} not found")
    return

if __name__=="__main__":
    uvicorn.run(app, port=8005)
