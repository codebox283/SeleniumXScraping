from flask import Flask, render_template_string
import scrape_twitter  # Import the scraping module

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <h1>Twitter Trends Scraper</h1>
    <button onclick="location.href='/run-script'">Click here to run the script</button>
    ''')

@app.route('/run-script')
def run_script():
    record = scrape_twitter.scrape_trending_topics()  # Call the scraping function
    
    return render_template_string(f'''
    <h2>These are the most happening topics as of {record['timestamp']}</h2>
    <ul>
      <li>{record['trends'][0]}</li>
      <li>{record['trends'][1]}</li>
      <li>{record['trends'][2]}</li>
      <li>{record['trends'][3]}</li>
      <li>{record['trends'][4]}</li>
    </ul>
    <p>The IP address used for this query was {record['ip_address']}.</p>
    <h3>Here’s a JSON extract of this record from the MongoDB:</h3>
    <pre>{record}</pre>
    <button onclick="location.href='/'">Click here to run the query again</button>
    ''')

if __name__ == "__main__":
    app.run(debug=True)
