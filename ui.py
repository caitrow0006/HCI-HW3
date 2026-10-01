from nicegui import ui
import requests

ui.colors(
      primary='#27B0F5',
      secondary='#2768F5',
      accent='#7847F5',
      positive='#a2e0b0',
      negative='#CD0404',
      info='#47E6F5',
      warning='#F2C037'
)

API_URL = "http://localhost:8005"

questions = []
page_body = ui.column()

def api_get(path):
    try:
        # Attempt to send GET request to API
        response = requests.get(f"{API_URL}{path}", timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, GET was successful so return response data
        return response.json()
    except requests.RequestException as e:
        # GET request was unsuccessful
        # Send an alert with error details to the UI and return empty list
        ui.notify(f"Could not reach API: {e}", type="negative")
        return []

def api_post(path, data):
    try:
        # Attempt to send POST request to API with data payload
        response = requests.post(f"{API_URL}{path}", json=data, timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, POST was successful so return True
        return True
    except requests.RequestException as e:
        # POST request was unsuccessful
        # Send an alert with error details to the UI and return False
        ui.notify(f"Could not reach API: {e}", type="negative")
        return False

# TODO: Create api_delete function that attempts to send a DELETE request to the API.
# The request method should use the string f"{API_URL}{path}/{id}" to access the correct path,
# where id refers to the id number of the question to be deleted. 
def api_delete(path, id):
    try:
        # Attempt to send DELETE request to API with data payload
        response = requests.delete(f"{API_URL}{path}/{id}", timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, DELETE was successful so return True
        return True
    except requests.RequestException as e:
        # DELETE request was unsuccessful
        # Send an alert with error details to the UI and return False
        ui.notify(f"Could not reach API: {e}", type="negative")
        return False

# TODO: Create api_put function that attempts to send a PUT request to the API.
# The request method should use the string f"{API_URL}{path}/{id}" to access the correct path,
# where id refers to the id number of the question to be deleted. The data passed as an argument
# to this function must be sent with the request so that the API knows the updated values to add 
# to the dataset (similar to how data is sent in api_post).
def api_put(path, id, data):
    try:
        # Attempt to send PUT request to API with data payload
        response = requests.put(f"{API_URL}{path}/{id}", json=data, timeout=5)
        # If we get an error code back, raise an exception
        response.raise_for_status()
        # Otherwise, PUT was successful so return True
        return True
    except requests.RequestException as e:
        # PUT request was unsuccessful
        # Send an alert with error details to the UI and return False
        ui.notify(f"Could not reach API: {e}", type="negative")
        return False

# TODO: Add edit and delete buttons dynamically to each question card. 
def render_question(question):
    #create UI card
    with ui.card() as card:
        card.classes("w-full")
        #on clicj toggle to show/hide answer
        card.on("click", lambda: toggle_answer(question["id"]))
        ui.label(question["q"])
        ui.label(question["a"]).classes("text-s text-green font-bold").bind_visibility_from(question["state"], "show_answer")
        
        #dialog first so that edit button knows it exists **?**
        with ui.dialog() as edit_dialog, ui.card():
            ui.label('Edit Question')
            
            #value field is prefill text
            question_edit = ui.textarea(label='Question:', value=question["q"])
            answer_edit = ui.textarea(label='Answer:', value=question["a"])
            
            #put buttons in row
            with ui.row():
                #when saving, call put but also close dialog
                ui.button('Save', on_click=lambda: (update_question( question["id"], question=question_edit.value, answer=answer_edit.value), edit_dialog.close))
                #https://github.com/zauberzeug/nicegui/discussions/1220
                
                #if cancel,, dont put, just close dialogue
                ui.button('Cancel', on_click=edit_dialog.close)
                
        with ui.row() as button_row:
        
            button_row.classes("bg-gray-300 rounded p-3")
            #make update question button
            update_question_btn = ui.button(text="Edit", on_click=edit_dialog.open).classes("bg-primary text-white font-bold py-2 px-4 rounded")
            
            #create delete button, on click call delete_question made earlier
            delete_question_btn = ui.button(text="Delete", on_click=lambda: delete_question(id=question["id"])).classes("bg-negative text-white font-bold py-2 px-4 rounded")
                

def toggle_answer(i):
    questions[i]["state"]["show_answer"] = not questions[i]["state"]["show_answer"]

def add_new_question(question, answer):
    api_post("/add", {"question": question, "answer": answer})
    render_page()

#helper to delete question, remeber to render page!!
def delete_question(id):
    api_delete(f"/delete", id)
    render_page()
    
#helper to update question, remeber to render page!!
def update_question(id, question, answer):
    api_put(f"/update", id, {"question": question, "answer": answer})
    render_page()

def render_text_inputs():
    new_question_input = ui.input(label="New question").props("clearable")
    new_answer_input = ui.input(label="New answer").props("clearable")
    add_question_btn = ui.button(text="Add question", on_click=lambda: add_new_question(
        question=new_question_input.value,
        answer=new_answer_input.value
    )).classes("bg-primary text-white font-bold py-2 px-4 rounded")

def init_page():
    render_page()

def render_page():
    global questions
    questions = api_get("/questions")
    page_body.clear()
    with page_body:
        with ui.column() as questions_col:
            questions_col.classes("bg-accent rounded p-3")
            for question in questions:
                question["state"] = {"show_answer": False}
                render_question(question)
        render_text_inputs()
    

init_page()
ui.run(port=8084, title="HCI Review Application")

#list of materials referenced:
#https://www.w3schools.com/python/python_arrays.asp
#https://tailwind.build/classes
#https://daisyui.com/components/button/
#https://htmlcolorcodes.com/color-picker/
#https://www.geeksforgeeks.org/python/put-method-python-requests/
#https://nicegui.io/documentation/textarea
#https://github.com/zauberzeug/nicegui/discussions/1220
#https://www.siteground.com/kb/422-error-code
