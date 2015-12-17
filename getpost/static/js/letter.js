function onRoleChange(role) {
  var hidden;
  var shown;
  switch ($('#role').val()) {
    case 'student':
      shown = ['aname', 'ocmr', 'tnum'];
      hidden = [];
      break;
    case 'employee':
    case 'admin':
      shown = [];
      hidden = ['aname', 'ocmr', 'tnum'];
      display = false;
      break;
  }
  $.each(shown, function(_, name) {
    $('#' + name).show(250).
    find('input[name="' + name + '"]').attr('disabled', false);
  });
  $.each(hidden, function(_, name) {
    $('#' + name).hide(250).
    find('input[name="' + name + '"]').attr('disabled', true);
  });
}

function validateNames(role) {
  var result = '';
  result += validateName($('#fname input[name="fname"]'), 'first', false);
  if (role === 'student') {
    result += validateName($('#aname input[name="aname"]'), 'preferred', true);
  }
  result += validateName($('#lname input[name="lname"]'), 'last', false);
  return result;
}

function validateName(name, type, empty) {
  if (name === '') {
    if (empty) {
      return '';
    } else {
      return 'Every account must have a ' + type + ' name\n';
    }
  } else {
    if (name.match(/[a-zA-Z '-]+/)) {
      return '';
    } else {
      return 'Invalid ' + type + ' name: can only contain letters, spaces, ' +
        'hyphens, and apostrophes\n';
    }
  }
}

function validateEmail() {
  var email = $('#email [name="email"]').val();
  if (email.match(/^[a-zA-Z0-9]+@oberlin.edu$/)) {
    return '';
  } else {
    if (email === '') {
      return 'An email address is required to create an account\n';
    } else if (!email.match(/^[a-zA-Z0-9]+@/)) {
      return 'Invalid email address: only letters and digits may precede the ' +
      '"@" symbol\n';
    } else if (!email.match(/@oberlin.edu$/)) {
      return 'Invalid email address: must end in "@oberlin.edu"\n';
    } else {
      return 'Invalid email address\n';
    }
  }
}

function validateTNumber(role) {
  if (role !== 'student') {
    return '';
  }
  var tnum = $('#tnum [name="tnum"]').val();
  if (tnum.match(/^T?[0-9]{8}$/)) {
    return '';
  } else {
    if (tnum === '') {
      return 'A T number is required to create a student account\n';
    } else {
      return 'Invalid T number: must contain exactly eight digits, ' +
      'optionally preceded by a capital "T"\n';
    }
  }
}

function validateOCMR(role) {
  if (role !== 'student') {
    return '';
  }
  var ocmr = $('#ocmr [name="ocmr"]').val();
  if (ocmr.match(/^[0-9]{1,4}$/)) {
    return '';
  } else {
    if (ocmr === '') {
      return 'An OCMR is required to create a student account\n';
    } else {
      return 'Invalid OCMR number: must contain between one and four digits\n';
    }
  }
}

function stripForm() {
  $('#passwordconfirm').remove();
}

function formSubmit(event) {
  role = $('#role').val();
  message = '';
  message += validateNames(role);
  message += validateEmail();
  message += validateTNumber(role);
  message += validateOCMR(role);
  if (message !== '') {
    alert('The following problems occurred while trying to submit your ' +
          'sign-up information:\n' + message);
    event.preventDefault();
  } else {
    stripForm();
  }
}

function onReady() {
  $('#role').change(onRoleChange);
  $('#signupform').submit(formSubmit);
}

$(document).ready(onReady);
