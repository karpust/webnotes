import React from 'react'

// это простой компонент без состояния.
// т к в каждый компонент передается объект props,
// кот содержит все переданные в компонент данные,
// укажем параметр {user}, т к из всех props нужен только user
const UserItem = ({user}) => {
    return (
        <tr>
            <td>
                {user.first_name}
            </td>
            <td>
                {user.last_name}
            </td>
            <td>
                {user.last_login}
            </td>
        </tr>
    )
}


// users - массив данных о юзере кот передастся в компонент
// превращаем каждого из users в UserItem
const UserList = ({users}) => {
    return (
        <table>
            <th>
                First name
            </th>
            <th>
                Last Name
            </th>
            <th>
                Last Login
            </th>
            {users.map((user) => <UserItem user={user}/>)}
        </table>

    )
}

export default UserList  // экспорт компонента для др модулей