from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Quiz links and class links per subject (you can modify these)
QUIZ_LINKS = {
    "Math": "https://www.proprofs.com/quiz-school/story.php?title=math-quiz",
    "Physics": "https://www.proprofs.com/quiz-school/story.php?title=physics-test",
    "Chemistry": "https://www.proprofs.com/quiz-school/story.php?title=chemistry-quiz",
    "Biology": "https://www.proprofs.com/quiz-school/story.php?title=biology-quiz",
    "English": "https://www.proprofs.com/quiz-school/story.php?title=english-grammar",
    "Computer": "https://www.proprofs.com/quiz-school/story.php?title=python-coding-quiz"
}

CLASS_LINKS = {
    "Math": "https://www.khanacademy.org/math",
    "Physics": "https://www.khanacademy.org/science/physics",
    "Chemistry": "https://www.khanacademy.org/science/chemistry",
    "Biology": "https://www.khanacademy.org/science/biology",
    "English": "https://www.britishcouncil.org/english",
    "Computer": "https://www.w3schools.com/python/"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_plan():
    name = request.form['name']
    subjects = request.form.getlist('subjects')
    weak = request.form['weak']
    confidence = request.form['confidence']
    time_available = int(request.form['time'])

    # Create adaptive message
    adaptive_message = []
    if confidence == "low":
        adaptive_message.append("Focus on confidence-building sessions (short 30-min topic reviews).")
    elif confidence == "medium":
        adaptive_message.append("Mix short and long sessions for consistent improvement.")
    else:
        adaptive_message.append("Maintain your pace but take weekly full-length tests.")

    # Create daily timetable based on total time
    timetable = []
    slots = ["Morning", "Afternoon", "Evening"]
    hours_per_slot = round(time_available / 3, 1)
    random.shuffle(slots)

    for slot, subject in zip(slots, subjects):
        timetable.append({
            "slot": slot,
            "subject": subject,
            "duration": f"{hours_per_slot} hrs",
            "quiz": QUIZ_LINKS.get(subject, "#"),
            "class": CLASS_LINKS.get(subject, "#")
        })

    # Add weak subject focus
    adaptive_message.append(f"Spend extra 30 mins daily on your weak subject: {weak}.")

    return render_template(
        'result.html',
        name=name,
        timetable=timetable,
        adaptive_message=adaptive_message
    )

if __name__ == '__main__':
    app.run(debug=True)

