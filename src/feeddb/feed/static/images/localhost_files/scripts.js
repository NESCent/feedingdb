$( document ).ready(function() {

  $(".chosen-select").chosen();

  $("#makeMeScrollable").smoothDivScroll({
			mousewheelScrolling: "allDirections",
			manualContinuousScrolling: true,
			autoScrollingMode: "onStart"
		});

  $("[data-toggle=tooltip]").tooltip();
  
  $( ".datepicker" ).datepicker();

  // Allow Bootstrap's data-toggle="collapse" to work on <option> elements by
  // triggering the click event when the option is selected.
  $("select").on('change', function(ev) {
    $(ev.target).find('option:selected').click();
  });
  
});