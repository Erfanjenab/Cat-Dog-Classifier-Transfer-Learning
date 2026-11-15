const imageInput = document.getElementById("imageInput");
const browseButton = document.getElementById("browseButton");
const dropZone = document.getElementById("dropZone");
const emptyState = document.getElementById("emptyState");
const previewState = document.getElementById("previewState");
const imagePreview = document.getElementById("imagePreview");
const fileName = document.getElementById("fileName");
const predictButton = document.getElementById("predictButton");
const removeButton = document.getElementById("removeButton");
const message = document.getElementById("message");
const resultSection = document.getElementById("resultSection");

let selectedFile = null;
let previewUrl = null;

function setMessage(text = "") {
  message.textContent = text;
}

function clearResult() {
  resultSection.hidden = true;
}

function showSelectedFile(file) {
  if (!file) return;
  const allowed = ["image/jpeg", "image/png", "image/webp"];
  if (!allowed.includes(file.type)) {
    setMessage("Please select a JPG, PNG, or WEBP image.");
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    setMessage("This file is larger than 10 MB.");
    return;
  }

  selectedFile = file;
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = URL.createObjectURL(file);
  imagePreview.src = previewUrl;
  emptyState.hidden = true;
  previewState.hidden = false;
  fileName.textContent = file.name;
  predictButton.disabled = false;
  setMessage();
  clearResult();
}

function resetSelection() {
  selectedFile = null;
  imageInput.value = "";
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  imagePreview.removeAttribute("src");
  previewState.hidden = true;
  emptyState.hidden = false;
  fileName.textContent = "No image selected";
  predictButton.disabled = true;
  setMessage();
  clearResult();
}

browseButton.addEventListener("click", (event) => {
  event.stopPropagation();
  imageInput.click();
});
dropZone.addEventListener("click", (event) => {
  if (event.target.closest("button")) return;
  imageInput.click();
});
dropZone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    imageInput.click();
  }
});
imageInput.addEventListener("change", () => showSelectedFile(imageInput.files[0]));
removeButton.addEventListener("click", (event) => {
  event.stopPropagation();
  resetSelection();
});

["dragenter", "dragover"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.add("dragover");
  });
});
["dragleave", "drop"].forEach((eventName) => {
  dropZone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropZone.classList.remove("dragover");
  });
});
dropZone.addEventListener("drop", (event) => {
  const file = event.dataTransfer.files[0];
  showSelectedFile(file);
});

function displayResult(data) {
  const cat = Number(data.probabilities.Cat ?? data.probabilities.cat ?? 0);
  const dog = Number(data.probabilities.Dog ?? data.probabilities.dog ?? 0);
  const isCat = data.class_name.toLowerCase() === "cat";

  document.getElementById("predictedClass").textContent = data.class_name;
  document.getElementById("resultEmoji").textContent = isCat ? "🐱" : "🐶";
  document.getElementById("confidenceValue").textContent = `${data.confidence}%`;
  document.getElementById("catValue").textContent = `${cat}%`;
  document.getElementById("dogValue").textContent = `${dog}%`;
  document.getElementById("catBar").style.width = `${Math.min(100, Math.max(0, cat))}%`;
  document.getElementById("dogBar").style.width = `${Math.min(100, Math.max(0, dog))}%`;
  resultSection.hidden = false;
}

predictButton.addEventListener("click", async () => {
  if (!selectedFile) return;
  const formData = new FormData();
  formData.append("image", selectedFile);

  predictButton.disabled = true;
  predictButton.classList.add("loading");
  setMessage("Sending your image to the model...");
  clearResult();

  try {
    const response = await fetch("/predict", { method: "POST", body: formData });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Prediction failed.");
    displayResult(data);
    setMessage();
  } catch (error) {
    setMessage(error.message || "Something went wrong. Please try again.");
  } finally {
    predictButton.disabled = !selectedFile;
    predictButton.classList.remove("loading");
  }
});
