import React from "react";
import {useParams} from "react-router-dom";

class ProjectForm extends React.Component {
    constructor(props) {
        super(props)
        this.state = {name: '', users: [], repo_url: '', is_active: 1}
    }

    handleUsersChange(event) {
        if (!event.target.selectedOptions) {
            this.setState({
                'users': []
            })
            return;
        }
        let participants = []
        for (let i = 0; i < event.target.selectedOptions.length; i++) {
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
        if (this.props.updateProject) {
            let project_id = this.props.params['projectId']
            this.setState({'id': project_id}, () =>
            {this.props.updateProject(this.state.id, this.state.name, this.state.users,
                this.state.repo_url, this.state.is_active)} // колбеком чтобы обновилось состояние
            )
        } else {
            this.props.createProject(this.state.name, this.state.users,
                this.state.repo_url, this.state.is_active)
        }
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
                    <select multiple={true} name="participants" className="form-control"
                            onChange={(event) => this.handleUsersChange(event)}>
                        {this.props.participants.map((item) => <option key={item.id}
                                                                       value={item.id}>{item.username}</option>)}
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="repo_url">repo_url</label>
                    <input type="text" className="form-control" name="repo_url" value={this.state.repo_url}
                           onChange={(event) => this.handleChange(event)}/>
                </div>
                <div className="form-group">
                    <label htmlFor="is_active">is_active</label>
                    <input type="text" className="form-control" name="is_active" value={this.state.is_active}
                           onChange={(event) => this.handleChange(event)}/>
                </div>
                <input type="submit" className="btn btn-primary" value="Save"/>
            </form>
        )
    }

}

// export default ProjectForm
export default (props) =>
    <ProjectForm
        {...props}
        params={useParams()}
    />  // т к классовый компонент не дает юзать хуки
