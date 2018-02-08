$(function() {

    $('#btnRegister').click(function() {

        $.ajax({
            url: '/registerUser',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                alert(response)
                //alert("Successfully Registered");
                document.location.href="/";
            },
            error: function(error) {
                console.log(error);
            }
        });

    });

    $('#btnReset').click(function() {
        $('#myForm')[0].reset();
    });

    $('#btnResetSignIn').click(function(){
        $('#signInForm')[0].reset();
    });

    $('#btnSignIn').click(function() {
        //var user = $('#userName').val();
        $.ajax({
            url: '/signIn',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                alert(response)
                next_page_url = "/showUserHomePage"
                console.log(next_page_url);
                window.location.href = next_page_url
            },
            error: function(error) {
                console.log(error);
            }
        });

    });


    $('#btnAddKey').click(function() {
        //var userName = $('#userName').val();
        $.ajax({
            url:'/addUserKeys',
            data: $('form').serialize(),
            type:'POST',
            success: function(response){
                console.log(response);
                alert(response);
                //alert(escape(response));
                //alert(escape('{"Message": "Key added successfully"}'));
                if (escape(response) == escape('{"Message": "Key added successfully"}') ) {
                document.location.href="/showUserHomePage";
                }
                else { document.location.href="/showAddUserKeys" }
            },
            error: function(error){
                console.log(error)
            }
        });
    });

    $('#btnResetAddKeyForm').click(function(){
        console.log('Resetting AddKey form')
        $('#addKeyForm')[0].reset();
    });

   /* $('.showPasswordBtn').click(function(){
        $(this).html($(this).html() == 'Show Password' ? 'this html' : 'Show Password');
    }); */


    $('.showPasswordBtn').click(function(){
        var $row = $(this).closest('tr')
        if ($(this).html() == 'Show Password') {
            $row.find('.UserPassword').show();
            $(this).html('Hide Password');
        }
        else {
            $row.find('.UserPassword').hide();
            $(this).html('Show Password');
        };
    });

   /* $("input:checkbox:not(:checked)").each(function() {
    var column = "table ." + $(this).attr("name");
    $(column).hide();
    }); */

});