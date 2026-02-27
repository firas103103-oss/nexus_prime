/**
 * Data Monitoring Dashboard — Immutable, read-only, 3-level taxonomy
 * No delete UI. Cycle Reset requires double auth.
 */

import { useState, useMemo } from "react";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { TaxonomySidebar } from "@/components/data-monitor/TaxonomySidebar";
import { DataGrid } from "@/components/data-monitor/DataGrid";
import { CycleResetModal } from "@/components/data-monitor/CycleResetModal";
import {
  MOCK_TAXONOMY,
  getRowsForNode,
} from "@/lib/dataMonitor/mockData";
import { Database, Lock } from "lucide-react";

export default function DataMonitor() {
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const rows = useMemo(
    () => (selectedId ? getRowsForNode(selectedId) : []),
    [selectedId]
  );

  const handleSelect = (nodeId: string, isLeaf: boolean) => {
    if (isLeaf) setSelectedId(nodeId);
  };

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-14 shrink-0 items-center gap-2 border-b px-4">
          <SidebarTrigger />
          <Separator orientation="vertical" className="h-6" />
          <Database className="h-5 w-5 text-muted-foreground" />
          <span className="font-semibold">مراقبة البيانات</span>
          <Badge
            variant="secondary"
            className="mr-auto gap-1 border-amber-500/50 bg-amber-500/10 text-amber-700 dark:text-amber-400"
          >
            <Lock className="h-3 w-3" />
            IMMUTABLE DATA - DELETION LOCKED
          </Badge>
          <CycleResetModal onConfirm={() => console.warn("Cycle Reset - not implemented")} />
        </header>

        <div className="flex h-[calc(100vh-3.5rem)]">
          <div className="w-64 shrink-0">
            <TaxonomySidebar
              taxonomy={MOCK_TAXONOMY}
              selectedId={selectedId}
              onSelect={handleSelect}
            />
          </div>
          <main className="flex-1 overflow-auto p-4">
            <div className="mb-4">
              <h2 className="text-lg font-medium">
                {selectedId ? `البيانات: ${selectedId}` : "اختر تصنيفاً من القائمة"}
              </h2>
              <p className="text-sm text-muted-foreground">
                عرض للقراءة فقط — لا يوجد حذف أو تعديل
              </p>
            </div>
            <DataGrid rows={rows} />
          </main>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}
