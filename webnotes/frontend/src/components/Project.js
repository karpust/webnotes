import React from 'react';
import {Link} from "react-router-dom";


const ProjectItem = ({project, deleteProject}) => {
    return (
        <tr>
            <td>{project.id}</td>
            <td>
                <Link to={`/projects/${project.id}`}>{project.name}</Link>
            </td>
            <td>{project.repo_url}</td>
            <td>{project.users}</td>
            <td>{project.is_active}</td>
            <td>
                <button onClick={() => deleteProject(project.id)} type='button'>Delete</button>
                {/*<button onClick={() => detailProject(project.id)} type='button'>Update</button>*/}
                <Link to={`/projects/${project.id}/update`} className="btn btn-info">Update</Link>
            </td>
        </tr>
    )
}


const ProjectList = ({projects, deleteProject}) => {
    return (
        <div>
            <table>
                <thead>
                <tr>
                    <th>ID</th>
                    <th>NAME</th>
                    <th>REPO_URL</th>
                    <th>USERS</th>
                    <th>IS_ACTIVE</th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {projects.map((project) => <ProjectItem key={project.id} project={project} deleteProject={deleteProject}/>)}
                </tbody>
            </table>
            <Link to='/projects/create'>Create</Link>
        </div>

    )
}

export default ProjectList