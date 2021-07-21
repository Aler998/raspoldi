import React, {useState, useEffect} from 'react'
import { Table } from 'react-bootstrap'
import axios from 'axios'

const LastMonthTable = (props) => {


    const [rows, setrows] = useState([])

    const fetch = async () => {
        await axios.get('http://' + props.ip + ':5000/transazioni')
            .then(res => {
                setrows(...rows, res.data)
            }, err => {
                console.log(err)
            })
    }

    const cancel = async (id) => {
        await axios.get('http://' + props.ip + ':5000/delete/'+ id)
        .then(res => {
            if (res.status === 200) {
                setrows(rows.filter((obj) => {
                    return obj.id !== id
                }))
            } else if (res.status === 300) {
                console.log('Something went wrong')
            }
        }, err => {
            console.log(err)
        }) 
    }

    useEffect(() => {
        fetch()
    }, [])

    return (
        <div>
            <Table responsive striped bordered hover size="sm" style={{height: '300px'}}>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Tipo</th>
                        <th>Euro</th>
                        <th>Descrizione</th>
                        <th>Created At</th>
                        <th>Edit</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        rows.map((row) => { 
                        
                        const arr = row.created_at.split("T")

                        return(
                            <tr key={row.id}>
                                <td>{row.id}</td>
                                <td>{row.tipo}</td>
                                <td>{row.euro}</td>
                                <td>{row.descrizione}</td>
                                <td>{arr[0]}</td>
                                <td><i onClick={() => cancel(row.id)} className="fas fa-trash" style={{cursor: 'pointer'}}></i></td>
                            </tr>
                        )})
                    }
                </tbody>
            </Table>
        </div>
    )
}

export default LastMonthTable
