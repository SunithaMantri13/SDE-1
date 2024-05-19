from flask import Flask, request, jsonify, render_template_string
import logging
import json
from datetime import datetime, timezone

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
debug_logger = logging.getLogger('debug_logger')
debug_logger.setLevel(logging.DEBUG)
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)
warning_logger = logging.getLogger('warning_logger')
warning_logger.setLevel(logging.WARNING)

# Create file handlers
debug_handler = logging.FileHandler('debug.log')
debug_handler.setLevel(logging.DEBUG)
error_handler = logging.FileHandler('error.log')
error_handler.setLevel(logging.ERROR)
info_handler = logging.FileHandler('info.log')
info_handler.setLevel(logging.INFO)
warning_handler = logging.FileHandler('warning.log')
warning_handler.setLevel(logging.WARNING)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
debug_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
info_handler.setFormatter(formatter)
warning_handler.setFormatter(formatter)

# Add handlers to loggers
debug_logger.addHandler(debug_handler)
error_logger.addHandler(error_handler)
info_logger.addHandler(info_handler)
warning_logger.addHandler(warning_handler)

@app.route('/')
def search_logs():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Search Logs</title>
            <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
        </head>
        <body>
            <h1>Search Logs</h1>
            <form action="/search" method="post">
                <label for="level">Log Level:</label>
                <select name="level" id="level">
                    <option value="">Any</option>
                    <option value="DEBUG">Debug</option>
                    <option value="INFO">Info</option>
                    <option value="WARNING">Warning</option>
                    <option value="ERROR">Error</option>
                </select><br><br>
                
                <label for="start_time">Start Time:</label>
                <input type="datetime-local" id="start_time" name="start_time"><br><br>
                
                <label for="end_time">End Time:</label>
                <input type="datetime-local" id="end_time" name="end_time"><br><br>
                
                <label for="source">Source:</label>
                <input type="text" id="source" name="source"><br><br>
                
                <input type="submit" value="Search">
            </form>
        </body>
        </html>
    ''')


@app.route('/search', methods=['POST'])
def search():
    level = request.form.get('level')
    start_time_str = request.form.get('start_time')
    end_time_str = request.form.get('end_time')
    source = request.form.get('source')

    # Convert start_time and end_time to datetime objects with UTC timezone
    start_time = datetime.fromisoformat(start_time_str).replace(tzinfo=timezone.utc) if start_time_str else None
    end_time = datetime.fromisoformat(end_time_str).replace(tzinfo=timezone.utc) if end_time_str else None

    results = []
    log_files = ["debug.log", "error.log", "info.log", "warning.log"]
    for log_file in log_files:
        with open(log_file, 'r') as file:
            for line in file:
                try:
                    log_entry = json.loads(line.split(' - ')[-1])
                    log_timestamp = datetime.fromisoformat(log_entry['timestamp'].replace('Z', '+00:00'))
                    if (
                        (not level or log_entry['level'].upper() == level.upper()) and
                        (not start_time or log_timestamp >= start_time) and
                        (not end_time or log_timestamp <= end_time) and
                        (not source or log_entry['metadata']['source'] == source)
                    ):
                        results.append(log_entry)
                except (json.JSONDecodeError, KeyError):
                    continue
    
    return jsonify(results)

# Log API endpoint to ingest logs
@app.route('/get-logs', methods=['POST'])
def get_log():
    data = request.get_json()
    log_message = {
        "level": data['log'],
        "log_string": data['string'],
        "timestamp": datetime.utcnow().isoformat() + 'Z',
        "metadata": {
            "source": data['source']
        }
    }
    if data['log'] == "debug":
         debug_logger.debug(json.dumps(log_message))
    elif data['log'] == "error":
         error_logger.error(json.dumps(log_message))
    elif data['log'] == "warning":
         warning_logger.warning(json.dumps(log_message))
    else:
         info_logger.info(json.dumps(log_message))
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)


