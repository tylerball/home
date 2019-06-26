class TTCCard extends HTMLElement {
  setConfig(config) {
    if (!config.entity) {
      throw new Error('Please specify an entity');
    }

    this._config = config;
  }

  set hass(hass) {
    if (!this.content) {
      var card = document.createElement('ha-card');
      this.content = document.createElement('div');
      this.content.id = 'wrapper';
      card.appendChild(this.content);
      this.appendChild(card);
    }

    var data = hass.states[this._config.entity]
    let predictions = [];

    function parsePrediction(pred, index) {
      if (index > 3) {
        return '';
      }
      let output;
      let minutes = parseInt(pred);
      if (minutes.toString() == "NaN") {
        output = pred;
      } else {
        output = `${pred}min`;
      }
      return `
        <div class="prediction">
          ${output}
        </div>
      `;
    }

    predictions = data.attributes.upcoming.split(', ').map(parsePrediction);

    this.content.innerHTML = `
      <style>
        .outer {
          padding: 1px 16px 16px;
        }
        .predictions {
          display: flex;
          justify-content: space-between;
        }
        .prediction {
          font-size: 2em;
        }
      </style>

      <div class="outer">
        <h3>${data.attributes.route}</h3>
        <div class="predictions">
          ${predictions.join(' ')}
        </div>
      </div>
    `
  }

  // The height of your card. Home Assistant uses this to automatically
  // distribute all cards over the available columns.
  getCardSize() {
    return 1;
  }
}

customElements.define('ttc-card', TTCCard);
