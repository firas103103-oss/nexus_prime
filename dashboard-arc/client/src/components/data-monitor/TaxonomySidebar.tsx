/**
 * 3-level taxonomy tree/accordion for Data Monitor
 */

import { useState } from "react";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { ChevronRight } from "lucide-react";
import type { TaxonomyNode } from "@/lib/dataMonitor/mockData";
import { cn } from "@/lib/utils";

interface TaxonomySidebarProps {
  taxonomy: TaxonomyNode[];
  selectedId: string | null;
  onSelect: (nodeId: string, isLeaf: boolean) => void;
}

function TaxonomyItem({
  node,
  selectedId,
  onSelect,
  level,
}: {
  node: TaxonomyNode;
  selectedId: string | null;
  onSelect: (nodeId: string, isLeaf: boolean) => void;
  level: number;
}) {
  const isLeaf = !node.children || node.children.length === 0;
  const isSelected = selectedId === node.id;

  if (isLeaf) {
    return (
      <button
        type="button"
        onClick={() => onSelect(node.id, true)}
        className={cn(
          "w-full flex items-center gap-2 py-2 px-3 rounded-md text-left text-sm transition-colors",
          "hover:bg-accent",
          isSelected && "bg-accent font-medium"
        )}
        style={{ paddingLeft: 12 + level * 16 }}
      >
        <ChevronRight className="h-4 w-4 shrink-0 opacity-50" />
        {node.labelAr ?? node.label}
      </button>
    );
  }

  return (
    <AccordionItem value={node.id} className="border-0">
      <AccordionTrigger
        className={cn(
          "py-2 px-3 hover:no-underline [&[data-state=open]>svg]:rotate-90",
          isSelected && "bg-accent/50"
        )}
        style={{ paddingLeft: 12 + level * 16 }}
        onClick={() => onSelect(node.id, false)}
      >
        <span className="flex items-center gap-2">
          <ChevronRight className="h-4 w-4 shrink-0 transition-transform" />
          {node.labelAr ?? node.label}
        </span>
      </AccordionTrigger>
      <AccordionContent className="pb-0 pt-0">
        <Accordion type="multiple" className="w-full">
          {node.children?.map((child) => (
            <TaxonomyItem
              key={child.id}
              node={child}
              selectedId={selectedId}
              onSelect={onSelect}
              level={level + 1}
            />
          ))}
        </Accordion>
      </AccordionContent>
    </AccordionItem>
  );
}

export function TaxonomySidebar({
  taxonomy,
  selectedId,
  onSelect,
}: TaxonomySidebarProps) {
  const [openItems, setOpenItems] = useState<string[]>(
    taxonomy.map((t) => t.id)
  );

  return (
    <div className="h-full overflow-y-auto border-r bg-muted/30">
      <div className="p-3">
        <h3 className="text-sm font-semibold text-muted-foreground mb-2">
          التصنيف
        </h3>
        <Accordion
          type="multiple"
          value={openItems}
          onValueChange={setOpenItems}
          className="w-full"
        >
          {taxonomy.map((node) => (
            <TaxonomyItem
              key={node.id}
              node={node}
              selectedId={selectedId}
              onSelect={onSelect}
              level={0}
            />
          ))}
        </Accordion>
      </div>
    </div>
  );
}
