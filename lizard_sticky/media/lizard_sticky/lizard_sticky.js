// javascript for lizard_sticky
// popup_click_handler


function sticky_popup_click_handler(x, y, map) {
    // get checked radiobutton
    var checked_button = $("form#sticky input:radio:checked");
    if (checked_button.attr("value") !== "add_sticky") {
        return popup_click_handler(x, y, map);
    }
    // else: handled by pointController
}

function save_sticky() {
    var url, x, y, reporter, title, description, tags, sticky_popup, old_feats, errors;
    // there is always max 1 sticky popup
    url = $("#sticky").attr("data-url-lizard-sticky-add");
    sticky_popup = $("form#add-sticky");
    reporter = sticky_popup.find("input#sticky-reporter").attr("value");
    title = sticky_popup.find("input#sticky-title").attr("value");
    description = sticky_popup.find("input#sticky-description").attr("value");
    tags = sticky_popup.find("input#sticky-tags").attr("value");
    x = sticky_popup.find("input#sticky-x").attr("value");
    y = sticky_popup.find("input#sticky-y").attr("value");
    errors = 0;
    sticky_popup.find("label").removeClass("alert");  // remove all previous errors
    if (reporter == '') {
        sticky_popup.find("label#reporter").addClass("alert");
        errors += 1;
    }
    if (title == '') {
        sticky_popup.find("label#title").addClass("alert");
        errors += 1;
    }
    if (description == '') {
        sticky_popup.find("label#description").addClass("alert");
        errors += 1;
    }
    if (errors == 0) {
        $.post(
            url,
            {x: x, y: y, reporter: reporter, title: title, description: description, tags: tags},
            function (data) {
                // destroy existing popups and features
                $("#sticky-popup").remove();
                old_feats = pointLayer.features;
                pointLayer.removeFeatures(old_feats);
                pointLayer.destroyFeatures(old_feats);
                // update all layers
                updateLayers(); 
                // TODO: update left menu
                //$("#sticky-browser-list").load("./ .sticky-browser-item");
                //setUpTree();
                // jump back to navigation mode
                $("form#sticky input:radio#sticky_navigate").click();
            }
        );
    }
}

function sticky_navigate() {
    pointController.deactivate();
}

function sticky_add() {
    pointController.activate();
}

function sticky_add_handler(event) {
    // TODO: django form??
    var old_feats, num_to_delete, popup, html, url, x, y;
    // destroy existing popups
    $("#sticky-popup").remove();
    // destroy "old" features, as a result there is always only 1 feature left.
    old_feats = [];
    num_to_delete = pointLayer.features.length-1;
    for (i=0; i<num_to_delete;i=i+1)
    {
        old_feats[i] = pointLayer.features[i];
    }
    pointLayer.removeFeatures(old_feats);
    pointLayer.destroyFeatures(old_feats);

    // prepare popup
    url = $("#sticky").attr("data-url-lizard-sticky-add");
    feature = pointLayer.features[0]
    x = feature.geometry.x;
    y = feature.geometry.y;

    // show popup
    html = 
        '<strong>Nieuw geeltje</strong>' +
        '<form id="add-sticky" style="background-color: lightyellow;" action="' + url + '" method="post">' +
        '<ol class="forms">' +
        '<li><label for="reporter" id="reporter">Naam</label><input id="sticky-reporter" type="text" name="reporter" /></li>' + 
        '<li><label for="title" id="title">Onderwerp</label><input id="sticky-title" type="text" name="title" /></li>' + 
        '<li><label for="description" id="description">Beschrijving</label><input id="sticky-description" type="text" name="description"/></li>' + 
        '<li><label for="tags">Tags</label><input id="sticky-tags" type="text" name="tags" /></li>' + 
        '<button id="submit-sticky" type="button">Sla op</button>' +
        '</ol>' +
        '<input id="sticky-x" type="hidden" name="x" value="' + x + '" />' +
        '<input id="sticky-y" type="hidden" name="y" value="' + y + '" />' +
        '</form>';
    popup = new OpenLayers.Popup("sticky-popup",
                                 new OpenLayers.LonLat(feature.geometry.x, feature.geometry.y),
                                 new OpenLayers.Size(400,310),
                                 html,
                                 true);
    map.addPopup(popup);
    $("#submit-sticky").bind("click", save_sticky);
    // make sure that when the window is closed, the object is removed as well
    $(".olPopupCloseBox").bind("click", function () {
        $(this).parent().parent().remove();
    });                          
}

function init_sticky() {
    pointLayer = new OpenLayers.Layer.Vector("Point Layer");
    pointController = new OpenLayers.Control.DrawFeature(
        pointLayer,
        OpenLayers.Handler.Point);
    pointLayer.events.on({"featureadded" : sticky_add_handler});

    map.addLayer(pointLayer);
    map.addControl(pointController);

    $("#sticky_navigate").bind("click", sticky_navigate);
    $("#sticky_add").bind("click", sticky_add);
    $("form#sticky input:radio#sticky_navigate").click()
}

$(document).ready(init_sticky);
