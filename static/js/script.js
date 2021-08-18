$(document).ready(function () {
  // jQurey functions sourced from Materialize - https://www.tutorialspoint.com/materialize/
  $('.sidenav').sidenav();
  $(".dropdown-trigger").dropdown();
  $('.datepicker').datepicker({maxDate: new Date(), format: 'dd-mm-yy'});
  $('select').formSelect();
  $('.collapsible').collapsible();
  $('.tooltipped').tooltip();

  // jQueryImplementation based on example from jQuery - https://api.jquery.com/delay/
  $("#fadeFlash").delay(5000).slideUp(300); //fade flash in 10 seconds 
  
  // jQuery Implementation based on example from Cloudtables - https://datatables.net/examples/
  $('#inventory').DataTable( {
    ordering: true,
    searching: false,
    paging:true
  });
});
