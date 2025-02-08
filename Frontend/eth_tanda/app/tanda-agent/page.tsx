"use client"
import {useState} from 'react'
import type React from "react"
import {default as axios} from "axios";

interface Message {
  role: "user" | "assistant"
  content: string
}
export default function TandaAgent() {
  const [input, setInput] = useState("")
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = { role: "user", content: input }
    setMessages((prevMessages) => [...prevMessages, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const response = await axios.post('http://127.0.0.1:8000/chat_response', {

              inquiry: `${input}`,
              chat_history: `${JSON.stringify(messages)}`,

          }, {
              headers: {
                  'accept': 'application/json',
                  'Content-Type': 'application/json'
              }
      }
      )



      if (!response) {
        throw new Error("Failed to get response")
      }

      const data = await response.data
      //const dataString = response
      const assistantMessage: Message = { role: "assistant", content: data.output}
      console.log(JSON.stringify(data.output))
      console.log(JSON.stringify(data))
      console.log(JSON.stringify(messages))
      setMessages((prevMessages) => [...prevMessages, assistantMessage])
    } catch (error) {
      console.error("Error:", error)

      // Optionally, add an error message to the chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: "assistant", content: "Sorry, I encountered an error. Please try again." },
      ])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
        Tanda AI Agent
      </h1>
      <div className="bg-gray-800 rounded-lg shadow-lg p-4 mb-4 h-[60vh] overflow-y-auto">
        {messages.map((m, index) => (
          <div key={index} className={`mb-4 ${m.role === "user" ? "text-right" : "text-left"}`}>
            <span
              className={`inline-block p-2 rounded-lg ${
                m.role === "user" ? "bg-blue-600 text-white" : "bg-gray-700 text-gray-200"
              }`}
            >
              {m.content}
            </span>
          </div>
        ))}
        {isLoading && (
          <div className="text-center">
            <span className="inline-block p-2 rounded-lg bg-gray-700 text-gray-200">Thinking...</span>
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
          className="flex-grow p-2 border rounded-lg bg-gray-700 text-white border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105 disabled:opacity-50"
          disabled={isLoading}
        >
          Send
        </button>
      </form>
    </div>
  )
}
