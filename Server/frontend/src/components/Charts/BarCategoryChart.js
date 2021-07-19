import React, {useState, useEffect} from 'react'
import CanvasJSReact from '../../convasjs/canvasjs.react'
import axios from 'axios'

const BarCategoryChart = (props) => {

    const [options, setoptions] = useState({})

    const fetchData = async() => {
        await axios.get('http://' + props.ip + ':5000/categoria_mensile')
            .then(res => {
                let opt = []
                console.log(res.data)
                res.data.forEach(element => {
                    opt.push({y: Number(element.total), label: element.categoria})
                });

                setoptions({
                    animationEnabled: true,
                    theme: "light2",
                    title: {
                        text: "Spese Mensili"
                    },
                    axisX: {
                        title: "Categorie",
                        reversed: true,
                    },
                    axisY: {
                        title: "Spesa per categoria",
                        includeZero: true,
                    },
                    data: [{
                        type: "bar",
                        dataPoints: opt
                    }]
                })           
                
            }, err => {
                console.log(err)
            }) 
    }


    useEffect(() => {
        fetchData()
    }, [])

    const CanvasJSChart = CanvasJSReact.CanvasJSChart


    return (
        <div>
            <CanvasJSChart options = {options} />
        </div>
    )
}

export default BarCategoryChart
