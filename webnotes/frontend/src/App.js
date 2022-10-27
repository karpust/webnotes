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
      // для проверки данные захардкодили потом будем брать с back-end
        const users = [
            {  // Далее эти данные мы будем получать с back-end, пока заглушки
                'first_name': 'Фёдор',
                'last_name': 'Достоевский',
                'last_login': 1821
            },
            {
                'first_name': 'Александр',
                'last_name': 'Грин',
                'last_login': 1880
            },
        ]
        this.setState(  // меняем состояние App, передаем данные users
            {
                'users': users
            }
        )
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

