class DiscogsCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      const card = document.createElement('ha-card');
      this.content = document.createElement('div');
      this.content.id = 'wrapper';
      card.appendChild(this.content);
      this.appendChild(card);
    }

    const image = hass.states['sensor.discogs_item_image'].state;

    this.content.innerHTML = `
      <style>img {
        display: block;
                height: auto;
                transition: filter 0.2s linear;
                width: 100%;
      }
      .footer {
        padding: 16px;
      }
      </style>

      <img src="${image}" />
      <div class="footer">
        ${hass.states['sensor.discogs_item_desc'].state}
      </div>
    `
  }

  setConfig(config) {
    this.config = config;
  }

  // The height of your card. Home Assistant uses this to automatically
  // distribute all cards over the available columns.
  getCardSize() {
    return 1;
  }
}

customElements.define('discogs-card', DiscogsCard);
