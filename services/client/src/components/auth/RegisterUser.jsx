import React from "react";

const RegisterUser = (props) => {
  return (
    <div className="ui container">
      <div className="ui relaxed divided padded full grid">
        <div className="row">
          <div className="ui huge header">Sign-Up</div>
        </div>
        <div className="ui divider"></div>
        <div className="row">
          <div className="eleven wide column">
            <form className="ui form">
              <div className="field">
                <label>Username</label>
                <input type="text" placeholder="Enter your username" />
              </div>
              <div className="field">
                <label>Email</label>
                <input type="email" placeholder="Enter your email" />
              </div>
              <div className="field">
                <label>Password</label>
                <input type="password" placeholder="Enter your Password" />
              </div>
              <button class="ui green button" type="submit">
                Submit
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterUser;
