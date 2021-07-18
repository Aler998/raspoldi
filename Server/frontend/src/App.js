import './App.css';
import { useState, useEffect } from 'react';
import axios from 'axios'
import {Container, Row, Col} from 'react-bootstrap'
import Header from './components/Header';
import LastMonthTable from './components/LastMonthTable';

const ip_t = "192.168.1.236"
const ip = "127.0.0.1"


const App = () => {

  return (
    <div className="App">

      <Container fluid>
        <Row>
          <Col>
            <Header />
          </Col>
        </Row>
        <Row>
          <Col sm md={8} ><LastMonthTable  ip={ip}/></Col>
          <Col sm md={4}>sm=true</Col>
          <Col sm md={8}>sm=true</Col>
        </Row>
      </Container>
      {/* <TableContainer component={Paper}>
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
      </TableContainer> */}
    </div>
  );
}

export default App;
