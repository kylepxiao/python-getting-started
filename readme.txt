This server is hosted on https://mysterious-earth-34330.herokuapp.com/

To test locally

1) Install Heroku and run venv python virtual environment (venv/Scripts/activate.bat)
2) run "python manage.py runserver"
3) send queries to local server

To run OCR evaluation
1) Go to gamblr_backend/server/opencv_card_detector
2) Run "python CardEvaluation.py"
3) Results are logged to console

To run strategy evaluation
1) Go to gamblr_backend/server/strategy_agent
2) Run "python evaluate_strategy.py"
3) Results are logged to results.txt

To run card counting detection
1) Go to gamblr_backend/server/strategy_agent
2) Run "python evaluate_counting_detection.py"
3) Script will train/test classifier from scratch and output to console

To run frontend app, see readme in app code