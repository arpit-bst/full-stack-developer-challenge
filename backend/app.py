from flask import Flask, render_template, redirect, url_for, flash, jsonify
from google.cloud import datastore
import random
import subprocess

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Datastore client
client = datastore.Client()

# Helper Functions
def get_all_apps():
    """Fetch all apps from the Datastore under the 'top_new_apps_1' kind."""
    query = client.query(kind="top_new_apps_1")
    results = list(query.fetch())
    random.shuffle(results)
    return [
        {
            "app_name": app.get("app_name", "N/A"),
            "app_ratings": app.get("app_ratings", "N/A"),
            "app_package": app.get("app_package", ""),
            "app_img": app.get("app_img", ""),
        }
        for app in results
    ]


def get_app_by_package_name(package_name):
    """Fetch a specific app by its package name."""
    query = client.query(kind="top_new_apps_1")
    query.add_filter("app_package", "=", package_name)
    apps = list(query.fetch())
    if apps:
        return apps[0]
    return None


@app.route('/')
def index():
    """Route to render the index page with all apps."""
    apps = get_all_apps()
    return render_template('index.html', apps=apps)


@app.route('/trigger-scraper', methods=['POST'])
def trigger_scraper():
    """Route to run scraper.py and monitor its progress."""
    try:
        # Run scraper.py in a blocking way and return when complete
        subprocess.run([
            r'C:\Users\arpit\Bluestacks\android_app_browser\env\Scripts\python.exe',
            r'C:\Users\arpit\Bluestacks\android_app_browser\backend\scraper.py'
        ], check=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/app/<string:package_name>')
def app_detail(package_name):
    """Route to display app details."""
    app = get_app_by_package_name(package_name)
    if not app:
        flash('App not found!', 'danger')
        return redirect(url_for('index'))
    return render_template('app_detail.html', app=app)


if __name__ == '__main__':
    app.run(debug=True)
