import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
const API_BASE_URL = import.meta.env.VITE_BACKEND_URL;
interface PayPalCheckoutProps {
  amount: number;
}

const PayPalCheckout = ({ amount }: PayPalCheckoutProps) => {
  const PAYPAL_CLIENT_ID =
    import.meta.env.VITE_PAYPAL_CLIENT_ID || "YOUR_PAYPAL_CLIENT_ID";

  return (
    <PayPalScriptProvider
      options={{
        clientId: PAYPAL_CLIENT_ID,
        currency: "CAD",
      }}
    >
      <PayPalButtons
        style={{ layout: "horizontal" }}
        createOrder={(_data, actions) => {
          return actions.order!.create({
            intent: "CAPTURE",
            purchase_units: [
              {
                amount: {
                  currency_code: "CAD",
                  value: amount.toFixed(2),
                },
              },
            ],
          });
        }}
        onApprove={(_data, actions) => {
          return actions.order!.capture().then((details) => {
            console.log(
              "Transaction completed by: ",
              details?.payer?.name?.given_name
            );

            // Send transaction details to Flask backend
            fetch(`${API_BASE_URL}/paypal/capture`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ orderID: details.id }),
            })
              .then((response) => response.json())
              .then((data) => console.log("Server response:", data))
              .catch((error) => console.error("Error:", error));
          });
        }}
      />
    </PayPalScriptProvider>
  );
};

export default PayPalCheckout;
