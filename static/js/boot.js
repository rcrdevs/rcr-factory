(function () {
    "use strict";

    var boot = document.querySelector("[data-boot]");
    var gif = document.querySelector("[data-boot-gif]");
    var iframe = document.querySelector("[data-boot-iframe]");
    var label = document.querySelector("[data-boot-label]");
    var pctEl = document.querySelector("[data-boot-pct]");
    if (!boot || !gif || !iframe || !label || !pctEl) return;

    var FULL_GIF_MS = 4600;   // duração da animação completa (com folga)
    var MIN_DISPLAY_MS = 900; // tempo mínimo do teaser, mesmo se o app carregar na hora

    var pct = 0;
    var iframeReady = false;
    var minTimeReached = false;
    var finished = false;

    function setPct(value) {
        pct = Math.min(99, Math.round(value));
        pctEl.textContent = pct + "%";
    }

    // Progresso falso: sobe rápido no início e desacelera perto de 90%,
    // nunca fecha em 100% sozinho -- isso só acontece quando o app avisa
    // que carregou de verdade.
    var tickTimer = setInterval(function () {
        var remaining = 92 - pct;
        setPct(pct + Math.max(0.4, remaining * 0.08));
    }, 180);

    setTimeout(function () {
        minTimeReached = true;
        maybeFinish();
    }, MIN_DISPLAY_MS);

    iframe.addEventListener("load", function () {
        iframeReady = true;
        maybeFinish();
    });

    function maybeFinish() {
        if (finished || !iframeReady || !minTimeReached) return;
        finished = true;
        clearInterval(tickTimer);

        pctEl.textContent = "100%";
        label.textContent = "pronto";

        // Troca pro gif completo, recarregando do frame 1 (cache-bust via query string).
        gif.src = gif.dataset.fullSrc + "?r=" + Date.now();

        setTimeout(function () {
            boot.classList.add("of-boot--out");
        }, FULL_GIF_MS);
    }
})();
