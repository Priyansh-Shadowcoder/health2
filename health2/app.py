from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///health.db"
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Register(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.String(500), nullable = False)
    Email = db.Column(db.String(100), nullable = False)
    Contact = db.Column(db.String(15), nullable = False)
    Pass = db.Column(db.String(20), nullable = False)
    date = db.Column(db.DateTime, default=lambda : datetime.now(timezone.utc))
    def __repr__(self) -> str:
        return f"{self.sno} - {self.Username} - {self.Email} - {self.Pass} - {self.Contact}"

class wellness(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    Mood = db.Column(db.String(200), nullable = False)
    Describe = db.Column(db.String(200), nullable = False)
    Stress_Rate = db.Column(db.String(5), nullable = False)
    STRESS = db.Column(db.String(500), nullable = False)
    TYPE = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = lambda : datetime.now(timezone.utc))
    def __repr__(self) -> str:
        return f"{self.sno} - {self.Mood} - {self.Stress_Rate} - {self.TYPE}"

class log(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    User = db.Column(db.String(500), nullable = False)
    Pass = db.Column(db.String(100), nullable = False)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.User} - {self.Pass}"

'''class schedule(db.Model):
    sno = db.Column(db.Integer, primary_key = False)
    User = db.Column(db.String(500), nullable = False)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.User} - {self.Pass}"'''



QUESTIONS = [
    {"id": 0, "q": "Overwhelmed: How often have you felt that you were unable to control the important things in your life?", "options": ["Never", "Sometimes", "Often", "Always"]},
    {"id": 1, "q": "Restlessness: How often have you felt so restless that it was hard to sit still?", "options": ["Never", "Sometimes", "Often", "Always"]},
    {"id": 2, "q": "Anhedonia: How often have you had little interest or pleasure in doing things you normally enjoy?", "options": ["Never", "Sometimes", "Often", "Always"]},
    {"id": 3, "q": "Sleep Quality: How often have you had trouble falling or staying asleep, or felt like you were sleeping too much?", "options": ["Never", "Sometimes", "Often", "Always"]},
    {"id": 4, "q": "Focus: How often have you found it difficult to concentrate on tasks, such as reading or working?", "options": ["Never", "Sometimes", "Often", "Always"]},
    {"id": 5, "q": "Self-Perception: How often have you felt bad about yourself—or that you are a failure or have let yourself or your family down?", "options": ["Never", "Sometimes", "Often", "Always"]},
    {"id": 6, "q": "Social Withdrawal: How often have you felt the urge to avoid social interactions or felt lonely even when around others?", "options": ["Never", "Sometimes", "Often", "Always"]},
    {"id": 7, "q": "Physical Tension: How often have you experienced physical symptoms of stress, such as headaches, muscle tension, or an upset stomach?", "options": ["Never", "Sometimes", "Often", "Always"]},
    {"id": 8, "q": "Irritability: How often have you felt easily annoyed, irritable, or on edge?", "options": ["Never", "Sometimes", "Often", "Always"]},
    {"id": 9, "q": "Future Outlook: How often have you felt pessimistic or hopeless about your future?", "options": ["Never", "Sometimes", "Often", "Always"]},    
]

@app.route('/quiz', methods=['GET', 'POST'])
def assessment():
    if request.method == 'POST':
        answers = request.form.get('all_answers').split(',')
        total_score = sum([int(a) for a in answers])
        
        status = "Low Stress"
        if total_score > 20: status = "Severe Stress"
        elif total_score > 15: status = "High Stress"
        elif total_score > 10: status = "Moderate Stress"
        elif total_score > 5 : status = "Regular"

        new_entry = wellness(
            Mood="Assessed", 
            Describe="Quiz Completion", 
            Stress_Rate=str(total_score), 
            STRESS=status, 
            TYPE="General"
        )
        db.session.add(new_entry)
        db.session.commit()
        
        return render_template('results.html', score=total_score, status=status)

    return render_template('quiz.html', questions=QUESTIONS)
@app.route('/', methods = ['GET','POST'])
def front():
    if(request.method == 'POST'):
        User = request.form['username']
        email = request.form['email']
        cont = request.form['contact']
        passw = request.form['password']

        HealthRegister = Register(Username = User, Email = email, Contact = cont, Pass = passw, )
        db.session.add(HealthRegister)
        db.session.commit()
        return redirect('/home')
        
    return render_template('index.html')

@app.route('/excercises')
def exc():
    return render_template('exercises.html')
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        USER = request.form['user']
        pasw = request.form['pass']

        Login = log(User = USER, Pass = pasw)
        db.session.add(Login)
        db.session.commit()
        return redirect('/home')

    return render_template('1.html')

@app.route('/schedule')
def shed():
    return render_template('3.1.html')

@app.route('/library')
def lib():
    return render_template('2.html')


@app.route('/appointment')
def appo():
    return render_template('3.html')

@app.route('/emergency')
def emer():
    return render_template('4.html')

@app.route('/mindfullness')
def mind():
    return render_template('mindfullness.html')

@app.route('/meditation')
def med():
    return render_template('meditation.html')

@app.route('/breathing')
def breath():
    return render_template('breathing.html')

@app.route('/cognitive')
def cog():
    return render_template('cognitive.html')

@app.route('/connect')
def con():
    return render_template('connect.html')

@app.route('/gratitude')
def grat():
    return render_template('gratitude.html')

@app.route('/physical')
def pyh():
    return render_template('physical.html')


@app.route('/sleep')
def slep():
    return render_template('sleep.html')





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)