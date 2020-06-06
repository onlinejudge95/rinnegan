import React from "react";
import { Button, Divider, Form, Input } from "semantic-ui-react";

const LoginUser = () => {
  return (
    <main className="content">
      <div className="ui container">
        <div class="ui relaxed divided padded full grid">
          <div class="row">
            <div class="column">
              <h1 class="ui header">
                <div class="content">Sign-In</div>
              </h1>
            </div>
          </div>
          <Divider />
          <div class="row">
            <div class="eleven wide column">
              <Form>
                <Form.Field>
                  <label>Email</label>
                  <Input placeholder="Email" type="email" />
                </Form.Field>
                <Form.Field>
                  <label>Password</label>
                  <Input placeholder="Password" type="password" />
                </Form.Field>
                <Button type="submit" color="green">
                  Submit
                </Button>
              </Form>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default LoginUser;
