$(document).ready(function() {
    console.log("Document is ready");

    // Function to set active link based on current URL
    function setActiveLink() {
        const currentUrl = window.location.href;

        // Remove active class from all nav links
        $('.nav_link').removeClass('active');

        // Add active class to the nav link matching the current URL
        $('.nav_link').each(function() {
            if ($(this).attr('href') === currentUrl) {
                $(this).addClass('active');
            }
        });
    }

    // Call setActiveLink on page load
    setActiveLink();
});
