$(document).ready(function() {
    setTimeout(function() {
        $('.alert-dismissible').alert('close');
    }, 5000);
    
    // Show loading spinner when submitting forms
    $('form').on('submit', function() {
        // Don't show spinner for simple toggle forms
        if (!$(this).hasClass('no-spinner')) {
            $('#spinner').removeClass('d-none');
        }
    });
    
    // Show spinner when clicking links with class 'show-spinner'
    $('.show-spinner').on('click', function() {
        $('#spinner').removeClass('d-none');
    });
    
    // Tooltip initialization
    $('[data-toggle="tooltip"]').tooltip();
    
    // Active nav links
    var currentUrl = window.location.pathname;
    $('.navbar-nav .nav-link').each(function() {
        var linkUrl = $(this).attr('href');
        if (linkUrl && currentUrl.includes(linkUrl) && linkUrl != '/') {
            $(this).addClass('active');
        }
    });
    
    // Table row highlight on hover
    $('.table-hover tr').hover(
        function() { $(this).addClass('bg-light'); },
        function() { $(this).removeClass('bg-light'); }
    );
    
    // Toggle filters visibility
    $('[data-target="#filtersCollapse"]').click(function() {
        if ($('#filtersCollapse').hasClass('show')) {
            $(this).text('Show Filters');
        } else {
            $(this).text('Hide Filters');
        }
    });
    
    // Initialize datepickers
    if ($.fn.datepicker) {
        $('.datepicker').datepicker({
            format: 'yyyy-mm-dd',
            autoclose: true,
            todayHighlight: true
        });
    }
    
    // Initialize select2 if available
    if ($.fn.select2) {
        $('.select2').select2({
            theme: 'bootstrap4',
            width: '100%'
        });
    }
});

// Global functions

// Function to confirm deletion
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}

// Function to copy text to clipboard
function copyToClipboard(text) {
    var tempInput = document.createElement('input');
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    
    // Show toast or alert
    alert('Copied to clipboard!');
}
