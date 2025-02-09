import { NextResponse } from "next/server"
import axios from 'axios';
export async function POST(req: Request) {
    const body = await req.json()

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

    return new NextResponse('Success', {status: 200})
}
