// frontend/src/hooks/navbar/useNavbarSearch.js
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export const useNavbarSearch = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
      setSearchQuery("");
    }
  };

  return {
    searchQuery,
    setSearchQuery,
    handleSearch,
  };
};
