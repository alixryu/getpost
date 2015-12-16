var DEFAULTS = {};

function stripForm() {
  $('#editform :input').not(':input[type="submit"]').each(
    function(_, e) {
      element = $(e);
      if (element.val() == DEFAULTS[element.attr('name')]) {
        element.remove();
      }
    }
  );
}

function formSubmit(event) {
  stripForm();
}

function populateDefaults() {
  $('#editform :input').not(':input[type="submit"]').each(
    function(_, e) {
      element = $(e);
      DEFAULTS[element.attr('name')] = element.val();
    }
  );
}

function onReady() {
  populateDefaults();
  $('#editform').submit(formSubmit);
}

$(document).ready(onReady);
