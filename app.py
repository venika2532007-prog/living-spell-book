from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'spellbook_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/add_spell', methods=['GET', 'POST'])
def add_spell():
    if request.method == 'POST':
        name = request.form['spell_name']
        category = request.form['category']
        emoji = request.form.get('emoji')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO spells (name, category, emoji) VALUES (%s, %s, %s)", (name, category, emoji))
        mysql.connection.commit()
        cur.close()

        return "✨ Spell Added Successfully! <br><a href='/spells'>View Spells</a>"

    return render_template("add_spell.html")

@app.route('/spells')
def view_spells():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM spells")
    spells = cur.fetchall()
    cur.close()
    return render_template("view_spells.html", spells=spells)

@app.route("/mood", methods=["GET", "POST"])
def mood():
    suggested_spell = None

    if request.method == "POST":
        mood = request.form["mood"]

        # Mood spell logic
        if mood == "happy":
            suggested_spell = "🎉 Celebration Charm ✨"
        elif mood == "sad":
            suggested_spell = "💙 Healing Tear Spell 💧"
        elif mood == "angry":
            suggested_spell = "🔥 Calm Flame Ritual 🔥"
        elif mood == "tired":
            suggested_spell = "🌙 Restful Dream Enchantment 😴"
        elif mood == "scared":
            suggested_spell = "🛡 Protection Shield Spell 🔮"
        else:
            suggested_spell = "🌀 Chaotic Magic: try again?"

    return render_template("mood.html", suggested_spell=suggested_spell)
@app.route('/stress', methods=['GET', 'POST'])
def stress():
    message = None

    if request.method == 'POST':
        level = request.form['level']
        note = request.form.get('note', '')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO stress_logs (level, note) VALUES (%s, %s)", (level, note))
        mysql.connection.commit()
        cur.close()

        message = f"✨ Stress Recorded! You're doing your best 💖"

    # Fetch old logs
    cur = mysql.connection.cursor()
    cur.execute("SELECT level, note, created_at FROM stress_logs ORDER BY created_at DESC")
    logs = cur.fetchall()
    cur.close()

    # Basic emotional guidance based on last stress level
    advice = None
    if logs:
        last_level = logs[0][0]
        if last_level <= 2:
            advice = "🌿 Your mind is calm. Keep protecting this peace. 💚"
        elif 3 <= last_level <= 5:
            advice = "💛 A little stress is okay. Breathe deeply — you’ve got this."
        elif 6 <= last_level <= 8:
            advice = "🔥 Your emotions are strong. Try journaling or going on a walk."
        else:
            advice = "💔 You're overwhelmed — please rest or talk to someone safe."

    return render_template("stress.html", logs=logs, message=message, advice=advice)
@app.route("/forest_data")
def forest_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM stress_log")
    total = cur.fetchone()[0]
    cur.close()

    return {"count": total}

@app.route("/forest")
def forest():
    return render_template("forest.html")
if __name__ == "__main__":
    app.run(debug=True)
