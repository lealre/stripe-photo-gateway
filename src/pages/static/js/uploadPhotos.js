const selectedFiles = [];

function handleFileSelect(event) {
  const previewContainer = document.getElementById("preview-container");
  previewContainer.innerHTML = "";
  selectedFiles.length = 0;

  const files = event.target.files;

  Array.from(files).forEach((file, index) => {
    const reader = new FileReader();

    reader.onload = function (e) {
      selectedFiles.push({ file, base64: e.target.result });

      const previewItem = document.createElement("div");
      previewItem.classList.add("preview-item");

      previewItem.innerHTML = `
                        <img src="${e.target.result}" alt="Photo Preview">
                        <div>
                            <label for="quantity-${index}">Quantity:</label>
                            <input 
                                type="number" 
                                id="quantity-${index}" 
                                name="quantity-${index}" 
                                data-index="${index}" 
                                min="1" 
                                max="100" 
                                value="1" 
                                onchange="updatePrice()"
                                required>
                        </div>
                    `;

      previewContainer.appendChild(previewItem);
      updatePrice();
    };

    reader.readAsDataURL(file);
  });
}

function updatePrice() {
  const meta = document.getElementById("my-data");
  const unitPrice = parseFloat(meta.dataset.unitPrice);

  let totalPrice = 0;
  let totalPhotos = 0;

  selectedFiles.forEach((file, index) => {
    const quantityInput = document.querySelector(`#quantity-${index}`);
    const quantity = quantityInput ? parseInt(quantityInput.value) : 1;

    totalPrice += quantity * unitPrice;
    totalPhotos += quantity;
  });

  document.getElementById("total-price").textContent = totalPrice.toFixed(2);
  document.getElementById("total-photos").textContent = totalPhotos;
}

function submitForm() {
  const formData = { photos: [] };

  selectedFiles.forEach((file, index) => {
    const quantityInput = document.querySelector(`#quantity-${index}`);
    const quantity = quantityInput ? parseInt(quantityInput.value) : 1;

    formData.photos.push({
      fileName: file.file.name,
      fileType: file.file.type,
      base64: file.base64,
      quantity: quantity,
    });
  });

  console.log("Sending form data:", formData);

  fetch("/orders/upload/photos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  })
    .then((response) => {
      if (response.ok) {
        console.log("Success:", response);
        window.location.href = "/order/details";
      } else {
        throw new Error("Failed to upload");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Failed to upload photos.");
    });
}
