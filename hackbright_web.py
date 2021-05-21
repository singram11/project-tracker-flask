"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    student_info = hackbright.get_student_by_github(github)
    
    # print("{} is the GitHub account for {} {}".format(github, first, last))
    project_data = hackbright.get_grades_by_github(github)
    # print(f"project title: {project_title}")
    # print(project_data)

    return render_template("student_info.html",
                            student=student_info,
                            project_data=project_data)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student-add")
def get_student_add_form():
    """Show form for adding a student."""

    return render_template("student_add.html")

@app.route("/new-student", methods=['POST'])
def adds_student():
    """Adds new student to database, alerts student was added, redirects to /student."""

    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    github = request.form.get('github')


    hackbright.make_new_student(first_name, last_name, github)

    # alert(f"{first_name} {last_name} was added to the directory!")
    # redirect(f"/student?github={github}")

    return render_template("new_student_added.html",
                            github=github) 

@app.route("/project")
def get_project_info():
    "Display project title, description, and maximum grade"

    project_title = request.args.get('title')

    project_info = hackbright.get_project_by_title(project_title)

    #list of tuples (github, grade)
    grades_by_github = hackbright.get_grades_by_title(project_title)
    # Loop over list of githup + grade 
        #find student name with get student function --
        #add it to the tuple??
    # name hackbright.get_student_by_github(github)

    return render_template("project_info.html",
                            project_info=project_info,
                            grades=grades_by_github)

@app.route("/")
def display_homepage():
    """Display homepage with list of students and projects"""

    # make list of students

    # make list of projects

    return render_template("homepage.html")

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
