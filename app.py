# # app.py
# from flask import Flask, render_template, request
# import os

# app = Flask(__name__)

# # --- simple example routes (replace with your real logic) ---
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate_plan():
#     name = request.form.get('name', 'Student')
#     subjects = request.form.getlist('subjects')
#     weak = request.form.get('weak', '')
#     confidence = request.form.get('confidence', 'medium')
#     time_available = int(request.form.get('time', 1) or 1)

#     # Simple adaptive message & timetable generation (demo)
#     timetable = []
#     slots = ["Morning", "Afternoon", "Evening"]
#     # ensure at least one subject
#     if not subjects:
#         subjects = ["Math", "English"]
#     hours_per_slot = round(time_available / len(slots), 1)
#     for i, slot in enumerate(slots):
#         subj = subjects[i % len(subjects)]
#         timetable.append({
#             "slot": slot,
#             "subject": subj,
#             "duration": f"{hours_per_slot} hrs",
#             "quiz": "#",
#             "class": "#"
#         })

#     adaptive_message = []
#     if confidence == "low":
#         adaptive_message.append("Short 25–30 min focused sessions recommended.")
#     elif confidence == "medium":
#         adaptive_message.append("Mix short & medium sessions; include weekly full test.")
#     else:
#         adaptive_message.append("Keep up with weekly mock tests and spaced revision.")
#     adaptive_message.append(f"Give extra 30 mins daily to weaker subject: {weak}.")

#     return render_template('result.html', name=name, timetable=timetable, adaptive_message=adaptive_message)

# # --- IMPORTANT: bind to 0.0.0.0 and dynamic PORT for Render ---
# if __name__ == '__main__':
#     # Render provides the PORT env var. Default to 5000 locally.
#     port = int(os.environ.get("PORT", 5000))
#     # host 0.0.0.0 makes the app visible externally (required on Render)
#     app.run(host='0.0.0.0', port=port, debug=False)

# app.py
from flask import Flask, render_template, request
import os

app = Flask(__name__)

# --- simple example routes (replace with your real logic) ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_plan():
    name = request.form.get('name', 'Student')
    subjects = request.form.getlist('subjects')
    weak = request.form.get('weak', '')
    confidence = request.form.get('confidence', 'medium')
    time_available = int(request.form.get('time', 1) or 1)

    # --- Remove weak subject from main subjects if accidentally selected ---
    if weak in subjects:
        subjects.remove(weak)

    # Simple adaptive message & timetable generation (demo)
    timetable = []
    slots = ["Morning", "Afternoon", "Evening"]

    # ensure at least one subject
    if not subjects:
        subjects = ["Math", "English"]

    hours_per_slot = round(time_available / len(slots), 1)
    for i, slot in enumerate(slots):
        subj = subjects[i % len(subjects)]
        timetable.append({
            "slot": slot,
            "subject": subj,
            "duration": f"{hours_per_slot} hrs",
            "quiz": "#",
            "class": "#"
        })

    # Adaptive messages
    adaptive_message = []
    if confidence == "low":
        adaptive_message.append("Short 25–30 min focused sessions recommended.")
    elif confidence == "medium":
        adaptive_message.append("Mix short & medium sessions; include weekly full test.")
    else:
        adaptive_message.append("Keep up with weekly mock tests and spaced revision.")
    
    adaptive_message.append(f"Give extra 30 mins daily to weaker subject: {weak}.")

    return render_template('result.html', name=name, timetable=timetable, adaptive_message=adaptive_message)

# --- IMPORTANT: bind to 0.0.0.0 and dynamic PORT for Render ---
if __name__ == '__main__':
    # Render provides the PORT env var. Default to 5000 locally.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
