

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

//validacion y confirmacion para la eliminacion de un punto turistico en puntos_turisticos.html

//    const form_punto_turistico=document.querySelectorAll('.form_eliminar_punto');
//
//    if (form_punto_turistico.length > 0) {
//        form_punto_turistico.forEach(form =>{
//            form.addEventListener('click', function(e){
//                const confirmado = confirm('¿Seguro que quieres eliminar este punto turístico?');
//                if (!confirmado) {
//                    e.preventDefault(); // Cancela el submit si no confirma
//                }
//            });
//        });
//    }
});
