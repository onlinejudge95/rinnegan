import React from "react";
import { Route, Switch } from "react-router-dom";
import RegisterUser from "./auth/RegisterUser";
import Loginuser from "./auth/LoginUser";
import ShowUser from "./user/ShowUser";
import RemoveUser from "./user/RemoveUser";
import UpdateUser from "./user/UpdateUser";
import About from "./About";
import NavBar from "./navbar/NavBar";

class App extends React.Component {
  onRegisterFormSubmit = () => {
    console.log("Register form submitted");
  };

  onLoginFormSubmit = () => {
    console.log("Login form submitted");
  };

  isAuthenticated = () => {
    return true;
  };

  render() {
    return (
      <div className="ui">
        <NavBar isAuthenticated={this.isAuthenticated} />
        <div className="ui container">
          <div className="ui segment">
            {/* TODO:- Display Messages */}
            <div className="ui grid">
              <div className="two wide column"></div>
              <div className="twelve wide column">
                <Switch>
                  <Route path="/" exact component={About} />
                  <Route
                    path="/register"
                    exact
                    component={() => (
                      <RegisterUser onFormSubmit={this.onRegisterFormSubmit} />
                    )}
                  />
                  <Route
                    path="/login"
                    exact
                    component={() => (
                      <Loginuser onFormSubmit={this.onLoginFormSubmit} />
                    )}
                  />
                  <Route path="/profile" exact component={() => <ShowUser />} />
                  <Route
                    path="/update"
                    exact
                    component={() => <UpdateUser />}
                  />
                  <Route
                    path="/remove"
                    exact
                    component={() => <RemoveUser />}
                  />
                </Switch>
              </div>
              <div className="two wide column"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
