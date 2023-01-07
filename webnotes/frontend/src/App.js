import React from "react";
// import logo from './logo.svg';
import './App.css';
import axios from "axios";
import {BrowserRouter, Link, Navigate, Route, Routes} from "react-router-dom";
import Cookies from "universal-cookie";
import TodoForm from "./components/TodoForm";
import UserList from "./components/User";
import ProjectList from "./components/Project";
import TodoList from "./components/Todo";
import TodosUser from "./components/TodosUser";
import NotFound404 from "./components/NotFound404";
import ProjectDetail from "./components/ProjectDetail";
import LoginForm from "./components/Auth";


// класс App наследуем от React.Component
class App extends React.Component {
    constructor(props) {  // в конструктор класса передаём объект props
        super(props);  // вызываем родительский конструктор
        this.state = {  // это объект состояния компонента
            users: [],  // хранит массив users кот получим с backend
            projects: [],
            todos: [],
            auth: {username: '', is_login: false}
        }
    }

    login(username, password) {
        axios.post('http://127.0.0.1:8000/api/token/',
            {username: username, password: password}).then(response => {
            // сохраняем в cookies:
            const cookies = new Cookies()
            cookies.set('access', response.data.access)  // response.data - данные с back-end
            cookies.set('refresh', response.data.refresh)  // оба токена будем хранить в cookies
            localStorage.setItem('login', username)  // а имя юзера в localStorage
            // сохраняем юзера в состояние(чтобы потом отобразить имя) и флаг:
            this.setState({auth: {username: username, is_login: true}}, () => this.load_data())
        }).catch(error => {
            error.response.status === 401 ? alert('Неверный логин или пароль') : console.log(error)
        })

    }

    logout() {  // обнуляем все:
        this.setState({
            auth: {username: '', is_login: false},
            users: [],
            todos: [],
            projects: []
        }, () => this.load_data())
        const cookies = new Cookies()
        cookies.set('access', '')
        cookies.set('refresh', '')
        localStorage.setItem('login', '')
    }

    get_headers() {
        const cookies = new Cookies()
        const headers = {'Content-Type': 'application/json'}
        // если юзер залогинился, добавляем access-токен в заголовки:
        if (this.state.auth.is_login) {
            const token = cookies.get('access')
            headers['Authorization'] = 'Bearer ' + token
        }
        return headers
    }


    deleteTodo(id) {
        const headers = this.get_headers()
        axios.delete(`http://127.0.0.1:8000/api/todos/${id}`, {headers})
            .then(() => {
                // в состояние записываем все кроме удаленной:
                // this.setState({todos: this.state.todos.filter((item) => item.id !== id)})
                // }).catch(error => console.log(error))
                this.load_data()
            }).catch(error => {
            console.log(error)
            this.setState({todos: []})  // если ошибка то список пустой
        })
    }

    deleteProject(id) {
        const headers = this.get_headers()
        axios.delete(`http://127.0.0.1:8000/api/projects/${id}`, {headers})
            .then(() => {
                this.load_data()
            }).catch(error => {
            console.log(error)
            this.setState({projects: []})
        })
    }

    createTodo(name, author, project, content) {
        const headers = this.get_headers()
        const data = {name: name, by_user: author, by_project: project, content: content}
        axios.post(`http://127.0.0.1:8000/api/todos/`, data, {headers})
            .then(response => {
                let new_todo = response.data
                // заменим id на объект:
                new_todo.by_user = this.state.users.filter((item) => item.id === new_todo.by_user)[0]
                new_todo.by_project = this.state.projects.filter((item) => item.id === new_todo.by_project)[0]
                this.setState({todos: [...this.state.todos, new_todo]})
            }).catch(error => console.log(error))
    }

    load_data() {
        // const cookies = new Cookies()
        // const headers = {'Content-Type': 'application/json'}
        // // если юзер залогинился, добавляем access-токен в заголовки:
        // if (this.state.auth.is_login) {
        //     const token = cookies.get('access')
        //     headers['Authorization'] = 'Bearer ' + token
        // }
        const headers = this.get_headers()

        // передаем заголовки в каждый запрос:
        axios.get('http://127.0.0.1:8000/api/users/', {headers})  // контроллер под users
            .then(response => {
                this.setState(  // меняем состояние App, передаем данные users
                    {
                        'users': response.data
                    })
            }).catch(error => console.log(error))


        axios.get('http://127.0.0.1:8000/api/projects/', {headers})  // контроллер под projects
            .then(response => {
                this.setState(  // меняем состояние App, передаем данные projects
                    {
                        'projects': response.data
                    })
                // console.log(this.state)
            }).catch(error => console.log(error))


        axios.get('http://127.0.0.1:8000/api/todos/', {headers})  // контроллер под todos
            .then(response => {
                this.setState(  // меняем состояние App, передаем данные projects
                    {
                        'todos': response.data
                    })
            }).catch(error => console.log(error))
    }

    componentDidMount() {
        // вызывается при монтировании компонента на страницу
        const username = localStorage.getItem('login')
        if (username !== '') {
            this.setState({auth: {username: username, is_login: true}}, () => this.load_data())
        }
    }


    render()  // отрисовка компонента(пока один тег div)
    {
        return (
            <div className="App">
                <BrowserRouter>
                    {/*nav>li*3>link*/}
                    <nav>
                        <ul>{this.state.auth.username}</ul>
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
                        <li>
                            {this.state.auth.is_login ? <button onClick={() => this.logout()}>Выйти</button> :
                                <Link to='/login'>Войти</Link>
                            }
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
                            <Route index element={<ProjectList projects={this.state.projects} deleteProject={
                                (id) => this.deleteProject(id)}/>
                            }/>
                            <Route path=':projectId' element={<ProjectDetail projects={this.state.projects}/>}/>
                        </Route>

                        <Route exact path='/todos' element={<TodoList todos={this.state.todos} deleteTodo={
                            (id) => this.deleteTodo(id)}/>
                        }/>
                        <Route exact path='/todos/create'
                               element={<TodoForm
                                   createTodo={(name, author, project, content) =>
                                       this.createTodo(name, author, project, content)}/>}/>

                        <Route exact path='/login' element={<LoginForm login={(username, password) =>
                            this.login(username, password)}/>}/>
                        {/*передали get_token в компонент LoginForm чтобы вызвать его после отправки формы*/}

                        {/* если сюда дойдет то страница не существует - отработает: */}
                        <Route path='*' element={<NotFound404/>}/>
                    </Routes>
                </BrowserRouter>
            </div>
        )
    }
}

export default App;  // экспорт компонента для др модулей

