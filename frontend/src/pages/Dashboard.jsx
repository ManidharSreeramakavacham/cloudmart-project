import { useEffect, useState } from "react"

import Header from "../components/Header"
import Sidebar from "../components/Sidebar"
import DashboardCards from "../components/DashboardCards"
import ProductTable from "../components/ProductTable"

function Dashboard() {
    const [products, setProducts] = useState([])
    useEffect(() => {
        fetchProducts()
    }, [])

    const fetchProducts = async () => {
        const response = await fetch("/api/products")
        const data = await response.json()
        setProducts(data)
    }
    return (

    <div className="app">

        <Sidebar />

        <div className="main-content">

            <Header />

            <DashboardCards products={products} />

            <ProductTable products={products} />

        </div>

    </div>

)
}
export default Dashboard
