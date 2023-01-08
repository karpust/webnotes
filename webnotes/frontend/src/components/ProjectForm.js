import React from "react";


class ProjectForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {name: '', users: []}
    }

    handleUsersChange(event) {
        if (!event.target.selectedOptions) {
            this.setState({
                'users': []
            })
            return;
        }
        let participants = []
        for(let i = 0; i < event.target.selectedOptions.length; i++) {
            participants.push(event.target.selectedOptions.item(i).value)
        }
        // console.log(users)
        this.setState(
            {'users': participants}
        )
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    handleSubmit(event) {
        this.props.createProject(this.state.name, this.state.users)
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
                    <label htmlFor="participants">participants</label>
                    <select multiple name="participants" className="form-control"
                            onChange={(event) => this.handleUsersChange(event)}>
                        {this.props.participants.map((item) => <option value={item.id}>{item.username}</option>)}
                    </select>
                </div>
                <input type="submit" className="btn btn-primary" value="Save"/>
            </form>
        )
    }

}

export default ProjectForm