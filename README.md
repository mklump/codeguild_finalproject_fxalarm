#Project Goal:

The goal of this project is to create a data harvest python program that is configurable and viewable through
an external website to specifically apply execution settings for the data harvest python program, and be able
to view what recently happened on the current trading session for the day for events. The second top level goal
for this project is to execute trades in reaction to this financial data through the MetaTrader terminal using the
language for that terminal.

## Specific Functionality

### USD Main Page
This page will shows you are about to view live steaming data for the USD dollar group which are the EUR/USD,
GBP/USD, USD/CAD, USD/JPY, USD/CHF, AUD/USD, and NZD/USD.
There will be show an image of the MetaTrader Engine as a backgroup, and a single button control to proceed to
the event viewer log webpage.

### Event Viewer Log Page
This page will show live streaming data updated each minute from our subscription website for the USD group mentioned
on the prior page.

### Middle Tier Logic Data Parse
There is a required logic module that must correctly receive the USD data with testing as stated on the Main page.
Please see the [design document link](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf) for the specific plan of creating this module.

1. Simulate the actual data source as if it was reading the body of the html document right off a request object network resource connection.
2. Perform and actually do the true html file dowload from a secure login session for true USD session acceleration data.

### Data Model
* Secure string for my credentials to auto login to the subscription website
* String for the subscription website that is the target of receiving data from,
* A float value immediately read in, and every 15 mininutes, for the USD 7 pairs of the the EUR/USD, GBP/USD, USD/CAD, USD/JPY,
USD/CHF, AUD/USD, and the NZD/USD.
* Lastly a time stamp for when the last data values for the US Dollar was saved.

## Technical Components
* The front-end HTML will be generated using Django templates with fixed CSS layout style, JavaScript, and JQuerry.
* The middle tier logic will be done using Python and Xml Style Sheel Transform to parse HTML either well-formed or
malformed bad HTML. Please see the [design document link](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf) for the specific plan of creating this module.
* The back-end data model will be completed through using Django's LINQ expression style query functions API to the
database.

## Schedule
Please see the [schedule document link](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FXAlarm_Timeline_Proposal.pdf) or below for the specific delivery schedule for this project.

## Further Work
* Expand the user interface to reflect a configurable UI as stated in the [design document link](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf) below for module details.
* Add Expanded View for the Event Log Viewer webpage to accomodate 8 currencies and 28 currency pairs
* Add Trade module configuration webpage
* Add Trade Execution Engine using C++ API calls through MQL4 script for Meta Trader 4 Terminal program.
* Add Email notificaition module for trades executed or significant theshold events.

##The following languages and software technologies will be used:
* Python
* HTML5
* CSS3
* JavaScript calls through JQuery
* Django frontend backend kit
* C++ API calls through MQL4 script

#####[Link for details to each major component to follow via visual design documents.](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf)

#####[Link for project schedule using .mpp MS Office Project document.](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FXAlarm_Timeline_Proposal.pdf)

#####[Link for each module details, project setup, maintenance, and execution verification testing.](https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Project%20Scope.pdf)