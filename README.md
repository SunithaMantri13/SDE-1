# Flask Log Search Application

This Flask application allows users to search through various log files based on specific criteria like log level, time range, and source. It also provides an API endpoint to ingest logs.


## Prerequisites

- Python 3.x
- Flask

## Installation

1.	Clone the repository:

git clone https://github.com/SunithaMantri13/SDE-1.git
cd flask-log-search

2. Install the required packages:
pip install Flask

## Usage

1. Run the Flask application:
    python app.py
    

2. Open a web browser and navigate to:
   http://127.0.0.1:5000/
    
3. Use the form on the main page to search logs by selecting the log level, specifying a time range, and/or providing a source.
Example:
Log level: Debug   
Start time: 14-05-2024 10:00
End time : 16-05-2024 12:06
Source: debug.log
Click on search
## API Endpoint

### Ingest Logs

**Endpoint:** `/get-logs`

**Method:** `POST`

**Payload:**
```json
{
    "log": "info",
    "string": "This is an info log message.",
    "source": info.log
}


RESPONSE:
{
    "status": "success"
}

Log Files
The application generates the following log files in the root directory:

debug.log
error.log
info.log
warning.log
CSS Styling
The application's CSS styles are defined in the static/styles.css file.

File Descriptions
app.py: Main application file.
static/styles.css: CSS file for styling the search form and other elements.

