/**
 * Check the checkbox on the collection.image model admin if title, object
 * number or active fields are clicked.
 */
(function($) {
    'use strict';
    $(document).ready(function() {
        $('td.field-title, td.field-object_number, td.field-active').on('click', function() {
            event.preventDefault();
            var self = $(this);
            self.parent().find('td.action-checkbox input.action-select').trigger('click');
            return false;
        });
    });
})(django.jQuery);
