document.addEventListener('DOMContentLoaded', () => {
  const checkboxes = document.querySelectorAll('.alergia');
  const platos = document.querySelectorAll('.plato');

  function filtrarPlatos() {
    const alergiasSeleccionadas = Array.from(checkboxes)
      .filter(cb => cb.checked)
      .map(cb => cb.value);
    
    platos.forEach(plato => {
      const alergenos = (plato.dataset.alergenos || '').split(/\s+/);
      if (alergiasSeleccionadas.some(alergia => alergenos.includes(alergia))) {
        plato.classList.add('oculto');
      } else {
        plato.classList.remove('oculto');
      }
    });
  }

  checkboxes.forEach(cb => cb.addEventListener('change', filtrarPlatos));
  filtrarPlatos();
});

// Desplegable de sección de alergias
document.addEventListener('DOMContentLoaded', function() {
  const tituloDesplegable = document.querySelector('.alergia-titulo');
  const contenidoDesplegable = document.querySelector('.alergia-contenido');

  if (!tituloDesplegable || !contenidoDesplegable) return;

  tituloDesplegable.addEventListener('click', function() {
    contenidoDesplegable.classList.toggle('activo');
    const pElement = tituloDesplegable.querySelector('p');
    if (pElement) {
      pElement.innerHTML = contenidoDesplegable.classList.contains('activo')
        ? 'Selecciona alergias: ⬆️'
        : 'Selecciona alergias: ⬇️';
    }
  });
});


