/*
Python Coding Bootcamp (pdxcodeguild)
Code File for static/finalproject_fxalarm/scripts/fxalarm_site.js
by: Matthew James K on 5/16/2016
*/
'use strict'

/*
 * This function provides the initial selected and hidden detail items within the select item controls.
 * The summary select list will show the first item selected, and the details list will show the first
 * details item visible, and the remaining item details items will be hidden.
 */
function initializeSelectControls() {
  $('select.view_select_summary > option')[0].selected = true;
  $('select.view_item_detail > option')[0].hidden = false;
  $('select.view_item_detail > option')[0].selected = true;
  var item_detail_collection = $('select.view_item_detail > option');
  for (var detail = 1; detail < item_detail_collection.length; detail++) {
    item_detail_collection[detail].hidden = true;
  }
}

/*
 * This function accepts the option selection summary that was clicked on, and then shows the associated
 * option selection details of that summary that was clicked on.
 * @param {<option></option>} [clickedSummary] that received the left click event
 */
function showDetailsBySummarySelection(clickedSummary) {
  var details = $('select.view_item_detail > option');
  for (var item in details) {
    if (clickedSummary.index === item.index) {
      item.hidden = false;
      item.selected = true;
    } else {
      item.hidden = true;
      item.selected = false;
    }
  }
}

/*
 * This function registers the click event of the summary select item option list to reveal the details.
 */
function registerSelectOptionClick() {
  $('select.view_select_summary > option').on('click', function (event) {
    showDetailsBySummarySelection(event.target);
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
  initializeSelectControls();
}

/*
 * This statement registers main() to be called when the associated page is 'ready'.
 */
$(document).ready(main);