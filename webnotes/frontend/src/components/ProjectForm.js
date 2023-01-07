import React from "react";


class ProjectForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {name: '', users: ''}
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    handleSubmit(event) {
        this.props.createProject(this.state.name, this.state.users)
    }

}