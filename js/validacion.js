// Generar formularios de pasajeros según la cantidad elegida
function generarPasajeros() {
    let cantidad = document.getElementById("cantidad").value;
    let contenedor = document.getElementById("contenedorPasajeros");

    contenedor.innerHTML = ""; // limpiamos

    for (let i = 1; i <= cantidad; i++) {
        contenedor.innerHTML += `
            <div class="card p-3 mb-3">
                <h5>Pasajero ${i}</h5>

                <label for="Nombre${i}">Nombre Completo:</label>
                <input id="Nombre${i}" class="form-control mb-2" placeholder="Apellido y Nombre">

                <label for="DNI${i}">DNI:</label>
                <input type="text" id="DNI${i}" class="form-control mb-2" placeholder="12345678">

                <label for="correo${i}">Correo electrónico:</label>
                <input type="email" id="correo${i}" class="form-control mb-2" placeholder="ejemplo@mail.com">

                <label for="nacimiento${i}">Fecha de Nacimiento:</label>
                <input type="date" id="nacimiento${i}" class="form-control mb-2">

                <label for="telefono${i}">Teléfono:</label>
                <input type="tel" id="telefono${i}" class="form-control mb-2" placeholder="Ej: 3834657689">
            </div>
        `;
    }
}

// Limpiar pasajeros al resetear
function limpiarPasajeros() {
    document.getElementById("contenedorPasajeros").innerHTML = "";
    document.getElementById("cantidad").value = "0";
}

// Validar formulario
function validarFormulario() {
    let recorrido = document.getElementById("recorrido").value;
    let cantidad = document.getElementById("cantidad").value;

    if (recorrido === "") {
        alert("Debe seleccionar un recorrido");
        return false;
    }
    if (cantidad === "0") {
        alert("Debe seleccionar la cantidad de pasajeros");
        return false;
    }

    // Validación de cada pasajero
    for (let i = 1; i <= cantidad; i++) {
        let nombre = document.getElementById("Nombre" + i).value.trim();
        let dni = document.getElementById("DNI" + i).value.trim();
        let correo = document.getElementById("correo" + i).value.trim();
        let nacimiento = document.getElementById("nacimiento" + i).value;
        let telefono = document.getElementById("telefono" + i).value.trim();

        if (nombre.length < 3) {
            alert(`El nombre del pasajero ${i} debe tener al menos 3 letras`);
            return false;
        }
        if (dni.length < 7 || dni.length > 8 || isNaN(dni)) {
            alert(`El DNI del pasajero ${i} debe tener entre 7 y 8 números`);
            return false;
        }
        if (correo === "") {
            alert(`Debe ingresar un correo electrónico para el pasajero ${i}`);
            return false;
        }
        if (telefono === "") {
            alert(`Debe ingresar un teléfono para el pasajero ${i}`);
            return false;
        }
        if (nacimiento) {
            let fechaNac = new Date(nacimiento + "T00:00:00");
            let hoy = new Date();
            hoy.setHours(0,0,0,0);
    
        if (fechaNac > hoy) {
            alert(`La fecha de nacimiento del pasajero ${i} no puede ser posterior a hoy`);
            return false;
            }
        }
        else {
            alert(`Debe ingresar una fecha de nacimiento para el pasajero ${i}`);
            return false;
        }
    }

    alert("¡Reserva realizada correctamente!");
    return true;
}