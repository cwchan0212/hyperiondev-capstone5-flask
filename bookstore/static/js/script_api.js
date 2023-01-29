// Script to handle the Book API

$(document).ready(function () {

    $("#get_all_books").mouseover(function() {
      $("#message").html("<i class='fa-solid fa-location-dot'></i> API Endpoint: /book/api/all")
    })

    $("#get_all_books").mouseout(function() {
      $("#message").html("")
    })

    $("#get_one_book").mouseover(function() {
      $("#message").html("<i class='fa-solid fa-location-dot'></i> API Endpoint: /book/api/&lt;uuid&gt;")
    })

    $("#get_one_book").mouseout(function() {
      $("#message").html("")
    })

    $("#add_one_book").mouseover(function() {
      $("#message").html("<i class='fa-solid fa-location-dot'></i> API Endpoint: /book/api/add")
    })

    $("#add_one_book").mouseout(function() {
      $("#message").html("")
    })

    $("#update_one_book").mouseover(function() {
      $("#message").html("<i class='fa-solid fa-location-dot'></i> API Endpoint: /book/api/update")
    })

    $("#update_one_book").mouseout(function() {
      $("#message").html("")
    })

    $("#delete_one_book").mouseover(function() {
      $("#message").html("<i class='fa-solid fa-location-dot'></i> API Endpoint: /book/api/delete")
    })

    $("#delete_one_book").mouseout(function() {
      $("#message").html("")
    })


    $("#get_all_books").click(function () {
      $.ajax({
        type: "GET",
        url: "/book/api/all",
        dataType: "json",
        success: function (response) {
          let one_index = Math.floor(Math.random() * response.length);
          console.log("uuid", response[one_index]["uuid"])
          let one_uuid = response[one_index]["uuid"];

          let put_index = Math.floor(Math.random() * response.length);
          let put_uuid = response[put_index]["uuid"];
          let put_title = response[put_index]["title"];
          let put_author = response[put_index]["author"];
          let put_description = response[put_index]["description"];
          let put_quantity = response[put_index]["quantity"];

          $("#json_result").text(JSON.stringify(response, null, 2));
          location.href = "#json_result";
          $("#get_book_uuid").val(one_uuid);

          $("#update_book_uuid").val(put_uuid);
          $("#update_book_title").val(put_title);
          $("#update_book_author").val(put_author);
          $("#update_book_description").val(put_description);
          $("#update_book_quantity").val(put_quantity);

          $("#delete_book_uuid").val(put_uuid);

          $("#message").html("<i>Get JSON for all books...</i>");
        },
        error: function (jqXHR, textStatus, errorThrown) {
          if (jqXHR.status >= 400 && jqXHR.status < 600) {
            // console.log("Error: " + jqXHR.responseText);
            $("#json_result").text(JSON.stringify(jqXHR.responseJSON, null, 2));
            location.href = "#json_result";
          } else {
            $("#json_result").text(textStatus);
            location.href = "#json_result";
          }
        },        
      });
    });

    $("#get_one_book").click(function () {
      let uuid = $("#get_book_uuid").val().trim();
      if (!uuid) {
        $("#message").html("<i>The uuid is blank.</i>");
        $("#get_book_uuid").focus();
      } else {
        $("#message").html("");
        $.ajax({
          type: "GET",
          url: "/book/api/" + uuid,

          // data: {param1: "value1", param2: "value2"},
          dataType: "json",
          success: function (response) {
            $("#json_result").text(JSON.stringify(response, null, 2));
            location.href = "#json_result";
            $("#message").html("<i>Get JSON for 1 book...</i>");
          },
          error: function (jqXHR, textStatus, errorThrown) {
            $("#json_result").text(textStatus);
          },
        });
      }
    });

    $("#add_one_book").click(function () {
      let title = $("#add_book_title").val().trim();
      let author = $("#add_book_author").val().trim();
      let description = $("#add_book_description").val().trim();
      let quantity = $("#add_book_quantity").val().trim();
      $("#message").html("");

      if (!title) {
        $("#message").html("<i>The title is blank.</i>");
        $("#add_book_title").focus();
      } else if (!author) {
        $("#message").html("<i>The author is blank.</i>");
        $("#add_book_author").focus();
      } else if (!description) {
        $("#message").html("<i>The description is blank.</i>");
        $("#add_book_description").focus();
      } else if (!quantity) {
        $("#message").html("<i>The quantity is blank.</i>");
        $("#add_book_quantity").focus();
        let error_message = error.join("<br>");
        $("#message").html("<i>" + error_message + "</i>");
      } else {
        $("#message").html("");

        $.ajax({
          type: "POST",
          url: "/book/api/add",
          contentType: "application/json",
          data: JSON.stringify({ title: title, author: author, description: description, quantity: quantity }),
          dataType: "json",
          success: function (response) {
            $("#json_result").text(JSON.stringify(response, null, 2));
            location.href = "#json_result";
            $("#json_result").focus();
            $("#update_book_title").val(title);
            $("#update_book_author").val(author);
            $("#update_book_description").val(description);
            $("#update_book_quantity").val(quantity);
            $("#message").html("<i>Get JSON for adding 1 book...</i>");
          },
          error: function (jqXHR, textStatus, errorThrown) {

            if (jqXHR.status >= 400 && jqXHR.status < 600) {
              // console.log("Error: " + jqXHR.responseText);
              $("#json_result").text(JSON.stringify(jqXHR.responseJSON, null, 2));
              location.href = "#json_result";
            } else {
              $("#json_result").text(textStatus);
              location.href = "#json_result";
            }
          },
        });
      }
    });

    $("#update_one_book").click(function () {
      let uuid = $("#update_book_uuid").val().trim();
      let title = $("#update_book_title").val().trim();
      let author = $("#update_book_author").val().trim();
      let description = $("#update_book_description").val().trim();
      let quantity = $("#update_book_quantity").val().trim();
      $("#message").html("");

      if (!title) {
        $("#message").html("<i>The title is blank.</i>");
        $("#update_book_title").focus();
      } else if (!author) {
        $("#message").html("<i>The author is blank.</i>");
        $("#update_book_author").focus();
      } else if (!description) {
        $("#message").html("<i>The description is blank.</i>");
        $("#update_book_description").focus();
      } else if (!quantity) {
        $("#message").html("<i>The quantity is blank.</i>");
        $("#update_book_quantity").focus();
        let error_message = error.join("<br>");
        $("#message").html("<i>" + error_message + "</i>");
      } else {
        $("#message").html("");
        $.ajax({
          type: "PUT",
          url: "/book/api/update",
          contentType: "application/json",
          data: JSON.stringify({ uuid: uuid, title: title, author: author, description: description, quantity: quantity }),
          dataType: "json",
          success: function (response) {
            $("#json_result").text(JSON.stringify(response, null, 2));
            location.href = "#json_result";
            $("#update_book_uuid").val(uuid);
            $("#update_book_title").val(title);
            $("#update_book_author").val(author);
            $("#update_book_description").val(description);
            $("#update_book_quantity").val(quantity);
            $("#message").html("<i>Get JSON for updating 1 book...</i>");
          },
          error: function (jqXHR, textStatus, errorThrown) {
            if (jqXHR.status >= 400 && jqXHR.status < 600) {
              // console.log("Error: " + jqXHR.responseText);
              $("#json_result").text(JSON.stringify(jqXHR.responseJSON, null, 2));
              location.href = "#json_result";
            } else {
              $("#json_result").text(textStatus);
              location.href = "#json_result";
            }

          },
        });
      }
    });

    $("#delete_one_book").click(function () {
      let uuid = $("#delete_book_uuid").val().trim();
      if (!uuid) {
        $("#message").html("<i>The uuid is blank.</i>");
        $("#delete_book_uuid").focus();
      } else {
        $("#message").html("");

        $.ajax({
          type: "DELETE",
          url: "/book/api/delete",
          data: JSON.stringify({ uuid: uuid }),
          dataType: "json",
          contentType: "application/json",
          success: function (response) {
            $("#json_result").text(JSON.stringify(response, null, 2));
            location.href = "#json_result";
            $("#message").html("<i>Get JSON for deleting 1 book...</i>");
          },
          error: function (jqXHR, textStatus, errorThrown) {
            if (jqXHR.status >= 400 && jqXHR.status < 600) {
              // console.log("Error: " + jqXHR.responseText);
              $("#json_result").text(JSON.stringify(jqXHR.responseJSON, null, 2));
              location.href = "#json_result";
            } else {
              $("#json_result").text(textStatus);
              location.href = "#json_result";
            }
          },
        });
      }
    });
  });


  


  // ------------------------------------------------------------------------------------------------------------------