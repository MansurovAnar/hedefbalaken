var myInput = document.getElementById("psw1");
var password2 = document.getElementById("psw2");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");


//password2.oninvalid = function(event) {
//	event.target.setCustomValidity('Daxil edilən parollar eyni deyil.');
//}

// Empty field error
function emptyUsername(event){
    if ( ! event.target.validity.valid ){
//        event.target.setCustomValidity('Daxil edilən parollar eyni deyil.');
        console.log("ERROR IN USERNAME FIELD")
        console.log(event.target.validity)
    }
}
//password2.addEventListener('input', emptyUsername);

myInput.onfocus = function() {
  document.getElementById("mymessage").style.display = "block";
}
myInput.onblur = function() {
  document.getElementById("mymessage").style.display = "none";
}

//password2.onkeyup = function() {
//    if(password2 != myInput){
//       $("#password2_error_message").html("Daxil edilən parollar eyni deyil.");
//       $("#password2_error_message").css("color", "#F90A0A");
//       $("#password2_error_message").css("font-size", "12px");
//       $("#password2_error_message").show();
//       $("#psw2").css("border","1px solid #F90A0A");
//    }
//    if(password2 === myInput) {
//        console.log("PArollar eynidir")
//        $("#password2_error_message").hide();
//        $("#psw2").css("border","1px solid #34F458");
//    }
//}

myInput.onkeyup = function() {

  // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  if(myInput.value.match(lowerCaseLetters)) {
    letter.classList.remove("invalid");
    letter.classList.add("valid");
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
    $("#password1_error_message").css("color", "#F90A0A");
    $("#password1_error_message").css("font-size", "12px");
    $("#password1_error_message").show();
    $("#psw1").css("border","1px solid #F90A0A");
  }

  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if(myInput.value.match(upperCaseLetters)) {
    capital.classList.remove("invalid");
    capital.classList.add("valid");
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
    $("#password1_error_message").css("color", "#F90A0A");
   $("#password1_error_message").css("font-size", "12px");
   $("#password1_error_message").show();
   $("#psw1").css("border","1px solid #F90A0A");
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if(myInput.value.match(numbers)) {
    number.classList.remove("invalid");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
    $("#password1_error_message").css("color", "#F90A0A");
   $("#password1_error_message").css("font-size", "12px");
   $("#password1_error_message").show();
   $("#psw1").css("border","1px solid #F90A0A");
  }

  // Validate length
  if(myInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
    $("#password1_error_message").css("color", "#F90A0A");
   $("#password1_error_message").css("font-size", "12px");
   $("#password1_error_message").show();
   $("#psw1").css("border","1px solid #F90A0A");
  }

  if(myInput.value.length >= 8 && myInput.value.match(numbers) && myInput.value.match(upperCaseLetters) && myInput.value.match(lowerCaseLetters)) {
    $("#password1_error_message").hide();
    $("#psw1").css("border","1px solid #34F458");
  }
}