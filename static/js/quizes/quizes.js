console.log('Hello Tekin')

$(function () {

  $(".js-create-quiz").click(function () {
    $.ajax({
      url: '/quiz/create/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-quiz").modal("show");
      },
      success: function (data) {
        $("#modal-quiz .modal-content").html(data.html_form);
      },
      error: function(error){
        console.log(error)
      }
    });
  });

$("modal-quiz").on("submit", ".js-quiz-create-form", function(){
        var form = $(this)
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid == "Valid"){
                    $("#quiz-table tbody").html(data.html_quiz_list);
                     $("#modal-quiz").modal("hide");
                     console.log("SUCCESSS");
                }
                else {
                    $("#modal-quiz .modal-content").html(data.html_form);
                    console.log("errorrrrrr");
                }
            }

        });
        return false;

    });

});

