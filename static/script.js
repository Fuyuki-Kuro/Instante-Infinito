function pad(v) {
    return v.toString().padStart(2, "0");
  }
  
  function updateClock() {
    const now = new Date();
    let diff = now - start; // usa a data definida no template
  
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    diff %= 1000 * 60 * 60 * 24;
  
    const hours = Math.floor(diff / (1000 * 60 * 60));
    diff %= 1000 * 60 * 60;
  
    const minutes = Math.floor(diff / (1000 * 60));
    diff %= 1000 * 60;
  
    const seconds = Math.floor(diff / 1000);
  
    document.getElementById(
      "contador"
    ).textContent = `${pad(days)}d:${pad(hours)}h:${pad(minutes)}m:${pad(seconds)}s`;
  }
  
  setInterval(updateClock, 1000);
  updateClock();
  