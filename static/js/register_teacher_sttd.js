const usernameField = document.querySelector("#form_username");
const firstnameField = document.querySelector("#form_firstname");
const lastnameField = document.querySelector("#form_lastname");
const emailField = document.querySelector("#form_email");

// Username validation
usernameField.addEventListener("keyup", (a) => {
    a.preventDefault();
    const usernameVal = a.target.value;
    console.log("Username:", usernameVal)

    if (usernameVal.length > 0 || usernameVal == null || usernameVal  == "")
     {
        fetch("/validate-username/", {
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            if(data.username_valid){
                $("#username_error_message").hide();
                $("#form_username").css("border","1px solid #34F458");
            }
            if(data.username_error){
                console.log("ERROR");
                $("#username_error_message").html(data.username_error);
                $("#username_error_message").css("font-size", "12px");
                $("#username_error_message").css("color", "#F90A0A");
                $("#username_error_message").show();
                $("#form_username").css("border","1px solid #F90A0A");
            }
        })
    }
});
// End of username validation

// Firstname validation
firstnameField.addEventListener("keyup", (b) => {
    b.preventDefault();
    const firstnameVal = b.target.value;
//    console.log("First name:", firstnameVal)

    if (firstnameVal.length > 0 || firstnameVal == null || firstnameVal  == "")
     {
        fetch("/validate-firstname/", {
        body: JSON.stringify({ first_name: firstnameVal }),
        method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            if(data.firstname_valid){
                $("#firstname_error_message").hide();
                $("#form_firstname").css("border","1px solid #34F458");
            }
            if(data.firstname_error){
                console.log("ERROR");
                $("#firstname_error_message").html(data.firstname_error);
                $("#firstname_error_message").css("font-size", "12px");
                $("#firstname_error_message").css("color", "#F90A0A");
                $("#firstname_error_message").show();
                $("#form_firstname").css("border","1px solid #F90A0A");
            }
        })
    }
});
// End of firstname validation

