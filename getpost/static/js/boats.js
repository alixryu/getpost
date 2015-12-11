function roleChange() {
  if (this.value === 'student') {
    $('#employeemessage').hide(100);
    $('#email').show(100);
    $('#tnum').show(100);
    $('#passone').show(100);
    $('#passtwo').show(100);
  } else if (this.value === 'employee') {
    $('#employeemessage').show(100);
    $('#email').hide(100);
    $('#tnum').hide(100);
    $('#passone').hide(100);
    $('#passtwo').hide(100);
  }
}

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
  if ($('input[type="radio"][name="role"][value="student"]').is(':checked')) {
    var tnum = $('#tnum [name="tnum"]').val();
    if (tnum.match(/^T?[0-9]{8}$/)) {
      return '';
    } else {
      if (tnum === '') {
        return 'A T number is required in order for students to sign up.\n';
      } else {
        return 'Invalid T number: must contain exactly eight digits, ' +
        'optionally preceded by a capital "T".\n';
      }
    }
  } else {
    return '';
  }
}

function validatePassword() {
  var passone = $('#passone [name="passone"]').val();
  var passtwo = $('#passtwo [name="passtwo"]').val();
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

function formSubmit(event) {
  message = '';
  message += validateEmail();
  message += validateTNumber();
  message += validatePassword();
  if (message !== '') {
    alert('The following problems occurred while trying to submit your ' +
          'sign-up information:\n' + message);
    event.preventDefault();
  }
}

function onReady() {
  $('input[type="radio"][name="role"]').change(roleChange);
  $('#signupform').submit(formSubmit);
}

$(document).ready(onReady);
