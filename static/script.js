function showMoreReviews() {
  // Mostrar las reseñas adicionales
  document.querySelector(".more-reviews").style.display = "block";
  // Ocultar el botón
  document.querySelector(".main--boton").style.display = "none";
}

// Validación del formulario de contacto
function validateContactForm() {
  // Obtener los valores de los campos
  var name = document.getElementById("name").value;
  var email = document.getElementById("email").value;
  var message = document.getElementById("message").value;

  // Validar nombre (no vacío)
  if (name === "") {
    alert("Por favor, ingresa tu nombre.");
    return false; // Evitar que el formulario se envíe
  }

  // Validar correo electrónico
  var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  if (!emailPattern.test(email)) {
    alert("Por favor, ingresa un correo electrónico válido.");
    return false;
  }

  // Validar mensaje (no vacío)
  if (message === "") {
    alert("Por favor, ingresa un mensaje.");
    return false;
  }

  // Si todo está bien, se puede enviar el formulario
  return true;
}
