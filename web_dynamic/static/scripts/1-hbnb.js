$(document).ready(function() {
    let amenities = {};
    $('input[type="checkbox"]').change(function() {
        const amenityId = $(this).data('id');
        const amenityName = $(this).data('name');
        if ($(this).is(':checked')) {
            amenities[amenityId] = amenityName;
        } else {
            delete amenities[amenityId];
        }
        const selectedAmenities = Object.values(amenities).join(', ');
        $('.amenities h4').text('Amenities: ' + selectedAmenities);
    });
});
