// static/script.js

function previewImages(input) {
    const preview = $('#imagePreview');
    preview.empty();

    if (input.files) {
        [...input.files].forEach(file => {
            const reader = new FileReader();
            reader.onload = function(e) {
                $('<img>').attr('src', e.target.result).appendTo(preview);
            }
            reader.readAsDataURL(file);
        });
    }
}

$('#uploaded_files').on('change', function() {
    previewImages(this);
});

$('#qaForm').on('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);

    if (formData.getAll('uploaded_files').length === 0) {
        $('#errorMessage').text('Please upload at least one screenshot.').show();
        return;
    }

    $('.loading-spinner').show();
    $('#errorMessage').hide();
    $('#responseSection').hide();

    $.ajax({
        url: '/describe',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function(data) {
            $('#responseText').text(data.response_text);
            $('#responseSection').show();
        },
        error: function(xhr) {
            let errorMsg = 'Error generating testing instructions.';
            if (xhr.responseJSON && xhr.responseJSON.error) {
                errorMsg = xhr.responseJSON.error;
            }
            $('#errorMessage').text(errorMsg).show();
        },
        complete: function() {
            $('.loading-spinner').hide();
        }
    });
});

