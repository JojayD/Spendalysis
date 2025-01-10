"use client"
import {InputFile} from "@/components/file";
import {ToggleHome} from "@/components/dark-light-toggle";
import {useRef, useState} from "react";

type CSVData = Array<{ [key: string]: string }>;

export default function Uploads() {
    const [darkMode, setDarkMode] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    const toggleDarkMode = () => {
        setDarkMode(!darkMode);
        if (darkMode) {
            document.documentElement.classList.remove("dark");
        } else {
            document.documentElement.classList.add("dark");
        }
    };

    const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0]; // Get the selected file
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file); // Append the file with the key "file"
        try {
            const response = await fetch("http://localhost:8000/upload", {
                method: "POST", body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                console.log("File uploaded successfully:", data);
            } else {
                console.error("Failed to upload file:", response.statusText);
            }
        } catch (error) {
            console.error("Error uploading file:", error);
        } finally {
            if (inputRef.current) {
                inputRef.current.value = "";
            }
        }
    }
    return (
        <div>
            <div className={`flex items-stretch justify-end`}>
                <ToggleHome mode={darkMode ? "dark" : "light"} onClick={toggleDarkMode}/>
            </div>
            <label>Upload a CSV</label>
            <InputFile changeEvent={handleFileChange}/>
        </div>
    );
}