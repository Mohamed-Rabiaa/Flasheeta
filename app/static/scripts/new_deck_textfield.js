$(document).ready(function() {
    if ($('#deck').val() === 'new') {
        $('.new-deck-field').show();
    }

    $('#deck').change(function() {
        if ($(this).val() === 'new') {
            $('.new-deck-field').show();
            console.log('The new deck text field has been shown');
        } else {
            $('.new-deck-field').hide();
            console.log('The new deck text field has been hidden');
        }
    });
});

