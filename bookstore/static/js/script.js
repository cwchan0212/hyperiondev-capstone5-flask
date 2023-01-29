// Script to handle the search criteria and search input in the Book Search

$(document).ready(function () {
  $("#search_criteria").change(function () {
    if ($(this).val() === "quantity") {
      $("#search_input").hide();
      $("#search_input").val("");
      $("#quantity_search_inputs").show();
    } else {
      $("#search_input").show();
      $("#quantity_min").val("");
      $("#quantity_max").val("");
      $("#quantity_search_inputs").hide();
    }
  });

  if ($("#search_criteria").val() === "quantity") {
    $("#search_input").hide();
    $("#quantity_search_inputs").show();
  }
});

$(document).ready(function () {
  $("#example").DataTable({
    fixedHeader: true,
    dom: '<"top"flip>rt<"bottom"><"clear">',
    paging: true,
    searching: false,
    scrollY: "500px",
    scrollCollapse: true,
    bDestroy: true,
    fnDrawCallback: function (oSettings) {
      $(".paginate_button.current").addClass("btn btn-outline-light btn-sm");
      $(".standardDataTable")
        .parent()
        .toggle(settings.fnRecordsDisplay() > 0);
    },
  });
});

function handleClear() {
  $("#search_criteria").val("Search criteria...");
  $("#search_input").val("");
  $("#quantity_min").val("");
  $("#quantity_max").val("");
  $("#records").html("");
}

// ------------------------------------------------------------------------------------------------------------------
