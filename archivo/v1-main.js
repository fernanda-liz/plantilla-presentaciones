const deck = document.getElementById("deck");
const slides = [...document.querySelectorAll(".slide")];
const progreso = document.getElementById("progreso");
const contador = document.getElementById("contador");
let actual = 0;
let saliendo = null;

const CONTENEDORES = ".grid-tarjetas, .reglas, .ranking, .split-2, .grid-iconos, .mosaico";

function prepararTurnos() {
  slides.forEach((slide) => {
    let i = 0;
    [...slide.children].forEach((hijo) => {
      if (hijo.classList.contains("fondo-animado") || hijo.classList.contains("notas")) return;
      hijo.style.setProperty("--i", i++);
    });
    slide.querySelectorAll(CONTENEDORES).forEach((cont) => {
      cont.classList.add("contenedor-anim");
      [...cont.children].forEach((item, j) => {
        item.classList.add("anim-item");
        item.style.setProperty("--j", j);
        item.style.setProperty("--i", cont.style.getPropertyValue("--i") || 0);
      });
    });
    slide.querySelectorAll(".diagrama .d-caja, .diagrama .d-cap, .r-nodo, .lt-fase").forEach((el, k) => el.style.setProperty("--k", k));
    slide.querySelectorAll(".diagrama .d-flecha, .diagrama .d-conector, .r-enlaces line").forEach((el, k) => el.style.setProperty("--k", k));
  });
}

function mostrar(indice, direccion) {
  const destino = Math.max(0, Math.min(indice, slides.length - 1));
  if (destino === actual && slides[actual].classList.contains("activa")) return;
  deck.dataset.dir = direccion || (destino > actual ? "adelante" : "atras");

  if (saliendo) saliendo.classList.remove("saliendo");
  const previa = slides[actual];
  if (previa && destino !== actual) {
    previa.classList.remove("activa");
    previa.classList.add("saliendo");
    saliendo = previa;
    setTimeout(() => previa.classList.remove("saliendo"), 500);
  }
  actual = destino;
  const nueva = slides[actual];
  nueva.classList.remove("activa");
  void nueva.offsetWidth;
  nueva.classList.add("activa");

  progreso.style.width = ((actual + 1) / slides.length) * 100 + "%";
  contador.textContent = `${actual + 1} / ${slides.length}`;
  if (location.hash !== "#" + (actual + 1)) history.replaceState(null, "", "#" + (actual + 1));
  ajustarFondos();
}

function siguiente() { if (actual < slides.length - 1) mostrar(actual + 1, "adelante"); }
function anterior() { if (actual > 0) mostrar(actual - 1, "atras"); }

function ajustarFondos() {
  slides.forEach((slide) => {
    const fondo = slide.querySelector(".fondo-animado");
    if (fondo) fondo.style.height = Math.max(slide.scrollHeight, slide.clientHeight) + "px";
  });
}

const TECLAS_SIGUIENTE = ["ArrowRight", "ArrowDown", "PageDown", " ", "Enter"];
const TECLAS_ANTERIOR  = ["ArrowLeft", "ArrowUp", "PageUp", "Backspace"];

document.addEventListener("keydown", (ev) => {
  if (ev.metaKey || ev.ctrlKey || ev.altKey) return;
  if (TECLAS_SIGUIENTE.includes(ev.key)) { ev.preventDefault(); siguiente(); }
  else if (TECLAS_ANTERIOR.includes(ev.key)) { ev.preventDefault(); anterior(); }
  else if (ev.key === "Home") { ev.preventDefault(); mostrar(0, "atras"); }
  else if (ev.key === "End") { ev.preventDefault(); mostrar(slides.length - 1, "adelante"); }
  else if (ev.key === "p" || ev.key === "P") { window.print(); }
  else if (ev.key === "n" || ev.key === "N") { document.body.classList.toggle("con-notas"); }
});

document.getElementById("siguiente").addEventListener("click", siguiente);
document.getElementById("anterior").addEventListener("click", anterior);
document.getElementById("btn-pdf").addEventListener("click", () => window.print());

document.addEventListener("click", (ev) => {
  if (ev.target.closest("a, button")) return;
  if (ev.clientX > window.innerWidth * 0.5) siguiente(); else anterior();
});

let tocoX = null;
document.addEventListener("touchstart", (ev) => { tocoX = ev.changedTouches[0].clientX; }, { passive: true });
document.addEventListener("touchend", (ev) => {
  if (tocoX === null) return;
  const salto = ev.changedTouches[0].clientX - tocoX;
  if (Math.abs(salto) > 55) { salto < 0 ? siguiente() : anterior(); }
  tocoX = null;
}, { passive: true });

// barras de ranking: el valor real vive en data-valor (0-100), CSS lo anima al activarse
slides.forEach((slide) => {
  slide.querySelectorAll(".fila-barra").forEach((fila) => {
    const v = fila.dataset.valor;
    if (v) fila.style.setProperty("--valor", v + "%");
  });
});

prepararTurnos();
const desdeHash = parseInt((location.hash || "").replace("#", ""), 10);
const inicial = Number.isFinite(desdeHash) && desdeHash > 0 ? desdeHash - 1 : 0;
actual = Math.max(0, Math.min(inicial, slides.length - 1));
slides.forEach((s) => s.classList.remove("activa"));
slides[actual].classList.add("activa");
progreso.style.width = ((actual + 1) / slides.length) * 100 + "%";
contador.textContent = `${actual + 1} / ${slides.length}`;
ajustarFondos();
window.addEventListener("resize", ajustarFondos);

// ── Vista previa 4:3 (mismo patrón que el deck de Computación Avanzada) ──
const esEmbebido = new URLSearchParams(location.search).get("embed") === "1";
const conmutadorFormato = document.getElementById("formato-conmutador");
if (esEmbebido) {
  conmutadorFormato?.remove();
} else {
  const btn169 = document.getElementById("btn-formato-169");
  const btn43 = document.getElementById("btn-formato-43");
  const simulador = document.getElementById("simulador-4-3");
  const iframe4x3 = document.getElementById("iframe-4-3");
  const btnCerrarSimulador = document.getElementById("btn-cerrar-simulador");

  function ajustarEscalaSimulador() {
    const margen = 0.92;
    const escala = Math.min((window.innerWidth * margen) / 1024, (window.innerHeight * margen) / 768);
    iframe4x3.style.transform = `scale(${escala})`;
  }
  function mostrarSimulador4x3() {
    iframe4x3.src = `index.html?embed=1#${actual + 1}`;
    simulador.classList.remove("oculto");
    ajustarEscalaSimulador();
    btn43.classList.add("formato-activo"); btn43.setAttribute("aria-pressed", "true");
    btn169.classList.remove("formato-activo"); btn169.setAttribute("aria-pressed", "false");
  }
  function ocultarSimulador4x3() {
    simulador.classList.add("oculto");
    iframe4x3.src = "about:blank";
    btn169.classList.add("formato-activo"); btn169.setAttribute("aria-pressed", "true");
    btn43.classList.remove("formato-activo"); btn43.setAttribute("aria-pressed", "false");
  }
  btn43?.addEventListener("click", mostrarSimulador4x3);
  btn169?.addEventListener("click", ocultarSimulador4x3);
  btnCerrarSimulador?.addEventListener("click", ocultarSimulador4x3);
  window.addEventListener("resize", () => { if (!simulador.classList.contains("oculto")) ajustarEscalaSimulador(); });
}
