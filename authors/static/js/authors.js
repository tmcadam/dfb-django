// # Place all the behaviors and hooks related to the matching controller here.
// # All this logic will automatically be available in application.js.
// # You can use CoffeeScript in this file: http://coffeescript.org/


$j = jQuery;

function moveTo(hash){
    if (hash.length > 0) {
        $j('span#' + hash).parent().addClass("bg-info", 100);
        $j.scrollTo($j('span#' + hash));
        window.scrollBy(0 ,-100);
        setTimeout( function() { 
                $j('span#' + hash).parent().removeClass("bg-info", 100);
            },
            100
        );
    }
}

function onArrange() {
    let hash = location.hash.replace('#', '');
    moveTo(hash);
}

function onAuthorClick() {
    hash = $j(this).data("hash");
    location.hash = hash;
    moveTo(hash);
}

$j(document).ready( function () { 
    $j('span.author-link').click(onAuthorClick);
    $j('#authors').on('layoutComplete', onArrange);
})