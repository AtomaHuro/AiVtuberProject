import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@/components/ui/select"

export default function MelodySelector() {
  const [melodies, setMelodies] = useState([])
  const [selected, setSelected] = useState("")

  useEffect(() => {
    fetch("/memory/sing_menu.json")
      .then(res => res.json())
      .then(data => setMelodies(data.featured))
  }, [])

  return (
    <Card className="w-full max-w-md p-4">
      <CardContent>
        <h2 className="text-xl font-bold mb-2">🎶 Select a Melody</h2>
        <Select onValueChange={setSelected} value={selected}>
          <SelectTrigger>
            <SelectValue placeholder="Choose a melody ID..." />
          </SelectTrigger>
          <SelectContent>
            {melodies.map((id) => (
              <SelectItem key={id} value={id}>{id}</SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Button className="mt-4" onClick={() => alert(`/sing ${selected}`)} disabled={!selected}>
          Play 🎤
        </Button>
      </CardContent>
    </Card>
  )
}
