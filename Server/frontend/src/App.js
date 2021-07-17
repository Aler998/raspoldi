import './App.css';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import { useState, useEffect } from 'react';
import axios from 'axios'


const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

const App = () => {

  const [rows, setrows] = useState([])
  const classes = useStyles();

  const fetch = async () => {
    await axios.get('http://localhost:5000/transazioni')
        .then(res => {
          console.log(res.data)
          setrows(...rows, res.data)
        }, err => {
          console.log(err)
        })
  }

  useEffect(() => {
    fetch()
  }, [])

  return (
    <div className="App">
      <TableContainer component={Paper}>
        <Table className={classes.table} size="small" aria-label="a dense table">
          <TableHead>
            <TableRow>
              <TableCell>Id</TableCell>
              <TableCell align="right">Tipo</TableCell>
              <TableCell align="right">euro</TableCell>
              <TableCell align="right">Descrizione</TableCell>
              <TableCell align="right">Created At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {
              rows.map((row) => (
                <TableRow key={row.id}>
                  <TableCell component="th" scope="row">
                    {row.id}
                  </TableCell>
                  <TableCell align="right">{row.tipo}</TableCell>
                  <TableCell align="right">{row.euro}</TableCell>
                  <TableCell align="right">{row.descrizione}</TableCell>
                  <TableCell align="right">{row.created_at}</TableCell>
                </TableRow>
              ))
            }
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}

export default App;
