import React from "react";
import {
  Button,
  Divider,
  Header,
  Form,
  Input,
  Container,
  Checkbox,
} from "semantic-ui-react";

const RemoveUser = () => {
  return (
    <main className="content">
      <Container>
        <div class="ui relaxed divided padded full grid">
          <div class="row">
            <div class="column">
              <Header as="h1">Remove Account</Header>
            </div>
          </div>
          <Divider />
          <div class="row">
            <div class="eleven wide column">
              <p>
                All your account related information will be removed from our
                servers. Note that this is an irreversible change.
              </p>
              <Form>
                <Form.Field>
                  <label>Password</label>
                  <Input placeholder="Password" type="password" />
                </Form.Field>
                <Form.Field>
                  <Checkbox label="I agree" />
                </Form.Field>
                <Button type="submit" color="green">
                  Submit
                </Button>
              </Form>
            </div>
          </div>
        </div>
      </Container>
    </main>
  );
};

export default RemoveUser;
