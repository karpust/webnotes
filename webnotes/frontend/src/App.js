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
            'todos': []
        }
    }

    set_token(token) {  // метод принимает токен, помещает его в cookies и записывает в состояние приложения
        const cookies = new Cookies()
        cookies.set('token', token)  // установка токена в cookies, для сохранения юзера при закрытии браузера
        this.setState({'token': token})  // установка токена в состояние, для обновления при авторизации
    }

    is_authenticated() {  // определяет авторизован ли юзер
        return this.state.token != ''  // если да - токен не пустой
    }

    logout() {  // обнуляет токен
        this.set_token('')
    }

    get_token_from_storage() {  // метод вызывается при открытии сайта: токен из cookies в состояние
        const cookies = new Cookies()
        const token = cookies.get('token')  // берет токен из куков
        this.setState({'token': token})  // записывает его в состояние
    }

    get_token(username, password) {  // метод получает токен авторизации
        // методом post отправляем логин и пароль на адрес(на сервер авторизации):
        axios.post('http://127.0.0.1:8000/api-token-auth/',
            {username: username, password: password}).then(response => {
            // методом set_token сохраняем токен в state и cookies:
            this.set_token(response.data['token'])
        }).catch(error => alert('Неверный логин или пароль'))

    }

    load_data() {
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

    componentDidMount() {
        // вызывается при монтировании компонента на страницу
        this.get_token_from_storage()
        this.load_data()

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
                        <li>
                            {this.is_authenticated() ? <button onClick={() => this.logout()}>Logout</button> :
                                <Link to='/login'>Login</Link>
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

