import Image from "next/image"

export default function Instructions() {
  return (
    <div className="max-w-4xl mx-auto space-y-12">
      <h1 className="text-4xl font-bold mb-8 text-center bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
        How to Use Tanda AI
      </h1>

      <section className="space-y-8">
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold text-blue-400">1. Start a Conversation</h2>
          <p className="text-gray-300">
            Deploy your association agreement to the blockchain, and make note of the contract address provide once deployed.
          </p>
          <div className="relative h-64 bg-gray-800 rounded-lg overflow-hidden">
            <Image
              src="/placeholder.svg?height=256&width=512"
              alt="Start a conversation"
              layout="fill"
              objectFit="cover"
              className="rounded-lg"
            />
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-2xl font-semibold text-purple-400">2. Reference your Tanda on Etherscan</h2>
          <p className="text-gray-300">
            Access your association contract on the blockchain.
          </p>
          <div className="relative h-64 bg-gray-800 rounded-lg overflow-hidden">
            <Image
              src="/placeholder.svg?height=256&width=512"
              alt="AI-powered responses"
              layout="fill"
              objectFit="cover"
              className="rounded-lg"
            />
          </div>
        </div>

        <div className="space-y-4">
          <h2 className="text-2xl font-semibold text-green-400">3. Participate in Your Tanda Association</h2>
          <p className="text-gray-300">
            Look under the contract tab to access the contract functionality and interact with your association.
          </p>
          <div className="relative h-64 bg-gray-800 rounded-lg overflow-hidden">
            <Image
              src="/placeholder.svg?height=256&width=512"
              alt="Refine your queries"
              layout="fill"
              objectFit="cover"
              className="rounded-lg"
            />
          </div>
        </div>
      </section>
    </div>
  )
}