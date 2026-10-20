from flask import Flask, request, render_template_string

from checker import check_password
from breach import check_breach

app = Flask(__name__)

PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Password Checker</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 480px; margin: 60px auto; padding: 0 16px; }
    input[type=password] { width: 100%; padding: 10px; font-size: 16px; box-sizing: border-box; }
    button { margin-top: 12px; padding: 10px 20px; font-size: 16px; cursor: pointer; }
    .box { margin-top: 24px; padding: 16px; border: 1px solid #ccc; border-radius: 6px; }
    .warn { color: #b00020; font-weight: bold; }
    .ok { color: #1b7f3b; font-weight: bold; }
  </style>
</head>
<body>
  <h2>Password Strength &amp; Breach Checker</h2>
  <form method="post">
    <input type="password" name="password" placeholder="Password likho" required>
    <button type="submit">Check karo</button>
  </form>

  {% if result %}
  <div class="box">
    <p><b>Strength:</b> {{ result.score }} ({{ result.entropy }} bits)</p>
    {% if result.feedback %}
    <ul>{% for tip in result.feedback %}<li>{{ tip }}</li>{% endfor %}</ul>
    {% endif %}

    {% if breach.error %}
      <p>{{ breach.error }}</p>
    {% elif breach.breached %}
      <p class="warn">Ye password {{ "{:,}".format(breach.count) }} baar leak ho chuka hai!</p>
    {% else %}
      <p class="ok">Known breaches mein nahi mila.</p>
    {% endif %}
  </div>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = breach = None
    if request.method == "POST":
        pwd = request.form.get("password", "")
        result = check_password(pwd)
        breach = check_breach(pwd)
    return render_template_string(PAGE, result=result, breach=breach)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)