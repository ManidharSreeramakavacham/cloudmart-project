import { useEffect, useState } from "react";

function App() {

  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {

    try {

      const response = await fetch("http://127.0.0.1:8000/products");

      const data = await response.json();

      setProducts(data);

    } catch (error) {

      console.error("Error fetching products:", error);

    }

  };

  return (
    <div>

      <h1>CloudMart ERP</h1>

      <hr />

      <h2>Inventory Dashboard</h2>

      {products.map((product) => (

        <div key={product.id}>

          <h3>{product.name}</h3>

          <p>Quantity: {product.quantity}</p>

          <p>Price: ₹{product.price}</p>

          <hr />

        </div>

      ))}

    </div>
  );

}

export default App