# Project Goal:

The goal of this project is to create a data harvest python program that is configurable and viewable through
an external website to specifically apply execution settings for the data harvest python program, and be able
to view what recently happened on the current trading session for the day for events. The second top level goal
for this project is to execute trades in reaction to this financial data through the MetaTrader terminal using the
language for that terminal.

## Setup
1. Install all the listed required python modules from requirements.txt
Please email Matthew James [matthew@klump-pdx.com](mailto:matthew@klump-pdx.com) for instructions on how to setup database using the django
administration tool if you are a subscriber our paid target website we are using.
2. If java virtual machine (JVM) is not preinstalled on your computer, then go to [this web site](https://java.com/) to download and install the java virtual machine - the installer should set the java environment variable for your computer. If not, you may email me for my path environment variable setup to run the java JVM.
3. Go to [this web site](https://github.com/SeleniumHQ/htmlunit-driver/releases/download/2.21/htmlunit-driver-standalone-2.21.jar), and specifically download the file htmlunit-driver-standalone-2.21.jar that is this version 2.21. Also there is available [this web page](https://github.com/SeleniumHQ/htmlunit-driver/releases) if there is a higher released version of this file, but you'll need to change pstart_loc_server.py line 28 to match.
4. Go to [this web site](http://goo.gl/EoH85x), and specifically download the file selenium-server-standalone-2.53.1.jar that is version 2.53.1. Also there is available [this web page](http://docs.seleniumhq.org/download/) if there is a higher released version of this file, but you'll need to change pstart_loc_server.py line 29 to match.
5. Take the files htmlunit-driver-standalone-2.21.jar and also selenium-server-standalone-2.53.1.jar, and place them into finalproject_fxalarm project folder both as sibling files next to the manage.py file.
6. Additionally, we are using an installed python x86 version 3.51 or higher with the python pip-installed packages listed in the requirements.txt file to run this release.

## Usage
After setup, execute django server within your virtual environment, navigate to the fist page, click the top bar
button to proceed to the live streamline viewer page, observer ideal live streaming data by first pressing the "Start Main Data Gathering Execution" button, and lastly always click the
button labeled "Stop Main Data Gathering Execution" to release the data gathering resources before pressing the start gathering button a second time if you wish to collect more raw USD
daily session price acceleration data. Updates are in the works to automatically release the gathering resources if the event viewer page becomes refreshed.

## Specific Functionality

### USD Main Page
This page will shows you are about to view live steaming data for the USD dollar group which are the EUR/USD,
GBP/USD, USD/CAD, USD/JPY, USD/CHF, AUD/USD, and NZD/USD.
There will be show an image of the MetaTrader Engine as a back group, and a single button control to proceed to
the event viewer log web page.

### Event Viewer Log Page
This page will show live streaming data updated each minute from our subscription website for the USD group mentioned
on the prior page.

### Middle Tier Logic Data Parse
There is a required logic module that must correctly receive the USD data with testing as stated on the Main page.
Please see the [design document link](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf) for the specific plan of creating this module.

1. Simulate the actual data source as if it was reading the body of the html document right off a request object network resource connection.
2. Perform and actually do the true html file download from a secure login session for true daily USD session acceleration data.

### Data Model
* Secure string for my credentials to auto login to the subscription website
* String for the subscription website that is the target of receiving data from,
* A float value immediately read in, and every 15 minutes, for the USD 7 pairs of the EUR/USD, GBP/USD, USD/CAD, USD/JPY,
USD/CHF, AUD/USD, and the NZD/USD.
* Lastly a time stamp for when the last data values for the US Dollar was saved.

## Technical Components
* The front-end HTML will be generated using Django templates with fixed CSS layout style, JavaScript, and JQuerry.
* The middle tier logic will be done using Python and the [Beautiful Soup XML/HTML python module](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse HTML either well-formed or
malformed bad HTML. Please see the [design document link](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf) for the specific plan of creating this module.
* The back-end data model will be completed through using Django's Query Set/LINQ expression style query functions API to the
database.

## Schedule
Please see the [schedule document link](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FXAlarm_Timeline_Proposal.pdf) or below for the specific delivery schedule for this project.

## Further Work
* Expand the user interface to reflect a configurable UI as stated in the [design document link](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf) below for module details.
* Add Expanded View for the Event Log Viewer web page to accommodate 8 currencies and 28 currency pairs
* Add Trade module configuration web page
* Add Trade Execution Engine using C++ API calls through MQL4 script for Meta Trader 4 Terminal program.
* Add Email notification module for trades executed or significant threshold events.

##The following languages and software technologies will be used:
* Python
* HTML5
* CSS3
* JavaScript calls through JQuery
* Django front-end back-end kit
* C++ API calls through MQL4 script

#####[Link for details to each major component to follow via visual design documents.](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf)

#####[Link for project schedule using .mpp MS Office Project document.](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FXAlarm_Timeline_Proposal.pdf)

#####[Link for each module details, project setup, maintenance, and execution verification testing.](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf)