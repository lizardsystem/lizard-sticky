// jslint configuration; btw: don't put a space before 'jslint' below.
/*jslint browser: true */
/*global $, OpenLayers, window, popup_click_handler, updateLayers, map */

var pointLayer, pointController;


function sticky_popup_click_handler(x, y, map) {
    var checked_button;
    // get checked radiobutton
    checked_button = $("form#sticky input:radio:checked");
    if (checked_button.attr("value") !== "add_sticky") {
        return popup_click_handler(x, y, map);
    }
    // else: handled by pointController
}

function save_sticky() {
    var url, x, y, reporter, title, description, tags, sticky_popup, old_feats, errors;

    // There is always max 1 sticky popup.
    url = $("#sticky").attr("data-url-lizard-sticky-add");
    sticky_popup = $("#add-sticky");

    // Check form for errors.
    reporter = sticky_popup.find("#sticky-reporter").attr("value");
    title = sticky_popup.find("#sticky-title").attr("value");
    description = sticky_popup.find("#sticky-description").attr("value");
    tags = sticky_popup.find("#sticky-tags").attr("value");
    x = sticky_popup.find("#sticky-x").attr("value");
    y = sticky_popup.find("#sticky-y").attr("value");
    errors = 0;
    sticky_popup.find("label").removeClass("alert");  // remove all previous errors
    if (reporter === '') {
        sticky_popup.find("label#reporter").addClass("alert");
        errors += 1;
    }
    if (title === '') {
        sticky_popup.find("label#title").addClass("alert");
        errors += 1;
    }
    if (description === '') {
        sticky_popup.find("label#description").addClass("alert");
        errors += 1;
    }

    // Post the sticky.
    if (errors === 0) {
        $.post(
            url,
            {x: x, y: y, reporter: reporter, title: title, description: description, tags: tags},
            function (data) {
                // destroy existing popups and features
                $("#add-sticky .close").click();

                old_feats = pointLayer.features;
                pointLayer.removeFeatures(old_feats);
                pointLayer.destroyFeatures(old_feats);
                // Update all layers.
                updateLayers();

                // TODO: update left menu
                //$("#sticky-browser-list").load("./ .sticky-browser-item");
                //setUpTree();

                // Jump back to navigation mode.
                $("form#sticky input:radio#sticky_navigate").click();
            }
        );
    }

    // Do not reload page.
    return false;
}

function sticky_navigate() {
    pointController.deactivate();
}

function sticky_add() {
    pointController.activate();
}

function sticky_add_handler(event) {
    var old_feats, num_to_delete, overlay, i, x, y, feature;

    // Destroy "old" features, as a result there is always only 1 feature left.
    old_feats = [];
    num_to_delete = pointLayer.features.length - 1;
    for (i = 0; i < num_to_delete; i = i + 1)
    {
        old_feats[i] = pointLayer.features[i];
    }
    pointLayer.removeFeatures(old_feats);
    pointLayer.destroyFeatures(old_feats);

    // Prepare popup.
    feature = pointLayer.features[0];
    x = feature.geometry.x;
    y = feature.geometry.y;
    $("#sticky-x").attr("value", x);
    $("#sticky-y").attr("value", y);

    // Popup.
    overlay = $("#add-sticky").overlay();
    overlay.load();
}

function init_sticky() {
    // Navigation or new sticky.
    pointLayer = new OpenLayers.Layer.Vector("Point Layer");
    pointController = new OpenLayers.Control.DrawFeature(
        pointLayer,
        OpenLayers.Handler.Point);
    pointLayer.events.on({"featureadded" : sticky_add_handler});

    map.addLayer(pointLayer);
    map.addControl(pointController);

    $("#sticky_navigate").bind("click", sticky_navigate);
    $("#sticky_add").bind("click", sticky_add);
    $("form#sticky input:radio#sticky_navigate").click();

    // Bind submit to js function
    $("#add-sticky").submit(save_sticky);
    $("#add-sticky").overlay({});

}

$(document).ready(init_sticky);
