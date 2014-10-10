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

  $( ".datepicker" ).datepicker({dateFormat: "yyyy-mm-dd" });

  // Allow Bootstrap's data-toggle="collapse" to work on <option> elements by
  // triggering the click event when the option is selected.
  $("select").on('change', function(ev) {
    $(ev.target).find('option:selected').click();
  });
  
  $('.download-picture .glyphicon-picture').addClass('glyphicon-save');
  $('.download-picture .glyphicon-picture').removeClass('glyphicon-picture');


});
