/* javascript to accompany jquery.html */

$(document).ready(
  /* this defines a function that gets called after the document is in memory */
  function () {
    /* add a click handler for our button */
    $("#addElement").click(function () {
      $("form").submit(function (event) {
        event.preventDefault();
      });

      /* ajax post */
      $.post(
        "/input_handler.html",
        /* pass a JavaScript dictionary */
        {
          type: "insert",
          elementNum: $("#elementNum").val() /* retrieve values from input */,
          elementCode: $("#elementCode").val(),
          elementName: $("#elementName").val(),
          color1: $("#color1").val(),
          color2: $("#color2").val(),
          color3: $("#color3").val(),
          radius: $("#radius").val(),

    
        }
      )
        .done(function (data) {
          console.log(data);
          alert("Element inserted!");
        })
        .fail(function (xhr, status, error) {
          alert("Error! Element could not be inserted!");
        });
    });

    $("#removeElement").click(function () {
      $("form").submit(function (event) {
        event.preventDefault();
      });

      /* ajax post */
      $.post(
        "/input_handler.html",
        /* pass a JavaScript dictionary */
        {
          type: "remove",
          removeElementName: $("#removeElementName").val() /* retrieve values from input */,
        }
      )
        .done(function (data) {
          alert("Element removed!");
        })
        .fail(function (xhr, status, error) {
          alert("Error! Element not found!");
        });
    });
    });
