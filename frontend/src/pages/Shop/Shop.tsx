import "./Shop.css";
import PostDisplayWrap from "../../components/PostDisplayWrap/PostDisplayWrap";
import { useState } from "react";

interface FilterState {
  minPrice: string;
  maxPrice: string;
  category: string;
  designer: string;
}

export default function Shop() {
  const [filters, setFilters] = useState<FilterState>({
    minPrice: "",
    maxPrice: "",
    category: "all",
    designer: "all",
  });

  const handleFilterChange = (filterType: keyof FilterState, value: string) => {
    setFilters((prev) => ({
      ...prev,
      [filterType]: value,
    }));
  };

  const handlePriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    // Only allow numbers and empty string
    if (value === "" || /^\d+$/.test(value)) {
      handleFilterChange(name as "minPrice" | "maxPrice", value);
      console.log("Price filter updated:", name, value);
    }
  };

  return (
    <div className="shop-container">
      <div className="filter-sidebar">
        <h2 className="filter-title">Filters</h2>

        <div className="filter-section">
          <h3>Price Range</h3>
          <div className="price-inputs">
            <div className="price-input-group">
              <label>Min $</label>
              <input
                type="text"
                name="minPrice"
                value={filters.minPrice}
                onChange={handlePriceChange}
                placeholder="0"
              />
            </div>
            <div className="price-input-group">
              <label>Max $</label>
              <input
                type="text"
                name="maxPrice"
                value={filters.maxPrice}
                onChange={handlePriceChange}
                placeholder="1000+"
              />
            </div>
          </div>
        </div>

        <div className="filter-section">
          <h3>Category</h3>
          <select
            value={filters.category}
            onChange={(e) => handleFilterChange("category", e.target.value)}
          >
            <option value="all">All Categories</option>
            <option value="tops">Tops</option>
            <option value="bottoms">Bottoms</option>
            <option value="outerwear">Outerwear</option>
            <option value="accessories">Accessories</option>
          </select>
        </div>

        <div className="filter-section">
          <h3>Designer</h3>
          <select
            value={filters.designer}
            onChange={(e) => handleFilterChange("designer", e.target.value)}
          >
            <option value="all">All Designers</option>
            <option value="nike">Nike</option>
            <option value="adidas">Adidas</option>
            <option value="puma">Puma</option>
          </select>
        </div>
      </div>

      <div className="posts-container">
        <PostDisplayWrap filters={filters} />
      </div>
    </div>
  );
}
