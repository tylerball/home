class GroupCard extends HTMLElement {

  setConfig(config) {
    if (!config.group) {
      throw new Error('Please specify a group');
    }

    if (this.lastChild) this.removeChild(this.lastChild);
    var cardConfig = Object.assign({}, config);
    if (!cardConfig.card) cardConfig.card = {};
    if (!cardConfig.card.type) cardConfig.card.type = 'entities';
    var element = document.createElement(`hui-${cardConfig.card.type}-card`);
    this.appendChild(element);
    this._config = cardConfig;
  }

  set hass(hass) {
    var config = this._config;
    var entities = hass.states[config.group].attributes['entity_id'];
    if (!config.card.entities || config.card.entities.length !== entities.length ||
      !config.card.entities.every(function (value, index) {
        return value.entity === entities[index].entity
      })) {
      config.card.entities = entities;
    }
    this.lastChild.setConfig(config.card);
    this.lastChild.hass = hass;
  }

  getCardSize() {
    return 'getCardSize' in this.lastChild ? this.lastChild.getCardSize() : 1;
  }
}

customElements.define('group-card', GroupCard);
