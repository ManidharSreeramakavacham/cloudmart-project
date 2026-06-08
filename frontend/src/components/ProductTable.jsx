function ProductTable({ products }) {

  return (

    <div className="table-container">

      <div className="table-toolbar">

        <button>Add Product</button>

        <input
          type="text"
          placeholder="Search products..."
        />

      </div>

      <table className="product-table">

        <thead>

          <tr>

            <th>ID</th>
            <th>Name</th>
            <th>Quantity</th>
            <th>Price</th>

          </tr>

        </thead>

        <tbody>

          {products.map((product) => (

            <tr key={product.id}>

              <td>{product.id}</td>
              <td>{product.name}</td>
              <td>{product.quantity}</td>
              <td>₹{product.price}</td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  )
}

export default ProductTable