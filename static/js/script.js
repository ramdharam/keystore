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
        var user = $('#userName').val();
        $.ajax({
            url: '/signIn',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
                alert(response)
                next_page_url = "/showUserHomePage/" + user
                console.log(next_page_url);
                window.location.href = next_page_url
            },
            error: function(error) {
                console.log(error);
            }
        });

    });


    $('#btnAddKey').click(function() {
        var userName = $('#userName').val();
        $.ajax({
            url:'/addUserKeys/' + userName,
            data: $('form').serialize(),
            type:'POST',
            success: function(response){
                console.log(response);
                alert(response);
                //alert(escape(response));
                //alert(escape('{"Message": "Key added successfully"}'));
                if (escape(response) == escape('{"Message": "Key added successfully"}') ) {
                document.location.href="/showUserHomePage/" + userName;
                }
                else { document.location.href="/showAddUserKeys/" + userName; }
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

});