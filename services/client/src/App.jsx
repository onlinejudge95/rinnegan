import React from "react";
import { Route, Switch } from "react-router-dom";
import axios from "axios";
import UserList from "./components/UserList";
import AddUser from "./components/AddUser";
import About from "./components/About";
import NavBar from "./components/NavBar";
import RegisterForm from "./components/RegisterForm";
import LoginForm from "./components/LoginForm";

class App extends React.Component {
  state = {
    users: [],
    username: "",
    email: "",
    password: "",
    title: "Sentimental",
  };

  addUser = (event) => {
    event.preventDefault();
    const headers = {
      Accept: "application/json",
      "Content-Type": "application/json",
    };

    const data = {
      username: this.state.username,
      email: this.state.email,
      password: this.state.password,
    };

    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data, {
        headers,
      })
      .then((response) => {
        console.log(response);
        this.getUsers();
        this.setState({ username: "", email: "", password: "" });
      })
      .catch((err) => console.log(err));
  };

  componentDidMount() {
    this.getUsers();
  }

  getUsers = () => {
    const headers = { Accept: "application/json" };

    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, { headers })
      .then((response) => {
        this.setState({ users: response.data });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  onHandleChange = (event) => {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  };

  render() {
    return (
      <div>
        <NavBar title={this.state.title} />
        <section className="section">
          <div className="container">
            <div className="columns">
              <div className="column is-half">
                <br />
                <Switch>
                  <Route
                    path="/"
                    exact
                    render={() => {
                      return (
                        <div>
                          <h1 className="title is-1">Sentimental</h1>
                          <hr />
                          <br />
                          <AddUser
                            addUser={this.addUser}
                            username={this.state.username}
                            email={this.state.email}
                            password={this.state.password}
                            handleChange={this.onHandleChange}
                          />
                          <br />
                          <br />
                          <UserList users={this.state.users} />
                        </div>
                      );
                    }}
                  />
                  <Route path="/about" component={About} exact />
                  <Route path="/register" component={RegisterForm} exact />
                  <Route path="/login" component={LoginForm} exact />
                </Switch>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default App;
