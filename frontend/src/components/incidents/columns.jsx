import { Checkbox } from "../ui/Checkbox"
import { format } from "date-fns"
import { Badge } from "../ui/Badge"
import { cn } from "../../lib/utils"

const statusStyles = {
  "Filed Fir": "bg-status-filed/20 text-status-filed border-status-filed/30",
  "Not filed FIr": "bg-status-not-filed/20 text-status-not-filed border-status-not-filed/30",
  "Completed": "bg-status-completed/20 text-status-completed border-status-completed/30",
  "Successful": "bg-status-successful/20 text-status-successful border-status-successful/30",
  "Unsuccessful": "bg-status-unsuccessful/20 text-status-unsuccessful border-status-unsuccessful/30",
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
    header: "Incident ID",
    cell: ({ row }) => <div className="font-mono">{row.getValue("id")}</div>,
  },
  {
    accessorKey: "touristId",
    header: "Tourist",
    cell: ({ row }) => {
      const incident = row.original;
      return (
        <div className="flex items-center gap-3">
          <img src={incident.touristAvatar} alt={incident.touristName} className="h-8 w-8 rounded-full object-cover" />
          <div>
            <div className="font-medium">{incident.touristName}</div>
            <div className="text-xs text-text-secondary font-mono">{incident.touristId}</div>
          </div>
        </div>
      )
    }
  },
  {
    accessorKey: "dateIssued",
    header: "Date Issued",
    cell: ({ row }) => format(new Date(row.getValue("dateIssued")), "PPp"),
  },
  {
    accessorKey: "locationTag",
    header: "Location Tag",
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
]
