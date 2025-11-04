

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

    //control del multi select de los puntos turisticos

    const multiSelect = document.getElementById('multiSelect');
    const selected = multiSelect.querySelector('.selected');
    const options = multiSelect.querySelector('.options');

    selected.addEventListener('click', () => {
      options.style.display = options.style.display === 'block' ? 'none' : 'block';
    });

    // Cerrar si se hace clic fuera del componente
    document.addEventListener('click', (event) => {
      if (!multiSelect.contains(event.target)) {
        options.style.display = 'none';
      }
    });

    // Mostrar las opciones seleccionadas
    const checkboxes = multiSelect.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(chk => {
      chk.addEventListener('change', () => {
        const selectedValues = Array.from(checkboxes)
          .filter(c => c.checked)
          .map(c => c.parentNode.textContent.trim());
        selected.textContent = selectedValues.length > 0 ? selectedValues.join(', ') : 'Seleccionar puntos turísticos';
      });
    });


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
