$j = jQuery;

$j(document).ready( function () { 

    $j('div#comment_success').hide();
    $j("div#comment_failure").hide();

    form = $j("form#comment_form");

    $j('#comments-form-modal').on('hidden.bs.modal', function() {
        form.show();
        $j("div#comment_success").hide();
        $j("div#comment_failure").hide();
    })

    function clear_form_fields() {
      form.find('input, textarea').not(':submit, :hidden').val('');
    }

    $j('#comment_form').submit(function() {
        $j.ajax({
            dataType: 'json',
            timeout: 10000,
            data: $j(this).serialize(),
            type: $j(this).attr('method'),
            url: commentSubmitUrl,
            success: function(response) {
                clear_form_fields();
                form.hide();
                $j("div#comment_success").show();
            },
            error: function(response) {
                console.log(response.responseJSON.errors);
                form.hide();
                $j("div#comment_failure").show();
            }
        });
        return false;
    });
})