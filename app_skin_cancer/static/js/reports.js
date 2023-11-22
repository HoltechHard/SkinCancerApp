$(document).ready(function(){
    
    // jquery function to load progress bar data
    function progress_bar_data(classes, probs){
        for(let i = 0; i < classes.length; i++){
            $(".grh_lblPred").eq(i).append(classes[i]);
            $(".progress-bar.bg-green").eq(i).css('width', Math.round(100 * probs[i]) + '%');            
            $(".grh_probPred").eq(i).append(parseFloat((100 * probs[i]).toFixed(2)) + '%');
        }
    }
    
    $('.btn.btn-primary.btn-sm').on('click', function(){
        // collect the id
        console.log('button clicked');
        var row = $(this).closest('tr');
        var id_patient = row.find('td:eq(1)').text();
        console.log('id patient: ' + id_patient);

        // send for backend to process the data
        $.ajax({
            url: '/reports/patient_reports',
            type: 'POST',
            data: {'id_patient': id_patient}, 
            success: function(res){
                console.log("success send data");

                // generate dynamically the image inside of container
                if(res.url_image){
                    var img = $('<img id="dynamic">');
                    img.attr('src', '/' + res.url_image);
                    img.attr('width', '150');
                    img.attr('height', '120');
                    img.appendTo("#image_container");
                }else{
                    console.log("not data was received");
                }

                // generate the prob distribution
                progress_bar_data(res.type_cancer, res.prob_scores);
            },
            error: function(err){
                console.log("Error: ", err);
            }
        });

    });

    // clean button
    $('.btn.btn-danger.btn-sm').on('click', function(){
        $('#image_container').empty();
        $('.grh_lblPred').empty();
        $('.progress-bar.bg-green').css('width', '0');
        $('.grh_probPred').empty();
    });

});
