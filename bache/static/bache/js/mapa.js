class MapaBaches {
    constructor() {
        this.map = null;
        this.marcadores = {};
        this.modal = new bootstrap.Modal(document.getElementById('bacheModal'));
    }

    inicializar() {
        this.crearMapa();
        this.configurarEventos();
        this.cargarBaches();
    }

    crearMapa() {
        this.map = L.map('map').setView([4.6097, -74.0817], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(this.map);
    }

    configurarEventos() {
        this.map.on('click', (e) => this.mostrarFormularioCreacion(e));
        document.getElementById('bacheForm').addEventListener('submit', (e) => this.enviarFormulario(e));
    }

    mostrarFormularioCreacion(e) {
        document.getElementById('latitud').value = e.latlng.lat.toFixed(6);
        document.getElementById('longitud').value = e.latlng.lng.toFixed(6);
        this.modal.show();
    }

    async cargarBaches() {
        try {
            const response = await fetch('/api/baches/');
            const baches = await response.json();
            
            baches.forEach(bache => {
                this.agregarMarcador(bache);
            });
        } catch (error) {
            console.error('Error cargando baches:', error);
        }
    }

    agregarMarcador(bache) {
        const icono = this.obtenerIcono(bache.estado);
        const marcador = L.marker([bache.latitud, bache.longitud], {icon: icono})
            .addTo(this.map)
            .bindPopup(this.crearPopup(bache));
        
        this.marcadores[bache.id_bache] = marcador;
    }

    obtenerIcono(estado) {
        const color = estado === 'arreglado' ? 'green' : estado === 'en_proceso' ? 'orange' : 'red';
        return L.icon({
            iconUrl: `/static/bache/images/marker-${color}.png`,
            iconSize: [25, 41]
        });
    }

    crearPopup(bache) {
        return `<b>Bache ${bache.id_bache}</b>
                <p>Estado: ${bache.estado}</p>
                <p>Localidad: ${bache.localidad__nombre || 'N/A'}</p>`;
    }

   async enviarFormulario(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        try {
            const csrfToken = this.getCSRFToken();
            const response = await fetch('/api/baches/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });
            
            if (!response.ok) {
                throw new Error(await response.text());
            }
            
            const data = await response.json();
            if(data.id_bache) {
                this.modal.hide();
                e.target.reset(); // Limpiar formulario
                this.agregarMarcador(data);
                this.mostrarMensaje('Bache registrado exitosamente', 'success');
            }
        } catch (error) {
            console.error('Error creando bache:', error);
            this.mostrarMensaje('Error al crear bache: ' + error.message, 'error');
        }
    }

    getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
    }

    mostrarMensaje(texto, tipo) {
        // Implementar según tu UI (puede ser un toast, alerta, etc.)
        alert(`${tipo.toUpperCase()}: ${texto}`);
    }
}

// Inicialización cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const mapa = new MapaBaches();
    mapa.inicializar();
});