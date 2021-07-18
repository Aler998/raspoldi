import React, {useState, useEffect} from 'react'
import CanvasJSReact from '../../convasjs/canvasjs.react'
import axios from 'axios'


const PieSumChart = (props) => {

    const [options, setoptions] = useState({})

    const fetchData = async() => {
        await axios.get('http://' + props.ip + ':5000/totale_mensile')
            .then(res => {
                const total = Number(res.data[0].total) + Number(res.data[1].total)
                if (res.data[0].tipo) {
                    setoptions({
                        // exportEnabled: false,
                        animationEnabled: true,
                        title: {
                            text: "Guadagni/Spese"
                        },
                        data: [{
                            type: "pie",
                            startAngle: 90,
                            toolTipContent: "<b>{label}</b>: {y}%",
                            // showInLegend: "true",
                            // legendText: "{label}",
                            // indexLabelFontSize: 12,
                            indexLabel: "{label} - {y}%",
                            dataPoints: [
                                {y: (Number(res.data[0].total) * 100)/total, label: "Guadagni"},
                                {y: (Number(res.data[1].total) * 100)/total, label: "Spese"}
                            ]
                        }]
                    })
                } else {
                    setoptions({
                        // exportEnabled: false,
                        animationEnabled: true,
                        title: {
                            text: "Guadagni/Spese"
                        },
                        data: [{
                            type: "pie",
                            startAngle: 90,
                            toolTipContent: "<b>{label}</b>: {y}%",
                            // showInLegend: "true",
                            // legendText: "{label}",
                            // indexLabelFontSize: 12,
                            indexLabel: "{label} - {y}%",
                            dataPoints: [
                                {y: (Number(res.data[0].total) * 100)/total, label: "Spese"},
                                {y: (Number(res.data[1].total) * 100)/total, label: "Guadagni"}
                            ]
                        }]
                    })
                }

                
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

export default PieSumChart
