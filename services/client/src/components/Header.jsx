import React from "react";
import { Link } from "react-router-dom";

const Header = () => {
  return (
    <div className="ui inverted pointing attached menu">
      <Link to="/" className="item">
        Rinnegan
      </Link>
      <Link to="/profile" className="item">
        Profile
      </Link>
      <div className="right menu">
        <Link to="/register" className="item">
          Sign-Up
        </Link>
        <Link to="/login" className="item">
          Sign-In
        </Link>
      </div>
    </div>
  );
};

export default Header;
