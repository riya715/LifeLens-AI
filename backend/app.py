import os
from textblob import TextBlob
from flask import Flask, request, send_file
from reportlab.pdfgen import canvas
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(BASE_DIR, "LifeLens_Report.pdf")




def create_app():
    app = Flask(__name__)

    @app.route("/")
    def home():
        return """
        <!DOCTYPE html>
        <html>

        <head>
            <title>LifeLens AI</title>

            <style>

                *{
                    margin:0;
                    padding:0;
                    box-sizing:border-box;
                    font-family:'Segoe UI',sans-serif;
                }

                body{

                    background:
                    linear-gradient(
                    135deg,
                    #09011f,
                    #16003b,
                    #1f1147
                    );

                    height:100vh;

                    display:flex;
                    justify-content:center;
                    align-items:center;

                    color:white;
                }

                .card{

                    width:600px;

                    background:
                    rgba(255,255,255,0.08);

                    backdrop-filter:blur(15px);

                    border:1px solid rgba(255,255,255,0.15);

                    border-radius:30px;

                    padding:50px;

                    text-align:center;

                    box-shadow:
                    0 0 30px rgba(255,0,255,0.2);
                }

                h1{

                    font-size:60px;

                    background:
                    linear-gradient(
                    90deg,
                    #ff4fd8,
                    #7b61ff,
                    #00d4ff
                    );

                    -webkit-background-clip:text;
                    -webkit-text-fill-color:transparent;

                    margin-bottom:20px;
                }

                p{

                    color:#d8d8d8;

                    font-size:22px;

                    margin-bottom:35px;
                }

                input[type=file]{

                    width:100%;

                    padding:15px;

                    border-radius:15px;

                    border:2px dashed #7b61ff;

                    background:rgba(255,255,255,0.05);

                    color:white;

                    margin-bottom:25px;
                }

                button{

                    width:100%;

                    padding:18px;

                    border:none;

                    border-radius:15px;

                    font-size:20px;

                    font-weight:bold;

                    cursor:pointer;

                    color:white;

                    background:
                    linear-gradient(
                    90deg,
                    #ff4fd8,
                    #7b61ff,
                    #00d4ff
                    );

                    transition:0.3s;
                }

                button:hover{

                    transform:scale(1.03);

                    box-shadow:
                    0 0 25px rgba(123,97,255,0.8);
                }

                .tag{

                    margin-bottom:25px;

                    color:#b9b9b9;

                    font-size:14px;
                }

            </style>

        </head>

        <body>

            <div class="card">

                <h1>🚀 LifeLens AI</h1>

                <p>
                    Upload your journal and discover
                    insights about yourself.
                </p>

                <div class="tag">
                    ✨ AI Powered Mood & Productivity Analyzer
                </div>

                <form
                action="/upload"
                method="POST"
                enctype="multipart/form-data">

                    <input
                    type="file"
                    name="journal_file">

                    <button type="submit">
                        Analyze Journal 🚀
                    </button>

                </form>

            </div>

        </body>

        </html>
        """

    @app.route("/upload", methods=["POST"])
    def upload():

        file = request.files.get("journal_file")

        if file is None:
            return "No file uploaded", 400

        data = file.read()

        try:
            content = data.decode("utf-8")
        except UnicodeDecodeError:
            return """
            <h2>❌ Invalid File</h2>
            <p>Please upload a plain UTF-8 encoded .txt journal file.</p>
            """, 400
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)
        lower_text = content.lower()

        mood = "Neutral 😐"
        productivity = "Medium"
        productivity_score = 40

        blob = TextBlob(content)
        sentiment_score = blob.sentiment.polarity

        if TextBlob is not None:
            blob = TextBlob(content)
            sentiment_score = blob.sentiment.polarity
            print(f"Sentiment score: {sentiment_score}")  # Debugging line
        else:
            sentiment_score = 0.0

        if sentiment_score > 0.2:
            mood = "Positive 😊"

           

        elif sentiment_score < -0.2:
            mood = "Negative 😔"

        else:
            mood = "Neutral 😐"

        

        if "excited" in lower_text or "happy" in lower_text:
            mood = "Positive 😊"

            

            if "studied" in lower_text:
                productivity_score += 20

            if "worked" in lower_text:
                productivity_score += 20

            if "project" in lower_text:
                productivity_score += 10

            if "learning" in lower_text:
                productivity_score += 10

            if "completed" in lower_text:
                productivity_score += 10

            if productivity_score >= 70:
                productivity = "High 🚀"
            else:
                productivity = "Medium"
                    
        if mood == "Positive 😊" and productivity == "High 🚀":
            insight = """
            You had a productive day.
            You spent time learning and working on your goals.
            Your journal reflects a positive and motivated mindset.
            Keep maintaining this momentum!
            """

        elif mood == "Positive 😊":
            insight = """
            You seem happy and emotionally positive today.
            Keep focusing on activities that make you feel this way.
            """

        elif productivity == "High 🚀":
            insight = """
            You were productive today.
            Continue building consistent habits and routines.
            """

        else:
            insight = """
            Today appears to be a normal day.
            Try setting one small goal for tomorrow.
            """

        if mood == "Positive 😊":
            motivation = "🚀 Keep going! You're making progress every day."

        elif mood == "Negative 😔":
            motivation = "💜 Tough days don't last. Tomorrow is a new opportunity."

        else:
            motivation = "✨ Small consistent actions create big results." 
        c = canvas.Canvas(PDF_PATH)
        

        

        y = 800

        c.setFont("Helvetica-Bold", 22)
        c.drawString(180, y, "LifeLens AI Report")
        c.line(80, y-15, 500, y-15)

        y -= 40

        c.setFont("Helvetica", 14)
        c.drawString(80, y, "Generated using LifeLens AI")

        y -= 25

        current_date = datetime.now().strftime("%d %B %Y %I:%M %p")
        c.drawString(80, y, f"Generated on: {current_date}")

        y -= 50

        c.setFont("Helvetica-Bold", 15)
        pdf_mood = mood.replace("😊", "").replace("😔", "")
        c.drawString(80, y, f"Mood : {pdf_mood}")

        y -= 25
        c.drawString(80, y, f"Mood Score : {round(sentiment_score,2)}")

        y -= 25
        pdf_productivity = productivity.replace("🚀", "")
        c.drawString(80, y, f"Productivity : {pdf_productivity}")

        y -= 25
        c.drawString(80, y, f"Productivity Score : {productivity_score}%")

        y -= 25
        c.drawString(80, y, f"Word Count : {word_count}")

        y -= 25
        c.drawString(80, y, f"Reading Time : {reading_time} min")

        y -= 45

        c.setFont("Helvetica-Bold",16)
        c.drawString(80,y,"AI Insight")

        y -= 25

        c.setFont("Helvetica",12)

        for line in insight.strip().split("\n"):
                c.drawString(80,y,line.strip())
                y -= 18

        y -= 20

        c.setFont("Helvetica-Bold",16)
        c.drawString(80,y,"Daily Motivation")

        y -= 25

        c.setFont("Helvetica",12)
        pdf_motivation = (
        motivation.replace("🚀", "")
              .replace("💜", "")
              .replace("✨", "")
        )

        c.drawString(80, y, pdf_motivation)

        y -= 40

        c.setFont("Helvetica-Bold",16)
        c.drawString(80,y,"Journal Entry")

        y -= 25

        c.setFont("Helvetica",12)

        for line in content.split("\n"):
                c.drawString(80,y,line)
                y -= 18
        
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(170, 30, "Generated by LifeLens AI | Created by Riya")

        c.save() 
        print("PDF Created Successfully!")
        print(PDF_PATH)
        print(os.path.exists(PDF_PATH))

        return f"""
        <!DOCTYPE html>
        <html>

        <head>

        <title>LifeLens AI Analysis</title>

        <style>

        body{{
            margin:0;
            font-family:'Segoe UI',sans-serif;

            background:
            linear-gradient(
            135deg,
            #09011f,
            #16003b,
            #1f1147
            );

            color:white;

            display:flex;
            justify-content:center;
            align-items:center;

            min-height:100vh;
        }}

        .container{{
            width:800px;
            background:
            rgba(255,255,255,0.08);
            backdrop-filter:blur(15px);
            border-radius:30px;
            padding:40px;
            border:1px solid rgba(255,255,255,0.15);
            box-shadow:
            0 0 30px rgba(255,0,255,0.2);
        }}

        h1{{
            text-align:center;
            background:
            linear-gradient(
            90deg,
            #ff4fd8,
            #7b61ff,
            #00d4ff
            );
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
            font-size:50px;
        }}

        .card{{
            background: rgba(255,255,255,0.05);
            padding:20px;
            margin-top:20px;
            border-radius:15px;
            border:1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
        }}

        .card:hover{{
            transform: translateY(-8px) scale(1.02);
            box-shadow:
                0 0 30px #ff4fd8,
                0 0 60px rgba(255,79,216,0.4);
        }}

        .insight-card{{
            border:2px solid rgba(255,79,216,0.4);
            box-shadow:
                0 0 15px rgba(255,79,216,0.3);
            transition: all 0.3s ease;
        }}

        .insight-card:hover{{
            transform: translateY(-8px) scale(1.02);
            box-shadow:
                0 0 30px #ff4fd8,
                0 0 60px rgba(255,79,216,0.6),
                0 0 90px rgba(123,97,255,0.4);
        }}

        .label{{
            font-size:24px;
            font-weight:bold;
        }}

        .value{{
            font-size:22px;
            margin-top:10px;
        }}

        .journal{{
            white-space:pre-wrap;
            line-height:1.8;
        }}

        .btn{{
            display:block;
            text-align:center;
            margin-top:30px;
            text-decoration:none;
            color:white;
            padding:15px;
            border-radius:15px;
            background:
            linear-gradient(
            90deg,
            #ff4fd8,
            #7b61ff,
            #00d4ff
            );
        }}

        </style>

        </head>

        <body>

        <div class="container">

        <h1>🚀 LifeLens AI</h1>

        <div class="card">

        <div class="label">
        😊 Mood
        </div>

        <div class="value mood">
        {mood}
        </div>

        </div>
        <div class="card">

        <div class="label">
        📈 Mood Score
        </div>

        <div class="value">
        {round(sentiment_score, 2)}
        </div>

        <div style="
        width:100%;
        height:12px;
        background:#2a1f4f;
        border-radius:10px;
        margin-top:12px;
        overflow:hidden;
        ">

        <div style="
        width:{int((sentiment_score + 1) * 50)}%;
        height:100%;
        background:linear-gradient(
        90deg,
        #ff4fd8,
        #7b61ff,
        #00d4ff
        );
        ">
        </div>

        </div>

        </div>
        <div class="card">

        <div class="label">
        🚀 Productivity
        </div>

        <div class="value productivity">
        {productivity}
        </div>

        </div>
        <div class="card">

        <div class="label">
        📈 Productivity Score
        </div>

        <div class="value">
        {productivity_score}%
        </div>

        </div>
        <div class="card">
    <div class="label">
        📊 Word Count
    </div>

    <div class="value">
        {word_count}
    </div>
</div>
    <div class="card">

    <div class="label">
        ⏱ Reading Time
    </div>

    <div class="value">
        {reading_time} min
    </div>

</div>


        <div class="card insight-card">

           <div class="label">
            ✨ AI Insight
           </div>

           <div class="journal">
            {insight}
           </div>

        </div>
        <div class="card">

        <div class="label">
        🔥 Daily Motivation
        </div>

        <div class="journal">
        {motivation}
        </div>

        </div>

        <div class="card">

        <div class="label">
        📖 Journal Entry
        </div>

        <div class="journal">
        {content}
        </div>

        </div>
        <a class="btn" href="/download-report">
    📄 Download PDF Report
</a>
        <br><br>
        <a class="btn" href="/">
            ⬅ Analyze Another Journal
        </a>

        </div>
        <p style="
        text-align:center;
        margin-top:20px;
        opacity:0.7;
        ">
        Built with ❤️ by Riya
        </p>

        </body>

        </html>
        """

    @app.route("/analyze", methods=["POST"])
    def analyze():
        journal_text = request.form.get("journal", "")

        if not journal_text.strip():
            return "No journal text provided", 400

        mood = "Neutral 😐"
        productivity = "Medium"
        insight = "You had a normal day."

        lower_text = journal_text.lower()

        if "excited" in lower_text or "happy" in lower_text:
            mood = "Positive 😊"

        if "studied" in lower_text or "worked" in lower_text:
            productivity = "High 🚀"

        if mood == "Positive 😊" and productivity == "High 🚀":
            insight = "You had a productive day. You spent time learning and working on your goals. Your journal reflects a positive and motivated mindset. Keep maintaining this momentum!"
        elif mood == "Positive 😊":
            insight = "You seem happy and emotionally positive today. Keep focusing on activities that make you feel this way."
        elif productivity == "High 🚀":
            insight = "You were productive today. Continue building consistent habits and routines."
        else:
            insight = "Today appears to be a normal day. Try setting one small goal for tomorrow."

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>LifeLens AI Analysis</title>
        </head>
        <body>
            <h1>LifeLens AI</h1>
            <p>Mood: {mood}</p>
            <p>Productivity: {productivity}</p>
            <p>Insight: {insight}</p>
            <p>{journal_text}</p>
        </body>
        </html>
        """
    @app.route("/download-report")
    def download_report():

        print("Downloading from:", PDF_PATH)
        print("Exists:", os.path.exists(PDF_PATH))

        return send_file(
            PDF_PATH,
            as_attachment=True
        )
    
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))