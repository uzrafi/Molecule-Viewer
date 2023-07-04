$(document).ready( 
    function(){
      
        $("#submit_sdf").click(function(event){
            event.preventDefault();

            var name = $('#mol-name').val().trim();
            var sdf= $('#sdf-file')[0].files[0];
            
            var formData = new FormData();
            formData.append('mol-name', name);
            formData.append('sdf-file', sdf);

            $.ajax({
                    url: 'uploadsdf',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,

                    success: function(response) {
                        alert("File uploaded!")
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        alert("Error. File not uploaded!");
                    },
                });

                $("#submit_sdf").trigger("reset")  

            }
        )
    }
)