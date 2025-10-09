from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from models import db, Owner, Horse, Jockey, Competition, Result
from hooks import register_error_handlers
from datetime import datetime
from config import Config  

app = Flask(__name__)
app.config.from_object(Config)  
db.init_app(app)

# Регистрация обработчиков ошибок
register_error_handlers(app)


@app.route('/')
def index():
    competitions = Competition.query.all()
    jockeys_count = Jockey.query.count()
    horses_count = Horse.query.count()
    return render_template('index.html', 
                          competitions=competitions, 
                          jockeys_count=jockeys_count, 
                          horses_count=horses_count)

@app.route('/add_competition', methods=['GET', 'POST'])
def add_competition():
    if request.method == 'POST':
        try:
            competition = Competition(
                date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
                time=datetime.strptime(request.form['time'], '%H:%M').time(),
                location=request.form['location'],
                name=request.form['name']
            )
            db.session.add(competition)
            db.session.commit()
            flash('Состязание успешно добавлено', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении состязания: {str(e)}', 'error')
    
    return render_template('add_competition.html')

@app.route('/add_jockey', methods=['GET', 'POST'])
def add_jockey():
    if request.method == 'POST':
        try:
            jockey = Jockey(
                name=request.form['name'],
                address=request.form['address'],
                age=int(request.form['age']),
                rating=float(request.form['rating'])
            )
            db.session.add(jockey)
            db.session.commit()
            flash('Жокей успешно добавлен', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении жокея: {str(e)}', 'error')
    
    return render_template('add_jockey.html')

@app.route('/add_horse', methods=['GET', 'POST'])
def add_horse():
    owners = Owner.query.all()
    
    if request.method == 'POST':
        try:
            horse = Horse(
                name=request.form['name'],
                gender=request.form['gender'],
                age=int(request.form['age']),
                owner_id=int(request.form['owner_id'])
            )
            db.session.add(horse)
            db.session.commit()
            flash('Лошадь успешно добавлена', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении лошади: {str(e)}', 'error')
    
    return render_template('add_horse.html', owners=owners)

@app.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    if request.method == 'POST':
        try:
            owner = Owner(
                name=request.form['name'],
                address=request.form['address'],
                phone=request.form['phone']
            )
            db.session.add(owner)
            db.session.commit()
            flash('Владелец успешно добавлен', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении владельца: {str(e)}', 'error')
    
    return render_template('add_owner.html')

@app.route('/add_result', methods=['GET', 'POST'])
def add_result():
    competitions = Competition.query.all()
    jockeys = Jockey.query.all()
    horses = Horse.query.all()
    
    if request.method == 'POST':
        try:
            result = Result(
                competition_id=int(request.form['competition_id']),
                jockey_id=int(request.form['jockey_id']),
                horse_id=int(request.form['horse_id']),
                position=int(request.form['position']),
                time=request.form['time']
            )
            db.session.add(result)
            db.session.commit()
            flash('Результат успешно добавлен', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ошибка при добавлении результата: {str(e)}', 'error')
    
    return render_template('add_result.html', competitions=competitions, jockeys=jockeys, horses=horses)

@app.route('/competition/<int:competition_id>')
def competition_results(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    results = Result.query.filter_by(competition_id=competition_id).all()
    return render_template('competition_results.html', competition=competition, results=results)

@app.route('/jockey/<int:jockey_id>')
def jockey_competitions(jockey_id):
    jockey = Jockey.query.get_or_404(jockey_id)
    results = Result.query.filter_by(jockey_id=jockey_id).all()
    return render_template('jockey_competitions.html', jockey=jockey, results=results)

@app.route('/horse/<int:horse_id>')
def horse_competitions(horse_id):
    horse = Horse.query.get_or_404(horse_id)
    results = Result.query.filter_by(horse_id=horse_id).all()
    return render_template('horse_competitions.html', horse=horse, results=results)

@app.route('/jockeys')
def jockeys_list():
    jockeys = Jockey.query.all()
    return render_template('jockeys_list.html', jockeys=jockeys)

@app.route('/horses')
def horses_list():
    horses = Horse.query.all()
    return render_template('horses_list.html', horses=horses)

if __name__ == '__main__':
    app.run(debug=True)
