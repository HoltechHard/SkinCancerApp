$(document).ready(function(){

    // jquery function to update color
    function prob_color(prob){
        prob = parseFloat(prob);

        if(prob > 0.9){
            $('#lblProbPred').css('color', 'green');
        }else{
            $('#lblProbPred').css('color', 'red');
        }
    }

    // jquery function to load progress bar data
    function progress_bar_data(classes, probs){
        for(let i = 0; i < classes.length; i++){
            $(".grh_lblPred").eq(i).append(classes[i]);
            $(".progress-bar.bg-green").eq(i).css('width', Math.round(100 * probs[i]) + '%');            
            $(".grh_probPred").eq(i).append(parseFloat((100 * probs[i]).toFixed(2)) + '%');
        }
    }

    // submition to form
    $('#frmPatientData').on('submit', function(e){
        e.preventDefault();
        
        // take all data from html form
        var formData = new FormData($(this)[0]);

        $.ajax({
            url: '/diagnosis/classification',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(res){
                // add content to labels
                $('#lblLabelPred').append(res.label_pred);
                $('#lblProbPred').append(res.prob_pred);
                prob_color(res.prob_pred);
                
                // print predicted results in browser
                console.log(res.label_pred);
                console.log(res.prob_pred);

                // add data to progress bar
                progress_bar_data(res.classes, res.probs);                
            },
            error: function(xhr, status, errort){
                console.log('Error in asynchronous data processing...');
                console.log('Http status: ' + xhr.status);
                console.log('Ajax error: ' + status);
                console.log('Thrown error: ' + errort);
                console.log('Response error: ' + xhr.responseText);

                if(xhr.status == 400){
                    alert(xhr.responseJSON.error);
                }
            }
        });
    });

    // clean the form
    $('#btnClean').click(function(e){
        e.preventDefault();

        $('#txtFullName').val('');
        $('#txtAge').val('');
        $('#txtAnatomy').val('');
        $('.gender').prop('checked', false);
        $('#cboTypeImage').prop('selectedIndex', 0);
        $('#file').val('');
        $('#lblLabelPred').val('');
        $('#lblProbPred').val('');
        $('#lblProbPred').css('color', 'gray');
        $('.grh_lblPred').empty();
        $('.progress-bar.bg-green').css('width', '0');
        $('.grh_probPred').empty();
    });

});
