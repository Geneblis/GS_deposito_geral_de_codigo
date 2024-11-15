let capitulo_var = 1
let idk_var = 1

function cap1_dizer_vaisefuder(){
    capitulo_var = 2
    idk_var = 2
}
function cap1_dizer_calma_la(){
    capitulo_var = 3
    idk_var = 3
}


function atualizarpagina(){
    if(capitulo_var == 2){
        document.getElementById("capitulo").textContent = "Parte 2, vai se fuder!!!!";
    }
    if(idk_var == 2){
        document.getElementById("idk").textContent = "sei la, cabou o dinheiro da firma.";
    }

    if(capitulo_var == 3){
        document.getElementById("capitulo").textContent = "Parte 2, vc disse sei la";
    }
    if(idk_var == 3){
        document.getElementById("idk").textContent = "ata po.";
    }
}
 
console.log(capitulo_var)
console.log(idk_var)