import React from "react";


class TodoForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {name: '', by_user: 0, by_project: 0, content: ''}
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    handleSubmit(event) {
        // console.log(this.state.name)
        // console.log(this.state.by_user)
        this.props.createTodo(this.state.name, this.state.by_user, this.state.by_project, this.state.content)
        event.preventDefault()
    }

    render() {
        return (
            <form onSubmit={(event) => this.handleSubmit(event)}>
                <div className="form-group">
                    <label htmlFor="login">name</label>
                    <input type="text" className="form-control" name="name" value={this.state.name}
                           onChange={(event) => this.handleChange(event)}/>
                </div>
                <div className="form-group">
                    <label htmlFor="by_user">author</label>
                    <input type="number" className="form-control" name="by_user" value={this.state.by_user}
                           onChange={(event) => this.handleChange(event)}/>
                </div>
                <div className="form-group">
                    <label htmlFor="by_project">project</label>
                    <input type="number" className="form-control" name="by_project" value={this.state.by_project}
                           onChange={(event) => this.handleChange(event)}/>
                </div>
                <div className="form-group">
                    <label htmlFor="text">content</label>
                    <input type="text" className="form-control" name="content" value={this.state.content}
                           onChange={(event) => this.handleChange(event)}/>
                </div>

                <input type="submit" className="btn btn-primary" value="Save"/>
            </form>
        );
    }
}

export default TodoForm