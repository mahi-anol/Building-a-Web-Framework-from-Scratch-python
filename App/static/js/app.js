$(document).ready(function(){
    // Get base URL for proxy compatibility
    const BASE_URL = window.location.origin
    // const BASE_URL = window.location.pathname.endsWith('/') 
    //     ? window.location.pathname 
    //     : window.location.pathname + '/';
    
    let token = localStorage.getItem("token");

    // Show/hide login form based on token presence
    if (token !== null) {
        $("#login-form-wrapper").hide();
    } else {
        $("#login-form-wrapper").show();
    }

    // Login functionality
    $("#login-button").on("click", function (event) {
        event.preventDefault();
        payload={
            username:$("#usernamer").val(),
            password:$("#password").val(),
        }

        $.ajax({
            type: 'POST',
            url: BASE_URL + "/token",
            headers: {
                "Content-Type":"application/json"
            },
            data: JSON.stringify(payload),
        }).done(function (data) {
            token = data["token"];
            localStorage.setItem("token", token);
            $("#login-form-wrapper").hide();
            alert("Successfully logged in!");
        }).fail(function () {
            alert("Failed to login!");
        });
    });

    // Create book functionality  
    $("#create-button").on("click", function (e) {
        e.preventDefault();

        let name = $("#name").val();
        let author = $("#author").val();
        // let token="abc123"
        if (!name || !author) {
            alert("Please fill in both name and author");
            return;
        }

        $.ajax({
            type: 'POST',
            url: BASE_URL + "/books",
            headers: {
                "Authorization": "Token: " + token,
                "Content-Type":"application/json"
            },
            data: JSON.stringify({"name": name, "author": author})
        }).done(function() {
            alert('Book created successfully!');
            location.reload();
        }).fail(function(xhr) {
            if (xhr.status === 401) {
                alert('Please log in first!');
            } else {
                alert("Failed to create book!");
            }
        });
    });

    // Delete book functionality
    $(".delete-button").on("click", function (e) {
        let confirmed = confirm("Are you sure you want to delete this book?");
        let bookId = $(this).data("id");
        // let token="abc123"
        if (confirmed) {
            $.ajax({
                type: 'DELETE',
                url: BASE_URL + "/books/" + bookId,
                headers: {
                    "Authorization": "Token: " + token,
                    "Content-Type":"application/json"
                }
            }).done(function() {
                alert('Book deleted successfully!');
                location.reload();
            }).fail(function(xhr) {
                if (xhr.status === 401) {
                    alert('Please log in first!');
                } else {
                    alert("Failed to delete book!");
                }
            });
        }
    });
});
