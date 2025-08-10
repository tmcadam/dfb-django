$j = jQuery;

$j(document).ready( function () { 
    $j('#authors-info').hide();
    $j('body').removeClass('modal-open');
    $j('.modal-backdrop').remove();
    $j('[data-toggle="popover"]').popover();

    $j('body').click(function(e) { 
        if ($j(e.target).data('toggle') != 'popover' && $j(e.target).parents('.popover.in').length == 0) {
            $j('[data-toggle="popover"]').popover('hide');
        }
    })
})