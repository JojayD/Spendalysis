import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export function InputFile() {
  return (
    <div className="grid w-full max-w-sm items-center gap-1.5 text-center">
      <Label htmlFor="picture">upload csv</Label>
      <Input id="picture" type="file" />
    </div>
  )
}
