(() => {
  "use strict";

  const trigger = document.querySelector(".easter-egg-link");
  const catImage = trigger?.querySelector(".cat-head");
  const message = trigger?.querySelector(".easter-message");
  if (!trigger || !catImage || !message) return;

  const states = [
    { src: trigger.dataset.catCalm, alt: "Minkas Katzenkopf mit misstrauischem Blick", text: "Minka beobachtet dich." },
    { src: trigger.dataset.catAnnoyed, alt: "Minkas Katzenkopf mit genervtem Blick", text: "Minka wird langsam ungeduldig." },
    { src: trigger.dataset.catAngry, alt: "Minkas Katzenkopf mit wütendem Blick", text: "Sie hat dich gewarnt …" },
    { src: trigger.dataset.catFurious, alt: "Minkas Katzenkopf mit sehr wütendem Blick", text: "Jetzt reicht es Minka!" },
  ];

  let stage = 0;
  let openingTimer = null;

  function preloadStage(index) {
    if (!states[index]) return;
    const preload = new Image();
    preload.src = states[index].src;
  }

  function showStage(nextStage) {
    stage = nextStage;
    const state = states[stage];
    catImage.src = state.src;
    catImage.alt = state.alt;
    message.textContent = state.text;
    trigger.dataset.stage = String(stage);
    trigger.classList.remove("is-reacting");
    window.requestAnimationFrame(() => trigger.classList.add("is-reacting"));
    preloadStage(stage + 1);
  }

  trigger.addEventListener("animationend", () => {
    trigger.classList.remove("is-reacting");
  });

  trigger.addEventListener("click", (event) => {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (openingTimer !== null) return;

    showStage(Math.min(stage + 1, states.length - 1));
    if (stage === states.length - 1) {
      trigger.setAttribute("aria-label", "Minka ist sauer – Katzenspiel wird geöffnet");
      openingTimer = window.setTimeout(() => {
        window.location.assign(trigger.href);
      }, 1200);
    }
  });

  preloadStage(1);
})();
