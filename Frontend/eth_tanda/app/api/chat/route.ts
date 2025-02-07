import { NextResponse } from "next/server"
const axios = require('axios').default
export async function POST(req: Request) {
  const message = req.headers.get("inquiry")
  const chatHistory = JSON.parse(req.headers.get("chat_history") || "[]")

/** jknjn */
//  const respons = await fetch("http://127.0.0.1:8000/chat_response", {
//    method: "POST",
//    headers: {
//      'Accept': 'application/json, text/plain, */*',
//      "Content-Type": "application/json",
//    },
//    body: JSON.stringify({
//      "inquiry": "vfvvd",
//      "chat_history": " "}
//      ),
//  })
  const response = await axios.post("http://127.0.0.1:8000/chat_response", {
            "inquiry": "what can you help with?",
            "chat_history": " "
    }, {
      headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
      }
  }
)

  const data = await response.json()

  return NextResponse.json(data)
}
