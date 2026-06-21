import os
from textblob import TextBlob
from flask import Flask, request




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

        content = file.read().decode("utf-8")
        word_count = len(content.split())
        reading_time = max(1, word_count // 200)
        lower_text = content.lower()

        mood = "Neutral 😐"
        productivity = "Medium"

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

        if "studied" in lower_text or "worked" in lower_text:
            productivity = "High 🚀"
        
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
        📖 Journal Entry
        </div>

        <div class="journal">
        {content}
        </div>

        </div>

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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))