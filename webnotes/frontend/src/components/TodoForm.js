import React from "react";


class TodoForm extends React.Component {
    constructor(props) {
        super(props)
        // by_user: props.authors[0].id - первый элем выпадающего списка
        this.state = {name: '', by_user: props.authors[0].id, by_project: props.projects[0].id, content: ''}
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    handleSubmit(event) {
        // console.log(this.state.name)
        // console.log(this.state.by_user)
        this.props.createTodo(this.state.name, this.state.author, this.state.project, this.state.content)
        event.preventDefault()
    }

    render() {
        return (
            <form onSubmit={(event) => this.handleSubmit(event)}>
                <div className="form-group">
                    <label htmlFor="name">name</label>
                    <input type="text" className="form-control" name="name" value={this.state.name}
                           onChange={(event) => this.handleChange(event)}/>
                </div>
                <div className="form-group">
                    <label htmlFor="by_user">author</label>
                    <select name="author" className="form-control" onChange={(event) => this.handleChange(event)}>
                        {this.props.authors.map((item) => <option value={item.id}>{item.username}</option>)}
                    </select>
                    {/*<input type="number" className="form-control" name="by_user" value={this.state.by_user}*/}
                    {/*       onChange={(event) => this.handleChange(event)}/>*/}
                </div>
                <div className="form-group">
                    <label htmlFor="by_project">project</label>
                    <select name="project" className="form-control" onChange={(event) => this.handleChange(event)}>
                        {this.props.projects.map((item) => <option value={item.id}>{item.name}</option>)}
                    </select>
                    {/*<input type="number" className="form-control" name="by_project" value={this.state.by_project}*/}
                    {/*       onChange={(event) => this.handleChange(event)}/>*/}
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