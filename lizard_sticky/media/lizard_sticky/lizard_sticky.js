// javascript for lizard_sticky
// popup_click_handler

var pointLayer = new OpenLayers.Layer.Vector("Point Layer");
var pointController = new OpenLayers.Control.DrawFeature(
    pointLayer,
    OpenLayers.Handler.Point);

function sticky_popup_click_handler(x, y, map) {
    // get checked radiobutton
    var checked_button = $("form#sticky input:radio:checked");
    if (checked_button.attr("value") == "add_sticky") {
        // alert("add sticky!");
        // pointController.click = function() {alert("click!");}
        alert("click!");
    } else {
        return popup_click_handler(x, y, map);
    }
}

function save_sticky() {
    // there is always max 1 sticky popup
    pointController.deactivate();
    pointController.finalize();
    pointController.destroyFeature();
    var sticky_form = $("form#new-sticky");
    $.post(
        url,
        {x: x, y: y, reporter: reporter, title: title, description: description, tags: tags},
        function (data) {
            // todo: refresh layers
        }
    );
}

function sticky_navigate() {
    // pointController.deactivate();
}

function sticky_add() {

    // map.addLayer(pointLayer);
    // map.addControl(pointController);

    // pointController.activate();
}

function init_sticky() {
    $("#sticky_navigate").click(sticky_navigate());
    $("#sticky_add").click(sticky_add());
}

$(document).ready(init_sticky);
