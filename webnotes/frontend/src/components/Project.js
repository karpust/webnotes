import React from 'react';

const ProjectItem = ({project}) => {
    return (
        <tr>
            <td>{project.id}</td>
            <td>{project.name}</td>
            <td>{project.repo_url}</td>
            <td>{project.users}</td>
            <td>{project.is_active}</td>
        </tr>
    )
}


const ProjectList = ({projects}) => {
    return (
        <table>
            <thead>
            <tr>
                <th>ID</th>
                <th>NAME</th>
                <th>REPO_URL</th>
                <th>USERS</th>
                <th>IS_ACTIVE</th>
            </tr>
            </thead>
            <tbody>
            {projects.map((project) => <ProjectItem project={project}/>)}
            </tbody>
        </table>
    )
}

export default ProjectList