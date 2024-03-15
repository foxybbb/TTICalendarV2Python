

# TTI Calendar v2 



## Installing

A step-by-step series of examples that tell you how to get a development environment running.
Setting up a Virtual Environment
1. Open your terminal and navigate to the project directory. 
2. Create a virtual environment by running:
```python
python3 -m venv venv
```

3. Activate the virtual environment:
- On Windows:

```
.\venv\Scripts\activate
```
- On Unix or MacOS:

```bash
source venv/bin/activate
```
        

Installing Required Packages

Install all the required packages using the requirements.txt file:

```bash 
pip install -r requirements.txt
```

## Google Calendar API Setup
*** Information copied from https://developers.google.com/calendar/api/quickstart/python

To use the Google Calendar API, you'll need to enable the API and obtain the necessary credentials. Follow these steps:

### Enable the API
Before using Google APIs, you need to turn them on in a Google Cloud project. You can turn on one or more APIs in a single Google Cloud project.

- In the Google Cloud console, enable the Google Calendar API.  https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com

### Configure the OAuth 

If you're using a new Google Cloud project to complete this quickstart, configure the OAuth consent screen and add yourself as a test user. If you've already completed this step for your Cloud project, skip to the next section.

In the Google Cloud console, go to Menu menu > APIs & Services > OAuth consent screen.

1. Go to OAuth consent screen \
    https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com
2. For User type select Internal, then click Create.
3. Complete the app registration form, then click Save and Continue.

4. For now, you can skip adding scopes and click Save and Continue. In the future, when you create an app for use outside of your Google Workspace organization, you must change the User type to External, and then, add the authorization scopes that your app requires.
5. Review your app registration summary. To make changes, click Edit. If the app registration looks OK, click Back to Dashboard.

** In the latest version of the API, add your email as, tester email, to access calendars.

### Authorize credentials for a desktop application
To authenticate end users and access user data in your app, you need to create one or more OAuth 2.0 Client IDs. A client ID is used to identify a single app to Google's OAuth servers. If your app runs on multiple platforms, you must create a separate client ID for each platform. 

1. In the Google Cloud console, go to Menu menu > APIs & Services > Credentials.

2. Go to Credentials \
   https://console.cloud.google.com/apis/credentials

3. Click Create Credentials > OAuth client ID.
4. Click Application type > Desktop app.
5. In the Name field, type a name for the credential. This name is only shown in the Google Cloud console.
6. Click Create. The OAuth client created screen appears, showing your new Client ID and Client secret.
7. Click OK. The newly created credential appears under OAuth 2.0 Client IDs.
8. Save the downloaded JSON file as `credentials.json`, and move the file to your working directory.

## Running the Project

### Setting Student data
    
Change the information about your group in the `DataPayload.py` file, also need to maintain a calendar id. 

`! It is important to create a new calendar, the programme deletes all events for the year.`

After setting up the environment and the API, you can run the project:

```bash
python main.py
```
## License

This project is licensed under the MIT License

See also the list of contributors who participated in this project.
License

