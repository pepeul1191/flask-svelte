/**
 * Clase AutoComplete - Autocompletado avanzado con búsqueda remota
 */
export class AutoComplete {
  constructor(config) {
    // Validación de configuraciones requeridas
    if (!config || typeof config !== 'object') {
      throw new Error('Se requiere un objeto de configuración');
    }

    const required = ['inputId', 'suggestionsId', 'apiUrl'];
    const missing = required.filter(field => !config[field]);
    if (missing.length > 0) {
      throw new Error(`Faltan parámetros requeridos: ${missing.join(', ')}`);
    }

    // Configuración con valores por defecto
    this.config = {
      minChars: 2,  // Cambiado a 2 para mejor UX
      displayKey: 'name',
      valueKey: 'id',
      emptyMessage: 'No se encontraron resultados',
      debounceTime: 300,
      dataWrapper: 'data',
      ...config
    };

    // Obtener elementos DOM
    this.input = document.getElementById(this.config.inputId);
    this.suggestionsDiv = document.getElementById(this.config.suggestionsId);
    this.hiddenInput = this.config.hiddenInputId 
      ? document.getElementById(this.config.hiddenInputId) 
      : null;

    if (!this.input || !this.suggestionsDiv) {
      throw new Error('No se encontraron los elementos del DOM especificados');
    }

    // Estado interno
    this.activeIndex = -1;
    this.currentSuggestions = [];
    this.lastRequest = null;

    this.initEvents();
  }

  initEvents() {
    // ELIMINADO: No hay evento focus que haga búsqueda

    // SOLO búsqueda con debounce al escribir (teclado)
    this.input.addEventListener('input', this.debounce(() => {
      this.handleInput();
    }, this.config.debounceTime));

    // Navegación con teclado (flechas, enter, escape)
    this.input.addEventListener('keydown', (e) => this.handleKeydown(e));

    // Cerrar al hacer clic fuera
    document.addEventListener('click', (e) => {
      if (!this.suggestionsDiv.contains(e.target) && e.target !== this.input) {
        this.clearSuggestions();
      }
    });

    // Evento personalizado cuando se selecciona un ítem
    this.input.addEventListener('autocomplete-select', (e) => {
      console.log('Ítem seleccionado:', e.detail);
    });
  }

  async handleInput() {
    const query = this.input.value.trim();
    this.activeIndex = -1;

    // Si el texto es menor al mínimo, limpiar y ocultar sugerencias
    if (query.length < this.config.minChars) {
      this.clearSuggestions();
      this.currentSuggestions = [];
      return;
    }

    try {
      // Cancelar petición anterior si existe
      if (this.lastRequest) {
        this.lastRequest.abort();
      }

      const controller = new AbortController();
      this.lastRequest = controller;

      const headers = {
        'Content-Type': 'application/json',
        ...(this.config.jwtToken && { 
          'Authorization': `Bearer ${this.config.jwtToken}` 
        })
      };

      const response = await fetch(
        `${this.config.apiUrl}?name=${encodeURIComponent(query)}`, 
        {
          headers,
          signal: controller.signal
        }
      );

      if (!response.ok) throw new Error(`Error HTTP: ${response.status}`);

      const data = await response.json();
      
      // Extraer los datos según el wrapper configurado
      if (this.config.dataWrapper && data[this.config.dataWrapper]) {
        this.currentSuggestions = data[this.config.dataWrapper];
      } else if (Array.isArray(data)) {
        this.currentSuggestions = data;
      } else {
        this.currentSuggestions = [];
      }
      
      this.renderSuggestions();

    } catch (error) {
      if (error.name !== 'AbortError') {
        console.error('Error en AutoComplete:', error);
        this.clearSuggestions();
      }
    } finally {
      this.lastRequest = null;
    }
  }

  renderSuggestions() {
    this.suggestionsDiv.innerHTML = '';

    if (!this.currentSuggestions || this.currentSuggestions.length === 0) {
      this.showEmptyMessage();
      return;
    }

    // Mostrar el contenedor
    this.suggestionsDiv.style.display = 'block';

    const fragment = document.createDocumentFragment();

    this.currentSuggestions.forEach((item, index) => {
      const div = document.createElement('div');
      div.className = `list-group-item list-group-item-action suggestion-item ${
        index === this.activeIndex ? 'active' : ''
      }`;
      
      // Mostrar el campo displayKey o name como fallback
      div.textContent = item[this.config.displayKey] || item.name || item.id;
      div.dataset.index = index;
      
      div.addEventListener('click', () => this.selectItem(index));
      div.addEventListener('mouseenter', () => {
        this.activeIndex = index;
        this.highlightItem(index);
      });

      fragment.appendChild(div);
    });

    this.suggestionsDiv.appendChild(fragment);
  }

  handleKeydown(e) {
    const items = this.suggestionsDiv.querySelectorAll('.suggestion-item');
    if (!items || items.length === 0) {
      // Si no hay sugerencias y presiona Enter, no hacer nada
      if (e.key === 'Enter') {
        // Permitir el envío del formulario si no hay sugerencias
        return;
      }
      return;
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        this.activeIndex = Math.min(this.activeIndex + 1, items.length - 1);
        this.highlightItem(this.activeIndex);
        break;

      case 'ArrowUp':
        e.preventDefault();
        this.activeIndex = Math.max(this.activeIndex - 1, 0);
        this.highlightItem(this.activeIndex);
        break;

      case 'Enter':
        e.preventDefault();
        if (this.activeIndex >= 0 && this.activeIndex < items.length) {
          this.selectItem(this.activeIndex);
        }
        break;

      case 'Escape':
        e.preventDefault();
        this.clearSuggestions();
        break;

      case 'Tab':
        this.clearSuggestions();
        break;

      default:
        break;
    }
  }

  selectItem(index) {
    if (!this.currentSuggestions || !this.currentSuggestions[index]) return;

    const selected = this.currentSuggestions[index];
    
    // Actualizar input visible
    this.input.value = selected[this.config.displayKey] || selected.name || selected.id;
    
    // Actualizar input hidden si existe
    if (this.hiddenInput) {
      this.hiddenInput.value = selected[this.config.valueKey] || selected.id;
    }

    this.clearSuggestions();
    
    // Disparar evento personalizado
    const event = new CustomEvent('autocomplete-select', {
      detail: selected,
      bubbles: true
    });
    this.input.dispatchEvent(event);
  }

  highlightItem(index) {
    const items = this.suggestionsDiv.querySelectorAll('.suggestion-item');
    items.forEach((item, i) => {
      item.classList.toggle('active', i === index);
    });
    
    // Scroll automático para mantener el ítem visible
    if (items[index]) {
      items[index].scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
      });
    }
  }

  clearSuggestions() {
    this.suggestionsDiv.innerHTML = '';
    this.suggestionsDiv.style.display = 'none';
    this.activeIndex = -1;
  }

  showEmptyMessage() {
    this.suggestionsDiv.style.display = 'block';
    const emptyMsg = document.createElement('div');
    emptyMsg.className = 'list-group-item text-muted';
    emptyMsg.textContent = this.config.emptyMessage;
    this.suggestionsDiv.appendChild(emptyMsg);
  }

  // Helpers
  debounce(func, wait) {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  // Métodos públicos adicionales
  destroy() {
    this.input.removeEventListener('input', this.handleInput);
    this.input.removeEventListener('keydown', this.handleKeydown);
    document.removeEventListener('click', this.handleOutsideClick);
    this.clearSuggestions();
  }
}