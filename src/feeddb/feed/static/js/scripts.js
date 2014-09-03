$( document ).ready(function() {

  $(".chosen-select").chosen();

  $("#makeMeScrollable").smoothDivScroll({
			mousewheelScrolling: "allDirections",
			manualContinuousScrolling: true,
			autoScrollingMode: "onStart"
		});

  $("[data-toggle=tooltip]").tooltip();
  
  $( ".datepicker" ).datepicker();

});



