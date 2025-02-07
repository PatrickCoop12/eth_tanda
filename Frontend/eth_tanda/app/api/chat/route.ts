import { NextResponse } from "next/server"

export async function POST(req: Request) {
  const message = req.headers.get("inquiry")
  const chatHistory = JSON.parse(req.headers.get("chat_history") || "[]")

  const request = {
    "inquiry": "what can you help with?",
    "chat_history": " ",
  }

  const response = await fetch("http://127.0.0.1:8000/chat_response", {
    method: "POST",
    headers: {
      'Accept': 'application/json, text/plain, */*',
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "inquiry": "vfvvd",
      "chat_history": " "
    }),
  })

  const data = await response.json()
  console.log(JSON.stringify({
      "inquiry": "vfvvd",
      "chat_history": " "
    }))
  return NextResponse.json(data)
}
