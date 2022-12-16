input = document.getElementById("loginForm");

// Execute a function when the user presses a key on the keyboard
input.addEventListener("keypress", function(event) {
  // If the user presses the "Enter" key on the keyboard
  if (event.key === "Enter") {
    // Trigger the button element with a click
    document.getElementById("submitForm").click()
  }
});


function getLoginInfo(){
    console.log("hello from the function")
    let username = document.getElementById("floatingInput").value;
    let passwd = document.getElementById("floatingPassword").value;

    $.ajax({
      type: 'POST',
      url: "/login/submit",
      data: {
        "username": username,
        "password": passwd
      },
      success: function(response){
        console.log(response)
        if (response["status"] == "ok"){
          document.cookie = "auth=True;";
          document.cookie = "username="+username;
          window.location.replace('/index');
        }
        else if (response["status"] == "Error" && document.getElementById("errorLogin") == null){
          divLogin = document.getElementById("divLogin");
          errorPop = document.createElement("a");
          errorPop.innerText = "Wrong login or password";
          errorPop.setAttribute("id", "errorLogin");
          divLogin.appendChild(errorPop)
        }
      }
    })
}
