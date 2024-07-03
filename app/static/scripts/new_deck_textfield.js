$(document).ready(function() {
    if ($('#deck').val() === 'new') {
	$('.newDeckField').show();
    }

    $('#deck').change(function() {
        if ($(this).val() === 'new') {       
	    $('.newDeckField').show();
	    console.log('The new deck text field has been shown');
	} else {
            $('.newDeckField').hide();
	    console.log('The new deck text field has been hiden');

        }
    });
});

