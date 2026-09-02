const botaoTema = document.getElementById("tema");


if(botaoTema){


    botaoTema.addEventListener("click",()=>{


        document.body.classList.toggle("claro");


        localStorage.setItem(
            "tema",
            document.body.classList.contains("claro")
        );


    });


}



if(localStorage.getItem("tema") === "true"){

    document.body.classList.add("claro");

}