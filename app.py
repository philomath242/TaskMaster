import pymongo
from flask import Flask, render_template, request, redirect
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

# print(pymongo.version)

client = pymongo.MongoClient('localhost', 27017)

# client = pymongo.MongoClient("mongodb+srv://philomath242:IITKharagpurTempo@mongo-heroku-cluster-ta.dajgi.mongodb.net/?retryWrites=true&w=majority")

db = client.taskmasterdb
todos = db.todos


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # put in database
        task_content = request.form['content']
        created_on = datetime.now().strftime("%d-%m-%Y at %H:%M")
        try:
            # add to database
            if task_content.strip():
                todos.insert_one({'content': task_content, 'created_on': created_on})
                return redirect('/')
            else:
                return "Task cannot be empty"
        except:
            return "There was an issue adding your task"

    else:
        tasks = todos.find()
        return render_template('index.html', tasks=tasks, count=todos.estimated_document_count())


@app.route('/delete/<id>')
def delete(id):
    task_to_delete = todos.find_one({"_id": ObjectId(id)})
    # print("task to delete", task_to_delete)
    try:
        # delete the document with id
        todos.delete_one(task_to_delete)
        return redirect('/')
    except:
        return "There was a problem with the database"


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    task = todos.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        try:
            new_content = request.form['content']
            todos.update_one(task, {"$set": {"content": new_content}})
            return redirect('/')
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
