import React from "react";
// import logo from './logo.svg';
import './App.css';
import UserList from "./components/User";
import axios from "axios";
import ProjectList from "./components/Project";
import TodoList from "./components/Todo";
import TodosUser from "./components/TodosUser";
import NotFound404 from "./components/NotFound404";
import {Routes, Route, BrowserRouter, Link, Navigate} from "react-router-dom";
import ProjectDetail from "./components/ProjectDetail";


// класс App наследуем от React.Component
// компонент App имеет состояние, остальные нет
class App extends React.Component {
    constructor(props) {  // в конструктор класса передаём объект props
        super(props);  // вызываем родительский конструктор
        this.state = {  // это объект состояния компонента
            'users': [],  // хранит массив users кот получим с backend
            'projects': [],
            'todos': []
        }
    }

    componentDidMount() {
        // вызывается при монтировании компонента на страницу
        // response.data - данные с back-end - список юзеров
        axios.get('http://127.0.0.1:8000/api/users/')  // контроллер под users
            .then(response => {
                const users = response.data
                this.setState(  // меняем состояние App, передаем данные users
                    {
                        'users': users
                    })
            }).catch(error => console.log(error))

        axios.get('http://127.0.0.1:8000/api/projects/')  // контроллер под projects
            .then(response => {
                this.setState(  // меняем состояние App, передаем данные projects
                    {
                        'projects': response.data
                    })
            }).catch(error => console.log(error))

        axios.get('http://127.0.0.1:8000/api/todos/')  // контроллер под todos
            .then(response => {
                this.setState(  // меняем состояние App, передаем данные projects
                    {
                        'todos': response.data
                    })
            }).catch(error => console.log(error))
    }

    render()  // отрисовка компонента(пока один тег div)
    {
        return (
            <div className="App">
                <BrowserRouter>
                    {/*nav>li*3>link*/}
                    <nav>
                        <li>
                            {/*Link - компонент как тэг <a> но не передает запрос на сервер */}
                            <Link to='/'>Users</Link>
                        </li>
                        <li>
                            <Link to='/projects'>Projects</Link>
                        </li>
                        <li>
                            <Link to='/todos'>Todos</Link>
                        </li>
                    </nav>
                    <Routes>
                        {/* если / то попадем на /users  */}
                        <Route exact path='/' element={<Navigate to='/users'/>}/>
                        <Route path='/users'>
                            <Route index element={<UserList users={this.state.users}/>}/>
                            <Route path=':userId' element={<TodosUser todos={this.state.todos}/>}/>
                        </Route>

                        <Route path='/projects'>
                            <Route index element={<ProjectList projects={this.state.projects}/>}/>
                            <Route path=':projectId' element={<ProjectDetail projects={this.state.projects}/>}/>
                        </Route>
                        {/*<Route exact path='/projects' element={<ProjectList projects={this.state.projects}/>}/>*/}
                        <Route exact path='/todos' element={<TodoList todos={this.state.todos}/>}/>

                        {/* если сюда дойдет то страница не существует, и отработает: */}
                        <Route path='*' element={<NotFound404/>}/>
                    </Routes>
                </BrowserRouter>
            </div>
        )
    }
}

export default App;  // экспорт компонента для др модулей

