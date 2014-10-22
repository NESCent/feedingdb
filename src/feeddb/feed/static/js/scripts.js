$( document ).ready(function() {

  $(".chosen-select, select[multiple]").chosen({
    search_contains: true
   ,placeholder_text_multiple: "Click to add"
   ,placeholder_text_single: "Click to add"
  });

  $("#makeMeScrollable").smoothDivScroll({
      mousewheelScrolling: "vertical",
      manualContinuousScrolling: true,
      autoScrollingMode: "onStart",
      mousewheelScrollingStep: 3,
      autoScrollingStep: 1,
      autoScrollingInterval: 20,
      autoScrollingStopped: function() {
        $("#makeMeScrollable").smoothDivScroll("startAutoScrolling");
      }
    });

  $("[data-toggle=tooltip]").tooltip();

  $( ".datepicker" ).datepicker({dateFormat: "yy-mm-dd" });

  // Allow Bootstrap's data-toggle="collapse" to work on <option> elements by
  // triggering the click event when the option is selected.
  $("select").on('change', function(ev) {
    $(ev.target).find('option:selected').click();
  });
  
  $('.download-picture .glyphicon-picture').addClass('glyphicon-save');
  $('.download-picture .glyphicon-picture').removeClass('glyphicon-picture');

  $('.data_file .glyphicon-picture').addClass('glyphicon-save');
  $('.data_file .glyphicon-picture').removeClass('glyphicon-picture');

  // This is like Bootstrap's modal insertion mechanism, but a better fit for
  // our needs here. Here's what's going on:
  //
  // 1. If a modal (with class "modal" and "ajax") is opened from an <a> tag
  //    with a 'href' attribute, load the content into the .modal element.
  // 2. Activate ajaxForm on any <form> tags loaded into the modal
  // 3. Remove the content when hiding modal
  $('.modal.ajax').on('show.bs.modal', function(e) {
    if (e.relatedTarget) {
      var href = e.relatedTarget.href
      var addNewTarget = $(e.relatedTarget).attr('data-addnew-target')
      var targetselector = '#' + e.target.id
      if (href) {
        var modal = this
        var ajaxify = function () {
          $(modal).find('form').first().ajaxForm({
            target: targetselector,
            success: function() {
              var obj = $(modal).find('new-object').get(0);
              if (obj && addNewTarget) {
                var pk = $(obj).attr('django-pk');
                var label = $(obj).attr('django-label');
                $(addNewTarget).append($('<option/>', {
                  text: label,
                  value: pk
                })) // add new element
                .val(pk) // select the new element
                .trigger('chosen:updated'); // update chosen with new state
                
                window.setTimeout(function() {
                  // hide the modal after a second
                  $(modal).modal('hide');
                }, 1000);
              }
              else {
                // This is the case of an error in the form, so the server has
                // sent us a new <form> tag. We need to re-run ourselves on the
                // form so that it too will be submitted via AJAX.
                ajaxify()
              }
            }
          });
        }
        $(modal).load(href, function(responseText, textStatus, jqXHR) {
          ajaxify();
        })
      }
    }
  })
  .on('hidden.bs.modal', function(e) {
    $(this).empty()
  })

});
