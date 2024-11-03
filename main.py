# Flask app with one endpoint
from flask import Flask, jsonify, request, render_template
import tester
import feedparse
import mongo

app = Flask(__name__)



@app.route("/")
def main():
    prompt = """Via Metaculus, Kamala Harris currently has a 52% chance of winning and Donald Trump has a 45% chance of winning. With the results in NE-02, the odds of a tie have increased to around 3%.
    Donald Trump has been holding an election night rally all night in North Carolina, via AP. He has been leading in the state, but early returns have not distinguished a front runner, says the NYT Needle, which puts NC at 60% for Trump.
    """
    live_summary = tester.get_ai_summary(prompt)
    summary = live_summary[0]["response"]["response"]
    htmlsummary = summary.replace("\n", "<br>")
    return render_template("main.html", live_summary=htmlsummary)

@app.route('/get_updates')
def get_updates():
    # You can add logic to fetch new updates here
    
    return jsonify(feedparse.grab_feed())

@app.route('/get_votes')
def get_votes():
    print("IM WORKING")
    states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]
    
    state_mapping = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
    "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
    "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
    "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
    "WI": "Wisconsin", "WY": "Wyoming"
        }


    def get_color(value):
        if value < 0 or value > 1:
            raise ValueError("Value must be between 0 and 1.")
        blue = int(value*255)
        red = int((0.98-value)*255)
        return (red, 0, blue)
    
    def rgbToHex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(rgb[0],rgb[1],rgb[2])


    # Function to get full state name from abbreviation
    def state_name(abbreviation):
        return state_mapping.get(abbreviation, "Unknown State")
    
    result = []
    print(result)
    
    for state in states:
        blue = mongo.get_candidate_percentage("Kamala Harris", state)[0]
        
        
        color = rgbToHex(get_color(blue))
        result.append((state_name(state), color))
        
    print(f"Result: {result}")
    
    final = [{"state": state, "color": color} for state, color in result]
    print(jsonify(final))
    return jsonify(final)



    
if __name__ == "__main__":
    app.debug = True
    app.run()
