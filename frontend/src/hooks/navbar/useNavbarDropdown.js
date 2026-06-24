import { useState, useEffect } from "react";

export const useNavbarDropdown = () => {
  const [open, setOpen] = useState(false);

  const toggle = () => setOpen((prev) => !prev);
  const close = () => setOpen(false);

  // Close dropdown
  useEffect(() => {
    const handleClick = (e) => {
      if (!e.target.closest(".navbar-user")) {
        close();
      }
    };

    document.addEventListener("click", handleClick);
    return () => document.removeEventListener("click", handleClick);
  }, []);

  return {
    open,
    toggle,
    close,
  };
};
