import React from "react";

const Avatar = ({ name, size = 40 }) => {
  const initials = (name || "A").split(" ").map(s => s[0]).slice(0,2).join("").toUpperCase();
  return (
    <div style={{ width: size, height: size }} className="rounded-full bg-white border border-primary text-primary flex items-center justify-center font-bold">
      {initials}
    </div>
  );
};

export default Avatar;
