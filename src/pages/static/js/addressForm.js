function submitOrderForm(event) {
  event.preventDefault();

  const address = document.getElementById("address").value;
  const city = document.getElementById("city").value;
  const postalCode = document.getElementById("postal-code").value;
  const phoneNumber = document.getElementById("contact-info").value;

  if (!address || !city || !postalCode || !phoneNumber) {
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
      console.log("Success:", data);
      if (data.is_validated === true) {
        window.location.href = "/";
      } else {
        alert(data.message || "Could not validate address");
      }
    });
}
