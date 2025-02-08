import Link from "next/link"

export default function Home() {
  return (
    <div className="space-y-12 max-w-4xl mx-auto">
      <section className="text-center space-y-6">
        <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
          Next-Gen AI Solutions
        </h1>
        <p className="text-xl text-gray-300">
          Empower your business with cutting-edge AI technology. Tanda Agent is designed to revolutionize customer
          service and boost productivity.
        </p>
        <Link
          href="/tanda-agent"
          className="inline-block bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-3 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105"
        >
          Experience AI Chat
        </Link>
      </section>

      <section className="grid md:grid-cols-2 gap-8">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-200">
          <h2 className="text-2xl font-semibold mb-4 text-blue-400">Our Technology</h2>
          <p className="text-gray-300">
            Tanda Agent leverages state-of-the-art natural language processing and machine learning algorithms to
            provide human-like interactions and insights.
          </p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-200">
          <h2 className="text-2xl font-semibold mb-4 text-purple-400">Key Benefits</h2>
          <ul className="list-disc list-inside text-gray-300 space-y-2">
            <li>24/7 Automated Customer Support</li>
            <li>Data-Driven Business Insights</li>
            <li>Scalable AI Solutions</li>
            <li>Increased Operational Efficiency</li>
          </ul>
        </div>
      </section>

      <section className="text-center">
        <h2 className="text-3xl font-bold mb-4">Ready to Transform Your Business?</h2>
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

