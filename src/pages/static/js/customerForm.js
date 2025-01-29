function submitOrderForm(event) {
  event.preventDefault();

  const address = document.getElementById("address").value;
  const city = document.getElementById("city").value;
  const postalCode = document.getElementById("postal-code").value;
  const phoneNumber = document.getElementById("contact-info").value;
  const email = document.getElementById("email").value;

  if (!address || !city || !postalCode || !phoneNumber || !email) {
    alert("All fields are required.");
    return;
  }

  const formData = {
    address,
    city,
    postalCode,
    phoneNumber,
  };

  fetch("/orders/address/validate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.is_validated === true) {
        const checkoutFormData = {
          ...formData,
          customerEmail: email,
          formattedAddress: data.formatted_address,
        };
        console.log(checkoutFormData);
        return checkoutSession(checkoutFormData);
      } else {
        alert(data.message || "Could not validate address");
      }
    });
}

function checkoutSession(formData) {
  fetch("/orders/checkout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
    credentials: "same-origin",
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Failed to upload");
      }
    })
    .then((data) => {
      window.location.href = data;
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred while processing your order.");
    });
}
