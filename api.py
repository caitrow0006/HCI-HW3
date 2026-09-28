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

# TODO: Add a new route that can be used to delete a question/answer from the dataset.
@app.delete("/delete/{id}")
def delete_question(id: int):
    for question in questions:
        if question.get("id") == id:
            questions.remove(question)
            #reset id numbers
            i = 0
            for question in questions:
                question["id"] = i
                i = i + 1
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with ID {id} not found")
    return

# TODO: Add a new route that can be used to update a question/answer within the dataset.
@app.put("/update/{id}")
def update_question(id: int, req: QuestionRequest):
    for question in questions:
        if question.get("id") == id:
            question["q"] = req.question
            question["a"] = req.answer
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Question with ID {id} not found")
    return

if __name__=="__main__":
    uvicorn.run(app, port=8005)
