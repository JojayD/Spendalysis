import { Toggle } from "@/components/ui/toggle";

type Props = {
  mode: "light" | "dark";
  onClick?: () => void;
};

export function ToggleHome({ mode, onClick }: Props) {
  return (
    <Toggle aria-label="Toggle dark mode" onClick={onClick}>
      <div>{mode === "dark" ? "🌙 Dark Mode" : "☀️ Light Mode"}</div>
    </Toggle>
  );
}
