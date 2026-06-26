// ─── Preview handling ─────────────────────────────────────────
function setupPreview(inputId, previewId, cardId) {
  const input = document.getElementById(inputId);
  const preview = document.getElementById(previewId);
  const card = document.getElementById(cardId);
  input.addEventListener("change", () => {
    const file = input.files[0];
    if (!file) return;
    const url = URL.createObjectURL(file);
    preview.src = url;
    card.classList.add("has-file");
  });
  // drag-over styling
  card.addEventListener("dragover", (e) => {
    e.preventDefault();
    card.classList.add("dragover");
  });
  card.addEventListener("dragleave", () => card.classList.remove("dragover"));
  card.addEventListener("drop", () => card.classList.remove("dragover"));
}
setupPreview("avatar-input", "avatar-preview", "avatar-card");
setupPreview("garment-input", "garment-preview", "garment-card");

// ─── Form submit ──────────────────────────────────────────────
const form = document.getElementById("tryon-form");
const statusArea = document.getElementById("status-area");
const submitBtn = document.getElementById("submit-btn");
let pollInterval = null;

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearInterval(pollInterval);

  submitBtn.disabled = true;
  submitBtn.textContent = "Sending…";
  statusArea.style.display = "block";
  statusArea.innerHTML = `
        <div class="status-pill">
          <div class="spinner"></div>
          Uploading your images…
        </div>`;

  const data = new FormData(form);

  try {
    const res = await fetch("/try-on/", { method: "POST", body: data });
    const json = await res.json();
    if (!res.ok || json.error) throw new Error(json.error || "Server error");

    const jobId = json.job_id;
    statusArea.innerHTML = `
          <div class="status-pill">
            <div class="spinner"></div>
            Running inference on HuggingFace Space… (this can take 30-90 s)
          </div>`;

    pollInterval = setInterval(() => pollResult(jobId), 5000); // 5secs
  } catch (err) {
    showError(err.message);
    resetBtn();
  }
});

async function pollResult(jobId) {
  try {
    const res = await fetch(`/result/${jobId}/`);
    const json = await res.json();

    if (json.status === "done" && json.result_url) {
      clearInterval(pollInterval);
      showResult(json.result_url);
      resetBtn();
    } else if (json.status === "error") {
      clearInterval(pollInterval);
      showError(
        json.error ||
          "Inference failed. The HuggingFace Space may be sleeping — try again in a moment."
      );
      resetBtn();
    }
    // status === 'queued' or 'running' → keep polling
  } catch (err) {
    clearInterval(pollInterval);
    showError("Lost connection while polling. Please try again.");
    resetBtn();
  }
}

function showResult(url) {
  statusArea.innerHTML = `
        <div class="result-wrap">
          <p class="result-label">Your try-on result</p>
          <img class="result-img" src="${url}" alt="Virtual try-on result" />
          <div class="result-actions">
            <a class="btn-outline" href="${url}" download="mydressr-result.png">Download</a>
            <button class="btn-outline" onclick="resetForm()">Try another</button>
          </div>
        </div>`;
}

function showError(msg) {
  statusArea.innerHTML = `
        <div class="error-box">
          <strong>Something went wrong.</strong> ${msg}
        </div>`;
}

function resetBtn() {
  submitBtn.disabled = false;
  submitBtn.textContent = "Try it on →";
}

function resetForm() {
  form.reset();
  ["avatar-card", "garment-card"].forEach((id) =>
    document.getElementById(id).classList.remove("has-file")
  );
  statusArea.style.display = "none";
  statusArea.innerHTML = "";
}
