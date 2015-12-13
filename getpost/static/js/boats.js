function validateEmail() {
  var email = $('#email [name="email"]').val();
  if (email.match(/^[a-zA-Z0-9]+@oberlin.edu$/)) {
    return '';
  } else {
    if (email === '') {
      return 'An email address is required in order to sign up.\n';
    } else if (!email.match(/^[a-zA-Z0-9]+@/)) {
      return 'Invalid email address: only letters and digits may precede the ' +
      '"@" symbol.\n';
    } else if (!email.match(/@oberlin.edu$/)) {
      return 'Invalid email address: must end in "@oberlin.edu".\n';
    } else {
      return 'Invalid email address.\n';
    }
  }
}

function validateTNumber() {
  var tnum = $('#tnum [name="tnum"]').val();
  if (tnum.match(/^T?[0-9]{8}$/)) {
    return '';
  } else {
    if (tnum === '') {
      return 'A T number is required in order to sign up.\n';
    } else {
      return 'Invalid T number: must contain exactly eight digits, ' +
      'optionally preceded by a capital "T".\n';
    }
  }
}

function validatePassword() {
  var passone = $('#password [name="password"]').val();
  var passtwo = $('#passwordconfirm [name="passwordconfirm"]').val();
  if (passone.length >= 6 && passtwo === passone) {
    return '';
  } else {
    if (passone === '') {
      return 'A password is required in order to sign up.\n';
    } else if (passone.length < 6) {
      return 'Invalid password: must contain at least six characters.\n';
    } else if (passone !== passtwo) {
      return 'Invalid password: confirmation does not match.\n';
    } else {
      return 'Invalid password.\n';
    }
  }
}

function stripForm() {
  $('#passwordconfirm').remove();
}

function formSubmit(event) {
  message = '';
  message += validateEmail();
  message += validateTNumber();
  message += validatePassword();
  if (message !== '') {
    alert('The following problems occurred while trying to submit your ' +
          'sign-up information:\n' + message);
    event.preventDefault();
  } else {
    stripForm();
  }
}

function onReady() {
  $('#signupform').submit(formSubmit);
}

$(document).ready(onReady);
