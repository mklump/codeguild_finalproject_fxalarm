/*
Python Coding Bootcamp (pdxcodeguild)
Code File for static/finalproject_fxalarm/scripts/fxalarm_site.js
by: Matthew James K on 5/16/2016
*/
'use strict'

/*
 * This function returns the usd_summary list of strings for processing.
 * @returns {Array} Of strings that is the usd_summary of each data capture snapshot.
 */
function getUSDSummaryCollection() {
  var summary = $('[name=\'usd_summary\']');
  return summary[0].value;
}

/*
 * This function returns the usd_summary list of strings for processing.
 * @returns {Array} Of strings that is the usd_detail of each data capture snapshot.
 */
function getUSDDetailCollection() {
  var detail = $('[name=\'usd_detail\']');
  return detail[0].value;
}

/*
 * This function registers the click event of the summary select item option list to reveal the details.
 */
function registerSelectOptionClick() {
  $('#view_select_summary > option').on('click', function(event) {
    var capture_summaries = getUSDSummaryCollection(); // Outputs "['This', 'inner', 'list']", and requires Array.from(arrayLike[, mapFn[, thisArg]])
    var count = 0;
    for (var line in capture_summaries) {
      if (line === event.target.value)
        break;
      else
        count++;
    }
    var summary;
    for (summary = 0; summary < capture_summaries.length; summary++) {
      if (capture_summaries[summary] === event.target.value)
        break;
    }
    $('#view_item_detail').innerHTML = '';
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
}

/*
 * This statement registers main() to be called when the associated page is 'ready'.
 */
$(document).ready(main);