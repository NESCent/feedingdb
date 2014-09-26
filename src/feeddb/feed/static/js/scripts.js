$( document ).ready(function() {

  $(".chosen-select, select[multiple]").chosen();

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

  $( ".datepicker" ).datepicker();

  // Allow Bootstrap's data-toggle="collapse" to work on <option> elements by
  // triggering the click event when the option is selected.
  $("select").on('change', function(ev) {
    $(ev.target).find('option:selected').click();
  });

});
