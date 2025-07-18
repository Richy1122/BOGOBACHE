/**
 * formularios.js - Manejo de formularios para la app Bache
 * 
 * Funcionalidades:
 * - Validación de formularios
 * - Filtros anidados (Localidad → UPZ → Barrio)
 * - Manejo de imágenes
 * - Envío AJAX de formularios
 */

class FormulariosBache {
  
  getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
 }
  constructor() {
    this.formCrearBache = document.getElementById('form-crear-bache');
    this.formEditarBache = document.getElementById('form-editar-bache');
    this.formFiltros = document.getElementById('form-filtros');
    
    this.initEventListeners();
    this.initSelectsAnidados();
  }
  /**
   * Inicializa los event listeners para los formularios
   */
  initEventListeners() {
    if (this.formCrearBache) {
      this.formCrearBache.addEventListener('submit', (e) => this.handleCrearBache(e));
    }

    if (this.formEditarBache) {
      this.formEditarBache.addEventListener('submit', (e) => this.handleEditarBache(e));
    }

    if (this.formFiltros) {
      this.formFiltros.addEventListener('submit', (e) => this.handleFiltrarBaches(e));
      this.formFiltros.addEventListener('reset', () => this.resetFiltros());
    }

    // Manejo de carga de imágenes
    document.querySelectorAll('.input-foto').forEach(input => {
      input.addEventListener('change', (e) => this.previewImage(e));
    });
  }

  /**
   * Configura los selects anidados (Localidad → UPZ → Barrio)
   */
  initSelectsAnidados() {
    const localidadSelect = document.getElementById('id_localidad');
    const upzSelect = document.getElementById('id_upz');
    const barrioSelect = document.getElementById('id_barrio');

    if (localidadSelect && upzSelect) {
      localidadSelect.addEventListener('change', async () => {
        const localidadId = localidadSelect.value;
        
        if (localidadId) {
          upzSelect.disabled = false;
          upzSelect.innerHTML = '<option value="">Cargando UPZs...</option>';
          
          try {
            const upzs = await this.fetchUPZs(localidadId);
            this.populateSelect(upzSelect, upzs);
            
            // Resetear barrio cuando cambia localidad
            if (barrioSelect) {
              barrioSelect.innerHTML = '<option value="">Seleccione UPZ primero</option>';
              barrioSelect.disabled = true;
            }
          } catch (error) {
            console.error('Error cargando UPZs:', error);
          }
        }
      });
    }

    if (upzSelect && barrioSelect) {
      upzSelect.addEventListener('change', async () => {
        const upzId = upzSelect.value;
        
        if (upzId) {
          barrioSelect.disabled = false;
          barrioSelect.innerHTML = '<option value="">Cargando barrios...</option>';
          
          try {
            const barrios = await this.fetchBarrios(upzId);
            this.populateSelect(barrioSelect, barrios);
          } catch (error) {
            console.error('Error cargando barrios:', error);
          }
        }
      });
    }
  }

  /**
   * Obtiene las UPZs para una localidad
   */
  async fetchUPZs(localidadId) {
      const response = await fetch(`/api/upzs-por-localidad/${localidadId}/`);
      if (!response.ok) throw new Error('Error al cargar UPZs');
      return await response.json();
  }

  async fetchBarrios(upzId) {
      const response = await fetch(`/api/barrios-por-upz/${upzId}/`);
      if (!response.ok) throw new Error('Error al cargar barrios');
      return await response.json();
  }

  /**
   * Llena un select con opciones
   */
  populateSelect(selectElement, items) {
    selectElement.innerHTML = '<option value="">Seleccione...</option>';
    
    items.forEach(item => {
      const option = document.createElement('option');
      option.value = item.id;
      option.textContent = item.nombre;
      selectElement.appendChild(option);
    });
  }

    // Agregar validación antes del envío
  async handleCrearBache(e) {
      e.preventDefault();
      if (!this.validarFormulario(this.formCrearBache)) {
          return;
      }
      // ... resto del código
  }
  validarFormulario(form) {
    let valido = true;
    // Ejemplo de validación básica
    form.querySelectorAll('[required]').forEach(input => {
        if (!input.value.trim()) {
            this.mostrarError(input, 'Este campo es requerido');
            valido = false;
        }
    });
    return valido;
  }
  /**
   * Maneja el envío del formulario de creación
   */
  async handleCrearBache(e) {
    e.preventDefault();
    const formData = new FormData(this.formCrearBache);
    
    try {
      const response = await fetch('/api/baches/crear/', {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': this.getCSRFToken()
        }
      });

      const data = await response.json();
      
      if (data.success) {
        this.mostrarMensaje('Bache creado exitosamente', 'success');
        this.resetForm(this.formCrearBache);
        
        // Si hay un mapa, actualizarlo
        if (window.mapaBaches) {
          window.mapaBaches.agregarMarcador(data.bache);
        }
      } else {
        this.mostrarErrores(data.errors);
      }
    } catch (error) {
      console.error('Error:', error);
      this.mostrarMensaje('Error al crear el bache', 'error');
    }
  }

  /**
   * Maneja el envío del formulario de edición
   */
  async handleEditarBache(e) {
    e.preventDefault();
    const bacheId = this.formEditarBache.dataset.bacheId;
    const formData = new FormData(this.formEditarBache);
    
    try {
      const response = await fetch(`/api/baches/${bacheId}/editar/`, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': this.getCSRFToken()
        }
      });

      const data = await response.json();
      
      if (data.success) {
        this.mostrarMensaje('Bache actualizado exitosamente', 'success');
        
        // Actualizar marcador en el mapa si existe
        if (window.mapaBaches) {
          window.mapaBaches.actualizarMarcador(data.bache);
        }
      } else {
        this.mostrarErrores(data.errors);
      }
    } catch (error) {
      console.error('Error:', error);
      this.mostrarMensaje('Error al actualizar el bache', 'error');
    }
  }

  /**
   * Maneja el filtrado de baches
   */
  async handleFiltrarBaches(e) {
    e.preventDefault();
    const formData = new FormData(this.formFiltros);
    const params = new URLSearchParams(formData).toString();
    
    try {
      // Si hay un mapa, actualizar los marcadores filtrados
      if (window.mapaBaches) {
        await window.mapaBaches.filtrarBaches(params);
      } else {
        // Recargar la página con los filtros aplicados
        window.location.href = `${window.location.pathname}?${params}`;
      }
    } catch (error) {
      console.error('Error al filtrar:', error);
    }
  }

  /**
   * Muestra una vista previa de la imagen seleccionada
   */
  previewImage(e) {
    const input = e.target;
    const preview = document.getElementById(`${input.id}-preview`);
    
    if (input.files && input.files[0]) {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        preview.src = e.target.result;
        preview.style.display = 'block';
      };
      
      reader.readAsDataURL(input.files[0]);
    }
  }

  /**
   * Muestra mensajes al usuario
   */
  mostrarMensaje(texto, tipo) {
    // Implementar según tu sistema de mensajes
    console.log(`${tipo}: ${texto}`);
    alert(`${tipo.toUpperCase()}: ${texto}`);
  }

  /**
   * Muestra errores de validación
   */
  mostrarErrores(errors) {
    // Limpiar errores previos
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    
    // Mostrar nuevos errores
    for (const [field, messages] of Object.entries(errors)) {
      const input = document.querySelector(`[name="${field}"]`);
      if (input) {
        const errorContainer = document.createElement('div');
        errorContainer.className = 'error-message text-danger mt-1';
        errorContainer.textContent = messages.join(', ');
        input.parentNode.appendChild(errorContainer);
      }
    }
  }

  /**
   * Obtiene el token CSRF
   */
  getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }

  /**
   * Resetea un formulario
   */
  resetForm(form) {
    form.reset();
    // Limpiar vistas previas de imágenes
    form.querySelectorAll('.image-preview').forEach(preview => {
      preview.style.display = 'none';
    });
  }

  /**
   * Resetea los filtros
   */
  resetFiltros() {
    if (window.mapaBaches) {
      window.mapaBaches.cargarBaches();
    } else {
      window.location.href = window.location.pathname;
    }
  }
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
  window.formulariosBache = new FormulariosBache();
});