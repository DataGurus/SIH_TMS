import { Checkbox } from "../ui/Checkbox"
import { Badge } from "../ui/Badge"
import { cn } from "../../lib/utils"

const statusStyles = {
  "Filed Fir": "bg-status-filed/20 text-status-filed border-status-filed/30",
  "Not filed FIr": "bg-status-not-filed/20 text-status-not-filed border-status-not-filed/30",
  "Completed": "bg-status-completed/20 text-status-completed border-status-completed/30",
  "Successful": "bg-status-successful/20 text-status-successful border-status-successful/30",
  "Unsuccessful": "bg-status-unsuccessful/20 text-status-unsuccessful border-status-unsuccessful/30",
};

const getSafetyScoreColor = (score) => {
  if (score < 40) return "bg-error";
  if (score < 70) return "bg-warning";
  return "bg-success";
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
    header: "Tourist ID",
    cell: ({ row }) => {
      const tourist = row.original;
      return (
        <div className="flex items-center gap-3">
          <img src={tourist.avatar} alt={tourist.name} className="h-8 w-8 rounded-full object-cover" />
          <div>
            <div className="font-medium">{tourist.name}</div>
            <div className="text-xs text-text-secondary font-mono">{tourist.id}</div>
          </div>
        </div>
      )
    }
  },
  {
    accessorKey: "incidentId",
    header: "Incident ID",
    cell: ({ row }) => <div className="font-mono">{row.getValue("incidentId") || 'N/A'}</div>,
  },
  {
    accessorKey: "incidentStatus",
    header: "Incident State",
    cell: ({ row }) => {
      const status = row.getValue("incidentStatus");
      if (!status) {
        return <span className="text-text-secondary">None</span>;
      }
      return (
        <Badge variant="outline" className={cn("capitalize", statusStyles[status])}>
          {status}
        </Badge>
      )
    }
  },
  {
    accessorKey: "safetyScore",
    header: "Safety Score",
    cell: ({ row }) => {
        const score = row.getValue("safetyScore");
        return (
            <div className="flex items-center gap-2">
                <div className={cn("h-2 w-2 rounded-full", getSafetyScoreColor(score))}></div>
                <span>{score}</span>
            </div>
        )
    }
  },
  {
    accessorKey: "locationTag",
    header: "Location Tag",
  },
]
