window.onload = function (){
    console.log("hello");

    console.log(document.cookie)

    let cookies = document.cookie.split("; ");
    console.log(cookies)
    let usernameCookie = "";
    
    for (let i = 0; i < cookies.length; i++){
      console.log(cookies[i].search("username="))
      if (cookies[i].search("username=") == 0){
        
        usernameCookie = cookies[i].split("=")[1];
        
        console.log(usernameCookie)
      }
    }
      if (usernameCookie != ""){
        console.log("it's execute time");

        let divNav = document.getElementById("navbarSupportedContent");

        let ulDrop = document.createElement("div");
        ulDrop.setAttribute("class", "navbar-nav mr-auto");
        ulDrop.setAttribute("id", "ulDrop");
        divNav.appendChild(ulDrop);

        let liDrop = document.createElement("li");
        liDrop.setAttribute("class", "nav-item dropdown");
        liDrop.setAttribute("id", "liDrop");

        let aDrop = document.createElement("a");
        aDrop.setAttribute("class", "nav-link dropdown-toggle");
        aDrop.setAttribute("id", "navbarDropdown");
        aDrop.setAttribute("role", "button");
        aDrop.setAttribute("data-toggle", "dropdown");
        aDrop.setAttribute("aria-haspopup", "true");
        aDrop.setAttribute("aria-expanded", "false");
        aDrop.innerText = usernameCookie  ;

        ulDrop.appendChild(liDrop);
        liDrop.appendChild(aDrop);
        
        let divDrop = document.createElement("div");
        divDrop.setAttribute("class", "dropdown-menu");
        divDrop.setAttribute("id", "divDrop");
        divDrop.setAttribute("aria-labelledby", "navbarDropdown");

        aDrop.appendChild(divDrop);

        let decoDrop = document.createElement("a");
        decoDrop.setAttribute("class", "dropdown-item");
        decoDrop.setAttribute("onclick", "disconnect()");
        decoDrop.innerText = "Deconnexion";

        divDrop.appendChild(decoDrop);
  
        while (!document.body.contains(document.getElementById("liMachine"))){
        }

        $.ajax({
          type: 'POST',
          url: '/index/getDekstop',
          data: {
            "username" : usernameCookie
          },

          success: function(response){
            console.log(response)
            if(response["status"] == "201"){
              liMachine = document.getElementById("Machine");
              liMachine.setAttribute("href", "http://" + response["ipv4"] + ":" + response["port"] + "/");
            }
          }
        })
  
    }
}

function disconnect(){
  $.ajax({
    type: 'GET',
    url: '/login/disconnect',
    dat:{

    },
    success:function(response){
      console.log(response);
      window.location.replace("/")
    }
  })
}