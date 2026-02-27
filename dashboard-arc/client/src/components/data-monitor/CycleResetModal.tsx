/**
 * Cycle Reset / Format — Super Admin double-auth modal
 */

import { useState } from "react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RotateCcw, ShieldAlert } from "lucide-react";

const CONFIRM_PHRASE = "CYCLE RESET CONFIRM";

interface CycleResetModalProps {
  onConfirm?: () => void;
}

export function CycleResetModal({ onConfirm }: CycleResetModalProps) {
  const [phrase, setPhrase] = useState("");
  const [step, setStep] = useState<1 | 2>(1);

  const handleOpen = () => {
    setPhrase("");
    setStep(1);
  };

  const handleStep1 = () => {
    if (phrase.trim().toUpperCase() === CONFIRM_PHRASE) {
      setStep(2);
      setPhrase("");
    }
  };

  const handleStep2 = () => {
    if (phrase.trim().toUpperCase() === CONFIRM_PHRASE) {
      onConfirm?.();
    }
  };

  const isValid = phrase.trim().toUpperCase() === CONFIRM_PHRASE;

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button variant="outline" size="sm" className="text-destructive border-destructive/50">
          <RotateCcw className="h-4 w-4 ml-2" />
          CYCLE RESET / FORMAT
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle className="flex items-center gap-2">
            <ShieldAlert className="h-5 w-5 text-destructive" />
            {step === 1 ? "التأكيد الأول" : "التأكيد الثاني (Super Admin)"}
          </AlertDialogTitle>
          <AlertDialogDescription>
            {step === 1
              ? "هذا الإجراء مدمر ولا يمكن التراجع عنه. اكتب العبارة التالية للتأكيد:"
              : "تأكيد ثانٍ مطلوب. اكتب العبارة مرة أخرى:"}
            <code className="block mt-2 p-2 bg-muted rounded text-xs">
              {CONFIRM_PHRASE}
            </code>
          </AlertDialogDescription>
        </AlertDialogHeader>
        <div className="py-4">
          <Label htmlFor="confirm-phrase">العبارة</Label>
          <Input
            id="confirm-phrase"
            value={phrase}
            onChange={(e) => setPhrase(e.target.value)}
            placeholder={CONFIRM_PHRASE}
            className="mt-2 font-mono"
          />
        </div>
        <AlertDialogFooter>
          <AlertDialogCancel>إلغاء</AlertDialogCancel>
          {step === 1 ? (
            <Button
              onClick={handleStep1}
              disabled={!isValid}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              متابعة للتأكيد الثاني
            </Button>
          ) : (
            <AlertDialogAction
              onClick={handleStep2}
              disabled={!isValid}
              className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
            >
              تنفيذ CYCLE RESET
            </AlertDialogAction>
          )}
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
