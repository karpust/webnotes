import React from "react";
import logo from './logo.svg';
import './App.css';
import UserList from "./components/User";
import axios from "axios";

// класс App наследуем от React.Component
// компонент App имеет состояние, остальные нет
class App extends React.Component {
    constructor(props) {  // в конструктор класса передаём объект props
        super(props)  // вызываем родительский конструктор
        this.state = {  // это объект состояния компонента
            'users': []  // он хранит массив users кот получим с backend
        }
    }

    componentDidMount() {
        // вызывается при монтировании компонента на страницу
        // response.data - данные с back-end - список юзеров
        axios.get('http://127.0.0.1:8000/api/users/')
            .then(response => {
                const users = response.data
                this.setState(  // меняем состояние App, передаем данные users
                    {
                        'users': users
                    }
                )
            }).catch(error => console.log(error))
    }

    render()  // отрисовка компонента(пока один тег div)
    {
        return (
            <div>
                <UserList users={this.state.users}/>
            </div>
        )
    }
}

export default App;  // экспорт компонента для др модулей

