/*
Python Coding Bootcamp (pdxcodeguild)
Code File for static/finalproject_fxalarm/scripts/fxalarm_site.js
by: Matthew James K on 5/16/2016
*/
'use strict';

/*
 * This function provides the initial selected and hidden detail items within the
 * select item controls.
 * The summary select list will show the first item selected, and the details list
 * will show the first details item visible, and the remaining item details items
 * will be hidden.
 */
function initializeSelectControls() {
    $('select.view_select_summary > option')[0].selected = true;
    $('select.view_item_detail > option')[0].hidden = false;
    $('select.view_item_detail > option')[0].selected = true;
    var itemDetails = $('select.view_item_detail > option');
    for (var detail = 1; detail < itemDetails.length; detail++) {
        itemDetails[detail].hidden = true;
    }
    $('select.view_select_summary').css('height', parseInt($('select.view_select_summary option').length) * 17.5);
    $('select.view_item_detail').css('height', 17.5);
}

/*
 * This function accepts the option selection summary that was clicked on, and then shows
 * the associated option selection details of that summary that was clicked on.
 * @param {<option></option>} [clickedSummary] that received the left click event
 */
function showDetailsBySummarySelection(clickedSummary) {
    var details = $('select.view_item_detail > option');
    for (var item = 0; item < details.length; item++) {
        details[item].selected = false;
    }
    for (var item = 0; item < details.length; item++) {
        if (clickedSummary.selected === true) {
            details[clickedSummary.index].hidden = false;
            details[clickedSummary.index].selected = true;
        } else {
            details[clickedSummary.index].hidden = true;
            details[clickedSummary.index].selected = false;
        }
    }
    changedDetailsViewHeight();
}

/*
 * This function accepts the details view structure select option list, and changes the height
 * of that html control based on the number of detail options that have been revealed.
 */
function changedDetailsViewHeight() {
    var details = $('select.view_item_detail > option');
    var changedHeight = 0;
    for (var item = 0; item < details.length; item++) {
        if (false == details[item].hidden)
            changedHeight++;
    }
    $('select.view_item_detail').css('height', parseInt(changedHeight) * 17.5);
}

/*
 * This function registers the click event handler of the summary select item option list
 * to reveal the details.
 */
function registerSelectOptionClick() {
    $('select.view_select_summary > option').on('click', function (event) {
        showDetailsBySummarySelection(event.target);
    });
}

/*
 * This function registers the click event handler of the VIEW ALL button that selects all
 * of the USD summaries in the summary select list, and also displays all of the USD detail instances
 * in the USD details select item list all at once.
 */
function registerViewAllBtnClick() {
    // Selector jquery select the VIEW ALL button by its assigned control type and style classes:
    $('input.eventlogviewall.eventloglabel').on('click', function () {
        var summaries = $('select.view_select_summary > option');
        var details = $('select.view_item_detail > option');
        for (var x = 0; x < summaries.length; x++) {
            summaries[x].selected = true;
            details[x].hidden = false;
            details[x].selected = true;
        }
        changedDetailsViewHeight();
    });
}

/*
 * This function registers all the required user input interaction events for the page of
 * fxalarm_usd_index.html, and also the page of fxalarm_event_log.html.
 */
function registerGlobalEventHandlers() {
    registerSelectOptionClick();
    registerViewAllBtnClick();
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