const usernameField = document.querySelector("#form_username");
    usernameField.addEventListener("keyup", (e) => {

        const usernameVal = e.target.value;
        console.log("Username:", usernameVal)

//        if (usernameVal.length > 0)
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

  $(function() {

     $("#fphone_error_message").hide();
     $("#username_error_message").hide();

     var error_fphone = false;
     var error_username = false;

     $("#form_fphone").focusout(function(){
        check_fphone();
     });

     $("#form_username").focusout(function(){
        check_username();
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
           $("#username_error_message").hide();
           $("#form_username").css("border","1px solid #34F458");
        } else {
           $("#username_error_message").html("İstifadəçi adı mütləqdir.");
           $("#username_error_message").css("color", "#F90A0A");
           $("#username_error_message").css("font-size", "12px");
           $("#username_error_message").show();
           $("#form_username").css("border","1px solid #F90A0A");
           error_username = true;
        }
     }

     $("#tchr_form").submit(function() {
        error_fphone = false;
        error_username = false;

        check_fphone();
        check_username();
  });
});