import React from "react";
import { BrowserRouter, Route } from "react-router-dom";
import RegisterUser from "./auth/RegisterUser";
import Loginuser from "./auth/LoginUser";
import ShowUser from "./user/ShowUser";
import RemoveUser from "./user/RemoveUser";
import UpdateUser from "./user/UpdateUser";
import About from "./About";

const App = () => {
  return (
    <div>
      <BrowserRouter>
        <div>
          <Route path="/" exact component={About}></Route>
          <Route path="/register" exact component={RegisterUser}></Route>
          <Route path="/login" exact component={Loginuser}></Route>
          <Route path="/home" exact component={ShowUser}></Route>
          <Route path="/update" exact component={UpdateUser}></Route>
          <Route path="/remove" exact component={RemoveUser}></Route>
        </div>
      </BrowserRouter>
    </div>
  );
};

export default App;
