import React from "react";
import { Redirect, Link } from "react-router-dom";
import { PropTypes } from "prop-types";

const CreateKeyword = (props) => {
  if (!props.isAuthenticated()) {
    return <Redirect to="/login" />;
  }

  return <div>Hello</div>;
};

CreateKeyword.propTypes = {
  user: PropTypes.object,
  onAddKeywordFormSubmit: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.func.isRequired,
};

export default CreateKeyword;
