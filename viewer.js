$(document).ready(function () {
  $.ajax({
    url: "/select",
    type: "GET",
    dataType: "json",
    success: function (data, status, xhr) {
      var moleculeList = $("#molecule-list"); 
      moleculeList.empty();

      if (xhr.status === 204) {
        
        var emptyBar = $('<div class="empty"></div>')
          .css("white-space", "pre-line")
          .text(
            "No molecules here...Click to add some!"
          );

        emptyBar.on("click", function () {
          window.location.href = "sdf.html";
        });

        moleculeList.append(emptyBar);
      } else {
        var molecules = data;
     
        for (var i = 0; i < molecules.length; i++) {
          var molecule = molecules[i];
       
          var molWindow = $('<div class="molecule-bar"></div>');

          molWindow.append(
            $('<span class="molecule-name"></span>').text(molecule.name)
          );

          var molInfo = $('<div class="molecule-info"></div>');
          molInfo.append(
            $('<span class="molecule-atoms"></span>').text(
              "Atoms: " + molecule.atom_count
            )
          );
          molInfo.append(
            $('<br></br>')
          );
          molInfo.append(
            $('<span class="molecule-bonds"></span>').text(
              "Bonds: " + molecule.bond_count
            )
          );
          molWindow.append(molInfo);

          molWindow.on("click", function () {
            var molName = $(this).find(".molecule-name").text();
            sendToMolecule(molName);
          });

          moleculeList.append(molWindow);
        }
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      console.log(xhr.status);
      console.log(errorThrown);
    },
  });
  
  function sendToMolecule(molName) {
    $.ajax({
      url: "/displayPage",
      type: "POST",
      data: { 'moleculeName': molName },
      success: function (response) {
        console.log(response);
        window.location.href = "display.html";
      },
      error: function (xhr, textStatus, errorThrown) {
        console.log(xhr.status);
        console.log(errorThrown);
      },
    });
  }
});
