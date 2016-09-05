# VolunteerHub
A hub to display data from different sources about volunteers on hasadna

This project creates a hub to centralize data about volunteers from:
  1. Google Forms
  2. Gmail conversations

and to display this data, grouped by user, in a convenient way.

gathering data from the different data sources happens in the etl.py

DESIGN
--------------------------------------------------------------------------------
The etl.py module has an abstract Connector class.
this is the base class for all datasources.

For each datasource there is an authentication phase, where login credentials
are used to connect to it. Hence the get Credentials method

and there is a data gathering phase, hence the getData method

Each connector implemets these methods as suitable for the datasource,
and there is a common way to work with all connectors

INSTALLATION:
--------------------------------------------------------------------------------
This project is built and tested with 
  python 2.7.12 
  Ubuntu 16.04 x64 bit
To install the python packages, run the install.sh file on the main directory

In order to run this project properly, you would have to go to the 
API documentation pages, and follow the steps there to:
  Create a project in the Google Developers Console and turn on the API for it
  Create OAuth client ID credentials
  Download the credentials file
  Move it to the project direcrory and name it client_secret.json

the credentials file is per gmail account, and is excluded from the git
repository for security reasons.

DOCUMENTATION:
--------------------------------------------------------------------------------
sheets API documentation
https://developers.google.com/sheets/quickstart/python

Gmail API documentation
https://developers.google.com/gmail/api/quickstart/python
