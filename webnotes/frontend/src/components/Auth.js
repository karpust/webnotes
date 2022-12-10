import React from "react";

class LoginForm extends React.Component {  // класс LoginForm наследуется от React.Component
    constructor(props) {
        super(props)
        this.state = {login: '', password: ''}  // компонент с состоянием (храним логин и пароль)
    }

    handleChange(event) {  // метод меняет состояние - записывает в event.target.name value
        // event - событие ввода данных в форму
        this.setState(
            {
                [event.target.name]: event.target.value
                // event.target это input, name будет login или password
            }
        );
    }

    handleSubmit(event) {  // метод вызывается при отправке формы, проверяет верный ли логин/пароль
        // console.log(this.state.login + ' ' + this.state.password)
        this.props.get_token(this.state.login, this.state.password) // вместо вывода в консоль, вызываем get_token
        event.preventDefault()  // отменит отправку формы т к мы сделаем это сами чз axios

    }

    render() {
        return (  // отрисовка компонента формы: связываем события с методами
            <form onSubmit={(event) => this.handleSubmit(event)}>
                <input type="text" name="login" placeholder="login" value={this.state.login}
                       onChange={(event) => this.handleChange(event)}/>
                <input type="password" name="password" placeholder="password" value={this.state.password}
                       onChange={(event) => this.handleChange(event)}/>
                <input type="submit" value="Login"/>
            </form>
        );
    }
}

export default LoginForm