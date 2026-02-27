/**
 * Read-only data grid (virtualized-ready) for Data Monitor
 */

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import type { DataRow } from "@/lib/dataMonitor/mockData";

interface DataGridProps {
  rows: DataRow[];
  columns?: string[];
}

export function DataGrid({ rows, columns }: DataGridProps) {
  const cols =
    columns ??
    (rows.length > 0
      ? Object.keys(rows[0]).filter((k) => k !== "id")
      : []);

  if (rows.length === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-muted-foreground">
        لا توجد بيانات لعرضها
      </div>
    );
  }

  return (
    <div className="overflow-auto max-h-[calc(100vh-280px)] rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            {cols.map((col) => (
              <TableHead key={col} className="whitespace-nowrap">
                {col}
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((row) => (
            <TableRow key={row.id as string}>
              {cols.map((col) => (
                <TableCell key={col} className="max-w-[300px] truncate">
                  {formatCell(row[col])}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

function formatCell(val: unknown): string {
  if (val == null) return "—";
  if (val instanceof Date) return val.toISOString();
  return String(val);
}
