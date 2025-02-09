import { NextResponse } from "next/server"
const axios = require('axios').default
export async function POST(req: Request) {
    const body = await req.json()
    const message = body.inquiry
    const chatHistory =  body.chat_history
    console.log(body.inquiry)
    console.log(body.chat_history)

  const response = await axios.post("http://54.209.78.170/chat_response", {
            "inquiry": `${body.inquiry}`,
            "chat_history": `${body.chat_history}`
    }, {
      headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
      }
  }
)

  const data = await response
  console.log(JSON.stringify(data.data.output))

  return new NextResponse(data)
}
