var DEFAULTS = {};

function extractValue(input) {
  switch (input.attr('type')) {
    case 'checkbox':
      return input.prop('checked');
      break;
    default:
      return input.val();
  }
}

function checkForChanges() {
  result = false;
  $('#editform :input').not('[type="submit"], [type="checkbox"]').each(
    function(_, e) {
      element = $(e);
      if (extractValue(element) != DEFAULTS[element.attr('name')]) {
        result = true;
      }
    }
  );
  return result;
}

function stripForm() {
  $('#editform :input').not('[type="submit"], [type="checkbox"]').each(
    function(_, e) {
      element = $(e);
      if (extractValue(element) == DEFAULTS[element.attr('name')]) {
        element.remove();
      }
    }
  );
}

function formSubmit(event) {
  if (!checkForChanges()) {
    alert('You haven\'t submitted any changes.');
    event.preventDefault();
  } else {
    stripForm();
  }
}

function populateDefaults() {
  $('#editform :input').not(':input[type="submit"]').each(
    function(_, e) {
      element = $(e);
      DEFAULTS[element.attr('name')] = extractValue(element);
    }
  );
}

function onReady() {
  populateDefaults();
  $('#editform').submit(formSubmit);
}

$(document).ready(onReady);
