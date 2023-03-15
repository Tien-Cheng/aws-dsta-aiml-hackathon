import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

const TableSummary = ({header, rows, headerColor}) => {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 500 }} aria-label="summary table">
        <TableBody>
          <TableCell sx={{ fontWeight: "bolder", fontSize: "16px", color: headerColor, width: "40%" }} rowSpan={rows.length + 1}>"{header}"</TableCell>
          {rows.map((row) => (
            <TableRow key={row.Name}>
              <TableCell style={{ fontWeight: "bold"}} component="th" scope="row">
                {row.Name}
              </TableCell>
              <TableCell sx={row.Score > 0.80 ? {color: "red"} : {}} align="right">
                {row.Score}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default TableSummary;