import { Checkbox } from "../ui/Checkbox"
import { Badge } from "../ui/Badge"
import { cn } from "../../lib/utils"

const statusStyles = {
  "Assigned": "bg-status-unsuccessful/20 text-status-unsuccessful border-status-unsuccessful/30",
  "Unassigned": "bg-status-successful/20 text-status-successful border-status-successful/30",
  "Inactive": "bg-neutral-500/20 text-neutral-400 border-neutral-500/30",
};

export const columns = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() && "indeterminate")
        }
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "id",
    header: "Unit ID",
    cell: ({ row }) => {
        const unit = row.original;
        return (
            <div className="flex items-center gap-3">
                <img src={unit.avatar} alt={unit.unitHead} className="h-8 w-8 rounded-full object-cover" />
                <div>
                    <div className="font-medium font-mono">{unit.id}</div>
                    <div className="text-xs text-text-secondary">{unit.unitHead}</div>
                </div>
            </div>
        )
    }
  },
  {
    accessorKey: "locationTag",
    header: "Location Tag",
  },
  {
    accessorKey: "type",
    header: "Unit Type",
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.getValue("status");
      return (
        <Badge variant="outline" className={cn("capitalize", statusStyles[status])}>
          {status}
        </Badge>
      )
    }
  },
  {
    accessorKey: "assignedIncidentId",
    header: "Assigned Incident",
    cell: ({ row }) => {
        const incidentId = row.getValue("assignedIncidentId");
        return incidentId ? <div className="font-mono">{incidentId}</div> : <span className="text-text-secondary">-</span>;
    }
  },
]
