 $("#addvariant").click(function () {
        var html = '';
        html += '<div id="variant_field_div">';
        html += '<input type="text" name="text" maxlength="200" placeholder="Variantı daxil edin" class="form-control" style="color:#3299a8;border-radius:10px; width: 50%;" id="variant_field" required="">';
        html += '</div>';

        $('#variant_field_add').append(html);
    });

 $("#removevariant").click(function () {
        var html = '';
        html += '<div id="variant_field_div">';
        html += '<input type="text" name="text" maxlength="200" placeholder="Variantı daxil edin" class="form-control" style="color:#3299a8;border-radius:10px; width: 50%;" id="variant_field" required="">';
        html += '</div>';

        $('#variant_field_div').remove();
    });