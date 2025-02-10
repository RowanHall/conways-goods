import { useCart } from "../../context/CartContext";
import "./Cart.css";
import Carousel from "../../components/Carousel/Carousel";

export default function Cart() {
  const { items, removeFromCart, total } = useCart();

  const handlePurchase = () => {
    alert("Purchase functionality coming soon!");
  };

  if (items.length === 0) {
    return <div className="cart-empty">Your cart is empty</div>;
  }

  return (
    <>
      <div className="cart-container">
        <h1 className="cart-title">Cart</h1>
        <div className="cart-items">
          {items.map((item) => (
            <div key={item.id} className="cart-item">
              <img
                src={item.image}
                alt={item.title}
                className="cart-item-image"
              />
              <div className="cart-item-details">
                <div className="item-info">
                  <h3 className="itm-title">{item.title}</h3>
                  <p className="itm-price">${item.price}</p>
                </div>
                <span
                  className="remove-button material-symbols-outlined"
                  onClick={() => removeFromCart(item.id)}
                >
                  delete
                </span>
              </div>
            </div>
          ))}
        </div>
        <div className="cart-summary">
          <h2 className="total-price">Total: ${total.toFixed(2)}</h2>
          <button className="purchase-button" onClick={handlePurchase}>
            Purchase
          </button>
        </div>
      </div>
      <Carousel />
    </>
  );
}
