function refresh() {
  if (window.location.pathname.indexOf('/lovelace') > -1) {
    window.location.reload(true);
  }
}

window.setInterval(refresh, 1000 * 60 * 5);
