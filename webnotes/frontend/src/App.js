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
import LoginForm from "./components/Auth";
import Cookies from "universal-cookie";


// класс App наследуем от React.Component
// компонент App имеет состояние, остальные нет
class App extends React.Component {
    constructor(props) {  // в конструктор класса передаём объект props
        super(props);  // вызываем родительский конструктор
        this.state = {  // это объект состояния компонента
            'users': [],  // хранит массив users кот получим с backend
            'projects': [],
            'todos': [],
            'token': ''
        }
    }

    get_headers() {  // метод добавляет токен в заголовки если юзер авторизован
        let headers = {
            'Content-Type': 'application/json'
        }
        if (this.is_authenticated()) {
            headers['Authorization'] = 'Bearer ' + this.state.access
        }  // словарь headers, ключ Authorization, значение - токен из состояния
        return headers
    }

    set_token(token) {  // метод принимает токен, помещает его в cookies и записывает в состояние приложения
        const cookies = new Cookies()
        cookies.set('access', token)  // установка токена в cookies, для сохранения юзера при закрытии браузера
        this.setState({'access': token}, () => this.load_data())
        // установка токена в состояние, для обновления при авторизации
        // указан callback кот срабатывает сразу после изменения состояния
        // чтобы данные не грузились раньше изменения состояния this.state.token

        // localStorage.setItem('token', token)  //  так сохранять токен в localStorage
    }

    is_authenticated() {  // определяет авторизован ли юзер
        return this.state.access != ''  // если да - токен не пустой
    }

    logout() {  // обнуляет токен, проекты и заметки
        this.set_token('')
        this.setState({todos: []})
        this.setState({projects: []})
        this.setState({users: []})
    }

    get_token_from_storage() {  // метод вызывается при открытии сайта: токен из cookies в состояние
        const cookies = new Cookies()
        const token = cookies.get('access')  // берет токен из куков
        this.setState({'access': token}, () => this.load_data())
    }

    get_token(username, password) {  // метод получает токен авторизации
        // методом post отправляем логин и пароль на адрес(на сервер авторизации):
        axios.post('http://127.0.0.1:8000/api/token/',
            {username: username, password: password}).then(response => {
            // методом set_token сохраняем токен в state и cookies:
            this.set_token(response.data['access'])
            console.log(response.data)
        }).catch(error => alert('Неверный логин или пароль'))
    }

    load_data() {
        const headers = this.get_headers()  // передаем заголовки в каждый запрос:
        // response.data - данные с back-end - список юзеров
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
        this.get_token_from_storage()
    }

    render()  // отрисовка компонента(пока один тег div)
    {
        return (
            <div className="App">
                <BrowserRouter>
                    {/*nav>li*3>link*/}
                    <nav>
                        <ul>{this.is_authenticated() ? <p>не гость</p>: <p>Гость</p>}</ul>
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
                            {this.is_authenticated() ? <button onClick={() => this.logout()}>Выйти</button> :
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
                            <Route index element={<ProjectList projects={this.state.projects}/>}/>
                            <Route path=':projectId' element={<ProjectDetail projects={this.state.projects}/>}/>
                        </Route>
                        {/*<Route exact path='/projects' element={<ProjectList projects={this.state.projects}/>}/>*/}
                        <Route exact path='/todos' element={<TodoList todos={this.state.todos}/>}/>

                        <Route exact path='/login' element={<LoginForm get_token={(username, password) =>
                            this.get_token(username, password)}/>}/>
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

