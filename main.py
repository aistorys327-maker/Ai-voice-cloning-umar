from flask import Flask, request, render_template_string
import requests
import os
import uuid

app = Flask(__name__)

API_KEY = "56d05eb3990544d2a82261365441605b"

HTML = """

<!DOCTYPE html>
<html>

<head>

<title>AI Voice Cloning</title>

<style>

body{
background:#020617;
font-family:sans-serif;
color:white;
text-align:center;
padding:20px;
}

.container{
background:#0f172a;
padding:25px;
border-radius:20px;
max-width:500px;
margin:auto;
}

h1{
font-size:36px;
}

textarea{
width:92%;
height:140px;
padding:15px;
border:none;
border-radius:15px;
font-size:18px;
margin-top:20px;
}

button{
margin-top:20px;
padding:15px 35px;
font-size:20px;
border:none;
border-radius:15px;
background:#2563eb;
color:white;
}

input[type=file]{
margin-top:20px;
font-size:16px;
}

audio{
margin-top:30px;
width:95%;
}

</style>

</head>

<body>

<div class="container">

<h1>🎤 AI Voice Cloning</h1>

<form method="POST" enctype="multipart/form-data">

<input type="file" name="voice" required>

<br>

<textarea
name="text"
placeholder="Type text here..."
required
></textarea>

<br>

<button type="submit">
Generate Voice
</button>

</form>

{% if audio %}

<audio controls autoplay>
<source src="{{ audio }}">
</audio>

<br><br>

<a href="{{ audio }}" download>
<button>Download MP3</button>
</a>

{% endif %}

</div>

</body>
</html>

"""

@app.route("/", methods=["GET","POST"])

def home():

    audio = None

    if request.method == "POST":

        text = request.form["text"]

        voice_file = request.files["voice"]

        if not os.path.exists("static"):
            os.makedirs("static")

        temp_voice = f"static/{uuid.uuid4()}.wav"

        voice_file.save(temp_voice)

        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }

        files = {
            "audio": open(temp_voice, "rb")
        }

        data = {
            "text": text
        }

        response = requests.post(
            "https://api.fish.audio/v1/tts",
            headers=headers,
            files=files,
            data=data
        )

        if response.status_code == 200:

            output = f"static/{uuid.uuid4()}.mp3"

            with open(output, "wb") as f:
                f.write(response.content)

            audio = "/" + output

    return render_template_string(
        HTML,
        audio=audio
    )

app.run(host="0.0.0.0", port=10000)
