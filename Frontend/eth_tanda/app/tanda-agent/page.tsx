"use client"
import { useChat } from "ai/react"

export default function TandaAgent() {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit: originalHandleSubmit,
  } = useChat({
    api: "/api/chat",
  })

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    const chatHistory = messages.map((m) => ({
      role: m.role,
      content: m.content,
    }))

    originalHandleSubmit(e, {
      options: {
        headers: {
          inquiry: input,
          chat_history: JSON.stringify(chatHistory),
        },
      },
    })
  }

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
        Tanda AI Agent
      </h1>
      <div className="bg-gray-800 rounded-lg shadow-lg p-4 mb-4 h-[60vh] overflow-y-auto">
        {messages.map((m) => (
          <div key={m.id} className={`mb-4 ${m.role === "user" ? "text-right" : "text-left"}`}>
            <span
              className={`inline-block p-2 rounded-lg ${
                m.role === "user" ? "bg-blue-600 text-white" : "bg-gray-700 text-gray-200"
              }`}
            >
              {m.content}
            </span>
          </div>
        ))}
      </div>
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message here..."
          className="flex-grow p-2 border rounded-lg bg-gray-700 text-white border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105"
        >
          Send
        </button>
      </form>
    </div>
  )
}
