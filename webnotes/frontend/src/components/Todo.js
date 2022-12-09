import React from 'react';

const TodoItem = ({todo}) => {
    return (
        <tr>
            <td>{todo.id}</td>
            <td>{todo.name}</td>
            <td>{todo.content}</td>
            <td>{todo.publication_date}</td>
            <td>{todo.by_user}</td>
            <td>{todo.by_project}</td>
            <td>{todo.status}</td>
        </tr>
    )
}


const TodoList = ({todos}) => {
    return (
        <table>
            <thead>
            <tr>
                <th>ID</th>
                <th>NAME</th>
                <th>CONTENT</th>
                <th>PUBLICATION_DATE</th>
                <th>BY_USER</th>
                <th>BY_PROJECT</th>
                <th>STATUS</th>
            </tr>
            </thead>
            <tbody>
            {todos.map((todo_) => <TodoItem todo={todo_}/>)}
            </tbody>
        </table>
    )
}

export default TodoList