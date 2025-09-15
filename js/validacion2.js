
//combino la validacion de html5 con js para los campos obligatorios

document.addEventListener('DOMContentLoaded', () => {
  const formulario = document.getElementById("form_recorrido");
  if (!formulario) return;

  const inputs_obligatorios = formulario.querySelectorAll("input[required]");

  
  formulario.addEventListener("submit", function(e) {
    
    inputs_obligatorios.forEach(input => {
      input.classList.remove("error_input");
      const msg = input.parentElement && input.parentElement.querySelector(".obligatorio");
      if (msg) msg.textContent = "";
    });

    
    if (!formulario.checkValidity()) {
      e.preventDefault();              
      inputs_obligatorios.forEach(input => {
        if (!input.checkValidity()) {
          input.classList.add("error_input");
          const msg = input.parentElement && input.parentElement.querySelector(".obligatorio");
          if (msg) msg.textContent = "Campo obligatorio";
        }
      });
      formulario.reportValidity();      
    }
    
  });

  
  inputs_obligatorios.forEach(input => {
    input.addEventListener("input", function() {
      const msg = this.parentElement && this.parentElement.querySelector(".obligatorio");
      if (this.value && this.value.toString().trim() !== "") {
        this.classList.remove("error_input");
        if (msg) msg.textContent = "";
      }
    });

    input.addEventListener("invalid", function(ev) {
      this.classList.add("error_input");
      const msg = this.parentElement && this.parentElement.querySelector(".obligatorio");
      if (msg) msg.textContent = "Campo obligatorio";
    });
  });
});
