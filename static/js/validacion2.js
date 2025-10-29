

document.addEventListener('DOMContentLoaded', () => {

    //validacion y confirmacion para la eliminacion de un recorrido en detalle_recorrido.html
    const formulario=document.getElementById("form_eliminar");

    if(formulario){

         formulario.addEventListener("submit", (event)=> {
            const confirmado = confirm("¿Está seguro que desea eliminar el recorrido?");
            if(!confirmado){
                event.preventDefault();
            }
        });

    }

});
