import React from "react";
// import logo from './logo.svg';
import './App.css';
import UserList from "./components/User";
import axios from "axios";
import ProjectList from "./components/Project";
import TodoList from "./components/Todo";
import {HashRouter,Routes,Route,BrowserRouter} from "react-router-dom";


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

                {/*в HashRouter поместили компоненты кот будут меняться в зависимости от адреса
                путь path указывает на компонент(у нас это ф-ция замыкания возвращающая компонент)
                указанный в component*/}
                {/*<HashRouter>*/}
                {/*    <Routes>*/}
                {/*        <Route exact path='/' component={() => <UserList users={this.state.users}/>}/>*/}
                {/*        <Route exact path='/projects' component={() => <ProjectList projects={this.state.projects}/>}/>*/}
                {/*        <Route exact path='/todos' component={() => <TodoList todos={this.state.todos}/>}/>*/}
                {/*    </Routes>*/}
                {/*</HashRouter>*/}

                <BrowserRouter>
                    <Routes>
                        <Route exact path='/' element={<UserList users={this.state.users}/>}/>
                        <Route exact path='/projects' element={<ProjectList projects={this.state.projects}/>}/>
                        <Route exact path='/todos' element={<TodoList todos={this.state.todos}/>}/>
                    </Routes>
                </BrowserRouter>

                {/*<UserList users={this.state.users} />*/}
                {/*<ProjectList projects={this.state.projects} />*/}
                {/*<TodoList todos={this.state.todos} />*/}

            </div>

        )
    }
}

export default App;  // экспорт компонента для др модулей

