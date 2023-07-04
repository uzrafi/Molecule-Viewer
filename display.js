$(document).ready( 
  //function to call when server is created
  function(){
      
  $.ajax({
      url: "/createSVG",
      type: "GET",
      dataType: "text",
      success: function(data, status, xhr){
          $("#window").empty()
          data = data.replace('width="1000"', 'width="500"');
          data = data.replace('height="1000"', 'height="400"');
          data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
          $("#window").append(data)
      }
  });

  $("#x-button").click(function(){
      var plane = "x";
      rotate(plane)
      {
          $.ajax({
              url: "/createSVG",
              type: "GET",
              dataType: "text",
              success: function(data, status, xhr){
                  $("#window").empty()
                  data = data.replace('width="1000"', 'width="500"');
                  data = data.replace('height="1000"', 'height="400"');
                  data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
                  $("#window").append(data)
              }
          });
      }

  }),

  $("#y-button").click(function(){
      var plane = "y";
      rotate(plane)
      {
          $.ajax({
              url: "/createSVG",
              type: "GET",
              dataType: "text",
              success: function(data, status, xhr){
                  $("#window").empty()
                  data = data.replace('width="1000"', 'width="500"');
                  data = data.replace('height="1000"', 'height="400"');
                  data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
                  $("#window").append(data)
              }
          });
      }
  }),

  $("#z-button").click(function(){
      var plane = "z";
      rotate(plane)
      {
          $.ajax({
              url: "/createSVG",
              type: "GET",
              dataType: "text",
              success: function(data, status, xhr){
                  $("#window").empty()
                  data = data.replace('width="1000"', 'width="500"');
                  data = data.replace('height="1000"', 'height="400"');
                  data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
                  $("#window").append(data)
              }
          });
      }
  })

  }
)

function rotate(plane){
  $.ajax({
      url: "/rotation", 
      type: "POST",
      data: {'plane': plane},
      success: function (response) {
          console.log("rotation success");
      },
      error: function (xhr, textStatus, errorThrown) {
          console.log("error!");
      }
  });
}