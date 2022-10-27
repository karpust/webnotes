import React from "react";
import logo from './logo.svg';
import './App.css';

// класс App наследуем от React.Component
// компонент App имеет состояние, остальные нет
class App extends React.Component {
  constructor(props) {  // в конструктор класса передаём объект props
    super(props)  // вызываем родительский конструктор
    this.state = {  // это объект состояния компонента
      'authors': []  // он хранит массив users кот получим с backend
    }

    render()  // отрисовка компонента(пока один тег div)
    {
      return (
          <div>
            Main App
          </div>
      )
    }
  }

}
// экспортируем наш компонент для использования в других модулях:
export default App;
