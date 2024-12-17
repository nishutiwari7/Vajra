document.getElementById("payment-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const amount = document.getElementById("amount").value;
    const currency = document.getElementById("currency").value;
    const payer = document.getElementById("payer").value;

    const orderResponse = await fetch("/create_order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount, currency, payer }),
    });

    const orderData = await orderResponse.json();

    if (orderData.error) {
        alert("Error creating order: " + orderData.error);
        return;
    }

    const paymentLinkResponse = await fetch(`/payment_link?currency=${currency}`);
    const paymentLinkData = await paymentLinkResponse.json();

    if (paymentLinkData.payment_link) {
        window.location.href = paymentLinkData.payment_link;
    } else {
        alert("Error: " + paymentLinkData.error);
    }
});
