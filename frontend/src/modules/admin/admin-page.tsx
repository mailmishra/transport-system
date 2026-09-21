import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { AgentsAdminTab } from "./agents-admin-tab";
import { TruckOwnersAdminTab } from "./truck-owners-admin-tab";
import { VehiclesAdminTab } from "./vehicles-admin-tab";
import { FirmSetupTab } from "./firm-setup-tab";

export function AdminPage() {
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-[19px] font-bold text-navy">Admin</h1>

      <Tabs defaultValue="firm">
        <TabsList>
          <TabsTrigger value="firm">Firm Setup</TabsTrigger>
          <TabsTrigger value="agents">Agents</TabsTrigger>
          <TabsTrigger value="truck-owners">Truck Owners</TabsTrigger>
          <TabsTrigger value="vehicles">Vehicles</TabsTrigger>
        </TabsList>

        <TabsContent value="firm">
          <FirmSetupTab />
        </TabsContent>
        <TabsContent value="agents">
          <AgentsAdminTab />
        </TabsContent>
        <TabsContent value="truck-owners">
          <TruckOwnersAdminTab />
        </TabsContent>
        <TabsContent value="vehicles">
          <VehiclesAdminTab />
        </TabsContent>
      </Tabs>
    </div>
  );
}
