function DashboardCards({ products }) {

  const totalProducts = products.length

  const totalValue = products.reduce(
    (total, product) =>
      total + (product.quantity * product.price),
    0
  )

  const lowStock = products.filter(
    (product) => product.quantity <= 2
  ).length

  return (

    <div className="dashboard-cards">

      <div className="card">

        <h3>Total Products</h3>

        <p>{totalProducts}</p>

      </div>

      <div className="card">

        <h3>Inventory Value</h3>

        <p>₹{totalValue}</p>

      </div>

      <div className="card">

        <h3>Low Stock Items</h3>

        <p>{lowStock}</p>

      </div>

    </div>
  )
}

export default DashboardCards
