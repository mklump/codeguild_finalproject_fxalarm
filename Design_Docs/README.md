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

### Data Model
* Secure string for my credentials to auto login to the subscription website
* String for the subscription website that is the target of receiving data from,
* The USD group flag enabled on 7 pairs to receive data from the Middle Tier Logic Data Parser.
* The last and most immediate float value read for the USD 7 pairs of the the EUR/USD, GBP/USD, USD/CAD, USD/JPY,
USD/CHF, AUD/USD, and NZD/USD

##The following languages and software technologies will be used:
* Python
* HTML5
* CSS3
* JavaScript calls through JQuery
* Django frontend backend kit
* C++ API calls through MQL4 script

#####Link for details to each major component to follow via visual design documents.
https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FXAlarm_Module_Layout.pdf

#####Link for project schedule using .mpp MS Office Project document.
https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FXAlarm_Timeline_Proposal.pdf

#####Link for each module details, project setup, maintenance, and execution verification testing.
https://github.com/mklump/codeguild_finalproject_fxalarm/blob/master/Design_Docs/FX%20Alarm%20Final%20Project%20Proposal%20same%20doc%201158pm.pdf