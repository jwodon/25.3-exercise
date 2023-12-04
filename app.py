from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "pass"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# disable caching in browser so changes update on reload
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = -1

debug = DebugToolbarExtension(app)


@app.route('/')
def get_title():
    session['current_question'] = 0  # Initialize the current question ID
    session['responses'] = []  # Initialize an empty list for responses
    return render_template("home.html", survey=survey)

@app.route('/questions/<int:question_id>', methods=['GET', 'POST'])
def get_questions(question_id):
    current_question = session.get('current_question', 0)

    if question_id != current_question:
        # User trying to access invalid question
        flash("You are trying to access an invalid question, please don't.")
        return redirect(f'/questions/{current_question}')



    if request.method == 'POST':
        # Handle the form submission
        user_response = request.form.get('response')
        session['responses'].append(user_response)

        # Move to the next question
        current_question += 1
        session['current_question'] = current_question

        if current_question < len(survey.questions):
            return redirect('/questions')
        else:
            return render_template('thankyou.html')

    if 0 <= current_question < len(survey.questions):
        question = survey.questions[current_question]
        return render_template('questions.html', survey=survey, question=question, question_id=current_question)


@app.route('/questions', methods=['GET', 'POST'])
def get_questions_redirect():
    current_question = session.get('current_question', 0)
    return redirect(f'/questions/{session.get("current_question", 0)}')



