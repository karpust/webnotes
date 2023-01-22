import React from 'react';
import {Link} from "react-router-dom";


const TodoItem = ({todo, deleteTodo}) => {
    return (
        <tr>
            <td>{todo.id}</td>
            <td>{todo.name}</td>
            <td>{todo.content}</td>
            <td>{todo.publication_date}</td>
            <td>{todo.by_user}</td>
            <td>{todo.by_project}</td>
            <td>{todo.status}</td>
            {/*<td><button type='button'>Delete</button></td>*/}
            {/*связываем функцию с нажатием на кнопку - callback:*/}
            <td><button onClick={() => deleteTodo(todo.id)} type='button'>Delete</button></td>
        </tr>
    )
}


const TodoList = ({todos, deleteTodo}) => {  // метод тоже передаем
    return (
        <div>
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
                <th></th>
            </tr>
            </thead>
            <tbody>
            {todos.map((todo_) => <TodoItem key={todo_.id} todo={todo_} deleteTodo={deleteTodo}/>)}
            </tbody>
        </table>
            <Link to='/todos/create'>Create</Link>
        </div>

    )
}

export default TodoList