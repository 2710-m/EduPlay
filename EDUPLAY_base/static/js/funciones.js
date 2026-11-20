document.querySelectorAll(".quiz").forEach((formulario) => {
  formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const materia = formulario.dataset.materia;
    const respuestasCorrectas = materia === "Lectura"
      ? { p1: "a", p2: "b", p3: "a" }
      : { p1: "b", p2: "b", p3: "c" };

    let correctas = 0;
    const total = Object.keys(respuestasCorrectas).length;

    for (const [pregunta, correcta] of Object.entries(respuestasCorrectas)) {
      const elegida = formulario.querySelector(`input[name="${pregunta}"]:checked`);
      const feedback = formulario.querySelector(`[data-feedback="${pregunta}"]`);
      if (elegida && elegida.value === correcta) {
        correctas++;
        feedback.textContent = "¡Correcto!";
        feedback.className = "retroalimentacion bien";
      } else {
        feedback.textContent = `Todavía no. Revisa la pregunta e inténtalo de nuevo.`;
        feedback.className = "retroalimentacion mal";
      }
    }

    const salida = formulario.querySelector(".resultado-quiz");
    salida.textContent = `Tu resultado: ${correctas} de ${total}.`;
    try {
      const respuesta = await fetch("/api/resultado", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ materia, correctas, total })
      });
      if (respuesta.status === 401 || respuesta.redirected) {
        salida.textContent += " Inicia sesión para guardar tu resultado.";
      } else if (respuesta.ok) {
        salida.textContent += " Resultado guardado en tu progreso.";
      } else {
        salida.textContent += " No se pudo guardar el resultado.";
      }
    } catch (error) {
      salida.textContent += " No se pudo conectar con el servidor.";
    }
  });
});

// AUDIO PARA LA LECTURA

const botonReproducir = document.getElementById("reproducir");
const botonPausar = document.getElementById("pausar");
const botonDetener = document.getElementById("detener");

if (botonReproducir) {
    const lectura = document.querySelector(".lectura-texto");

    botonReproducir.addEventListener("click", () => {
        if (speechSynthesis.paused) {
            speechSynthesis.resume();
            return;
        }

        speechSynthesis.cancel();

        const voz = new SpeechSynthesisUtterance(lectura.innerText);
        voz.lang = "es-MX";
        voz.rate = 1;

        speechSynthesis.speak(voz);
    });

    botonPausar.addEventListener("click", () => {
        speechSynthesis.pause();
    });

    botonDetener.addEventListener("click", () => {
        speechSynthesis.cancel();
    });
}