# Slack-Windows-Upgrade


Running `pip install -r requirements.txt` in a new Python environment will download the latest compatible versions of those packages along with their dependencies


Here’s the clean, no-drama way to build a Lambda Layer that contains your Python packages:
`mkdir -p slack_layer/python`
`pip install --upgrade pip`
`pip install -r requirements.txt -t slack_layer/python`

Then zip the python directory
`cd slack_layer`
`zip -r ../slack_layer.zip python`
`cd ..`

You should end up with `slack_layer.zip` whose root contains the python/ folder.
