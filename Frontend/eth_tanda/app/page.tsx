import Link from "next/link"

export default function Home() {
  return (
      <div className="space-y-12 max-w-4xl mx-auto">
        <section className="text-center space-y-6">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
            ETH Tanda
          </h1>
          <p className="text-xl text-gray-300">
            Seamlessly form Tanda associations on the Blockchain. ETH
            Tanda&#39;s Agent is designed to walk you through formation and deploy
            a smart contract directly to the blockchain with just a conversation.
          </p>
          <Link
              href="/tanda-agent"
              className="inline-block bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-3 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105"
          >
            Use ETH Tanda Agent
          </Link>
        </section>

        <section className="grid md:grid-cols-2 gap-8">
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-200">
            <h2 className="text-2xl font-semibold mb-4 text-blue-400">What is a Tanda?</h2>
            <p className="text-gray-300">
              A Tanda is a rotating savings and credit association (ROSCA) where a
              group of people (friends, family, and/or community members) contribute money
              to a pool and then take turns receiving the pooled money. Tandas are common in
              Latin American cultures as a means for individuals to access a viable savings
              and lending vehicle.
            </p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-200">
            <h2 className="text-2xl font-semibold mb-4 text-purple-400">Key Benefits of Blockchain</h2>
            <ul className="list-disc list-inside text-gray-300 space-y-2">
              <li>Smart Contracts Can Secure Agreements Among Association Members</li>
              <li>Members Can Trust Their Funds are Secure</li>
              <li>Association Agreements Programmed Directly Into Contracts and Cannot be Adjusted</li>
              <li>Greater Visability for Members</li>
            </ul>
          </div>
        </section>

        <section className="grid md:grid-cols-2 gap-8">
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-200">
            <h2 className="text-2xl font-semibold mb-4 text-blue-400">How Does ETH Tanda Work?</h2>
            <p className="text-gray-300">
              ETH Tanda makes it as easy as having a conversation to bring your Tanda association(s) to the blockchain.
              Simply chat with our AI agent specialized in answering your questions about Tandas generally, smart
              contracts,
              blockchain, and how they all tie together. Our agent will ask you for a few details required to form your
              Tanda on the blockchain, and will handle all the work from there. After you will be provided with
              the contract address to interact with on the blockchain.
            </p>
          </div>
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-200">
            <h2 className="text-2xl font-semibold mb-4 text-purple-400">What you&#39;ll need to get started</h2>
            <p className="text-lg mb-4">ETH Agent Will Ask For the Following:</p>
            <ul className="list-disc list-inside text-gray-300 space-y-2">
              <li>Number of members in your association</li>
              <li>How often members are to contribute (in weeks)</li>
              <li>Contribution amounts (noted in ETH)</li>
              <li>The frequency the pooled pot will be given to a member</li>
              <li>The wallet addresses of the members</li>
            </ul>
          </div>
        </section>

        <section className="text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Form Your Tanda Association?</h2>
          <Link
              href="/tanda-agent"
              className="inline-block bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors duration-200"
          >
            Get Started Now
          </Link>
        </section>
      </div>
  )
}

