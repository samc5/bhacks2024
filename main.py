# Flask app with one endpoint
from flask import Flask, jsonify, request, render_template
import tester

app = Flask(__name__)



@app.route("/")
def main():
    prompt = """Via Metaculus, Kamala Harris currently has a 52% chance of winning and Donald Trump has a 45% chance of winning. With the results in NE-02, the odds of a tie have increased to around 3%.
    Donald Trump has been holding an election night rally all night in North Carolina, via AP. He has been leading in the state, but early returns have not distinguished a front runner, says the NYT Needle, which puts NC at 60% for Trump.
    """
    live_summary = tester.get_ai_summary(prompt)

    return render_template("main.html", live_summary=live_summary[0]["response"]["response"])


    
if __name__ == "__main__":
    app.debug = True
    app.run()
