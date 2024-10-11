import React, { useState } from "react";
import "./Button.css";

type ButtonProps = {
  /** Chose the level of the button */
  type: "primary" | "secondary";
  /** Button contents */
  label: string;
  /** Optional click handler */
  onClick?: () => void;
  /** How large should the button be? Default: medium */
  size?: "small" | "medium" | "large";
};

const Button: React.FC<ButtonProps> = ({ type, label, size = "medium" }) => {
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width - 0.5) * 20; // Adjust the multiplier for range
    const y = ((e.clientY - rect.top) / rect.height - 0.5) * 20; // Adjust the multiplier for range
    setPosition({ x, y });
  };

  const handleMouseLeave = () => {
    setPosition({ x: 0, y: 0 });
  };

  return (
    <button
      className={`btn btn-${type} btn-${size}`}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={
        {
          "--x": `${position.x}px`,
          "--y": `${position.y}px`,
        } as React.CSSProperties
      }
    >
      {label}
    </button>
  );
};

export default Button;
