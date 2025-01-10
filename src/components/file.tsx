import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { forwardRef } from "react";

type Props = {
  changeEvent: (event: React.ChangeEvent<HTMLInputElement>) => void;
};

export const InputFile = forwardRef<HTMLInputElement, Props>(({ changeEvent }, ref) => {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5 text-center">
      <Label htmlFor="file-input">Upload CSV</Label>
      <Input id="file-input" type="file" onChange={changeEvent} ref={ref} />
    </div>
  );
});

InputFile.displayName = "InputFile";