// lastname validation
lastnameField.addEventListener("keyup", (c) => {
    c.preventDefault();
    const lastnameVal = c.target.value;

    if (lastnameVal.length > 0 || lastnameVal == null || lastnameVal  == "")
     {
        fetch("/validate-lastname/", {
        body: JSON.stringify({ last_name: lastnameVal }),
        method: "POST",
        })
        .then((res) => res.json())
        .then((data) => {
            console.log(data);
            if(data.lastname_valid){
                $("#lastname_error_message").hide();
                $("#form_lastname").css("border","1px solid #34F458");
            }
            if(data.lastname_error){
                console.log("ERROR");
                $("#lastname_error_message").html(data.lastname_error);
                $("#lastname_error_message").css("font-size", "12px");
                $("#lastname_error_message").css("color", "#F90A0A");
                $("#lastname_error_message").show();
                $("#form_lastname").css("border","1px solid #F90A0A");
            }
        })
    }
});
// End of lastname validation

  $(function() {

     $("#fphone_error_message").hide();
     $("#username_error_message").hide();
     $("#firstname_error_message").hide();
     $("#lastname_error_message").hide();
     $("#email_error_message").hide();
     $("#password1_error_message").hide();
     $("#password2_error_message").hide();

     var error_fphone = false;
     var error_username = false;
     var error_firstname = false;
     var error_lastname = false;
     var error_email = false;
     var error_password1 = false;
     var error_password2 = false;


     $("#form_fphone").focusout(function(){
        check_fphone();
     });

     $("#form_username").focusout(function(){
        check_username();
     });

     $("#form_firstname").focusout(function(){
        check_firstname();
     });

     $("#form_lastname").focusout(function(){
        check_lastname();
     });

     $("#form_email").focusout(function(){
        emailIsValid();
     });

     $("#psw1").focusout(function(){
        check_password();
     });
     $("#psw2").focusout(function(){
        check_password();
     });

     function check_fphone() {
        var pattern = /^[0-9]{7,7}$/;
        var fphone = $("#form_fphone").val();
        if (pattern.test(fphone) && fphone !== '') {
           $("#fphone_error_message").hide();
           $("#form_fphone").css("border","1px solid #34F458");
        } else {
           $("#fphone_error_message").html("Mobil nömrə ancaq rəqəmlərdən ibarət ola bilər");
           $("#fphone_error_message").css("color", "#F90A0A");
           $("#fphone_error_message").css("font-size", "12px");
           $("#fphone_error_message").show();
           $("#form_fphone").css("border","1px solid #F90A0A");
           error_fphone = true;
        }
        if (fphone.length < 7 ){
          $("#fphone_error_message").html("Mobil nömrə 7 rəqəmdən ibarət olmalıdır");
          $("#fphone_error_message").css("color", "#F90A0A");
          $("#fphone_error_message").css("font-size", "12px");
          $("#fphone_error_message").show();
          $("#form_fphone").css("border","1px solid #F90A0A");
          error_fphone = true;
        }
     }

     function check_username() {
        var user_name = $("#form_username").val();
        if (user_name){
            if(user_name.length < 3){
               $("#username_error_message").html("İstifadəçi adı minimum 3 simvoldan ibarət ola bilər.");
               $("#username_error_message").css("color", "#F90A0A");
               $("#username_error_message").css("font-size", "12px");
               $("#username_error_message").show();
               $("#form_username").css("border","1px solid #F90A0A");
               error_username = true;
            }
            else if(user_name.length >= 3){
                if(!user_name.match(/^[0-9a-z]+$/)){
                   $("#username_error_message").html("İstifadəçi adı ancaq hərf və rəqəmdən ibarət ola bilər.");
                   $("#username_error_message").css("color", "#F90A0A");
                   $("#username_error_message").css("font-size", "12px");
                   $("#username_error_message").show();
                   $("#form_username").css("border","1px solid #F90A0A");
                   error_username = true;
                }
                else {
                    $("#username_error_message").hide();
                    $("#form_username").css("border","1px solid #34F458");

                }

            }

        } else {
           $("#username_error_message").html("İstifadəçi adı mütləqdir.");
           $("#username_error_message").css("color", "#F90A0A");
           $("#username_error_message").css("font-size", "12px");
           $("#username_error_message").show();
           $("#form_username").css("border","1px solid #F90A0A");
           error_username = true;
        }
     }

     function check_firstname() {
        var first_name = $("#form_firstname").val();

        if (first_name){
            if(first_name.length < 3){
               $("#firstname_error_message").html("Ad minimum 3 hərfdən ibarət ola bilər.");
               $("#firstname_error_message").css("color", "#F90A0A");
               $("#firstname_error_message").css("font-size", "12px");
               $("#firstname_error_message").show();
               $("#form_firstname").css("border","1px solid #F90A0A");
               error_firstname = true;
            }
            else if(first_name.length >= 3){
                if(!first_name.match(/^[a-z]+$/)){
                   $("#username_error_message").html("Ad ancaq hərfdən ibarət ola bilər.");
                   $("#username_error_message").css("color", "#F90A0A");
                   $("#username_error_message").css("font-size", "12px");
                   $("#username_error_message").show();
                   $("#form_username").css("border","1px solid #F90A0A");
                   error_firstname = true;
                }
                else {
                    $("#firstname_error_message").hide();
                    $("#form_firstname").css("border","1px solid #34F458");
                }

            }
        } else {
           $("#firstname_error_message").html("Ad mütləqdir.");
           $("#firstname_error_message").css("color", "#F90A0A");
           $("#firstname_error_message").css("font-size", "12px");
           $("#firstname_error_message").show();
           $("#form_firstname").css("border","1px solid #F90A0A");
           error_firstname = true;
        }
     }

     function check_lastname() {
        var last_name = $("#form_lastname").val();
        if (last_name){
           if(last_name.length < 3){
               $("#lastname_error_message").html("Soyad minimum 3 hərfdən ibarət ola bilər.");
               $("#lastname_error_message").css("color", "#F90A0A");
               $("#lastname_error_message").css("font-size", "12px");
               $("#lastname_error_message").show();
               $("#form_lastname").css("border","1px solid #F90A0A");
               error_lastname = true;
           }
           else if(last_name.length >= 3){
                if(!last_name.match(/^[a-z]+$/)){
                   $("#lastname_error_message").html("Soyad ancaq hərfdən ibarət ola bilər.");
                   $("#lastname_error_message").css("color", "#F90A0A");
                   $("#lastname_error_message").css("font-size", "12px");
                   $("#lastname_error_message").show();
                   $("#form_lastname").css("border","1px solid #F90A0A");
                   error_lastname = true;
                }
                else {
                    $("#lastname_error_message").hide();
                    $("#form_lastname").css("border","1px solid #34F458");
                }

            }
        } else {
           $("#lastname_error_message").html("Soyad mütləqdir.");
           $("#lastname_error_message").css("color", "#F90A0A");
           $("#lastname_error_message").css("font-size", "12px");
           $("#lastname_error_message").show();
           $("#form_lastname").css("border","1px solid #F90A0A");
           error_lastname = true;
        }
     }

  var emailIsValid = function check_email() {
        console.log("NEW");
        var pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        var email = $("#form_email").val();
        if (pattern.test(email) && email !== '') {
           $("#email_error_message").hide();
           $("#form_email").css("border","1px solid #34F458");
           return "EmailOkay";
        } else {
           $("#email_error_message").html("Email düzgün formatda deyil.");
           $("#email_error_message").css("color", "#F90A0A");
           $("#email_error_message").css("font-size", "12px");
           $("#email_error_message").show();
           $("#form_email").css("border","1px solid #F90A0A");
           error_email = true;
//           return "Wrong email";
        }
     }

     function check_password() {
        var pswrd1 = $("#psw1").val();
        var pswrd2 = $("#psw2").val();

        var lowerCaseLetters = /[a-z]/g;
        var upperCaseLetters = /[A-Z]/g;
        var numbers = /[0-9]/g;

        if(!pswrd1){
            $("#password1_error_message").html("Parol mütləqdir.");
            $("#password1_error_message").css("color", "#F90A0A");
            $("#password1_error_message").css("font-size", "12px");
            $("#password1_error_message").show();
            $("#psw1").css("border","1px solid #F90A0A");
            error_password1 = true;
        }
        else {
            $("#password1_error_message").hide();
        }

        if(pswrd2) {
            if(pswrd2 != pswrd1){
               $("#psw1").css("border","1px solid #F90A0A");

               $("#password2_error_message").html("Parollar eyni deyil.");
               $("#password2_error_message").css("color", "#F90A0A");
               $("#password2_error_message").css("font-size", "12px");
               $("#password2_error_message").show();
               $("#psw2").css("border","1px solid #F90A0A");
               error_password1 = true;
               error_password2 = true;
            }
            else {
                $("#password1_error_message").hide();
                $("#psw1").css("border","1px solid #34F458");
                $("#password2_error_message").hide();
                $("#psw2").css("border","1px solid #34F458");
            }
        }

     }

//     if (!error_username){
//            $("#submit_form").attr("disabled", false);
//
//            console.log("NOT disabled");
//        }
//        else {
//            console.log("Disabled");
//            $("#submit_form").attr("disabled", true);
//        }

     $("#tchr_form").submit(function(event) {
        var valid = emailIsValid();
        console.log(valid)
        if(valid !== "EmailOkay"){
            event.preventDefault();
            alert('Invalid input data. Reason' + valid);
        }

        error_fphone = false;
        error_username = false;
        error_firstname = false;
        error_lastname = false;
        error_email = false;
        error_password1 = false;
        error_password2 = false;

        check_fphone();
        check_username();
        check_firstname();
        check_lastname();
        emailIsValid();
        check_password();


  });
});