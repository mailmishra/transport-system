import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { useFirms } from "@/api/firms";
import { DayBookTab } from "./day-book-tab";
import { OutstandingTab } from "./outstanding-tab";
import { GstTab } from "./gst-tab";
import { VehicleActivityTab } from "./vehicle-activity-tab";
import { PendingLoadingSlipsTab } from "./pending-loading-slips-tab";
import { ReceivablesTab } from "./receivables-tab";

/** Reports landing page -- grouped by who reads them (Reports + PDF
 * template plan, Part 2a): Overview/Owner, Accounts, Dispatch. The
 * Bilti-wise and Loading Slip registers aren't separate tabs here -- they
 * ARE the existing Bilti / GR and Loading Slips list screens, which
 * already support the same date_from/date_to/vehicle/agent/truck-owner
 * filters these reports use.
 */
export function ReportsPage() {
  const { data: firms } = useFirms();
  const firmId = firms?.[0]?.id;

  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-[19px] font-bold text-navy">Reports</h1>

      <Tabs defaultValue="day-book">
        <TabsList>
          <TabsTrigger value="day-book">Day Book</TabsTrigger>
          <TabsTrigger value="outstanding">Outstanding</TabsTrigger>
          <TabsTrigger value="receivables">Receivables</TabsTrigger>
          <TabsTrigger value="gst">GST</TabsTrigger>
          <TabsTrigger value="vehicle-activity">Vehicle Activity</TabsTrigger>
          <TabsTrigger value="pending-loading-slips">Pending Loading Slips</TabsTrigger>
        </TabsList>

        <TabsContent value="day-book">
          <DayBookTab firmId={firmId} />
        </TabsContent>
        <TabsContent value="outstanding">
          <OutstandingTab firmId={firmId} />
        </TabsContent>
        <TabsContent value="receivables">
          <ReceivablesTab firmId={firmId} />
        </TabsContent>
        <TabsContent value="gst">
          <GstTab firmId={firmId} />
        </TabsContent>
        <TabsContent value="vehicle-activity">
          <VehicleActivityTab firmId={firmId} />
        </TabsContent>
        <TabsContent value="pending-loading-slips">
          <PendingLoadingSlipsTab firmId={firmId} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
