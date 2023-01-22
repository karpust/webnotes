import React from 'react';
import {useParams} from "react-router-dom";

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

const
    ProjectDetail = ({projects}) => {
    let {projectId} = useParams()
    let project_detail = projects.filter((project) => project.id == projectId)
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
            {project_detail.map((project_) => <ProjectItem key={project_.id} project={project_}/>)}
            </tbody>
        </table>
    )
}

export default ProjectDetail