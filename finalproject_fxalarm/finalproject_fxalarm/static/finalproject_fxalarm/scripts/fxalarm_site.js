/*
Python Coding Bootcamp (pdxcodeguild)
Code File for static/finalproject_fxalarm/scripts/fxalarm_site.js
by: Matthew James K on 5/16/2016
*/
'use strict'

function getUSDSummaryCollection() {
  var summary = '{{ usd_summary }}'.replace(/&quot;/g,"\"");
  return summary;
}

function getUSDDetailCollection() {

}

function registerSelectOptionClick() {
  var select_summary = $('#view_select_summary > option').on('click', function() {

  });
}

/*
 * This function registers all the required user input interaction events for the page of
 * fxalarm_usd_index.html, and also the page of fxalarm_event_log.html.
 */
function registerGlobalEventHandlers() {
  registerSelectOptionClick();
}

/*
 * This is the main entry point for this file.
 */
function main() {
  registerGlobalEventHandlers();
  getUSDSummaryCollection();
}

/*
 * This statement registers main() to be called when the associated page is 'ready'.
 */
$(document).ready(main);